# scope-triggers

Checks the revisit triggers of [`docs/coverage-scope.md`](../../docs/coverage-scope.md) against the silo, so the weekly taxonomy triage (#18) does not do it by hand (issue #35, Plan 08 P3).

```bash
uv run tools/silo-snapshot/snapshot.py apply      # refresh the snapshot first
uv run tools/scope-triggers/triggers.py           # report; exit 1 if any trigger fired, 2 on error
uv run tools/scope-triggers/test_triggers.py      # offline tests
```

## Inputs

- [`docs/coverage-triggers.toml`](../../docs/coverage-triggers.toml): one table per 3T silo product that has a coverage decision. Keys: `decision`, `recorded_status` (required), `status_in`, `min_catalog_entries`, `manual`.
- [`reports/silo-snapshot.json`](../../reports/silo-snapshot.json) from `tools/silo-snapshot`. The tool reads no silo data itself.

## What fires

Only documented revisit triggers, and entries that no longer match the silo:

| Condition | Example |
|---|---|
| The silo status is in `status_in` | Interceptor Proxy becomes "Shipped" |
| The catalog holds ≥ `min_catalog_entries` | Enterprise Data Suite reaches 20 |
| A 3T silo product has no analysis folder and no entry | a new product appears in the silo |
| An entry is missing from the snapshot, or is no longer a 3T product | a product was removed from the silo |
| An entry's product now has an analysis folder | the entry is obsolete; remove it |

`manual` triggers ("ships as a standalone product") cannot be checked by a script. They are listed under "Check by hand" and never fire.

A status change that is not a trigger (for example an out-of-scope product going from Live to Deprecated, or Studio 3T EE going from Alpha to Beta) is listed under "Noted, no action" and does not fire. [`coverage-scope.md`](../../docs/coverage-scope.md) says to skip out-of-scope products and act only on the trigger column.

Exit codes: 0 nothing fired, 1 a trigger fired, 2 bad or missing input (TOML, snapshot).

## Guarantees

- **Writes nothing.** It prints a report and sets the exit code.
- **Deterministic** for the same snapshot and trigger file; findings are sorted by slug.
- **Kept in step with the doc.** A test checks that `coverage-triggers.toml` and the `coverage-scope.md` table list the same products with the same *Silo status*.
- **Not a decision.** A fired trigger asks a human to revisit the coverage decision; the tool never changes `coverage-scope.md`.
