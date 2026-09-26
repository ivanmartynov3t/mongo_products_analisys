#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""Candidate-signal queue: silo sub-feature tags with no matrix row (issue #36).

    uv run tools/silo-candidates/candidates.py plan      # print the report, write nothing
    uv run tools/silo-candidates/candidates.py apply     # write reports/silo-candidates.md

For every analysed product that has a silo product of the same name, lists the silo's
sub-feature tags (from `data/catalog_index.json`) that no row of the product's matrices
covers, and the matrix IDs the silo never tags for that product. The silo classifier is
noisy: a candidate is a lead for the LLM part (Plan 08 part 2) and a human, never a fact.

Read-only by construction: the silo is read from git objects at a pinned ref; the only
file this tool may write is the configured output. Documents from repositories are only
counted, never named: this repository is public and many silo repositories are private.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
import tomllib
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent

sys.path.insert(0, str(HERE.parent / "silo-review"))
from review import (FM_RE, SILO_GENERATED, ReadOnlyViolation, cat_batch, domain, frontmatter, git,  # noqa: E402
                    guarded_write, matrix_table_ids, normalize_url)


class CandidatesError(RuntimeError):
    pass


# ---------------------------------------------------------------- analysis repo


def matrix_ids(product_dir: Path) -> tuple[set[str], set[str]]:
    """(capability IDs, pointer IDs) over all of the product's matrices (rules in review.matrix_table_ids)."""
    caps: set[str] = set()
    pointers: set[str] = set()
    for m in sorted(product_dir.glob("features/*/feature-matrix.md")):
        c, p = matrix_table_ids(m.read_text(encoding="utf-8"))
        caps |= c
        pointers |= p
    return caps, pointers - caps


def load_mapping(tsv: Path) -> dict[str, str]:
    """Dictionary ID -> the silo tag that detects it (directly, or through the ID it maps to)."""
    rows = {r["id"]: r for r in csv.DictReader(tsv.open(encoding="utf-8"), delimiter="\t")}
    if not rows:
        raise CandidatesError(f"{tsv} is empty")
    out = {}
    for i, r in rows.items():
        tag = r.get("silo_detects_via") or rows.get(r.get("maps_to") or "", {}).get("silo_detects_via", "")
        if tag:
            out[i] = tag
    return out


# ---------------------------------------------------------------- silo


@dataclass
class Signal:
    tag: str
    web: list[tuple[float, str, str]] = field(default_factory=list)  # (probability, title, url) — public pages
    repo_docs: int = 0
    source_files: int = 0
    shared: int = 0   # entries whose page or file is also indexed under another product

    @property
    def total(self) -> int:
        return len(self.web) + self.repo_docs + self.source_files


def load_catalog(silo: Path, ref: str, catalog_path: str, data_dir: str) -> tuple[str, str, dict]:
    sha = git(silo, "rev-parse", "--verify", f"{ref}^{{commit}}").strip()
    cdate = git(silo, "show", "-s", "--format=%cs", sha).strip()
    raw = cat_batch(silo, [f"{sha}:{catalog_path}"])[f"{sha}:{catalog_path}"]
    if not raw:
        raise CandidatesError(f"{catalog_path} is missing at silo {sha[:10]}")
    catalog = json.loads(raw)
    if not isinstance(catalog, dict) or not isinstance(catalog.get("by_product"), dict):
        raise CandidatesError(f"{catalog_path} has no 'by_product' object at silo {sha[:10]}")
    return sha, cdate, catalog["by_product"]


def web_urls(silo: Path, sha: str, data_dir: str, paths: list[str]) -> dict[str, str]:
    """source_url of stored web pages (top level of a product folder), by catalog path."""
    specs = {p: f"{sha}:{data_dir}/{p}" for p in paths}
    blobs = cat_batch(silo, sorted(set(specs.values())))
    return {p: frontmatter(blobs[s]).get("source_url", "") for p, s in specs.items() if blobs.get(s)}


def is_public(url: str, non_public_hosts: list[str]) -> bool:
    """A page that may be named in this public report: not on a code host or internal system."""
    host = domain(normalize_url(url)).split(":", 1)[0] if url else ""
    return bool(host) and not any(host == h or host.endswith("." + h) for h in non_public_hosts)


