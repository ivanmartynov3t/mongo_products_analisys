#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Per-product snapshot of prod_info_silo for this repository (issue #34).

    uv run tools/silo-snapshot/snapshot.py plan      # print the Markdown snapshot, write nothing
    uv run tools/silo-snapshot/snapshot.py apply     # write reports/silo-snapshot.md and .json

One place for the silo facts this repository otherwise copies by hand: silo commit, and per
product its status, track, document counts, last retrieval dates and seed URLs.

Read-only by construction: the silo is read from git objects at a pinned ref (never checked
out, never written), and the only files this tool may write are the two configured outputs.
Silo data is context for a human, never evidence for a ✅ or ❌.
"""

from __future__ import annotations

import argparse
import json
import sys
import tomllib
from pathlib import Path, PurePosixPath

import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent

sys.path.insert(0, str(HERE.parent / "silo-review"))
from review import ReadOnlyViolation, cat_batch, frontmatter, git  # noqa: E402

# Generated files in a product folder that are not documents (same rule as the silo's
# TaxonomyClassifier.is_generated_dashboard_or_strings).
GENERATED = {"README.md", "DIFF.md", "repo_source_strings.md"}
REPO_SYMBOLS = "repo_symbols_and_strings.json"


class SnapshotError(RuntimeError):
    """A silo input is missing or malformed; better no snapshot than a snapshot of zeros."""


# ---------------------------------------------------------------- write guard


def guarded_write(path: Path, text: str, allowed: set[Path]) -> None:
    """The only write in this tool. Anything but the configured outputs is refused."""
    if path.resolve() not in {a.resolve() for a in allowed}:
        raise ReadOnlyViolation(f"refusing to write {path}: only {sorted(map(str, allowed))} may be written")
    path.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------- silo


def _latest_date(values: list[str]) -> str:
    """Latest YYYY-MM-DD among timestamps like '2026-09-25 14:16:54 UTC' or ISO 8601; '' if none."""
    days = [v.strip()[:10] for v in values if len(v.strip()) >= 10 and v.strip()[4] == "-"]
    return max(days) if days else ""


def load_silo(root: Path, ref: str, data_dir: str, config_path: str, catalog_path: str) -> dict:
    """Everything the snapshot needs, read from git objects at `ref` only."""
    sha = git(root, "rev-parse", "--verify", f"{ref}^{{commit}}").strip()
    cdate = git(root, "show", "-s", "--format=%cs", sha).strip()
    paths = git(root, "ls-tree", "-r", "--name-only", "-z", sha, "--", data_dir).split("\0")
    paths = [p for p in paths if p]

    blobs = cat_batch(root, [f"{sha}:{config_path}", f"{sha}:{catalog_path}"])
    for path in (config_path, catalog_path):
        if not blobs[f"{sha}:{path}"]:
            raise SnapshotError(f"{path} is missing or empty at silo {sha[:10]}")
    config = yaml.safe_load(blobs[f"{sha}:{config_path}"])
    catalog = json.loads(blobs[f"{sha}:{catalog_path}"])
    if not isinstance(config, dict) or not isinstance(config.get("products"), list):
        raise SnapshotError(f"{config_path} has no 'products' list at silo {sha[:10]}")
    if not isinstance(catalog, dict) or not isinstance(catalog.get("by_product"), dict):
        raise SnapshotError(f"{catalog_path} has no 'by_product' object at silo {sha[:10]}")

    # data/<category>/<slug>/...
    web: dict[tuple[str, str], list[str]] = {}
    repo_docs: dict[tuple[str, str], list[str]] = {}
    symbols: dict[tuple[str, str], list[str]] = {}
    for p in paths:
        parts = PurePosixPath(p).parts
        if len(parts) < 4 or parts[0] != data_dir:
            continue
        key = (parts[1], parts[2])
        name = parts[-1]
        if len(parts) == 4 and name.endswith(".md") and name not in GENERATED:
            web.setdefault(key, []).append(p)
        elif len(parts) > 4 and parts[3] == "repo_docs" and name.endswith(".md"):
            repo_docs.setdefault(key, []).append(p)
        elif len(parts) == 4 and name == REPO_SYMBOLS:
            symbols.setdefault(key, []).append(p)

    texts = cat_batch(root, [f"{sha}:{p}" for ps in (*web.values(), *symbols.values()) for p in ps])
    web_dates = {k: _latest_date([frontmatter(texts[f"{sha}:{p}"]).get("updated_at", "") for p in ps]) for k, ps in web.items()}
    repo_scraped: dict[tuple[str, str], str] = {}
    for k, ps in symbols.items():
        stamps = []
        for p in ps:
            try:
                data = json.loads(texts[f"{sha}:{p}"])
            except json.JSONDecodeError:
                continue
            if isinstance(data, dict):
                stamps.append(str(data.get("scraped_at", "")))
            else:
                pass
        repo_scraped[k] = _latest_date(stamps)

    return {
        "sha": sha, "commit_date": cdate, "data_dir": data_dir,
        "products": config["products"], "catalog": catalog,
        "stored": {p for ps in (*web.values(), *repo_docs.values()) for p in ps},
        "web": web, "repo_docs": repo_docs, "web_dates": web_dates, "repo_scraped": repo_scraped,
    }


# ---------------------------------------------------------------- snapshot


def build_snapshot(silo: dict, repo: Path, products_dir: str) -> dict:
    by_product = silo["catalog"].get("by_product") or {}
    configured = {(p.get("category", ""), p["slug"]): p for p in silo["products"] if p.get("slug")}
    keys = set(configured) | set(silo["web"]) | set(silo["repo_docs"]) | set(silo["repo_scraped"])
    for slug, entries in by_product.items():
        cats = {e.get("category", "") for e in entries}
        keys |= {(c, slug) for c in cats}

    rows = []
    for cat, slug in sorted(keys):
        cfg = configured.get((cat, slug), {})
        entries = [e for e in by_product.get(slug, []) if e.get("category", "") == cat]
        # Any stored document counts, wherever it lives: the catalog may file a page under
        # another product's folder (e.g. 3t-lens entries in policy-engine/repo_docs/).
        source_files = sum(1 for e in entries if f"{silo['data_dir']}/{e.get('path', '')}" not in silo["stored"])
        folder = PurePosixPath(products_dir, cat, slug)
        rows.append({
            "slug": slug,
            "category": cat,
            "name": cfg.get("name", ""),
            "track": cfg.get("track", ""),
            "status": cfg.get("status", ""),
            "in_config": bool(cfg),
            "web_pages": len(silo["web"].get((cat, slug), [])),
            "repo_docs": len(silo["repo_docs"].get((cat, slug), [])),
            "catalog_entries": len(entries),
            "catalog_source_files": source_files,
            "web_retrieved": silo["web_dates"].get((cat, slug), ""),
            "repo_scraped": silo["repo_scraped"].get((cat, slug), ""),
            "entry_urls": sorted(cfg.get("entry_urls") or []),
            "sitemap_urls": sorted(cfg.get("sitemap_urls") or []),
            # Count only: many of these repositories are private, and this repository is public.
            "github_repos": len(cfg.get("github_repos") or []),
            "analysis_folder": str(folder) if (repo / folder).is_dir() else "",
        })

    matched = {r["analysis_folder"] for r in rows if r["analysis_folder"]}
    unmatched = sorted(
        str(PurePosixPath(products_dir, d.parent.name, d.name))
        for d in (repo / products_dir).glob("*/*") if d.is_dir()
        and str(PurePosixPath(products_dir, d.parent.name, d.name)) not in matched
    )
    return {
        "silo": {
            "commit": silo["sha"],
            "commit_date": silo["commit_date"],
            "catalog_total_documents": silo["catalog"].get("total_documents"),
        },
        "products": rows,
        "analysis_folders_without_silo_product": unmatched,
    }


def _cell(value) -> str:
    text = str(value) if value not in ("", None) else "—"
    return text.replace("|", "\\|")


def _product_cell(r: dict) -> str:
    name = " ".join(str(r["name"] or r["slug"]).split()).replace("[", "\\[").replace("]", "\\]")
    return f"[{_cell(name)}](../{r['analysis_folder']}/product-report.md)" if r["analysis_folder"] else _cell(name)


def render_markdown(snap: dict, output_json: str) -> str:
    s = snap["silo"]
    out = [
        "# Silo snapshot",
        "",
        f"> Generated by [`tools/silo-snapshot`](../tools/silo-snapshot/README.md) from `prod_info_silo` commit "
        f"`{s['commit'][:10]}` ({s['commit_date']}). Do not edit by hand; re-run the tool. "
        f"Machine-readable copy: [`{PurePosixPath(output_json).name}`]({PurePosixPath(output_json).name}).",
        "",
        "Silo facts only. A count here says what the silo holds, not what a product can do.",
        "",
        "## Columns",
        "",
        "- **Web pages:** crawled pages stored for the product (generated dashboards excluded).",
        "- **Repo docs:** documents copied from the product's GitHub repositories (`repo_docs/`).",
        "- **Catalog:** entries in the silo's `catalog_index.json` for the product: classified web pages and repo docs, "
        "plus indexed source files (in brackets). This is the figure earlier records called \"docs\".",
        "- **Web written:** the latest date a stored web page was written or changed (`updated_at`; unchanged pages are not rewritten).",
        "- **Repo scraped:** the latest date the silo scraped the product's repositories.",
        "- **Seed URLs / Repos:** public web entry points, and the number of GitHub repositories the silo scrapes.",
        "- **Analysis:** the matching folder in this repository (same name as the silo slug).",
        "",
    ]
    titles = {"3t": "3T products", "third-party": "Third-party products"}
    cats = sorted({r["category"] for r in snap["products"]}, key=lambda c: (c not in titles, list(titles).index(c) if c in titles else 0, c))
    for cat in cats:
        title, with_track = titles.get(cat, f"Category `{cat or '(none)'}`"), cat != "third-party"
        rows = [r for r in snap["products"] if r["category"] == cat]
        if not rows:
            continue
        head = ["Product", "Silo slug"] + (["Track", "Status"] if with_track else []) + \
               ["Web pages", "Repo docs", "Catalog", "Web written", "Repo scraped", "Seed URLs", "Repos", "Analysis"]
        out += [f"## {title}", "", "| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
        for r in rows:
            seeds = len(r["entry_urls"]) + len(r["sitemap_urls"])
            cells = [_product_cell(r), f"`{r['slug']}`" + ("" if r["in_config"] else " (not in config)")]
            if with_track:
                cells += [_cell(r["track"]), _cell(r["status"])]
            cells += [str(r["web_pages"]), str(r["repo_docs"]),
                      f"{r['catalog_entries']} ({r['catalog_source_files']})",
                      _cell(r["web_retrieved"]), _cell(r["repo_scraped"]), str(seeds), str(r["github_repos"]),
                      "✓" if r["analysis_folder"] else "—"]
            out.append("| " + " | ".join(cells) + " |")
        out.append("")

    out += ["## Analysis folders without a silo product", ""]
    out += [f"- `{f}`" for f in snap["analysis_folders_without_silo_product"]] or ["None."]
    out += ["", "## Seed URLs", "",
            "Public web entry points from the silo's `config/products.yaml` (entry URLs and sitemaps). "
            "GitHub repositories are counted in the tables but not named: many are private.", ""]
    for r in snap["products"]:
        seeds = [*r["entry_urls"], *r["sitemap_urls"]]
        if not seeds:
            continue
        out.append(f"- **{r['name'] or r['slug']}** (`{r['slug']}`)")
        out += [f"  - {u}" for u in seeds]
    out.append("")
    return "\n".join(out)


# ---------------------------------------------------------------- main


def load_config(path: Path = HERE / "silo-snapshot.toml", repo: Path = REPO) -> dict:
    cfg = tomllib.loads(path.read_text(encoding="utf-8"))
    cfg["repo"] = repo
    cfg["silo_path"] = (repo / cfg["silo_path"]).resolve()
    cfg["output_md_path"] = (repo / cfg["output_md"]).resolve()
    cfg["output_json_path"] = (repo / cfg["output_json"]).resolve()
    reports = (repo / "reports").resolve()
    for key in ("output_md_path", "output_json_path"):
        if cfg[key].parent != reports:
            raise ReadOnlyViolation(f"{cfg[key]} is outside {reports}; outputs must be in reports/")
    return cfg


def run(cfg: dict, command: str, silo_root: Path | None = None, ref: str | None = None) -> str:
    """Execute one command against a loaded config; returns what `main` prints."""
    silo = load_silo(silo_root or cfg["silo_path"], ref or cfg["silo_ref"], cfg.get("silo_data_dir", "data"),
                     cfg.get("silo_config", "config/products.yaml"), cfg.get("silo_catalog", "data/catalog_index.json"))
    snap = build_snapshot(silo, cfg["repo"], cfg.get("products_dir", "products"))
    md = render_markdown(snap, cfg["output_json"])
    if command == "plan":
        return md
    allowed = {cfg["output_md_path"], cfg["output_json_path"]}
    guarded_write(cfg["output_md_path"], md, allowed)
    guarded_write(cfg["output_json_path"], json.dumps(snap, indent=2, sort_keys=True, ensure_ascii=False) + "\n", allowed)
    return f"wrote {cfg['output_md']} and {cfg['output_json']} (silo {silo['sha'][:10]}, {len(snap['products'])} products)"


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
