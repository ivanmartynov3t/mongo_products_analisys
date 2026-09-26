# /// script
# requires-python = ">=3.11"
# ///
"""Offline tests for the porting validator.

    uv run tools/silo-candidates/test_validate.py

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

import candidates  # noqa: E402
import validate  # noqa: E402

failures: list[str] = []
SECRET = "hiddenrepo-x"          # a private repository name: must never reach the output


def check(name: str, actual, expected) -> None:
    if actual != expected:
        failures.append(f"{name}\n     expected: {expected!r}\n     actual:   {actual!r}")


def sh(root: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True, text=True).stdout


def commit(root: Path, msg: str = "c") -> str:
    sh(root, "add", "-A")
    sh(root, "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", "commit", "-qm", msg)
    return sh(root, "rev-parse", "HEAD").strip()


def entry(path: str, tags: dict[str, float]) -> dict:
    return {"path": path, "title": "T", "sub_feature_tags": sorted(tags), "sub_feature_probabilities": tags}


BODY = "The tool supports saved filter bars for every collection view.\n\nIt does not offer any plugin marketplace today."
CATALOG = {"by_product": {
    "prod": [entry("vendor/prod/page1.md", {"QUERY-new": 0.9}), entry("vendor/prod/page2.md", {"QUERY-new": 0.9}),
             entry(f"vendor/prod/repo_docs/{SECRET}/README.md", {"QUERY-repo": 0.9})],
    "other": [entry("vendor/other/o1.md", {"QUERY-o": 0.9}), entry("vendor/other/o2.md", {"QUERY-o": 0.9})],
}}

DICTIONARY = """# Dictionary

