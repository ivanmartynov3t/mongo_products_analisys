#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""Candidate-signal queue: silo sub-feature tags with no matrix row (issues #36, #52).

    uv run tools/silo-candidates/candidates.py plan      # print the report, write nothing
    uv run tools/silo-candidates/candidates.py apply     # write reports/silo-candidates.md

For every analysed product that has a silo product of the same name, lists the silo's
sub-feature tags (from `data/catalog_index.json`) that no row of the product's matrices
covers, and the matrix IDs the silo never tags for that product. The silo classifier is
noisy: a candidate is a lead for the LLM part (Plan 09) and a human, never a fact.

Candidates already decided in the triage ledger (`triage.tsv`) leave the tables; one comes
back when the silo holds more public pages for it than when it was decided.

Read-only by construction: the silo is read from git objects at a pinned ref; the only
file this tool may write is the configured output. Documents from repositories are only
counted, never named: this repository is public and many silo repositories are private.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import tomllib
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent

sys.path.insert(0, str(HERE.parent / "silo-review"))
from review import (FM_RE, SILO_GENERATED, ReadOnlyViolation, cat_batch, frontmatter, git,  # noqa: E402
                    guarded_write, host_matches, host_of, matrix_table_ids, normalize_url)


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


# ---------------------------------------------------------------- triage ledger

OUTCOMES = ("add-row", "existing-row", "other-product", "noise", "needs-human")
LEDGER_COLUMNS = ["product", "tag", "outcome", "date", "silo_commit", "web_docs", "ref"]
_SHA_RE = re.compile(r"[0-9a-f]{7,40}")
_TAG_RE = re.compile(r"[A-Z]+-[A-Za-z0-9-]+")   # every silo tag; the tag is the one ledger field the report shows
_COUNT_RE = re.compile(r"[0-9]+")


def _is_date(text: str) -> bool:
    try:
        if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", text):
            return False
        date.fromisoformat(text)   # raises on an impossible date such as 2026-02-30
        return True
    except ValueError:
        return False


@dataclass(frozen=True)
class Decision:
    product: str
    tag: str
    outcome: str
    web_docs: int   # public pages the silo held for the candidate when it was decided


def load_ledger(path: Path, products: set[str]) -> dict[tuple[str, str], Decision]:
    """(product, tag) -> decision. Any malformed row stops the run: a typo must not hide a candidate."""
    if not path.exists():
        return {}
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].split("\t") != LEDGER_COLUMNS:
        raise CandidatesError(f"{path.name}: the header must be {chr(9).join(LEDGER_COLUMNS)!r}")
    out: dict[tuple[str, str], Decision] = {}
    for n, line in enumerate(lines[1:], start=2):
        if not line.strip():
            continue
        cells = line.split("\t")
        if len(cells) != len(LEDGER_COLUMNS):
            raise CandidatesError(f"{path.name}:{n}: {len(cells)} columns, expected {len(LEDGER_COLUMNS)}")
        r = dict(zip(LEDGER_COLUMNS, (c.strip() for c in cells)))
        problems = []
        if r["product"] not in products:
            problems.append(f"unknown product {r['product']!r}")
        if not _TAG_RE.fullmatch(r["tag"]):
            problems.append(f"tag {r['tag']!r} is not a silo tag (e.g. QUERY-projection)")
        if r["outcome"] not in OUTCOMES:
            problems.append(f"outcome {r['outcome']!r} is not one of {', '.join(OUTCOMES)}")
        if not _is_date(r["date"]):
            problems.append(f"date {r['date']!r} is not a YYYY-MM-DD date")
        if not _SHA_RE.fullmatch(r["silo_commit"]):
            problems.append(f"silo_commit {r['silo_commit']!r} is not 7-40 lowercase hex")
        if not _COUNT_RE.fullmatch(r["web_docs"]):
            problems.append(f"web_docs {r['web_docs']!r} is not a count")
        if not r["ref"]:
            problems.append("empty ref (a PR or a one-line reason)")
        if problems:
            raise CandidatesError(f"{path.name}:{n}: " + "; ".join(problems))
        key = (r["product"], r["tag"])
        if key in out:
            raise CandidatesError(f"{path.name}:{n}: {r['product']} / {r['tag']} is already decided on an earlier line")
        out[key] = Decision(r["product"], r["tag"], r["outcome"], int(r["web_docs"]))
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
    norm = normalize_url(url) if url else ""
    return bool(host_of(norm)) and not host_matches(norm, non_public_hosts)


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