def shared_paths(silo: Path, sha: str, data_dir: str, by_product: dict[str, list[dict]]) -> set[str]:
    """Catalog paths whose page or file is also indexed under another silo product.

    Two entries are the same when their path below the product folder matches and so does
    their content: the normalised source_url for a top-level page, the body (frontmatter
    removed) for any other stored file, and the path alone for a source file the silo does
    not store. Unrelated products' index.md or blog.md therefore never count as shared.
    """
    groups: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for slug, entries in by_product.items():
        for e in entries:
            path = e.get("path", "")
            groups["/".join(PurePosixPath(path).parts[2:])].append((slug, path))
    groups = {k: v for k, v in groups.items() if len({s for s, _ in v}) > 1}
    specs = sorted({f"{sha}:{data_dir}/{p}" for v in groups.values() for _, p in v})
    blobs = cat_batch(silo, specs)

    def key(path: str, suffix: str) -> str:
        text = blobs.get(f"{sha}:{data_dir}/{path}", "")
        if not text:
            return "path:" + suffix
        if len(PurePosixPath(path).parts) == 3:
            return "url:" + normalize_url(frontmatter(text).get("source_url", "") or suffix)
        return "body:" + hashlib.sha256(FM_RE.sub("", text, count=1).encode("utf-8")).hexdigest()

    out: set[str] = set()
    for suffix, members in groups.items():
        keyed = [(slug, path, key(path, suffix)) for slug, path in members]
        slugs_by_key: dict[str, set[str]] = defaultdict(set)
        for slug, _, k in keyed:
            slugs_by_key[k].add(slug)
        out |= {path for _, path, k in keyed if len(slugs_by_key[k]) > 1}
    return out


def signals_for(entries: list[dict], urls: dict[str, str], shared: set[str],
                min_probability: float, non_public_hosts: list[str]) -> dict[str, Signal]:
    out: dict[str, Signal] = {}
    seen_web: dict[str, set[str]] = defaultdict(set)
    for e in entries:
        path = e.get("path", "")
        parts = PurePosixPath(path).parts
        for tag in e.get("sub_feature_tags") or []:
            prob = float((e.get("sub_feature_probabilities") or {}).get(tag, 0))
            if prob < min_probability:
                continue
            s = out.setdefault(tag, Signal(tag))
            url = urls.get(path, "") if len(parts) == 3 else ""
            if url and is_public(url, non_public_hosts):
                norm = normalize_url(url)
                if norm in seen_web[tag]:
                    continue  # the same page captured twice (…/page and …/page/)
                seen_web[tag].add(norm)
                s.web.append((prob, str(e.get("title", "")), url))
            elif len(parts) > 3 and parts[2] == "repo_docs":
                s.repo_docs += 1
            else:
                s.source_files += 1
            s.shared += path in shared
    for s in out.values():
        s.web.sort(key=lambda w: (-w[0], w[2]))
    return out


# ---------------------------------------------------------------- report


def _cell(text: str) -> str:
    return " ".join(str(text).split()).replace("|", "\\|").replace("[", "\\[").replace("]", "\\]")


