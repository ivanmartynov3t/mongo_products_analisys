# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Offline tests for silo-snapshot.

    uv run tools/silo-snapshot/test_snapshot.py

Everything runs on a throwaway silo (a git repository) and a throwaway analysis repository
built in a temp directory; the real repositories are never read.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import snapshot  # noqa: E402

failures: list[str] = []


def check(name: str, actual, expected) -> None:
    if actual != expected:
        failures.append(f"{name}\n     expected: {expected!r}\n     actual:   {actual!r}")


# ------------------------------------------------------------------ fixtures

CONFIG = """products:
  - slug: alpha
    category: 3t
    track: Build Track
    status: Live
    name: Alpha | One
    entry_urls:
      - https://alpha.example/
    sitemap_urls:
      - https://alpha.example/sitemap.xml
    github_repos:
      - https://github.com/org/alpha
  - slug: beta
    category: 3t
    track: Govern Track
    status: Planned
    name: Beta
  - slug: gamma
    category: third-party
    name: Gamma
    entry_urls:
      - https://gamma.example/
"""


def page(url: str, updated: str) -> str:
    return f"---\ntitle: T\nsource_url: {url}\nupdated_at: {updated}\n---\n\n# T\n\nBody.\n"


CATALOG = {
    "version": "1.0",
    "total_documents": 7,
    "by_product": {
        "alpha": [
            {"path": "3t/alpha/one.md", "category": "3t"},
            {"path": "3t/alpha/repo_docs/org/README.md", "category": "3t"},
            {"path": "3t/alpha/src/main.py", "category": "3t"},
            {"path": "3t/alpha/src/util.py", "category": "3t"},
            {"path": "3t/delta/repo_docs/x.md", "category": "3t"},  # stored under another product's folder
        ],
        "gamma": [{"path": "third-party/gamma/index.md", "category": "third-party"},
                  {"path": "3t/gamma/other.md", "category": "3t"}],  # same slug, other category
    },
}

SILO_FILES = {
    "config/products.yaml": CONFIG,
    "data/catalog_index.json": json.dumps(CATALOG),
    "data/README.md": "# master dashboard\n",
    "data/3t/alpha/README.md": "# dashboard\n",
    "data/3t/alpha/DIFF.md": "# diff\n",
    "data/3t/alpha/repo_source_strings.md": "strings\n",
    "data/3t/alpha/one.md": page("https://alpha.example/one", "2026-09-20 10:00:00 UTC"),
    "data/3t/alpha/two.md": page("https://alpha.example/two", "2026-09-22 08:00:00 UTC"),
    "data/3t/alpha/repo_docs/org/README.md": "# repo readme\n",
    "data/3t/alpha/repo_symbols_and_strings.json": json.dumps({"scraped_at": "2026-09-23T01:02:03+00:00"}),
    "data/3t/delta/repo_docs/x.md": "# not in config\n",
    "data/third-party/gamma/index.md": page("https://gamma.example/", "2026-09-01 00:00:00 UTC"),
}


def git_commit(root: Path, msg: str) -> None:
    env = {**os.environ, "GIT_AUTHOR_DATE": "2026-09-24T12:00:00", "GIT_COMMITTER_DATE": "2026-09-24T12:00:00"}
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True, env=env)
    subprocess.run(["git", "-C", str(root), "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false",
                    "commit", "-qm", msg], check=True, env=env)


def build_silo(root: Path) -> None:
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    for rel, text in SILO_FILES.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    git_commit(root, "silo")
    # Uncommitted working-tree changes must never reach the snapshot.
    (root / "data/3t/alpha/uncommitted.md").write_text(page("https://alpha.example/new", "2026-09-30 00:00:00 UTC"))
    (root / "data/3t/alpha/one.md").write_text(page("https://alpha.example/one", "2026-09-29 00:00:00 UTC"))


def build_repo(root: Path) -> None:
    for rel in ("products/3t/alpha", "products/3t/govern", "products/third-party/gamma"):
        (root / rel).mkdir(parents=True)
        (root / rel / "product-report.md").write_text("# report\n")
    (root / "reports").mkdir()
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    git_commit(root, "init")


