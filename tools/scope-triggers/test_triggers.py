# /// script
# requires-python = ">=3.11"
# ///
"""Offline tests for scope-triggers.

    uv run tools/scope-triggers/test_triggers.py
"""

from __future__ import annotations

import json
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import triggers  # noqa: E402

failures: list[str] = []


def check(name: str, actual, expected) -> None:
    if actual != expected:
        failures.append(f"{name}\n     expected: {expected!r}\n     actual:   {actual!r}")


TOML = """
[products.same]
recorded_status = "PoC"

[products.shipped]
recorded_status = "PoC"
status_in = ["Shipped"]

[products.drifted]
recorded_status = "PoC"
status_in = ["Shipped"]

[products.out]
decision = "Out of scope"
recorded_status = "Live"

[products.big]
recorded_status = "Planned"
min_catalog_entries = 20

[products.edge]
recorded_status = "Planned"
min_catalog_entries = 20

[products.small]
recorded_status = "Planned"
min_catalog_entries = 20

[products.manual]
recorded_status = "Live"
manual = "It ships standalone"

[products.vanished]
recorded_status = "Live"

[products.moved]
recorded_status = "Live"

[products.analysed]
recorded_status = "Live"
"""


def row(slug: str, status: str, entries: int = 0, folder: str = "", category: str = "3t") -> dict:
    return {"slug": slug, "category": category, "status": status, "catalog_entries": entries, "analysis_folder": folder}


SNAPSHOT = {
    "silo": {"commit": "a" * 40, "commit_date": "2026-09-26"},
    "products": [
        row("same", "PoC"),
        row("shipped", "Shipped"),
        row("drifted", "Beta"),
        row("out", "Deprecated"),
        row("big", "Planned", 25),
        row("edge", "Planned", 20),
        row("small", "Planned", 19),
        row("manual", "Live"),
        row("moved", "Live", category="third-party"),
        row("analysed", "Beta", folder="products/3t/analysed"),
        row("newcomer", "Alpha"),
        row("competitor", "", category="third-party"),
        row("same", "", category="third-party"),  # same slug in another category: must not hide the 3T row
        row("newcomer", "", category="third-party"),
    ],
}


def test_check(tmp: Path) -> None:
    tpath, spath = tmp / "t.toml", tmp / "s.json"
    tpath.write_text(TOML, encoding="utf-8")
    spath.write_text(json.dumps(SNAPSHOT), encoding="utf-8")
    code, text = triggers.run(tpath, spath)
    check("report (sorted by slug; noted changes never fire)", text, "\n".join([
        "Coverage triggers at silo aaaaaaaaaa (2026-09-26): 7 fired",
        "",
        "FIRED   analysed: entry obsolete: now analysed in products/3t/analysed; "
        "remove it from coverage-triggers.toml and coverage-scope.md",
        "FIRED   big: silo holds 25 catalog entries (trigger: ≥ 20)",
        "FIRED   edge: silo holds 20 catalog entries (trigger: ≥ 20)",
        "FIRED   moved: no longer a 3T product in the silo snapshot (category third-party)",
        "FIRED   newcomer: untracked: silo product (status Alpha) with no analysis folder and no coverage decision",
        "FIRED   shipped: status is Shipped (was PoC)",
        "FIRED   vanished: in coverage-triggers.toml but not in the silo snapshot",
        "",
        "Check by hand (not machine-checkable):",
        "        manual: It ships standalone",
        "",
        "Noted, no action (status changes that are not revisit triggers):",
        "        drifted: status changed: PoC → Beta (not a revisit trigger)",
        "        out: status changed: Live → Deprecated (not a revisit trigger)",
    ]))
    check("exit 1 when fired", code, 1)
    check("deterministic", triggers.run(tpath, spath), (code, text))

    quiet = {"silo": SNAPSHOT["silo"], "products": [row("same", "PoC"), row("out", "Deprecated")]}
    spath.write_text(json.dumps(quiet), encoding="utf-8")
    tpath.write_text('[products.same]\nrecorded_status = "PoC"\n[products.out]\nrecorded_status = "Live"\n', encoding="utf-8")
    check("exit 0 when only noted changes", triggers.run(tpath, spath)[0], 0)