def build(cfg: dict, silo: Path, ref: str) -> str:
    repo = cfg["repo"]
    sha, cdate, by_product = load_catalog(silo, ref, cfg["silo_catalog"], cfg["silo_data_dir"])
    mapping = load_mapping(repo / cfg["reconciliation_tsv"])
    tag_to_ids: dict[str, set[str]] = defaultdict(set)
    for i, tag in mapping.items():
        tag_to_ids[tag].add(i)

    products = []
    for d in sorted((repo / cfg["products_dir"]).glob("*/*")):
        if d.is_dir() and d.name in by_product:
            products.append((d.parent.name, d.name, d))
    shared = shared_paths(silo, sha, cfg["silo_data_dir"], by_product)
    top_paths = [e["path"] for _, slug, _ in products for e in by_product[slug]
                 if len(PurePosixPath(e.get("path", "")).parts) == 3 and PurePosixPath(e["path"]).name not in SILO_GENERATED]
    urls = web_urls(silo, sha, cfg["silo_data_dir"], top_paths)
    hosts = list(cfg.get("non_public_hosts", []))

    min_docs, min_prob, top = int(cfg["min_docs"]), float(cfg["min_probability"]), int(cfg["top_docs"])
    L = [
        "# Silo candidate signals",
        "",
        f"> Generated by [`tools/silo-candidates`](../tools/silo-candidates/README.md) from `prod_info_silo` commit "
        f"`{sha[:10]}` ({cdate}). Do not edit by hand; re-run the tool.",
        "",
        "**Leads, not facts.** The silo's classifier tags documents by keyword and probability. A candidate means "
        "the silo sees a sub-feature for a product that no matrix row covers. It is input for the LLM-assisted step "
        "(Plan 08 part 2) and for a human; it never becomes a ✅ or ❌ without a checked source.",
        "",
        f"- A tag counts for a document when its probability is ≥ {min_prob:.2f}; a candidate needs ≥ {min_docs} such documents.",
        "- A matrix row covers a tag when its ID is the tag, or maps to it in "
        "[`taxonomy-reconciliation.tsv`](taxonomy-reconciliation.tsv).",
        "- **Web** documents are public pages, listed by URL. **Repo** documents and **source** files come from "
        "GitHub repositories, many private: they are counted, never named. A page whose URL is on a code host, "
        "or whose file the silo does not store, counts as **source**.",
        "- **Shared**: entries whose page (same URL) or file (same content) is indexed under more than one silo "
        "product, for example the same repository copied into several products. A candidate that is mostly shared "
        "may belong to another product.",
        "- IDs in a matrix's pointer table (rows documented in another product's matrix) are not candidates; "
        "they are listed per product instead.",
        "",
        "## Summary",
        "",
        "| Product | Matrix IDs | Candidates | Web-backed | Only repo/source | Mostly shared | Matrix IDs the silo never tags |",
        "|---|---|---|---|---|---|---|",
    ]
    sections = []
    for cat, slug, d in products:
        ids, pointer_ids = matrix_ids(d)
        covered_tags = {mapping.get(i, i) for i in ids}
        pointer_tags = {mapping.get(i, i) for i in pointer_ids} - covered_tags
        sig = signals_for(by_product[slug], urls, shared, min_prob, hosts)
        leads = [s for t, s in sig.items() if s.total >= min_docs and t not in covered_tags]
        cands = sorted((s for s in leads if s.tag not in pointer_tags), key=lambda s: (-len(s.web), -s.total, s.tag))
        elsewhere = sorted(s.tag for s in leads if s.tag in pointer_tags)
        # "never tags" looks at every probability: a weak tag is still a tag
        seen_tags = {t for e in by_product[slug] for t in (e.get("sub_feature_tags") or [])}
        unseen = sorted(i for i in ids if mapping.get(i, i) not in seen_tags)
        web_backed = sum(bool(s.web) for s in cands)
        mostly_shared = sum(s.shared * 2 > s.total for s in cands)
        L.append(f"| [{slug}](#{slug}) | {len(ids)} | {len(cands)} | {web_backed} | {len(cands) - web_backed} | "
                 f"{mostly_shared} | {len(unseen)} |")
        S = [f"## {slug}", "", f"Matrices: [`{cat}/{slug}`](../products/{cat}/{slug}/product-report.md) · "
             f"{len(ids)} matrix IDs · {len(cands)} candidates", ""]
        if cands:
            S += ["| Silo tag | Also known as | Web | Repo | Source | Shared | Top public pages |", "|---|---|---|---|---|---|---|"]
            for s in cands:
                aka = ", ".join(f"`{i}`" for i in sorted(tag_to_ids.get(s.tag, set()) - {s.tag})) or "—"
                pages = " · ".join(f"[{_cell(t) or u}]({u}) ({p:.2f})" for p, t, u in s.web[:top]) or "—"
                S.append(f"| `{s.tag}` | {aka} | {len(s.web)} | {s.repo_docs} | {s.source_files} | {s.shared} | {pages} |")
            S.append("")
        if elsewhere:
            S += ["Silo tags for rows this product's pointer table documents in another product's matrix: "
                  + ", ".join(f"`{t}`" for t in elsewhere), ""]
        if unseen:
            S += ["Matrix IDs the silo never tags for this product (at any probability): "
                  + ", ".join(f"`{i}`" for i in unseen), ""]
        sections += S
    unmatched = sorted(f"{d.parent.name}/{d.name}" for d in (repo / cfg["products_dir"]).glob("*/*")
                       if d.is_dir() and d.name not in by_product)
    L += ["", *sections, "## Analysed products without a silo product", ""]
    L += [f"- `{u}`" for u in unmatched] or ["None."]
    L.append("")
    return "\n".join(L)


# ---------------------------------------------------------------- main


def load_config(path: Path = HERE / "silo-candidates.toml", repo: Path = REPO) -> dict:
    cfg = tomllib.loads(path.read_text(encoding="utf-8"))
    cfg["repo"] = repo
    cfg["silo_path"] = (repo / cfg["silo_path"]).resolve()
    cfg["output_path"] = (repo / cfg["output"]).resolve()
    if cfg["output_path"].parent != (repo / "reports").resolve() or not cfg["output_path"].name.startswith("silo-candidates") \
            or cfg["output_path"].suffix != ".md":
        raise ReadOnlyViolation(f"{cfg['output_path']} is not reports/silo-candidates*.md (other reports belong to other tools)")
    return cfg


def run(cfg: dict, command: str, silo_root: Path | None = None, ref: str | None = None) -> str:
    report = build(cfg, silo_root or cfg["silo_path"], ref or cfg["silo_ref"])
    if command == "plan":
        return report
    guarded_write(cfg["output_path"], report, cfg["output_path"])
    return f"wrote {cfg['output']}"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("command", choices=["plan", "apply"])
    ap.add_argument("--silo", type=Path, help="override silo_path from the config")
    ap.add_argument("--ref", help="override silo_ref from the config")
    a = ap.parse_args(argv)
    print(run(load_config(), a.command, a.silo.resolve() if a.silo else None, a.ref))
    return 0


if __name__ == "__main__":
    sys.exit(main())