| Sub-feature ID | Name | Description |
|---|---|---|
| QUERY-covered | Covered | An existing capability |
| QUERY-new | Filter bar | A saved filter bar per collection view |
| QUERY-old | Old | Old thing — *Retired 2026-09-24: alias of `QUERY-new` (issue #15).* |
| QUERY-plugins | Plugins | A plugin marketplace |
"""

HEAD_ROW = "| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Sources | Notes |\n| --- | --- | --- | --- | --- | --- |\n"
LEGACY = "| QUERY-covered | Covered | Whatever legacy text | old | S3 | legacy row, never checked |\n"


def matrix(pin: str, rows: str = "") -> str:
    return f"""# Feature Matrix — Prod / Querying

## Source index

- S1: Vendor page one, https://vendor.test/one (silo: `data/vendor/prod/page1.md@{pin}`, captured 2026-09-20)
- S2: Research notes, `research/notes.md`
- S3: Vendor docs, https://vendor.test/docs

## Capability matrix (low-level)

{HEAD_ROW}{LEGACY}{rows}
## Feature-level conclusion

Nothing.
"""


def build(tmp: Path) -> tuple[Path, Path, str]:
    silo, repo = tmp / "silo", tmp / "repo"
    sh(tmp, "init", "-q", str(silo))
    files = {"data/catalog_index.json": json.dumps(CATALOG),
             "data/vendor/prod/page1.md": f"---\ntitle: One\nsource_url: https://vendor.test/one\n---\n\n{BODY}\n",
             "data/vendor/prod/page2.md": "---\ntitle: Two\nsource_url: https://vendor.test/two\n---\n\nTwo.\n",
             f"data/vendor/prod/repo_docs/{SECRET}/README.md": "---\ntitle: R\n---\n\nPrivate.\n",
             "data/vendor/other/o1.md": "---\ntitle: O\nsource_url: https://other.test/1\n---\n\nO.\n",
             "data/vendor/other/o2.md": "---\ntitle: O\nsource_url: https://other.test/2\n---\n\nO.\n"}
    for rel, text in files.items():
        (silo / rel).parent.mkdir(parents=True, exist_ok=True)
        (silo / rel).write_text(text, encoding="utf-8")
    pin = commit(silo)[:8]
    sh(tmp, "init", "-q", "-b", "main", str(repo))
    w = {"feature-dictionary.md": DICTIONARY,
         "products/g/prod/features/querying/feature-matrix.md": matrix(pin),
         "products/g/other/features/q/feature-matrix.md": "# M\n",
         "research/notes.md": 'Notes: the export wizard writes "CSV" files with a header row.\n',
         "reports/taxonomy-reconciliation.tsv": "id\tname\tin_silo\tverdict\tmaps_to\tsilo_detects_via\n"
                                                "QUERY-covered\tc\tyes\tsame definition\tQUERY-covered\tQUERY-covered\n",
         "tools/silo-candidates/triage.tsv": "\t".join(candidates.LEDGER_COLUMNS) + "\n",
         "README.md": "# Readme\n"}
    for rel, text in w.items():
        (repo / rel).parent.mkdir(parents=True, exist_ok=True)
        (repo / rel).write_text(text, encoding="utf-8")
    return silo, repo, pin


def configs(repo: Path, silo: Path) -> tuple[dict, dict]:
    vcfg = validate.load_config(validate.HERE / "validate.toml", repo)
    ccfg = candidates.load_config(candidates.HERE / "silo-candidates.toml", repo)
    ccfg["silo_path"], ccfg["silo_ref"] = silo, "HEAD"
    return vcfg, ccfg


def fresh(repo: Path) -> None:
    sh(repo, "checkout", "-q", "-f", "main")
    sh(repo, "clean", "-fdq")
    sh(repo, "checkout", "-q", "-B", "work")


def ledger_add(repo: Path, *rows: tuple[str, str, str, int]) -> None:
    p = repo / "tools/silo-candidates/triage.tsv"
    p.write_text(p.read_text() + "".join("\t".join([prod, tag, out, "2026-09-26", "abcdef1", str(web), "#1"]) + "\n"
                                         for prod, tag, out, web in rows), encoding="utf-8")


def add_rows(repo: Path, pin: str, rows: str) -> None:
    (repo / "products/g/prod/features/querying/feature-matrix.md").write_text(matrix(pin, rows), encoding="utf-8")


def regen(ccfg: dict) -> None:
    candidates.run(ccfg, "apply")


GOOD = '| QUERY-new | Filter bar | Confirmed | Vendor page: "supports saved filter bars for every collection view." | S1 | — |\n'


def hashes(root: Path) -> dict[str, str]:
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*")) if p.is_file() and ".git" not in p.parts}


def test_all(tmp: Path) -> None:
    silo, repo, pin = build(tmp)
    vcfg, ccfg = configs(repo, silo)
    regen(ccfg)
    commit(repo)

    def run(item: str = "prod") -> tuple[int, str]:
        return validate.validate(vcfg, ccfg, item, "main", silo, "HEAD")

    # clean run: a new confirmed row with a checkable quote, its ledger row, the regenerated report
    fresh(repo)
    add_rows(repo, pin, GOOD)
    ledger_add(repo, ("prod", "QUERY-new", "add-row", 2))
    regen(ccfg)
    before = hashes(repo)
    rc, out = run()
    check("clean item passes (uncommitted and untracked changes included)", (rc, out.splitlines()[-1]), (0, "ok: no findings"))
    check("deterministic", run(), (rc, out))
    check("validator writes nothing", hashes(repo), before)

    cases = {
        "invented quote": ('| QUERY-new | F | Confirmed | "supports saved filter bars in every single view" | S1 | — |\n',
                           "quote not found in the cited sources (S1)"),
        "unknown ID": ('| QUERY-nope | F | Confirmed | x | S1 | — |\n', "QUERY-nope is not in feature-dictionary.md"),
        "retired ID": ('| QUERY-old | F | Confirmed | x | S1 | — |\n', "QUERY-old is retired"),
        "no legal status": ('| QUERY-new | F | Maybe | x | S1 | — |\n', "has no legal label"),
        "unverified without note": ('| QUERY-new | F | Unverified | x | S1 | — |\n', 'needs a note "Checked <URL> on <YYYY-MM-DD>"'),
        "confirmed without dated URL source": ('| QUERY-new | F | Supported | x | S3 | — |\n', "needs a cited source with a URL and a YYYY-MM-DD date"),
        "quote with no checkable source": ('| QUERY-new | F | Confirmed | "supports saved filter bars for every collection" | S3 | — |\n',
                                           "no cited source has a silo pin or a repository file"),
        "absent without a quote": ('| QUERY-plugins | P | Not supported | none | S1 | — |\n', "needs a quoted exclusion found in a cited silo page or repository file"),
        "no sources": ('| QUERY-new | F | Confirmed | x | — | — |\n', "the Sources cell names no Source index entry"),
    }
    for name, (row, expect) in cases.items():
        fresh(repo)
        add_rows(repo, pin, row)
        rc, out = run()
        check(f"{name}: exit 1 with the finding", (rc, expect in out), (1, True))

    ok_rows = {
        "unverified with a Checked note": '| QUERY-new | F | Unverified | Checked https://vendor.test/one on 2026-09-26; no documentation of capability found. | S1 | — |\n',
        "absent with a checked exclusion": '| QUERY-plugins | P | Not supported | "It does not offer any plugin marketplace today." | S1 | — |\n',
        "quote from a repository file, nested quotes re-quoted": "| QUERY-new | F | Partial | \"the export wizard writes 'CSV' files\" | S2 | — |\n",
        "quote split at a bracketed ellipsis": '| QUERY-new | F | Confirmed | "The tool supports saved filter bars […] every collection view." | S1 | — |\n',
        "confirmed absent is one class": '| QUERY-plugins | P | Not supported (confirmed absent) | "It does not offer any plugin marketplace today." | S1 | — |\n',
        "quote split at an ellipsis; dictionary quote": '| QUERY-new | F | Confirmed | "The tool supports saved filter bars ... for every collection view"; the dictionary says "A saved filter bar per collection view" | S1 | — |\n',
    }
    for name, row in ok_rows.items():
        fresh(repo)
        add_rows(repo, pin, row)
        rc, out = run()
        check(f"{name}: no row finding", [l for l in out.splitlines() if "feature-matrix.md" in l], [])

    # an untouched legacy row with an illegal status is never judged
    fresh(repo)
    add_rows(repo, pin, GOOD)
    check("legacy row untouched: not judged", "legacy" in run()[1] or "Whatever" in run()[1], False)

    # a pin that changed at the silo ref
    fresh(repo)
    add_rows(repo, pin, GOOD)
    (silo / "data/vendor/prod/page1.md").write_text("---\ntitle: One\nsource_url: https://vendor.test/one\n---\n\nRewritten.\n")
    commit(silo)
    rc, out = run()
    check("changed pin on a touched row", "S1: silo pin is changed at the silo ref" in out, True)
    sh(silo, "reset", "-q", "--hard", "HEAD~1")

    # private names and non-public URLs: reported, never printed
    fresh(repo)
    add_rows(repo, pin, GOOD.replace("| — |\n", f"| see {SECRET} and https://github.com/acme/{SECRET}/blob/main/x.md |\n"))
    ledger_add(repo, ("prod", "QUERY-new", "add-row", 2))
    regen(ccfg)
    rc, out = run()
    check("private repository name flagged", "names a silo repository that this repository does not name yet" in out, True)
    check("non-public URL flagged", "links a non-public host (github.com)" in out, True)
    check("private name and URL never printed", (SECRET in out, "acme" in out), (False, False))

    # scope, stale generated report, open candidates, ledger rows for another product
    fresh(repo)
    (repo / "README.md").write_text("# Readme\n\nchanged\n")
    rc, out = run()
    check("README outside a product item's scope", "README.md: outside the scope of item 'prod'" in out, True)
    (repo / "scratch.txt").write_text("untracked\n")
    check("untracked files are part of the diff", "scratch.txt: outside the scope of item 'prod'" in run()[1], True)
    (repo / "scratch.txt").unlink()
    check("README in scope for the readme item", "README.md: outside" in run("readme")[1], False)
    check("open web-backed candidate without a ledger row", "1 open web-backed candidates of prod have no ledger row: QUERY-new" in out, True)

    fresh(repo)
    ledger_add(repo, ("prod", "QUERY-new", "noise", 2), ("other", "QUERY-o", "noise", 2))
    rc, out = run()
    check("stale silo-candidates.md (ledger changed, report not regenerated)", "differs from a fresh" in out, True)
    regen(ccfg)
    rc, out = run()
    check("regenerated report accepted", "differs from a fresh" in out, False)
    check("ledger row for another product", "ledger row for another product than 'prod'" in out, True)

    fresh(repo)
    (repo / "reports/review-queue.md").write_text("# hand edit\n")
    check("other tool-owned report needs a human", "tool-owned report changed" in run("cross-product")[1], True)

    # review round 1: evidence rules
    fresh(repo)
    add_rows(repo, pin, '| QUERY-plugins | P | Not supported | "A saved filter bar per collection view" | S1 | — |\n')
    check("not supported: a dictionary quote is no exclusion", "needs a quoted exclusion found" in run()[1], True)
    fresh(repo)
    (repo / "products/g/prod/evidence.md").write_text("It has no plugin marketplace at all, none.\n")
    add_rows(repo, pin, '| QUERY-plugins | P | Not supported | "It has no plugin marketplace at all" | S4 | — |\n')
    mp = repo / "products/g/prod/features/querying/feature-matrix.md"
    mp.write_text(mp.read_text().replace("- S3: Vendor docs", "- S4: Own notes, `products/g/prod/evidence.md`\n- S3: Vendor docs"))
    check("evidence added in the same change cannot verify itself", "needs a quoted exclusion found" in run()[1], True)
    fresh(repo)
    add_rows(repo, pin, '| QUERY-plugins | P | Not supported | "Private." | S4 | — |\n')
    mp.write_text(mp.read_text().replace("- S3: Vendor docs", f"- S4: Outside, `../silo/data/vendor/prod/repo_docs/{SECRET}/README.md`\n- S3: Vendor docs"))
    rc, out = run()
    check("a path outside the repository is never read", "needs a quoted exclusion found" in out, True)
    check("  ... and its private name is withheld", SECRET in out, False)

    # review round 1: private names never printed, in any column
    fresh(repo)
    add_rows(repo, pin, f'| QUERY-{SECRET} | F | {SECRET} maybe | "no such {SECRET} text anywhere here" | S1 {SECRET} | — |\n')
    rc, out = run()
    check("secret in ID, status, quote and Sources cells never printed", (rc, SECRET in out, SECRET.upper() in out), (1, False, False))
    fresh(repo)
    add_rows(repo, pin, GOOD.replace("| — |\n", f"| {SECRET}-docs, https://github.com/acme/tool and https://x.atlassian.net/wiki/y |\n"))
    rc, out = run()
    check("name followed by a hyphen is still a name", "names a silo repository" in out, True)
    check("non-public host printed as its policy entry only", ("(atlassian.net)" in out, "x.atlassian.net" in out), (True, False))
    fresh(repo)
    (repo / "products/g/prod/features/querying/feature-matrix.md").write_text(
        (repo / "products/g/prod/features/querying/feature-matrix.md").read_text() + "\nSee https://github.com/acme/tool-public.\n")
    commit(repo, "base cites a public repo")
    sh(repo, "branch", "-f", "main", "HEAD")
    fresh(repo)
    add_rows(repo, pin, GOOD.replace("| — |\n", "| https://github.com/acme/tool/blob/main/a.md |\n"))
    mp.write_text(mp.read_text() + "\nSee https://github.com/acme/tool-public.\n")
    check("a repository prefix is matched exactly, not as a substring", "links a non-public host (github.com)" in run()[1], True)
    fresh(repo)
    (repo / f"products/g/prod/{SECRET}-notes.html").write_text("<p>nothing</p>\n")
    rc, out = run()
    check("a new path naming a private repository is flagged, any suffix", ("names a silo repository" in out, SECRET in out), (True, False))

    # review round 1: scope and ledger
    fresh(repo)
    sh(repo, "mv", "products/g/other/features/q/feature-matrix.md", "products/g/prod/moved.md")
    check("a rename out of another product is out of scope", "products/g/other/features/q/feature-matrix.md: outside" in run()[1], True)
    fresh(repo)
    ledger_add(repo, ("other", "QUERY-o", "noise", 2))
    regen(ccfg)
    commit(repo, "other product decided")
    sh(repo, "branch", "-f", "main", "HEAD")
    fresh(repo)
    lp = repo / "tools/silo-candidates/triage.tsv"
    lp.write_text("\t".join(candidates.LEDGER_COLUMNS) + "\n\n")
    regen(ccfg)
    rc, out = run()
    check("removing another product's ledger row is flagged", "ledger row for another product than 'prod'" in out, True)
    check("a blank ledger line is not a row", out.count("ledger row for another product") == 1, True)

    # review round 1: dangling citation
    fresh(repo)
    mp.write_text(mp.read_text().replace("- S3: Vendor docs, https://vendor.test/docs\n", ""))
    check("a row citing a removed Source index entry is judged", "cites S3, which is no longer in the Source index" in run()[1], True)

    # errors
    fresh(repo)
    (repo / "tools/silo-candidates/triage.tsv").write_text("wrong\n")
    try:
        run()
        failures.append("malformed ledger did not raise")
    except candidates.CandidatesError:
        pass
    fresh(repo)
    for bad_item, bad_base in (("nope", "main"), ("prod", "no-such-ref")):
        try:
            validate.validate(vcfg, ccfg, bad_item, bad_base, silo, "HEAD")
            failures.append(f"item {bad_item} / base {bad_base} did not raise")
        except validate.ValidationError:
            pass


def test_status_classes() -> None:
    vocab = validate.load_config()["status"]
    check("not supported is absent only", validate.status_classes("Not supported", vocab), ["absent"])
    check("compound cell: every class", validate.status_classes("Confirmed (x); Unverified (y)", vocab), ["unverified", "confirmed"])
    check("icons", validate.status_classes("✅ / 🗺️", vocab), ["roadmap", "confirmed"])
    check("unsupported words", validate.status_classes("Corrected — x", vocab), [])
    check("partially supported is partial only", validate.status_classes("Partially supported", vocab), ["partial"])
    check("unverified, not found: unverified only", validate.status_classes("Unverified — not found", vocab), ["unverified"])


def test_quotes() -> None:
    check("fragments at ellipses; short quotes skipped",
          validate.quotes('said "one two three four ... five six seven eight" and "short one"', 4),
          ["one two three four", "five six seven eight"])
    check("normalise: links, emphasis, curly quotes, dashes, case",
          validate.normalise("**The** [tool](http://x) — “says” `this`"), "the tool - 'says' this")


def test_main_exit_codes() -> None:
    import contextlib
    import io
    orig = validate.validate
    for exc, name in ((UnicodeDecodeError("utf-8", b"x", 0, 1, "bad"), "unexpected UnicodeDecodeError"),
                      (KeyError(SECRET), "unexpected KeyError"), (validate.ValidationError("bad base"), "bad base")):
        def boom(*a, _e=exc, **k):
            raise _e
        validate.validate = boom
        try:
            with contextlib.redirect_stderr(io.StringIO()) as err:
                rc = validate.main(["--item", "x"])
            check(f"main: {name} exits 2, secret not echoed", (rc, name in err.getvalue(), SECRET in err.getvalue()), (2, True, False))
        finally:
            validate.validate = orig


def main() -> int:
    with tempfile.TemporaryDirectory() as d:
        test_all(Path(d))
    test_status_classes()
    test_quotes()
    test_main_exit_codes()
    if failures:
        print(f"FAILED ({len(failures)}):")
        for f in failures:
            print(" -", f)
        return 1
    print("ok: all validate tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
