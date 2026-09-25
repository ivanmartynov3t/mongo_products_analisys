# /// script
# requires-python = ">=3.11"
# ///
"""Offline tests for silo-review.

    uv run tools/silo-review/test_review.py

Everything runs on a throwaway silo (a git repository with dated commits) and a
throwaway analysis repository built in a temp directory; the real repositories are
never read.
"""

from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import review  # noqa: E402

failures: list[str] = []


def check(name: str, actual, expected) -> None:
    if actual != expected:
        failures.append(f"{name}\n     expected: {expected!r}\n     actual:   {actual!r}")


# ------------------------------------------------------------------ fixtures

CHROME = "Found this useful? Add this vendor as a preferred source in your news feed."
BODY_V1 = "The export wizard supports CSV, JSON and BSON formats for every collection.\nScheduling an export requires the Pro edition of the product today."
BODY_V2 = BODY_V1 + "\nA new Parquet export format was added in release twelve for all editions."


def doc(url: str, body: str, *, checksum: str, lm: str = "", fetched: str = "2026-09-10", banner: bool = False) -> str:
    extra = f"\n{CHROME}" if banner else ""
    return (f"---\ntitle: T\nsource_url: {url}\nupdated_at: {fetched} 10:00:00 UTC\n"
            f"checksum_sha256: {checksum}\n" + (f"http_last_modified: {lm}\n" if lm else "") +
            f"---\n\n# Page title\n\n> **Source:** [{url}]({url})\n\n{body}{extra}\n")


def commit(root: Path, day: str, files: dict[str, str | None], msg: str) -> None:
    for rel, text in files.items():
        p = root / rel
        if text is None:
            p.unlink()
        else:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8")
    env = {**os.environ, "GIT_AUTHOR_DATE": f"{day}T12:00:00", "GIT_COMMITTER_DATE": f"{day}T12:00:00"}
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True, env=env)
    subprocess.run(["git", "-C", str(root), "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", msg], check=True, env=env)


def build_silo(root: Path) -> None:
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    P = "data/vendor/prod/"
    # 09-01: first capture of everything
    commit(root, "2026-09-01", {
        P + "changed.md": doc("https://www.vendor.test/export/", BODY_V1, checksum="a1"),
        P + "rerender.md": doc("https://vendor.test/rerender", BODY_V1, checksum="b1", banner=True),
        P + "stable.md": doc("https://vendor.test/stable", BODY_V1, checksum="c1"),
        P + "stamped.md": doc("https://vendor.test/stamped", BODY_V1, checksum="e1",
                              lm="Thu, 10 Sep 2026 10:00:00 GMT", fetched="2026-09-10"),
        P + "gone.md": doc("https://vendor.test/gone", BODY_V1, checksum="f1"),
        P + "other1.md": doc("https://vendor.test/o1", "Unrelated page one with enough words here.", checksum="o1", banner=True),
        P + "other2.md": doc("https://vendor.test/o2", "Unrelated page two with enough words here.", checksum="o2", banner=True),
    }, "chore(silo): scrape")
    # 09-05: taxonomy-style commit — frontmatter rewritten, no content change
    commit(root, "2026-09-05", {
        P + "stable.md": doc("https://vendor.test/stable", BODY_V1, checksum="c1").replace("title: T", "title: T2"),
    }, "feat(taxonomy): retag")
    # 09-08: real change on one page; silo strips a banner from another (checksum moves, content does not)
    commit(root, "2026-09-08", {
        P + "changed.md": doc("https://www.vendor.test/export/", BODY_V2, checksum="a2"),
        P + "rerender.md": doc("https://vendor.test/rerender", BODY_V1, checksum="b2"),
        P + "gone.md": None,
        # first captured after the review: only the server's Last-Modified can speak for the gap
        P + "lastmod.md": doc("https://vendor.test/lastmod", BODY_V1, checksum="d1",
                              lm="Mon, 07 Sep 2026 10:00:00 GMT", fetched="2026-09-10"),
    }, "chore(silo): scrape")


MATRIX = """# Feature Matrix — Vendor / Data Transfer

## Feature metadata

- Product name: Vendor
- Analysis date: 2026-09-03

## Source index

- S1: https://vendor.test/export
- S2: http://vendor.test/rerender/#section
- S3: https://vendor.test/stable
- S4: https://vendor.test/lastmod
- S5: https://vendor.test/stamped
- S6: https://vendor.test/gone
- S7: https://forum.example.org/thread/1

| Sub-feature ID | Status |
|---|---|
| TRANSFER-export-csv | confirmed (S1) |
"""


