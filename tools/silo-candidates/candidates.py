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
import json
import re
import sys
import tomllib
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent

sys.path.insert(0, str(HERE.parent / "silo-review"))
from review import ReadOnlyViolation, cat_batch, frontmatter, git, guarded_write  # noqa: E402

ID_HEADERS = ("Sub-feature ID", "Capability ID")
GENERATED = {"README.md", "DIFF.md", "repo_source_strings.md"}


class CandidatesError(RuntimeError):
    pass


# ---------------------------------------------------------------- analysis repo


def matrix_ids(product_dir: Path) -> set[str]:
    """First-column IDs of every capability table (one with a status column) in the product's matrices."""
    ids: set[str] = set()
    for m in sorted(product_dir.glob("features/*/feature-matrix.md")):
        in_table = False
        for line in m.read_text(encoding="utf-8").splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")] if line.startswith("|") else []
            if not cells:
                in_table = False
            elif cells[0].startswith(ID_HEADERS):
                # capability tables only (they have a status column), not "Moved to" or index tables
                in_table = "Current support" in cells or "Status" in cells
            elif in_table and not set(cells[0]) <= set("-: "):
                ids.add(cells[0].strip("`* "))
    return ids


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
    shared: int = 0   # entries whose file is also indexed under another product

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


def signals_for(entries: list[dict], urls: dict[str, str], shared_suffixes: set[str],
                min_probability: float) -> dict[str, Signal]:
    out: dict[str, Signal] = {}
    for e in entries:
        path = e.get("path", "")
        parts = PurePosixPath(path).parts
        suffix = "/".join(parts[2:])
        for tag in e.get("sub_feature_tags") or []:
            prob = float((e.get("sub_feature_probabilities") or {}).get(tag, 0))
            if prob < min_probability:
                continue
            s = out.setdefault(tag, Signal(tag))
            if len(parts) == 3 and path in urls and urls[path] and "github.com" not in urls[path]:
                s.web.append((prob, str(e.get("title", "")), urls[path]))
            elif len(parts) > 3 and parts[2] == "repo_docs":
                s.repo_docs += 1
            else:
                s.source_files += 1
            s.shared += suffix in shared_suffixes
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
    suffix_products: dict[str, set[str]] = defaultdict(set)
    for slug, entries in by_product.items():
        for e in entries:
            suffix_products["/".join(PurePosixPath(e.get("path", "")).parts[2:])].add(slug)
    shared = {s for s, ps in suffix_products.items() if len(ps) > 1}
    top_paths = [e["path"] for _, slug, _ in products for e in by_product[slug]
                 if len(PurePosixPath(e.get("path", "")).parts) == 3 and PurePosixPath(e["path"]).name not in GENERATED]
    urls = web_urls(silo, sha, cfg["silo_data_dir"], top_paths)

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
        "GitHub repositories, many private: they are counted, never named.",
        "- **Shared**: entries whose file is indexed under more than one silo product (the same repository copied "
        "into several products). A candidate that is mostly shared may belong to another product.",
        "",
        "## Summary",
        "",
        "| Product | Matrix IDs | Candidates | Web-backed | Only repo/source | Mostly shared | Matrix IDs the silo never tags |",
        "|---|---|---|---|---|---|---|",
    ]
    sections = []
    for cat, slug, d in products:
        ids = matrix_ids(d)
        covered_tags = {mapping.get(i, i) for i in ids}
        sig = signals_for(by_product[slug], urls, shared, min_prob)
        cands = sorted((s for t, s in sig.items() if s.total >= min_docs and t not in covered_tags),
                       key=lambda s: (-len(s.web), -s.total, s.tag))
        seen_tags = {t for t, s in sig.items()}
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
        if unseen:
            S += ["Matrix IDs the silo never tags for this product: " + ", ".join(f"`{i}`" for i in unseen), ""]
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
    if cfg["output_path"].parent != (repo / "reports").resolve():
        raise ReadOnlyViolation(f"{cfg['output_path']} is outside reports/")
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
