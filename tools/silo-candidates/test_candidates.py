# /// script
# requires-python = ">=3.11"
# ///
"""Offline tests for silo-candidates.

    uv run tools/silo-candidates/test_candidates.py

Runs on a throwaway silo and a throwaway analysis repository in a temp directory.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import candidates  # noqa: E402

failures: list[str] = []


def check(name: str, actual, expected) -> None:
    if actual != expected:
        failures.append(f"{name}\n     expected: {expected!r}\n     actual:   {actual!r}")


def entry(path: str, tags: dict[str, float], title: str = "T") -> dict:
    return {"path": path, "title": title, "sub_feature_tags": sorted(tags), "sub_feature_probabilities": tags}


CATALOG = {"by_product": {
    "prod": [
        entry("vendor/prod/page1.md", {"QUERY-new": 0.9, "QUERY-covered": 0.9, "QUERY-mapped": 0.9, "QUERY-weak": 0.5}, "Page one"),
        entry("vendor/prod/page2.md", {"QUERY-new": 0.8, "QUERY-covered": 0.8, "QUERY-mapped": 0.8, "QUERY-weak": 0.6}, "Page two"),
        entry("vendor/prod/gh.md", {"QUERY-new": 0.95}, "Private repo readme"),
        entry("vendor/prod/repo_docs/secret-service/README.md", {"QUERY-repo": 0.9}, "Secret service"),
        entry("vendor/prod/src/secret_module.py", {"QUERY-repo": 0.9}, "secret_module.py (Source Code)"),
        entry("vendor/prod/shared.md", {"QUERY-single": 0.9}),
    ],
    "other": [entry("vendor/other/shared.md", {"QUERY-single": 0.9})],
}}


def page(url: str) -> str:
    return f"---\ntitle: T\nsource_url: {url}\n---\n\nBody.\n"


MATRIX = """# M

| Sub-feature ID | Moved to | Why |
|---|---|---|
| QUERY-new | elsewhere | moved |

