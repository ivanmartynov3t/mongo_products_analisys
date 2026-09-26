#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""Check the coverage-scope revisit triggers against the silo snapshot (issue #35).

    uv run tools/scope-triggers/triggers.py            # report; exit 1 if any trigger fired, 2 on error
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


def _is_str_list(v) -> bool:
    return isinstance(v, list) and bool(v) and all(isinstance(x, str) and x for x in v)


def load_triggers(path: Path) -> dict[str, dict]:
    products = tomllib.loads(path.read_text(encoding="utf-8")).get("products")
    if not isinstance(products, dict) or not products:
        raise TriggerConfigError(f"{path}: no [products.<slug>] tables")
    for slug, t in products.items():
        if not isinstance(t, dict):
            raise TriggerConfigError(f"{path}: {slug}: must be a [products.{slug}] table")
        unknown = set(t) - KNOWN_KEYS
        if unknown:
            raise TriggerConfigError(f"{path}: {slug}: unknown keys {sorted(unknown)}")
        if not isinstance(t.get("recorded_status"), str):
            raise TriggerConfigError(f"{path}: {slug}: recorded_status is required and must be a string")
        for key in ("decision", "manual"):
            if key in t and not (isinstance(t[key], str) and t[key]):
                raise TriggerConfigError(f"{path}: {slug}: {key} must be a non-empty string")
        if "status_in" in t and not _is_str_list(t["status_in"]):
            raise TriggerConfigError(f"{path}: {slug}: status_in must be a non-empty list of strings")
        n = t.get("min_catalog_entries", 0)
        if isinstance(n, bool) or not isinstance(n, int) or n < 0:
            raise TriggerConfigError(f"{path}: {slug}: min_catalog_entries must be an integer ≥ 0")
    return products


def _valid_row(r) -> bool:
    """Every field check() reads has the type silo-snapshot writes."""
    if not (isinstance(r, dict) and isinstance(r.get("slug"), str) and isinstance(r.get("category"), str)):
        return False
    n = r.get("catalog_entries", 0)
    return (isinstance(r.get("status", ""), str) and isinstance(r.get("analysis_folder", ""), str)
            and isinstance(n, int) and not isinstance(n, bool))


def validate_snapshot(snapshot, path: Path) -> None:
    ok = (isinstance(snapshot, dict) and isinstance(snapshot.get("silo"), dict)
          and isinstance(snapshot["silo"].get("commit"), str) and isinstance(snapshot.get("products"), list)
          and all(_valid_row(r) for r in snapshot["products"]))
    if not ok:
        raise TriggerConfigError(f"{path}: not a silo snapshot (needs `silo.commit` and `products` rows with a `slug`); "
                                 "regenerate it with tools/silo-snapshot")


def check(triggers: dict[str, dict], snapshot: dict) -> tuple[list[Finding], list[Finding], list[Finding]]:
    """Returns (fired, manual, noted).

    fired:  a documented revisit trigger, a new untracked 3T product, or an entry that no longer
            matches the snapshot. Only these set exit 1.
    manual: triggers no script can check, listed for the human.
    noted:  a status change that is not a documented trigger (e.g. an out-of-scope product
            changing status). coverage-scope.md says to skip these, so they never fire.
    """
    # The snapshot keys products by (category, slug): filter to 3T first, so a third-party row
    # with the same slug never hides the 3T one.
    rows = {r["slug"]: r for r in snapshot["products"] if r.get("category") == "3t"}
    other_category = {r["slug"]: r.get("category") for r in snapshot["products"] if r.get("category") != "3t"}
    fired, manual, noted = [], [], []
    for slug in sorted(set(rows) | set(triggers)):
        row, t = rows.get(slug), triggers.get(slug)
        if row and row.get("analysis_folder"):
            if t is not None:
                fired.append(Finding(slug, f"entry obsolete: now analysed in {row['analysis_folder']}; "
                                           "remove it from coverage-triggers.toml and coverage-scope.md"))
            continue
        if row is None:
            fired.append(Finding(slug, f"no longer a 3T product in the silo snapshot (category {other_category[slug]})"
                                 if slug in other_category else "in coverage-triggers.toml but not in the silo snapshot"))
            continue
        if t is None:
            fired.append(Finding(slug, f"untracked: silo product (status {row.get('status') or '—'}) "
                                       "with no analysis folder and no coverage decision"))
            continue
        status = row.get("status", "")
        if status in t.get("status_in", []):
            fired.append(Finding(slug, f"status is {status} (was {t['recorded_status']})"))
        elif status != t["recorded_status"]:
            noted.append(Finding(slug, f"status changed: {t['recorded_status']} → {status or '—'} (not a revisit trigger)"))
        if "min_catalog_entries" in t and row.get("catalog_entries", 0) >= t["min_catalog_entries"]:
            fired.append(Finding(slug, f"silo holds {row['catalog_entries']} catalog entries "
                                       f"(trigger: ≥ {t['min_catalog_entries']})"))
        if t.get("manual"):
            manual.append(Finding(slug, t["manual"]))
    return fired, manual, noted


def render(fired: list[Finding], manual: list[Finding], noted: list[Finding], snapshot: dict) -> str:
    silo = snapshot["silo"]
    out = [f"Coverage triggers at silo {silo['commit'][:10]} ({silo.get('commit_date', '')}): "
           f"{len(fired)} fired", ""]
    out += [f"FIRED   {f.slug}: {f.reason}" for f in fired] or ["No trigger fired."]
    if manual:
        out += ["", "Check by hand (not machine-checkable):"]
        out += [f"        {f.slug}: {f.reason}" for f in manual]
    if noted:
        out += ["", "Noted, no action (status changes that are not revisit triggers):"]
        out += [f"        {f.slug}: {f.reason}" for f in noted]
    return "\n".join(out)


def run(triggers_path: Path = TRIGGERS, snapshot_path: Path = SNAPSHOT) -> tuple[int, str]:
    triggers = load_triggers(triggers_path)
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    validate_snapshot(snapshot, snapshot_path)
    fired, manual, noted = check(triggers, snapshot)
    return (1 if fired else 0), render(fired, manual, noted, snapshot)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--triggers", type=Path, default=TRIGGERS)
    ap.add_argument("--snapshot", type=Path, default=SNAPSHOT)
    a = ap.parse_args(argv)
    try:
        code, text = run(a.triggers, a.snapshot)
    except (OSError, ValueError) as e:  # ValueError covers JSON, TOML, UTF-8 and TriggerConfigError
        print(f"error: {e}", file=sys.stderr)
        return 2  # distinct from 1 (a trigger fired), so an automated run can tell them apart
    print(text)
    return code


if __name__ == "__main__":
    sys.exit(main())
