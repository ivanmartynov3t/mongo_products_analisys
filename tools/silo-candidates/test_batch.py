# /// script
# requires-python = ">=3.11"
# ///
"""Offline tests for the evidence batches.

    uv run tools/silo-candidates/test_batch.py

Runs on a throwaway silo and a throwaway analysis repository in a temp directory.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import batch  # noqa: E402
import candidates  # noqa: E402

failures: list[str] = []
SECRET = "hiddenrepo-x"


def check(name: str, actual, expected) -> None:
    if actual != expected:
        failures.append(f"{name}\n     expected: {expected!r}\n     actual:   {actual!r}")


def sh(root: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True, text=True).stdout


def commit(root: Path) -> str:
    sh(root, "add", "-A")
    sh(root, "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", "commit", "-qm", "c")
    return sh(root, "rev-parse", "HEAD").strip()


def entry(path: str, tags: dict[str, float], title: str = "T") -> dict:
    return {"path": path, "title": title, "sub_feature_tags": sorted(tags), "sub_feature_probabilities": tags}


CATALOG = {"by_product": {"prod": [
    entry("vendor/prod/p1.md", {"QUERY-new": 0.9, "QUERY-done": 0.9}, "Page | one"),
    entry("vendor/prod/p2.md", {"QUERY-new": 0.8, "QUERY-done": 0.9}, "Page two"),
    entry("vendor/prod/gh.md", {"QUERY-new": 0.95}),                            # code host: not public
    entry(f"vendor/prod/repo_docs/{SECRET}/README.md", {"QUERY-new": 0.9, "QUERY-repo": 0.9}),
    entry("vendor/prod/src/secret_module.py", {"QUERY-repo": 0.9}),
]}}


def page(url: str, body: str, updated: str = "2026-09-20 10:00:00 UTC") -> str:
    return f"---\ntitle: T\nsource_url: {url}\nupdated_at: {updated}\n---\n\n{body}\n"


def build(tmp: Path) -> tuple[Path, Path, str]:
    silo, repo = tmp / "silo", tmp / "repo"
    sh(tmp, "init", "-q", str(silo))
    for rel, text in {"data/catalog_index.json": json.dumps(CATALOG),
                      "data/vendor/prod/p1.md": page("https://vendor.test/one", "Filter bars are saved per view."),
                      "data/vendor/prod/p2.md": page("https://vendor.test/two", "Second page body.", "2026-09-21 x"),
                      "data/vendor/prod/gh.md": page(f"https://github.com/acme/{SECRET}/blob/main/README.md", "Private readme."),
                      f"data/vendor/prod/repo_docs/{SECRET}/README.md": "---\ntitle: R\n---\n\nPrivate doc.\n"}.items():
        (silo / rel).parent.mkdir(parents=True, exist_ok=True)
        (silo / rel).write_text(text, encoding="utf-8")
    sha = commit(silo)
    for rel, text in {
        "feature-dictionary.md": "| Sub-feature ID | Name | Description |\n|---|---|---|\n"
                                 "| QUERY-new | Filter bar | A saved filter bar \\| per view |\n| QUERY-alias | Alias | Old name |\n",
        "products/g/prod/features/q/feature-matrix.md": "| Sub-feature ID | Name | Current support | Sources |\n|---|---|---|---|\n"
                                                        "| QUERY-covered | C | Confirmed | S1 |\n",
        "reports/taxonomy-reconciliation.tsv": "id\tname\tin_silo\tverdict\tmaps_to\tsilo_detects_via\n"
                                               "QUERY-covered\tc\tyes\tsame definition\tQUERY-covered\tQUERY-covered\n"
                                               "QUERY-alias\ta\tno\tretired\tQUERY-new\tQUERY-new\n",
        "tools/silo-candidates/triage.tsv": "\t".join(candidates.LEDGER_COLUMNS) + "\n"
                                            + "\t".join(["prod", "QUERY-done", "noise", "2026-09-26", "abcdef1", "2", "#1"]) + "\n",
    }.items():
        (repo / rel).parent.mkdir(parents=True, exist_ok=True)
        (repo / rel).write_text(text, encoding="utf-8")
    return silo, repo, sha


def tree(root: Path) -> dict[str, str]:
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*")) if p.is_file() and ".git" not in p.parts}


def test_all(tmp: Path) -> None:
    silo, repo, sha = build(tmp)
    ccfg = candidates.load_config(candidates.HERE / "silo-candidates.toml", repo)
    ccfg["silo_path"], ccfg["silo_ref"] = silo, "HEAD"
    before, silo_before = tree(repo), tree(silo)
    check("plan writes nothing", (batch.run(ccfg, "plan").startswith("would write 1 batches, 1 candidates, 2 pages"), tree(repo)),
          (True, before))
    check("apply summary", batch.run(ccfg, "apply").startswith("wrote .local/silo-batches: 1 batches, 1 candidates, 2 pages"), True)
    out = repo / ".local/silo-batches/prod"
    readme = (out / "README.md").read_text()
    check("only open web-backed candidates: decided and repo-only ones left out",
          ("## `QUERY-new`" in readme, "QUERY-done" in readme, "QUERY-repo" in readme), (True, False, False))
    check("aliases and dictionary definitions (escaped pipes kept)",
          ("Also known as: `QUERY-alias`" in readme, "Dictionary `QUERY-new`: Filter bar — A saved filter bar \\| per view" in readme),
          (True, True))
    check("every public page, best first, with retrieval date and pin",
          [l.split(" | ")[2:5] for l in readme.splitlines() if l.startswith("| 1 ") or l.startswith("| 2 ")],
          [["0.90", "2026-09-20", f"`https://vendor.test/one` (silo: `data/vendor/prod/p1.md@{sha[:8]}`)"],
           ["0.80", "2026-09-21", f"`https://vendor.test/two` (silo: `data/vendor/prod/p2.md@{sha[:8]}`)"]])
    check("page title with a pipe escaped", "[Page \\| one](https://vendor.test/one)" in readme, True)
    bodies = sorted(p.read_text() for p in (out / "pages").glob("*.md"))
    check("page bodies without frontmatter", bodies, ["Filter bars are saved per view.\n", "Second page body.\n"])
    everything = "".join(p.read_text() for p in out.rglob("*") if p.is_file())
    check("no private repository, code-host page or source file", any(x in everything for x in (SECRET, "acme", "secret_module",
                                                                                                "Private")), False)
    check("current matrix rows listed", "| QUERY-covered | Confirmed |" in readme, True)
    changed = sorted(k for k, v in tree(repo).items() if before.get(k) != v)
    check("apply writes only under .local/silo-batches", all(k.startswith(".local/silo-batches/") for k in changed), True)
    check("silo untouched", tree(silo), silo_before)
    first = tree(out)
    (out / "stale.md").write_text("old")
    batch.run(ccfg, "apply")
    check("rebuilt from scratch and deterministic", tree(out), first)

    # a catalog page the silo does not store has no URL, so it is never a web page (candidates counts it as source)
    cat = json.loads(json.dumps(CATALOG))
    cat["by_product"]["prod"].append(entry("vendor/prod/p3.md", {"QUERY-new": 0.85}))
    (silo / "data/catalog_index.json").write_text(json.dumps(cat))
    commit(silo)
    batch.run(ccfg, "apply")
    readme = (out / "README.md").read_text()
    check("unstored page never listed", "vendor/prod/p3.md" in readme, False)

    (repo / "tools/silo-candidates/triage.tsv").write_text("wrong\n")
    try:
        batch.run(ccfg, "plan")
        failures.append("malformed ledger accepted")
    except candidates.CandidatesError:
        pass


def test_write_guard(tmp: Path) -> None:
    repo = tmp / "guard"
    for bad in (repo / "reports", repo / ".local" / "other", tmp / "elsewhere" / ".local" / "silo-batches"):
        try:
            batch.write(repo, bad, {"p": {"README.md": "x"}})
            failures.append(f"write to {bad} accepted")
        except batch.ReadOnlyViolation:
            pass
    root = repo / ".local" / "silo-batches"
    batch.write(repo, root, {"p": {"README.md": "old"}})
    try:
        batch.write(repo, root, {"p": {"../../escape.md": "x"}})
        failures.append("path escape accepted")
    except batch.ReadOnlyViolation:
        pass
    check("escape not written; previous batches kept on a failed write",
          ((repo / "escape.md").exists(), (root / "p/README.md").read_text(), (repo / ".local/silo-batches.new").exists()),
          (False, "old", False))


def main() -> int:
    with tempfile.TemporaryDirectory() as d:
        test_all(Path(d))
        test_write_guard(Path(d))
    if failures:
        print(f"FAILED ({len(failures)}):")
        for f in failures:
            print(" -", f)
        return 1
    print("ok: all batch tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
