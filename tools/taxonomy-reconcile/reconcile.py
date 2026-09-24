#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""
Taxonomy reconciliation between feature-dictionary.md and prod_info_silo (issue #15).

Joins four inputs into one mapping table:
  1. feature-dictionary.md                      (this repository: our IDs)
  2. <silo>/config/taxonomy.yaml                (silo IDs, names, descriptions)
  3. <silo>/data/catalog_index.json             (silo classifier output: docs per ID)
  4. tools/taxonomy-reconcile/decisions.tsv     (reviewed verdict per ID)

Writes:
  reports/taxonomy-reconciliation.tsv           (machine-readable, read by the weekly triage #18)
  the generated table block in reports/taxonomy-reconciliation.md

Exit code 1 if the inputs disagree (an ID without a decision, a silo ID missing
from the dictionary, a decision for an unknown ID). That is the #18 "new signal" check.

Usage:
    uv run tools/taxonomy-reconcile/reconcile.py [--silo ../prod_info_silo] [--check]
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent.parent
DICT = REPO / "feature-dictionary.md"
DECISIONS = Path(__file__).resolve().parent / "decisions.tsv"
TSV_OUT = REPO / "reports" / "taxonomy-reconciliation.tsv"
MD_OUT = REPO / "reports" / "taxonomy-reconciliation.md"
BEGIN, END = "<!-- BEGIN GENERATED TABLE -->", "<!-- END GENERATED TABLE -->"
ROW = re.compile(r"^\|\s*`?([A-Z]+-[A-Za-z0-9-]+)`?\s*\|([^|]*)\|")


def load_dictionary() -> dict[str, str]:
    ids: dict[str, str] = {}
    for line in DICT.read_text(encoding="utf-8").splitlines():
        m = ROW.match(line)
        if m and not m.group(1).startswith("F-") and m.group(1) not in ids:
            ids[m.group(1)] = m.group(2).strip()
    return ids


def load_silo(silo: Path) -> tuple[dict[str, tuple[str, str]], dict[str, int]]:
    tax = yaml.safe_load((silo / "config" / "taxonomy.yaml").read_text(encoding="utf-8"))
    ids: dict[str, tuple[str, str]] = {}
    for fid, fd in tax["features"].items():
        for sid, sd in (fd.get("sub_features") or {}).items():
            ids[sid] = (fid, sd.get("name", ""))
    for pid, pd in (tax.get("proposed_features") or {}).items():
        ids[pid] = ("PROP", pd.get("name", ""))
    cat = json.loads((silo / "data" / "catalog_index.json").read_text(encoding="utf-8"))
    docs = {k: len(v) for k, v in cat.get("by_subfeature", {}).items()}
    docs.update({k: len(v) for k, v in cat.get("by_proposed_feature", {}).items()})
    return ids, docs


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--silo", type=Path, default=REPO.parent / "prod_info_silo")
    ap.add_argument("--check", action="store_true", help="only report problems, write nothing")
    args = ap.parse_args()

    ours = load_dictionary()
    silo, docs = load_silo(args.silo)
    decisions = {r["id"]: r for r in csv.DictReader(DECISIONS.open(encoding="utf-8"), delimiter="\t")}

    problems = []
    problems += [f"silo ID not in dictionary (new signal): {i}" for i in sorted(set(silo) - set(ours))]
    problems += [f"dictionary ID without a decision: {i}" for i in sorted(set(ours) - set(decisions))]
    problems += [f"decision for unknown ID: {i}" for i in sorted(set(decisions) - set(ours))]
    for i, d in decisions.items():
        if d["maps_to"] and d["maps_to"] not in ours:
            problems.append(f"{i} maps to unknown ID {d['maps_to']}")

    rows = []
    for i in sorted(ours):
        d = decisions.get(i, {})
        in_silo = i in silo
        target = d.get("maps_to") or ""
        detect_id, hop, seen = i, target, {i}
        while detect_id not in silo and hop and hop not in seen:  # follow survivor/parent chain
            seen.add(hop)
            detect_id, hop = hop, decisions.get(hop, {}).get("maps_to", "")
        if detect_id not in silo:
            detect_id = ""
        rows.append({
            "id": i,
            "name": ours[i],
            "in_silo": "yes" if in_silo else "no",
            "verdict": d.get("verdict", ""),
            "maps_to": target,
            "silo_detects_via": detect_id,
            "silo_docs": str(docs.get(detect_id, 0)) if detect_id else "",
            "silo_action": d.get("silo_action", ""),
            "probe_hits": d.get("probe_hits", ""),
            "precision": d.get("precision", ""),
            "reason": d.get("reason", ""),
        })

    for p in problems:
        print("PROBLEM:", p)
    if args.check:
        return 1 if problems else 0

    with TSV_OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

    head = "| ID | Verdict | Maps to | Silo detects via (docs) | Silo action | Reason |\n|---|---|---|---|---|---|"
    esc = lambda s: s.replace("|", "\\|")
    body = [
        f"| `{r['id']}` | {r['verdict']} | {('`' + r['maps_to'] + '`') if r['maps_to'] and r['maps_to'] != r['id'] else ''} | "
        f"{(r['silo_detects_via'] + ' (' + r['silo_docs'] + ')') if r['silo_detects_via'] else '—'} | {esc(r['silo_action'])} | {esc(r['reason'])} |"
        for r in rows
    ]
    md = MD_OUT.read_text(encoding="utf-8")
    a, b = md.index(BEGIN) + len(BEGIN), md.index(END)
    MD_OUT.write_text(md[:a] + "\n\n" + head + "\n" + "\n".join(body) + "\n\n" + md[b:], encoding="utf-8")
    print(f"wrote {TSV_OUT.relative_to(REPO)} ({len(rows)} rows) and table in {MD_OUT.relative_to(REPO)}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
