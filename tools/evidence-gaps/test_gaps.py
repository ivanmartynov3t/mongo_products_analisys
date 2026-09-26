# /// script
# requires-python = ">=3.11"
# ///
"""Offline tests for evidence-gaps.

    uv run tools/evidence-gaps/test_gaps.py

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

import gaps  # noqa: E402

failures: list[str] = []


def check(name: str, actual, expected) -> None:
    if actual != expected:
        failures.append(f"{name}\n     expected: {expected!r}\n     actual:   {actual!r}")


def commit(root: Path, files: dict[str, str]) -> None:
    for rel, text in files.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text, encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(root), "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false",
                    "commit", "-qm", "c"], check=True)


MATRIX_URLS = """# M

## Feature metadata

- Analysis date: 2026-09-20

## Source index

- S1: https://vendor.test/tracked
- S2: https://www.reddit.com/r/x/1
- S3: https://jira.example.atlassian.net/browse/X-1
- S4: https://github.com/org/repo/releases
- S5: https://docs.other.test/page
- S6: https://sub.reddit.com/thread
- S7: http://127.0.0.1:27117/admin
- S8: https://notreddit.com/page
- S9: https://github.com/org/repo/issues/12
- S10: https://github.com/org/repo
- S11: https://github.com/org
- S12: https://github.com/org/repo/blob/abc123/docs/guide.md
- S13: https://vendor.test/deleted
- S14: https://github.com/orgs/org/repositories

| Sub-feature ID | Capability | Current support | Sources |
| --- | --- | --- | --- |
| QUERY-a | A | Supported | S1 |
| QUERY-b | B | Supported | S5 |
| QUERY-c | C | Supported | S5 |
"""

MATRIX_NONE = """# M

## Feature metadata

- Analysis date: 2026-09-20

