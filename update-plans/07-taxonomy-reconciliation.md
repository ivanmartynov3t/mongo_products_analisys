# Plan 07 — Taxonomy reconciliation with prod_info_silo (issue #15)

Tracks GitHub issue [#15](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/15). The same checklist is mirrored in the issue body; keep both in sync.

## Scope

In scope: vocabulary (IDs, names, definitions, silo patterns) shared between `feature-dictionary.md` and `prod_info_silo/config/taxonomy.yaml`, the migration this causes in this repository, and the upstream change to the silo taxonomy.

Out of scope: product coverage decisions (#16), citation staleness (#14), the recurring weekly triage itself (#18 — it only consumes this plan's output). No capability status (✅/❌/❓ etc.) is changed by this plan; merged rows with conflicting evidence become ❓.

## Decision rules (fixed, so no step needs discretion)

- Strategy: **A + C** — prune and harmonise, and document the rest as Tier 2 (analysis-only).
- Per-ID verdicts: `same definition` (shared IDs), `feed-upstream`, `retire (synonym)`, `child-of`, `analysis-only`; silo-side actions: `added to silo`, `widened`, `tightened`, `boundary-bug fixed`, `no corpus evidence; pattern kept`. Shipped capabilities that the silo lists only as `PROP-*` get a real sub-feature under our ID; the silo's `PROP-*` entry stays, mirroring our Proposed Feature Registry.
- **Feed-upstream** only if: no same-meaning silo ID exists, precision ≥ 6/8 on hits the silo does not already catch, and evidence from ≥ 2 products or from a 3T product's own docs. Otherwise `analysis-only`.
- **Retire** only true synonyms (same meaning at the same granularity). Survivor = the descriptive (non-numbered) ID, unless the numbered ID is broader in scope (recorded exception: `GOV-013`). Retired IDs keep a dictionary row marked "Retired → alias of X".
- **Child-of** instead of retire when an ID is a finer-grained distinction of a silo ID with its own evidence (e.g. `SCHED-recur-daily` under `SCHED-types-time`): the matrix row stays; the silo detects the parent.
- **Historical records are not rewritten**: `research/` findings, `update-plans/` logs and changelog history keep the IDs they were written with; the dictionary alias rows keep them resolvable. Only living artifacts (`products/`, `reports/`) are migrated.
- A widened silo pattern is accepted only if sampled precision on newly tagged docs is ≥ 6/8.
- Landing: this repository and `prod_info_silo` both on `main`.
- **Dead silo patterns** (0 corpus docs, confirmed against the silo's own `catalog_index.json`) are a detection gap, not a meaning disagreement. They are handled in three buckets:
  1. Dead IDs that a verdict of this plan points at (retire survivor or promotion target): rewrite the pattern now, using the retired ID's definition probe.
  2. Word-boundary bug (`\b` next to a non-word character such as `$`, so the alternative can never match): fix mechanically with lookarounds, covered by a regression test.
  3. All other dead IDs: one looser definition probe each; rewrite only if the probe gets ≥ 5 docs and ≥ 6/8 on-topic, else record "no corpus evidence; pattern kept".
- **Over-broad live patterns**: precision-sample every silo ID with > 500 docs and every ID seen as a frequent off-topic catcher; tighten if < 6/8.
- **Acceptance of silo changes** uses the silo's own classifier output (`catalog_index.json` → `by_subfeature`), compared before and after, not an external regex walk.

## Checklist

### Phase 0 — Decisions
- [x] 0.1 Strategy A + C confirmed
- [x] 0.2 Decision rules above applied to borderline verdicts (precision ≤ 3/5, single-vendor)
- [x] 0.3 Landing target confirmed (`main` in both repositories)

### Phase 1 — Piece 1: confirm the 268 shared definitions
- [x] 1.1 Compare name/description of every shared ID (ours vs silo)
- [x] 1.2 Measure each silo pattern against its definition (catch rate of a definition probe, precision sample)
- [x] 1.3 Verdict per shared ID: same / widen / tighten / meaning differs (+ which definition wins)
- [x] 1.4 Silo `PROP-*` (14): identify the ones already shipped and give them a real sub-feature counterpart

### Phase 2 — Mapping table
- [x] 2.1 Full table: all 364 of our IDs + all 282 silo IDs, relation, verdict, survivor, action, reason, evidence
- [x] 2.2 Committed as `reports/taxonomy-reconciliation.md` (human) and `reports/taxonomy-reconciliation.tsv` (machine, for #18)
- [x] 2.3 Measurement scripts committed under `tools/taxonomy-reconcile/` with a README
- [x] 2.4 Method and limitations documented in the report

### Phase 3 — Migration in this repository
- [x] 3.1 `feature-dictionary.md`: retired IDs marked with alias; reconciliation section pointing to the per-ID table (child-of and Tier-2 IDs); internal cross-references fixed; Changelog entry
- [x] 3.2 Scripted rename of retired IDs in living matrices and reports (`products/`, `reports/`)
- [x] 3.3 Manual merge of rows where a retired ID and its survivor share a matrix (status kept or set to ❓, never upgraded)
- [x] 3.4 `tools/normalize-matrices/normalize.py` re-run; no undefined ID in any matrix; retired IDs appear in living files only where marked retired/alias
- [x] 3.5 Comparison/gap reports that count sub-features re-checked

### Phase 4 — prod_info_silo
- [x] 4.1 `config/taxonomy.yaml`: add new sub-features (incl. shipped counterparts of `PROP-*`), widen/tighten/fix patterns from Phase 1
- [x] 4.2 `tests/test_taxonomy.py`: positive and negative fixtures for every changed ID
- [x] 4.3 Test suite passes
- [x] 4.4 Catalog rebuilt with the existing pipeline; before/after doc counts per changed ID recorded; precision ≥ 6/8 on new tags
- [x] 4.5 Committed and pushed to `main`

### Phase 5 — Close the loop
- [x] 5.1 Reconciliation re-run after the silo change: `reconcile.py --check` reports 0 problems (no silo ID missing here, every dictionary ID has a decision)
- [x] 5.2 #18 links to `reports/taxonomy-reconciliation.tsv`
- [x] 5.3 Results comment posted on #15
- [x] 5.4 This repository committed and pushed to `main`; execution log below and in `00-overview-and-master-plan.md` updated
- [ ] 5.5 Issue #15 checklist fully ticked; issue closed after owner approval

## Execution log

(One line per completed phase: date — what was actually done.)

- 2026-09-24 — Phase 0: strategy A + C and landing on `main` confirmed by the owner in chat; decision rules fixed in this file before being applied (rules for child-of, historical records and the `GOV-013` survivor exception were added during execution, when real matrix rows showed that merging fine-grained rows would destroy evidence).
- 2026-09-24 — Phase 1: all 282 silo IDs share our definition (11 are shortened forms). Every silo pattern run over the 8,176-file corpus: 72 of 282 IDs had zero documents in the silo catalog; a word-boundary bug found in 22 patterns; 4 over-broad patterns found by precision sampling; 65 dead IDs re-probed with looser definition probes.
- 2026-09-24 — Phase 2: `reports/taxonomy-reconciliation.md` + `.tsv` (364 rows) generated by `tools/taxonomy-reconcile/reconcile.py` from `decisions.tsv`; probes committed as `probes.py`.
- 2026-09-24 — Phase 3: 20 synonyms marked *Retired* in the dictionary; 22 living files migrated; 3 alias rows merged by hand (no status upgraded); 0 undefined IDs in matrices before and after; `normalize.py --dry-run` reports 0 changes.
- 2026-09-24 — Phase 4: silo taxonomy changed (8 new sub-features, 26 widened, boundary fix kept for 14 + 2 feature patterns and reverted for 6 after acceptance, 4 tightened); 41 regression tests (175 passed); catalog rebuilt twice with `run_pipeline.sh --force` (second run changed only dashboards). Acceptance on the real catalog: every kept change ≥ 6/8 on newly tagged documents; zero-document silo IDs 72/282 → 53/290.
- 2026-09-24 — Phase 5: `reconcile.py --check` reports 0 problems; both repositories pushed to `main`; #15 and #18 updated. Closing #15 is left to the owner.