def build_repo(root: Path) -> None:
    (root / "products/g/vendor/features/data-transfer").mkdir(parents=True)
    (root / "products/g/vendor/features/data-transfer/feature-matrix.md").write_text(MATRIX, encoding="utf-8")
    (root / "reports").mkdir()
    (root / "README.md").write_text("See https://vendor.test/stable for details.\n", encoding="utf-8")
    (root / "tools/silo-review").mkdir(parents=True)
    (root / "tools/silo-review/silo-review.toml").write_text(
        'silo_path = "../silo"\nsilo_ref = "HEAD"\nsilo_data_dir = "data"\noutput = "reports/review-queue.md"\n'
        'scan = ["*.md", "products/**/*.md", "reports/**/*.md"]\nexclude = ["reports/review-queue.md"]\n', encoding="utf-8")
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    commit(root, "2026-09-20", {}, "init") if False else None
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    env = {**os.environ, "GIT_AUTHOR_DATE": "2026-09-02T12:00:00", "GIT_COMMITTER_DATE": "2026-09-02T12:00:00"}
    subprocess.run(["git", "-C", str(root), "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "init"], check=True, env=env)


def tree_hashes(root: Path, skip: Path) -> dict[str, str]:
    out = {}
    for p in sorted(root.rglob("*")):
        if p.is_file() and ".git" not in p.parts and p.resolve() != skip.resolve():
            out[p.relative_to(root).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


# ------------------------------------------------------------------ tests


def test_normalize_url() -> None:
    n = review.normalize_url
    check("scheme/www/slash/fragment", n("http://www.Vendor.test/a/b/#x"), n("https://vendor.test/a/b"))
    check("trailing punctuation", n("https://vendor.test/a)."), "vendor.test/a)")
    check("host only", n("https://www.vendor.test/"), "vendor.test")


def test_content_lines_ignore_rendering() -> None:
    a = review.content_lines(doc("u", "Some **bold** [link text](https://x.test/a) sentence here today!", checksum="1"))
    b = review.content_lines(doc("u", "Some bold link text sentence here today", checksum="2"))
    check("markdown, links and punctuation are not content", a, b)
    check("silo header and H1 skipped", any("source" in l or "page title" in l for l in a), False)


def test_end_to_end(tmp: Path) -> None:
    silo, repo = tmp / "silo", tmp / "repo"
    build_silo(silo)
    build_repo(repo)
    cfg = review.load_config(repo / "tools/silo-review/silo-review.toml", repo)
    report = review.run(cfg, "plan")
    sha = subprocess.run(["git", "-C", str(silo), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()

    check("records silo commit", sha in report, True)
    s1 = next(l for l in report.splitlines() if "vendor.test/export" in l and "content changed" in l)
    check("S1 real change reported with source id", s1.startswith("- **S1**"), True)
    check("S1 change date", "2026-09-08" in s1, True)
    check("S1 quotes new text", "parquet export format" in s1, True)
    check("re-render (banner stripped) is not a change", "vendor.test/rerender/#section> — content changed" in report
          or re.search(r"rerender.*content changed", report) is not None, False)
    check("frontmatter-only commit is not a change", re.search(r"vendor.test/stable.*content changed", report) is not None, False)
    s4 = [l for l in report.splitlines() if "vendor.test/lastmod" in l]
    check("server Last-Modified after review, before fetch", bool(s4) and "server `Last-Modified` 2026-09-07" in s4[0], True)
    check("Last-Modified equal to fetch day is ignored", "vendor.test/stamped>" in report, False)
    check("deleted page reported as dropped", "https://vendor.test/gone" in report.split("### Dropped by the silo")[-1], True)
    health = report.split("## 2. Citation health")[1]
    check("untracked URL is not checkable, never unchanged",
          re.search(r"\| forum\.example\.org \| 0 \| 0 \| 0 \| 0 \| 0 \| 1 \|", health) is not None, True)

    # deterministic: same silo commit, same output
    check("deterministic output", review.run(cfg, "plan"), report)

    # read-only: apply writes the configured output and nothing else
    before = tree_hashes(repo, cfg["output_path"])
    silo_before = tree_hashes(silo, silo / "__none__")
    msg = review.run(cfg, "apply")
    check("apply reports what it wrote", msg.startswith("wrote reports/review-queue.md"), True)
    check("output written", cfg["output_path"].read_text(encoding="utf-8"), report)
    check("no analysis file modified", tree_hashes(repo, cfg["output_path"]), before)
    check("silo not modified", tree_hashes(silo, silo / "__none__"), silo_before)

    churn = review.run(cfg, "churn")
    check("churn: frontmatter-only week", "| 2026-W36 | 4 | 0 | 0 |" in churn, True)
    check("churn separates checksum noise from real change", "| 2026-W37 | 3 | 2 | 1 |" in churn, True)


def test_write_guard(tmp: Path) -> None:
    allowed = tmp / "reports" / "review-queue.md"
    allowed.parent.mkdir(parents=True, exist_ok=True)
    try:
        review.guarded_write(tmp / "products" / "x.md", "x", allowed)
        failures.append("guarded_write accepted a path other than the output")
    except review.ReadOnlyViolation:
        pass


def test_single_write_site() -> None:
    src = (Path(review.__file__)).read_text(encoding="utf-8")
    writes = re.findall(r"\.write_text\(|\.write_bytes\(|open\([^)]*['\"][wa]", src)
    check("the only write in review.py is inside guarded_write", len(writes), 1)
    check("no subprocess call can write to git", re.search(r"\"(commit|push|checkout|reset|add|rm)\"", src) is None, True)


def main() -> int:
    test_normalize_url()
    test_content_lines_ignore_rendering()
    test_single_write_site()
    with tempfile.TemporaryDirectory() as t:
        test_end_to_end(Path(t))
        test_write_guard(Path(t))
    for f in failures:
        print("FAIL", f)
    print(f"{'FAILED' if failures else 'OK'}: {len(failures)} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