def test_config_errors(tmp: Path) -> None:
    cases = {
        "empty": "",
        "empty products": "[products]\n",
        "unknown key": '[products.x]\nrecorded_status = "A"\nstatus = "B"\n',
        "no recorded_status": '[products.x]\nstatus_in = ["A"]\n',
        "recorded_status not a string": "[products.x]\nrecorded_status = 5\n",
        "status_in a string": '[products.x]\nrecorded_status = "A"\nstatus_in = "Shipped"\n',
        "min_catalog_entries a string": '[products.x]\nrecorded_status = "A"\nmin_catalog_entries = "20"\n',
        "min_catalog_entries negative": '[products.x]\nrecorded_status = "A"\nmin_catalog_entries = -1\n',
        "entry not a table": "[products]\nx = 1\n",
        "empty decision": '[products.x]\nrecorded_status = "A"\ndecision = ""\n',
        "empty manual": '[products.x]\nrecorded_status = "A"\nmanual = ""\n',
    }
    for name, text in cases.items():
        p = tmp / f"{name}.toml"
        p.write_text(text, encoding="utf-8")
        try:
            triggers.load_triggers(p)
            failures.append(f"{name}: accepted")
        except triggers.TriggerConfigError:
            pass
    ok = tmp / "ok.toml"
    ok.write_text('[products.x]\nrecorded_status = "A"\n', encoding="utf-8")
    snaps = {"no products": '{"silo": {"commit": "a"}}', "not json": "{", "no commit": '{"products": []}',
             "a list": "[1]", "silo a string": '{"silo": "x", "products": []}',
             "row without slug": '{"silo": {"commit": "a"}, "products": [{"category": "3t"}]}'}
    bad_row = '{"silo": {"commit": "a"}, "products": [{"slug": "s", "category": "3t", %s}]}'
    snaps |= {"catalog_entries a string": bad_row % '"catalog_entries": "9"',
              "catalog_entries null": bad_row % '"catalog_entries": null',
              "catalog_entries a bool": bad_row % '"catalog_entries": true',
              "analysis_folder a list": bad_row % '"analysis_folder": ["x"]',
              "status a list": bad_row % '"status": ["Live"]',
              "category missing": '{"silo": {"commit": "a"}, "products": [{"slug": "s"}]}'}
    for name, text in snaps.items():
        sp = tmp / f"{name}.json"
        sp.write_text(text, encoding="utf-8")
        check(f"exit 2 on a bad snapshot: {name}", triggers.main(["--triggers", str(ok), "--snapshot", str(sp)]), 2)
    bad = tmp / "bad.toml"
    bad.write_text("[products\n", encoding="utf-8")
    good = tmp / "good.json"
    good.write_text('{"silo": {"commit": "a"}, "products": []}', encoding="utf-8")
    latin = tmp / "latin.json"
    latin.write_bytes(b'{"silo": {"commit": "\xe9"}, "products": []}')
    check("exit 2 on a non-UTF-8 snapshot", triggers.main(["--triggers", str(ok), "--snapshot", str(latin)]), 2)
    latin_toml = tmp / "latin.toml"
    latin_toml.write_bytes(b'[products.x]\nrecorded_status = "\xe9"\n')
    check("exit 2 on a non-UTF-8 TOML", triggers.main(["--triggers", str(latin_toml), "--snapshot", str(good)]), 2)
    check("exit 2 on a TOML syntax error", triggers.main(["--triggers", str(bad), "--snapshot", str(good)]), 2)
    check("exit 2 on a missing snapshot", triggers.main(["--triggers", str(ok), "--snapshot", str(tmp / "none.json")]), 2)


def test_real_config_matches_coverage_scope() -> None:
    t = triggers.load_triggers(triggers.TRIGGERS)
    table = {}
    for line in (triggers.REPO / "docs" / "coverage-scope.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\| `([a-z0-9-]+)` \| ([^|]+?) \|", line)
        if m:
            table[m.group(1)] = m.group(2)
    check("coverage-scope.md table and TOML list the same products", sorted(t), sorted(table))
    check("recorded_status equals the table's Silo status",
          {s: v["recorded_status"] for s, v in t.items()}, table)


def test_writes_nothing() -> None:
    src = (triggers.HERE / "triggers.py").read_text(encoding="utf-8")
    check("no write calls", re.findall(r"\.(?:write_text|write_bytes)\(|open\([^)]*['\"][wa]", src), [])


def main() -> int:
    with tempfile.TemporaryDirectory() as d:
        test_check(Path(d))
        test_config_errors(Path(d))
    test_real_config_matches_coverage_scope()
    test_writes_nothing()
    if failures:
        print(f"FAILED ({len(failures)}):")
        for f in failures:
            print(" -", f)
        return 1
    print("ok: all scope-triggers tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