def build(cfg: dict, silo: Path, ref: str, open_web: dict[str, list[str]] | None = None) -> str:
    """The report. When `open_web` is given, it also receives each product's open web-backed candidate tags."""
    repo = cfg["repo"]
    # The ledger is checked first: a malformed one stops the run before the silo is read.
    folders = {d.name for d in (repo / cfg["products_dir"]).glob("*/*") if d.is_dir()}
    ledger = load_ledger(repo / cfg["triage_ledger"], folders)
    sha, cdate, by_product = load_catalog(silo, ref, cfg["silo_catalog"], cfg["silo_data_dir"])
    no_silo = sorted({p for p, _ in ledger if p not in by_product})
    if no_silo:
        raise CandidatesError(f"{PurePosixPath(cfg['triage_ledger']).name}: no silo product for "
                              + ", ".join(no_silo) + " (such rows would have no effect)")
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
        "(Plan 09) and for a human; it never becomes a ✅ or ❌ without a checked source.",
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
        "- Candidates decided in the triage ledger "
        f"([`{PurePosixPath(cfg['triage_ledger']).name}`](../{cfg['triage_ledger']})) leave the tables. One is "
        "**re-opened** when the silo now holds more public pages for it than when it was decided. "
        "`needs-human` decisions stay listed per product until someone resolves them.",
        "",
        "## Summary",
        "",
        "Candidates, Web-backed, Only repo/source and Mostly shared count open candidates only.",
        "",
        "| Product | Matrix IDs | Candidates | Web-backed | Only repo/source | Mostly shared | Triaged | Matrix IDs the silo never tags |",
        "|---|---|---|---|---|---|---|---|",
    ]
    sections = []
    for cat, slug, d in products:
        ids, pointer_ids = matrix_ids(d)
        covered_tags = {mapping.get(i, i) for i in ids}
        pointer_tags = {mapping.get(i, i) for i in pointer_ids} - covered_tags
        sig = signals_for(by_product[slug], urls, shared, min_prob, hosts)
        leads = [s for t, s in sig.items() if s.total >= min_docs and t not in covered_tags]
        decided = {t: dec for (p, t), dec in ledger.items() if p == slug}
        reopened = {s.tag for s in leads if s.tag in decided and len(s.web) > decided[s.tag].web_docs}
        cands = sorted((s for s in leads if s.tag not in pointer_tags and (s.tag not in decided or s.tag in reopened)),
                       key=lambda s: (-len(s.web), -s.total, s.tag))
        elsewhere = sorted(s.tag for s in leads if s.tag in pointer_tags)
        # "never tags" looks at every probability: a weak tag is still a tag
        seen_tags = {t for e in by_product[slug] for t in (e.get("sub_feature_tags") or [])}
        unseen = sorted(i for i in ids if mapping.get(i, i) not in seen_tags)
        web_backed = sum(bool(s.web) for s in cands)
        if open_web is not None:
            open_web[slug] = [s.tag for s in cands if s.web]
        mostly_shared = sum(s.shared * 2 > s.total for s in cands)
        per_outcome = {o: sum(d.outcome == o for d in decided.values()) for o in OUTCOMES}
        triaged = " · ".join(f"{o} {n}" for o, n in per_outcome.items() if n) or "—"
        L.append(f"| [{slug}](#{slug}) | {len(ids)} | {len(cands)} | {web_backed} | {len(cands) - web_backed} | "
                 f"{mostly_shared} | {triaged} | {len(unseen)} |")
        S = [f"## {slug}", "", f"Matrices: [`{cat}/{slug}`](../products/{cat}/{slug}/product-report.md) · "
             f"{len(ids)} matrix IDs · {len(cands)} candidates", ""]
        if cands:
            S += ["| Silo tag | Also known as | Web | Repo | Source | Shared | Top public pages |", "|---|---|---|---|---|---|---|"]
            for s in cands:
                aka = ", ".join(f"`{i}`" for i in sorted(tag_to_ids.get(s.tag, set()) - {s.tag})) or "—"
                pages = " · ".join(f"[{_cell(t) or u}]({u}) ({p:.2f})" for p, t, u in s.web[:top]) or "—"
                note = (f" (re-opened: {decided[s.tag].outcome} with {decided[s.tag].web_docs} web)"
                        if s.tag in reopened else "")
                S.append(f"| `{s.tag}`{note} | {aka} | {len(s.web)} | {s.repo_docs} | {s.source_files} | {s.shared} | {pages} |")
            S.append("")
        lead_tags = {s.tag for s in leads}
        waiting = sorted(t for t, dec in decided.items()
                         if dec.outcome == "needs-human" and t in lead_tags and t not in reopened)
        if waiting:
            S += ["Waiting for a human (`needs-human` in the ledger): " + ", ".join(f"`{t}`" for t in waiting), ""]
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
    try:
        print(run(load_config(), a.command, a.silo.resolve() if a.silo else None, a.ref))
    except (CandidatesError, ReadOnlyViolation) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