def config_for(repo: Path, silo: Path) -> dict:
    cfg = snapshot.load_config(snapshot.HERE / "silo-snapshot.toml", repo)
    cfg["silo_path"] = silo
    cfg["silo_ref"] = "HEAD"
    return cfg


def tree_hashes(root: Path) -> dict[str, str]:
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*")) if p.is_file() and ".git" not in p.parts}


def git_state(root: Path) -> dict[str, str]:
    refs = subprocess.run(["git", "-C", str(root), "for-each-ref", "--format=%(refname) %(objectname)"],
                          capture_output=True, text=True, check=True).stdout
    return {".git/HEAD": (root / ".git/HEAD").read_text(), ".git/refs": refs}


# ------------------------------------------------------------------ tests


def test_missing_inputs(tmp: Path) -> None:
    """A missing or malformed config or catalog stops the run; it never yields a snapshot of zeros."""
    cases = {
        "missing catalog": {"data/catalog_index.json": None},
        "missing config": {"config/products.yaml": None},
        "catalog without by_product": {"data/catalog_index.json": json.dumps({"total_documents": 0})},
        "config without products": {"config/products.yaml": "other: 1\n"},
    }
    for name, change in cases.items():
        root = tmp / name.replace(" ", "-")
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        for rel, text in {**SILO_FILES, **change}.items():
            if text is None:
                continue
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            (root / rel).write_text(text, encoding="utf-8")
        git_commit(root, "silo")
        try:
            snapshot.load_silo(root, "HEAD", "data", "config/products.yaml", "data/catalog_index.json")
            failures.append(f"{name}: no error raised")
        except snapshot.SnapshotError:
            pass


def test_output_paths_restricted(tmp: Path) -> None:
    cfg_file = tmp / "bad.toml"
    cfg_file.write_text((snapshot.HERE / "silo-snapshot.toml").read_text().replace(
        'output_md = "reports/silo-snapshot.md"', 'output_md = "products/x.md"'))
    try:
        snapshot.load_config(cfg_file, tmp)
        failures.append("load_config accepted an output outside reports/")
    except snapshot.ReadOnlyViolation:
        pass


