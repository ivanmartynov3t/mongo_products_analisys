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
        entry("vendor/prod/page1.md", {"QUERY-new": 0.9, "QUERY-covered": 0.9, "QUERY-mapped": 0.9, "QUERY-weak": 0.5}, "Page [one] | x"),
        entry("vendor/prod/page2.md", {"QUERY-new": 0.75, "QUERY-covered": 0.8, "QUERY-mapped": 0.8, "QUERY-weak": 0.6}, "Page two"),
        entry("vendor/prod/page1dup.md", {"QUERY-new": 0.9}, "Page one again"),  # same page, trailing slash
        entry("vendor/prod/gh.md", {"QUERY-new": 0.95}, "Private repo readme"),
        entry("vendor/prod/repo_docs/secret-service/README.md", {"QUERY-repo": 0.9}, "Secret service"),
        entry("vendor/prod/src/secret_module.py", {"QUERY-repo": 0.9}, "secret_module.py (Source Code)"),
        entry("vendor/prod/shared.md", {"QUERY-shared": 0.9}),
        entry("vendor/prod/repo_docs/lib/guide.md", {"QUERY-shared": 0.9}, "Lib guide"),
        entry("vendor/prod/index.md", {"QUERY-home": 0.9}),
        entry("vendor/prod/features.md", {"QUERY-home": 0.9}),
        entry("vendor/prod/moved1.md", {"QUERY-moved": 0.9}),
        entry("vendor/prod/moved2.md", {"QUERY-moved": 0.9}),
        entry("vendor/prod/annot1.md", {"QUERY-pending": 0.9, "QUERY-b": 0.9}),
        entry("vendor/prod/annot2.md", {"QUERY-pending": 0.9, "QUERY-b": 0.9}),
    ],
    "other": [
        entry("vendor/other/shared.md", {"QUERY-x": 0.9}),                 # same URL: shared
        entry("vendor/other/repo_docs/lib/guide.md", {"QUERY-x": 0.9}),    # same body: shared
        entry("vendor/other/index.md", {"QUERY-x": 0.9}),                  # same name, another vendor: not shared
    ],
}}


def page(url: str, body: str = "Body.") -> str:
    return f"---\ntitle: T\nsource_url: {url}\n---\n\n{body}\n"


MATRIX = """# M

| Sub-feature ID | Moved to | Why |
|---|---|---|
| QUERY-moved, QUERY-gone | [elsewhere](x.md) | moved |

| Sub-feature ID | Capability | Current support | Sources |
| --- | --- | --- | --- |
| QUERY-covered | Covered | Supported | S1 |
| QUERY-child | Child row | Supported | S1 |
| QUERY-unseen | Never tagged | Supported | S1 |
| QUERY-weak | Weakly tagged | Supported | S1 |
| `QUERY-pending` **(PENDING DICTIONARY ADDITION — borderline F-CONN)** | Annotated | Supported | S1 |
| QUERY-a / QUERY-b | Compound | Supported | S1 |
"""

MATRIX2 = """# M2

| Capability ID | Capability | Status |
|---|---|---|
| QUERY-cap | From a Capability ID table | Supported |
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
        "data/vendor/prod/page1dup.md": page("https://vendor.test/one/"),
        "data/vendor/prod/gh.md": page("https://github.com/org/private-repo/blob/main/README.md"),
        "data/vendor/prod/shared.md": page("https://vendor.test/shared"),
        "data/vendor/other/shared.md": page("https://www.vendor.test/shared/"),
        "data/vendor/prod/repo_docs/lib/guide.md": page("https://github.com/o/lib/blob/a/guide.md", "Same guide."),
        "data/vendor/other/repo_docs/lib/guide.md": page("https://github.com/o/lib/blob/b/guide.md", "Same guide."),
        "data/vendor/prod/index.md": page("https://vendor.test/"),
        "data/vendor/other/index.md": page("https://another.test/"),
        "data/vendor/prod/features.md": page("https://vendor.test/features"),
        "data/vendor/prod/moved1.md": page("https://vendor.test/m1"),
        "data/vendor/prod/moved2.md": page("https://vendor.test/m2"),
        "data/vendor/prod/annot1.md": page("https://vendor.test/a1"),
        "data/vendor/prod/annot2.md": page("https://vendor.test/a2"),
    }
    subprocess.run(["git", "init", "-q", str(silo)], check=True)
    for rel, text in files.items():
        (silo / rel).parent.mkdir(parents=True, exist_ok=True)
        (silo / rel).write_text(text, encoding="utf-8")
    git_commit(silo)
    (repo / "products/g/prod/features/querying").mkdir(parents=True)
    (repo / "products/g/prod/features/querying/feature-matrix.md").write_text(MATRIX, encoding="utf-8")
    (repo / "products/g/prod/features/shell").mkdir(parents=True)
    (repo / "products/g/prod/features/shell/feature-matrix.md").write_text(MATRIX2, encoding="utf-8")
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
    check("capability and pointer IDs (annotations and compound cells parsed)", candidates.matrix_ids(repo / "products/g/prod"),
          ({"QUERY-covered", "QUERY-child", "QUERY-unseen", "QUERY-weak", "QUERY-pending", "QUERY-a", "QUERY-b", "QUERY-cap"},
           {"QUERY-moved", "QUERY-gone"}))
    report = candidates.run(cfg, "plan")
    prod = report.split("## prod")[1]
    rows = [l for l in prod.splitlines() if l.startswith("| `")]
    check("candidate rows: web first, then total, then tag; Web | Repo | Source | Shared", [l.split(" | ")[0:6] for l in rows], [
        ["| `QUERY-new`", "—", "2", "0", "1", "0"],      # 0.75 counts; …/one/ is the same page; GitHub page is source
        ["| `QUERY-home`", "—", "2", "0", "0", "0"],     # index.md of another vendor is not shared
        ["| `QUERY-shared`", "—", "1", "1", "0", "2"],   # same URL and same body under another product
        ["| `QUERY-repo`", "—", "0", "1", "1", "0"],
    ])
    check("web pages listed by URL, best first, titles escaped", rows[0].split(" | ")[6],
          "[Page \\[one\\] \\| x](https://vendor.test/one) (0.90) · [Page two](https://vendor.test/two) (0.75) |")
    check("summary row", next(l for l in report.splitlines() if l.startswith("| [prod]")), "| [prod](#prod) | 8 | 4 | 3 | 1 | 1 | 3 |")
    check("covered directly, via child-of mapping, annotated or compound IDs are not candidates",
          [t for t in ("QUERY-covered", "QUERY-mapped", "QUERY-pending", "QUERY-b") if f"| `{t}`" in prod], [])
    check("pointer-table IDs listed, not candidates",
          "documents in another product's matrix: `QUERY-moved`" in prod and "| `QUERY-moved`" not in prod, True)
    check("below probability threshold is not a candidate", "`QUERY-weak` |" in report, False)
    check("never tags: any probability counts; child row seen through its mapping",
          "never tags for this product (at any probability): `QUERY-a`, `QUERY-cap`, `QUERY-unseen`" in prod, True)
    for secret in ("secret", "Secret", "private-repo", "Private repo", "Lib guide", "github.com/o/lib"):
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
