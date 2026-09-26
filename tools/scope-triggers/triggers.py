#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""Check the coverage-scope revisit triggers against the silo snapshot (issue #35).

    uv run tools/scope-triggers/triggers.py            # report; exit 1 if any trigger fired
    uv run tools/scope-triggers/test_triggers.py       # offline tests

Reads docs/coverage-triggers.toml and reports/silo-snapshot.json (regenerate it first with
tools/silo-snapshot). Writes nothing. A fired trigger is a prompt for the weekly taxonomy
triage (#18) to revisit a coverage decision, never a decision itself.
"""

from __future__ import annotations

import argparse
import json
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
TRIGGERS = REPO / "docs" / "coverage-triggers.toml"
SNAPSHOT = REPO / "reports" / "silo-snapshot.json"

KNOWN_KEYS = {"decision", "recorded_status", "status_in", "min_catalog_entries", "manual"}


@dataclass
class Finding:
    slug: str
    reason: str


class TriggerConfigError(ValueError):
    pass


def load_triggers(path: Path) -> dict[str, dict]:
    products = tomllib.loads(path.read_text(encoding="utf-8")).get("products")
    if not isinstance(products, dict) or not products:
        raise TriggerConfigError(f"{path}: no [products.<slug>] tables")
    for slug, t in products.items():
        unknown = set(t) - KNOWN_KEYS
        if unknown:
            raise TriggerConfigError(f"{path}: {slug}: unknown keys {sorted(unknown)}")
        if "recorded_status" not in t:
            raise TriggerConfigError(f"{path}: {slug}: recorded_status is required")
    return products


def check(triggers: dict[str, dict], snapshot: dict) -> tuple[list[Finding], list[Finding]]:
    """Returns (fired, manual): triggers that fired, and manual triggers to look at by hand."""
    rows = {r["slug"]: r for r in snapshot.get("products", []) if r.get("category") == "3t"}
    fired, manual = [], []
    for slug in sorted(set(rows) | set(triggers)):
        row, t = rows.get(slug), triggers.get(slug)
        if row and row.get("analysis_folder"):
            continue  # analysed here; nothing to revisit
        if row is None:
            fired.append(Finding(slug, "in coverage-triggers.toml but not in the silo snapshot"))
            continue
        if t is None:
            fired.append(Finding(slug, f"untracked: silo product (status {row.get('status') or '—'}) "
                                       "with no analysis folder and no coverage decision"))
            continue
        status = row.get("status", "")
        if status != t["recorded_status"]:
            fired.append(Finding(slug, f"status changed: {t['recorded_status']} → {status or '—'}"))
        if status in t.get("status_in", []):
            fired.append(Finding(slug, f"status is {status}"))
        if "min_catalog_entries" in t and row.get("catalog_entries", 0) >= t["min_catalog_entries"]:
            fired.append(Finding(slug, f"silo holds {row['catalog_entries']} catalog entries "
                                       f"(trigger: ≥ {t['min_catalog_entries']})"))
        if t.get("manual"):
            manual.append(Finding(slug, t["manual"]))
    return fired, manual


def render(fired: list[Finding], manual: list[Finding], snapshot: dict) -> str:
    silo = snapshot.get("silo", {})
    out = [f"Coverage triggers at silo {str(silo.get('commit', ''))[:10]} ({silo.get('commit_date', '')}): "
           f"{len(fired)} fired", ""]
    out += [f"FIRED   {f.slug}: {f.reason}" for f in fired] or ["No trigger fired."]
    if manual:
        out += ["", "Check by hand (not machine-checkable):"]
        out += [f"        {f.slug}: {f.reason}" for f in manual]
    return "\n".join(out)


def run(triggers_path: Path = TRIGGERS, snapshot_path: Path = SNAPSHOT) -> tuple[int, str]:
    triggers = load_triggers(triggers_path)
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    fired, manual = check(triggers, snapshot)
    return (1 if fired else 0), render(fired, manual, snapshot)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--triggers", type=Path, default=TRIGGERS)
    ap.add_argument("--snapshot", type=Path, default=SNAPSHOT)
    a = ap.parse_args(argv)
    code, text = run(a.triggers, a.snapshot)
    print(text)
    return code


if __name__ == "__main__":
    sys.exit(main())