def test_snapshot(tmp: Path) -> None:
    silo, repo = tmp / "silo", tmp / "repo"
    build_silo(silo)
    build_repo(repo)
    cfg = config_for(repo, silo)
    sha = subprocess.run(["git", "-C", str(silo), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()

    s = snapshot.load_silo(silo, "HEAD", "data", "config/products.yaml", "data/catalog_index.json")
    snap = snapshot.build_snapshot(s, repo, "products")
    rows = {r["slug"]: r for r in snap["products"]}

    check("silo commit recorded", snap["silo"]["commit"], sha)
    check("silo commit date", snap["silo"]["commit_date"], "2026-09-24")
    check("every configured product and every data folder is listed", sorted(set(rows)), ["alpha", "beta", "delta", "gamma"])
    a = rows["alpha"]
    check("web pages exclude dashboards, strings and uncommitted files", a["web_pages"], 2)
    check("repo docs counted", a["repo_docs"], 1)
    check("catalog entries", a["catalog_entries"], 5)
    check("catalog entries that are not stored files are source files (any folder)", a["catalog_source_files"], 2)
    check("web retrieved is the latest committed updated_at", a["web_written"], "2026-09-22")
    check("repo scraped from repo_symbols_and_strings.json", a["repo_scraped"], "2026-09-23")
    check("seeds from config", (a["entry_urls"], a["sitemap_urls"], a["github_repos"]),
          (["https://alpha.example/"], ["https://alpha.example/sitemap.xml"], 1))
    check("analysis folder matched by slug", a["analysis_folder"], "products/3t/alpha")
    b = rows["beta"]
    check("configured product with no data is listed with zeros",
          (b["in_config"], b["web_pages"], b["repo_docs"], b["catalog_entries"], b["web_written"], b["analysis_folder"]),
          (True, 0, 0, 0, "", ""))
    check("data folder missing from config is flagged", (rows["delta"]["in_config"], rows["delta"]["repo_docs"]), (False, 1))
    check("catalog entries are counted only under their own category",
          (rows["gamma"]["catalog_entries"], {(r["category"], r["slug"]) for r in snap["products"]} >= {("3t", "gamma"), ("third-party", "gamma")}), (1, True))
    check("third-party product has no track or status", (rows["gamma"]["track"], rows["gamma"]["status"]), ("", ""))
    check("analysis folders without a silo product", snap["analysis_folders_without_silo_product"], ["products/3t/govern"])

    before = tree_hashes(repo)
    silo_before = tree_hashes(silo) | git_state(silo)
    md = snapshot.run(cfg, "plan")
    check("plan writes nothing", tree_hashes(repo), before)
    check("deterministic output", snapshot.run(cfg, "plan"), md)
    check("pipe in a product name is escaped", "Alpha \\| One" in md, True)
    check("report names the silo commit", sha[:10] in md, True)
    check("GitHub repository names are never published", "github.com/org/alpha" in md or "github.com/org/alpha" in json.dumps(snap), False)
    check("report does not show uncommitted silo content", "alpha.example/new" in md or "2026-09-29" in md, False)

    msg = snapshot.run(cfg, "apply")
    check("apply message", msg.startswith("wrote reports/silo-snapshot.md and reports/silo-snapshot.json"), True)
    after = tree_hashes(repo)
    check("apply writes exactly the two outputs",
          sorted(k for k in after if before.get(k) != after[k]), ["reports/silo-snapshot.json", "reports/silo-snapshot.md"])
    check("markdown output equals plan output", (repo / "reports/silo-snapshot.md").read_text(), md)
    data = json.loads((repo / "reports/silo-snapshot.json").read_text())
    check("json output equals the snapshot", data, snap)
    check("silo tree, HEAD and refs unchanged", tree_hashes(silo) | git_state(silo), silo_before)

    # Determinism across processes: set ordering differs between hash seeds.
    outs = {subprocess.run([sys.executable, "-c",
                            "import sys; sys.path.insert(0, sys.argv[1]); import snapshot, pathlib;"
                            "cfg = snapshot.load_config(snapshot.HERE / 'silo-snapshot.toml', pathlib.Path(sys.argv[2]));"
                            "cfg['silo_path'] = pathlib.Path(sys.argv[3]); cfg['silo_ref'] = 'HEAD';"
                            "print(snapshot.run(cfg, 'plan'))", str(snapshot.HERE), str(repo), str(silo)],
                           capture_output=True, text=True, check=True,
                           env={**os.environ, "PYTHONHASHSEED": seed}).stdout for seed in ("1", "2", "3")}
    check("identical output under different hash seeds", len(outs), 1)
    snapshot.run(cfg, "apply")
    check("re-apply is byte-identical", tree_hashes(repo), after)


def test_write_guard(tmp: Path) -> None:
    allowed = {tmp / "reports" / "silo-snapshot.md", tmp / "reports" / "silo-snapshot.json"}
    try:
        snapshot.guarded_write(tmp / "products" / "x.md", "x", allowed)
        failures.append("guarded_write accepted a path other than the outputs")
    except snapshot.ReadOnlyViolation:
        pass


def test_single_write_site() -> None:
    src = (snapshot.HERE / "snapshot.py").read_text(encoding="utf-8")
    writes = re.findall(r"\.(?:write_text|write_bytes)\(|open\([^)]*['\"][wa]", src)
    check("the only write in snapshot.py is inside guarded_write", len(writes), 1)


def test_latest_date() -> None:
    check("mixed timestamp formats", snapshot._latest_date(["2026-09-20 10:00:00 UTC", "2026-09-21T00:00:00+00:00", "", "N/A"]),
          "2026-09-21")
    check("no dates", snapshot._latest_date(["", "unknown"]), "")


def main() -> int:
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        test_snapshot(tmp)
        test_write_guard(tmp)
        test_missing_inputs(tmp)
        test_output_paths_restricted(tmp)
    test_single_write_site()
    test_latest_date()
    if failures:
        print(f"FAILED ({len(failures)}):")
        for f in failures:
            print(" -", f)
        return 1
    print("ok: all silo-snapshot tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
