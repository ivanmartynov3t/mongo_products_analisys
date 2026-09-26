# scope-triggers

Checks the revisit triggers of [`docs/coverage-scope.md`](../../docs/coverage-scope.md) against the silo, so the weekly taxonomy triage (#18) does not do it by hand (issue #35, Plan 08 P3).

```bash
uv run tools/silo-snapshot/snapshot.py apply      # refresh the snapshot first
uv run tools/scope-triggers/triggers.py           # report; exit 1 if any trigger fired
uv run tools/scope-triggers/test_triggers.py      # offline tests
```

## Inputs

- [`docs/coverage-triggers.toml`](../../docs/coverage-triggers.toml): one table per 3T silo product that has a coverage decision. Keys: `decision`, `recorded_status` (required), `status_in`, `min_catalog_entries`, `manual`.
- [`reports/silo-snapshot.json`](../../reports/silo-snapshot.json) from `tools/silo-snapshot`. The tool reads no silo data itself.

## What fires

| Condition | Example |
|---|---|
| The silo status differs from `recorded_status` | Studio 3T AI Chat leaves "Internal demo only" |
| The silo status is in `status_in` | Interceptor Proxy becomes "Shipped" |
| The catalog holds ≥ `min_catalog_entries` | Enterprise Data Suite reaches 20 |
| A 3T silo product has no analysis folder and no entry | a new product appears in the silo |
| An entry is missing from the snapshot | a product was removed from the silo |

`manual` triggers ("ships as a standalone product") cannot be checked by a script. They are listed under "Check by hand" and never fire. Products with an analysis folder are skipped.

## Guarantees

- **Writes nothing.** It prints a report and sets the exit code.
- **Deterministic** for the same snapshot and trigger file.
- **Not a decision.** A fired trigger asks a human to revisit the coverage decision; the tool never changes `coverage-scope.md`.
