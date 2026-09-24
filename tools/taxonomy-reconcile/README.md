# taxonomy-reconcile

Keeps [`feature-dictionary.md`](../../feature-dictionary.md) and the `prod_info_silo` taxonomy in step (issue #15).

## Files

| File | What it is |
|---|---|
| `reconcile.py` | Joins the dictionary, `prod_info_silo/config/taxonomy.yaml`, the silo's `data/catalog_index.json` and `decisions.tsv`; writes `reports/taxonomy-reconciliation.tsv` and the generated table in `reports/taxonomy-reconciliation.md`. |
| `decisions.tsv` | One reviewed decision per dictionary ID: `verdict` (`same definition`, `feed-upstream`, `retire (synonym)`, `child-of`, `analysis-only`), `maps_to`, the silo-side action and the evidence summary. Edit this file, never the generated table. |
| `probes.py` | The hand-written definition probes used as evidence (one regex per ID) and a corpus runner that prints docs, distinct snippets and products per probe, plus 8 random samples for precision review. |

## Usage

```bash
# weekly triage (#18): list new or unmapped IDs, write nothing; exit code 1 if any
uv run tools/taxonomy-reconcile/reconcile.py --check

# after changing decisions.tsv or the silo: regenerate the TSV and the report table
uv run tools/taxonomy-reconcile/reconcile.py

# evidence for a new decision: run probes over the silo corpus (slow, ~2 min)
uv run tools/taxonomy-reconcile/probes.py --silo ../prod_info_silo AI-local-mcp SCHED-history
```

`--silo` defaults to `../prod_info_silo` (a sibling checkout).

## Decision rules

Fixed in [`update-plans/07-taxonomy-reconciliation.md`](../../update-plans/07-taxonomy-reconciliation.md#decision-rules-fixed-so-no-step-needs-discretion). In short: feed upstream or rewrite a silo pattern only at ≥ 5 documents and ≥ 6/8 sampled on-topic; retire only true synonyms (survivor = descriptive ID unless the numbered one is broader); keep finer-grained IDs as `child-of` rather than merging matrix rows. No decision here changes a capability status.