| Sub-feature ID | Capability | Current support | Sources |
| --- | --- | --- | --- |
| QUERY-x | X | Supported | research file |
"""


def build(tmp: Path) -> tuple[Path, Path]:
    silo, repo = tmp / "silo", tmp / "repo"
    subprocess.run(["git", "init", "-q", str(silo)], check=True)
    page = lambda url, ck: (f"---\ntitle: T\nsource_url: {url}\nupdated_at: 2026-09-10 10:00:00 UTC\n"  # noqa: E731
                            f"checksum_sha256: {ck}\n---\n\nThe page at {url} has enough words to count as content.\n")
    commit(silo, {"data/vendor/prod/tracked.md": page("https://vendor.test/tracked", "c1"),
                  "data/vendor/prod/deleted.md": page("https://vendor.test/deleted", "d1")})
    (silo / "data/vendor/prod/deleted.md").unlink()
    commit(silo, {})  # the silo dropped this page: a gap, like an untracked one
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    snapshot = {"silo": {"commit": "b" * 40}, "products": [
        {"slug": "prod", "analysis_folder": "products/g/prod", "web_pages": 1, "repo_docs": 0},
        {"slug": "rich", "analysis_folder": "products/g/rich", "web_pages": 50, "repo_docs": 0},
        {"slug": "even", "analysis_folder": "products/g/even", "web_pages": 2, "repo_docs": 0},
    ]}
    commit(repo, {
        "products/g/prod/features/querying/feature-matrix.md": MATRIX_URLS,
        "products/g/rich/features/querying/feature-matrix.md": MATRIX_NONE,
        "products/g/orphan/features/querying/feature-matrix.md": MATRIX_NONE,
        # two matrices, two IDs in total, two silo documents: not thin (IDs of both matrices count)
        "products/g/even/features/querying/feature-matrix.md": MATRIX_NONE,
        "products/g/even/features/export/feature-matrix.md": MATRIX_NONE.replace("QUERY-x", "EXPORT-y"),
        "reports/silo-snapshot.json": json.dumps(snapshot),
        "tools/silo-review/silo-review.toml": 'silo_path = "../silo"\nsilo_ref = "HEAD"\nsilo_data_dir = "data"\n'
            'output = "reports/review-queue.md"\nscan = ["products/**/*.md"]\nexclude = []\n',
    })
    return silo, repo


def hashes(root: Path) -> dict[str, str]:
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*")) if p.is_file() and ".git" not in p.parts}


def section(report: str, title: str) -> str:
    return report.split(title, 1)[1].split("\n### ", 1)[0].split("\n## ", 1)[0]


def test_all(tmp: Path) -> None:
    silo, repo = build(tmp)
    cfg = gaps.load_config(gaps.HERE / "evidence-gaps.toml", repo)
    cfg["silo_path"], cfg["silo_ref"] = silo, "HEAD"
    report = gaps.run(cfg, "plan")
    check("matrices without URLs listed", "4 of 5 feature matrices cite no URL" in report, True)
    check("matrix with URLs not listed as no-URL", "products/g/prod/features" in section(report, "## 1."), False)
    thin = section(report, "## 2.")
    check("thin: fewer silo docs than matrix IDs", "| `products/g/prod` | 3 | 1 | — |" in thin, True)
    check("thin: product with no silo product", "| `products/g/orphan` | 1 | 0 | no silo product |" in thin, True)
    check("thin: well-covered product not listed", "products/g/rich" in thin, False)
    check("thin: documents equal to IDs is not thin, IDs summed over matrices", "products/g/even" in thin, False)
    ev_rows = [l for l in thin.splitlines() if l.startswith("| `")]
    check("thin rows", ev_rows, ["| `products/g/orphan` | 1 | 0 | no silo product |", "| `products/g/prod` | 3 | 1 | — |"])
    check("tracked URL is not a gap; dropped URL is", "| vendor.test | 1 |" in section(report, "### Crawlable"), True)
    check("12 untracked or dropped URLs", "13 of 14 distinct cited URLs" in report, True)
    check("crawlable rows (count desc, then domain)", [l for l in section(report, "### Crawlable").splitlines() if l.startswith("| ") and "---" not in l], [
        "| Domain | URLs |", "| github.com | 3 |", "| docs.other.test | 1 |", "| notreddit.com | 1 |", "| vendor.test | 1 |"])
    check("excluded by policy, subdomains included",
          ("| reddit.com | 1 |" in section(report, "### Excluded"), "| sub.reddit.com | 1 |" in section(report, "### Excluded")),
          (True, True))
    check("internal, port ignored", [l for l in section(report, "### Internal").splitlines() if l.startswith("| ") and "---" not in l],
          ["| Domain | URLs |", "| 127.0.0.1:27117 | 1 |", "| jira.example.atlassian.net | 1 |"])
    check("GitHub issues are excluded like other trackers", "| github.com | 1 |" in section(report, "### Excluded"), True)
    check("other GitHub pages (organisation, /orgs/)", "| github.com | 2 |" in section(report, "### Other GitHub"), True)
    check("plural", ("2 URLs on 1 domain." in section(report, "### Other GitHub"),
                     "2 URLs on 2 domains." in section(report, "### Internal")), (True, True))
    check("host_matches: subdomains and ports, not look-alikes",
          [gaps.review.host_matches(n, ["reddit.com", "127.0.0.1"]) for n in
           ("reddit.com/x", "old.reddit.com/x", "notreddit.com/x", "127.0.0.1:27117/a", "")],
          [True, True, False, True, False])
    check("snapshot from another commit is flagged", "**Warning:** the snapshot" in report, True)
    check("no full URLs in the report", re.search(r"https?://(?!github\.com/ivanmartynov3t)", report) is None, True)
    check("deterministic", gaps.run(cfg, "plan"), report)

    before, silo_before = hashes(repo), hashes(silo)
    gaps.run(cfg, "apply")
    after = hashes(repo)
    check("apply writes only the output", sorted(k for k in after if after[k] != before.get(k)), ["reports/evidence-gaps.md"])
    check("silo untouched", hashes(silo), silo_before)


def test_output_restricted(tmp: Path) -> None:
    for out in ("products/x.md", "reports/review-queue.md", "reports/evidence-gaps.json"):
        bad = tmp / "bad.toml"
        bad.write_text((gaps.HERE / "evidence-gaps.toml").read_text().replace(
            'output = "reports/evidence-gaps.md"', f'output = "{out}"'), encoding="utf-8")
        try:
            gaps.load_config(bad, tmp)
            failures.append(f"output {out} accepted")
        except gaps.ReadOnlyViolation:
            pass


def test_no_direct_writes() -> None:
    src = (gaps.HERE / "gaps.py").read_text(encoding="utf-8")
    check("only review.guarded_write writes", re.findall(r"\.(?:write_text|write_bytes)\(|open\([^)]*['\"][wa]", src), [])


def main() -> int:
    with tempfile.TemporaryDirectory() as d:
        test_all(Path(d))
        test_output_restricted(Path(d))
    test_no_direct_writes()
    if failures:
        print(f"FAILED ({len(failures)}):")
        for f in failures:
            print(" -", f)
        return 1
    print("ok: all evidence-gaps tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
