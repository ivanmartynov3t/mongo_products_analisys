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

[products.big]
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
        row("big", "Planned", 25),
        row("small", "Planned", 3),
        row("manual", "Live"),
        row("analysed", "Beta", folder="products/3t/analysed"),
        row("newcomer", "Alpha"),
        row("competitor", "", category="third-party"),
    ],
}


def test_check(tmp: Path) -> None:
    tpath, spath = tmp / "t.toml", tmp / "s.json"
    tpath.write_text(TOML, encoding="utf-8")
    spath.write_text(json.dumps(SNAPSHOT), encoding="utf-8")
    fired, manual = triggers.check(triggers.load_triggers(tpath), SNAPSHOT)
    got = sorted((f.slug, f.reason.split(":")[0].split(" (")[0]) for f in fired)
    check("fired triggers", got, [
        ("big", "silo holds 25 catalog entries"),
        ("newcomer", "untracked"),
        ("shipped", "status changed"),
        ("shipped", "status is Shipped"),
        ("vanished", "in coverage-triggers.toml but not in the silo snapshot"),
    ])
    check("manual triggers listed, never fired", [(m.slug, m.reason) for m in manual], [("manual", "It ships standalone")])
    code, text = triggers.run(tpath, spath)
    check("exit 1 when fired", code, 1)
    check("report names the silo commit", "aaaaaaaaaa" in text, True)
    check("deterministic", triggers.run(tpath, spath), (code, text))

    quiet = {"silo": SNAPSHOT["silo"], "products": [row("same", "PoC")]}
    spath.write_text(json.dumps(quiet), encoding="utf-8")
    tpath.write_text('[products.same]\nrecorded_status = "PoC"\n', encoding="utf-8")
    check("exit 0 when nothing fired", triggers.run(tpath, spath)[0], 0)


def test_config_errors(tmp: Path) -> None:
    for name, text in {"empty": "", "unknown key": '[products.x]\nrecorded_status = "A"\nstatus = "B"\n',
                       "no recorded_status": '[products.x]\nstatus_in = ["A"]\n'}.items():
        p = tmp / f"{name}.toml"
        p.write_text(text, encoding="utf-8")
        try:
            triggers.load_triggers(p)
            failures.append(f"{name}: accepted")
        except triggers.TriggerConfigError:
            pass


def test_real_config_is_valid() -> None:
    t = triggers.load_triggers(triggers.TRIGGERS)
    check("every coverage-scope product has a trigger entry", len(t), 12)


def test_writes_nothing() -> None:
    src = (triggers.HERE / "triggers.py").read_text(encoding="utf-8")
    check("no write calls", re.findall(r"\.(?:write_text|write_bytes)\(|open\([^)]*['\"][wa]", src), [])


def main() -> int:
    with tempfile.TemporaryDirectory() as d:
        test_check(Path(d))
        test_config_errors(Path(d))
    test_real_config_is_valid()
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