| Sub-feature ID | Capability | Current support | Sources |
| --- | --- | --- | --- |
| QUERY-covered | Covered | Supported | S1 |
| QUERY-child | Child row | Supported | S1 |
| QUERY-unseen | Never tagged | Supported | S1 |
"""

TSV = ("id\tname\tin_silo\tverdict\tmaps_to\tsilo_detects_via\n"
       "QUERY-covered\tc\tyes\tsame definition\tQUERY-covered\tQUERY-covered\n"
       "QUERY-parent\tp\tyes\tsame definition\tQUERY-parent\tQUERY-mapped\n"
       "QUERY-child\tch\tno\tchild-of\tQUERY-parent\t\n")


def git_commit(root: Path) -> None:
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(root), "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false",
                    "commit", "-qm", "c"], check=True)


def build(tmp: Path) -> tuple[Path, Path]:
    silo, repo = tmp / "silo", tmp / "repo"
    files = {
        "data/catalog_index.json": json.dumps(CATALOG),
        "data/vendor/prod/page1.md": page("https://vendor.test/one"),
        "data/vendor/prod/page2.md": page("https://vendor.test/two"),
        "data/vendor/prod/gh.md": page("https://github.com/org/private-repo/blob/main/README.md"),
        "data/vendor/prod/shared.md": page("https://vendor.test/shared"),
        "data/vendor/other/shared.md": page("https://vendor.test/shared"),
    }
    subprocess.run(["git", "init", "-q", str(silo)], check=True)
    for rel, text in files.items():
        (silo / rel).parent.mkdir(parents=True, exist_ok=True)
        (silo / rel).write_text(text, encoding="utf-8")
    git_commit(silo)
    (repo / "products/g/prod/features/querying").mkdir(parents=True)
    (repo / "products/g/prod/features/querying/feature-matrix.md").write_text(MATRIX, encoding="utf-8")
    (repo / "products/g/unmatched").mkdir(parents=True)
    (repo / "reports").mkdir()
    (repo / "reports/taxonomy-reconciliation.tsv").write_text(TSV, encoding="utf-8")
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    git_commit(repo)
    return silo, repo


def hashes(root: Path) -> dict[str, str]:
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*")) if p.is_file() and ".git" not in p.parts}


def test_all(tmp: Path) -> None:
    silo, repo = build(tmp)
    cfg = candidates.load_config(candidates.HERE / "silo-candidates.toml", repo)
    cfg["silo_path"], cfg["silo_ref"] = silo, "HEAD"
    check("capability tables only", candidates.matrix_ids(repo / "products/g/prod"),
          {"QUERY-covered", "QUERY-child", "QUERY-unseen"})
    report = candidates.run(cfg, "plan")
    rows = [l for l in report.split("## prod")[1].splitlines() if l.startswith("| `")]
    tags = [l.split("`")[1] for l in rows]
    check("candidates: uncovered tags with enough strong documents", tags, ["QUERY-new", "QUERY-repo"])
    new = rows[0]
    check("web pages listed by URL", "(https://vendor.test/one) (0.90)" in new and "(https://vendor.test/two)" in new, True)
    check("counts: 2 web, GitHub-sourced page counted as source", new.split(" | ")[2:5], ["2", "0", "1"])
    check("covered directly and via child-of mapping are not candidates",
          "QUERY-covered" in tags or "QUERY-mapped" in tags, False)
    check("below probability threshold is not a candidate", "QUERY-weak" in report, False)
    check("single-document tag is not a candidate", "`QUERY-single`" in report, False)
    check("matrix IDs the silo never tags", "never tags for this product: `QUERY-child`, `QUERY-unseen`" in report, False)
    check("child row counts as seen through its mapping", "never tags for this product: `QUERY-unseen`" in report, True)
    for secret in ("secret", "Secret", "private-repo", "Private repo"):
        check(f"repository content never named ({secret})", secret in report, False)
    check("unmatched analysis folder listed", "- `g/unmatched`" in report, True)
    check("silo commit recorded", subprocess.run(["git", "-C", str(silo), "rev-parse", "HEAD"], capture_output=True,
          text=True).stdout.strip()[:10] in report, True)
    check("deterministic", candidates.run(cfg, "plan"), report)

    before, silo_before = hashes(repo), hashes(silo)
    candidates.run(cfg, "plan")
    check("plan writes nothing", hashes(repo), before)
    candidates.run(cfg, "apply")
    after = hashes(repo)
    check("apply writes only the output", sorted(k for k in after if after[k] != before.get(k)), ["reports/silo-candidates.md"])
    check("silo untouched", hashes(silo), silo_before)

    (silo / "data/catalog_index.json").unlink()
    git_commit(silo)
    try:
        candidates.run(cfg, "plan")
        failures.append("missing catalog did not raise")
    except candidates.CandidatesError:
        pass


def test_output_restricted(tmp: Path) -> None:
    bad = tmp / "bad.toml"
    bad.write_text((candidates.HERE / "silo-candidates.toml").read_text().replace(
        'output = "reports/silo-candidates.md"', 'output = "products/x.md"'), encoding="utf-8")
    try:
        candidates.load_config(bad, tmp)
        failures.append("output outside reports/ accepted")
    except candidates.ReadOnlyViolation:
        pass


def test_single_write_site() -> None:
    src = (candidates.HERE / "candidates.py").read_text(encoding="utf-8")
    check("no direct writes (only review.guarded_write)",
          re.findall(r"\.(?:write_text|write_bytes)\(|open\([^)]*['\"][wa]", src), [])


def main() -> int:
    with tempfile.TemporaryDirectory() as d:
        test_all(Path(d))
        test_output_restricted(Path(d))
    test_single_write_site()
    if failures:
        print(f"FAILED ({len(failures)}):")
        for f in failures:
            print(" -", f)
        return 1
    print("ok: all silo-candidates tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
