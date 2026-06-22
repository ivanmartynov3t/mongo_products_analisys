# Create feature-level report

You are analyzing a single product feature in depth.

## Task

Create or update:

`products/<group>/<product-name>/features/<feature-folder>/feature-report.md`

Use `templates/feature-report-template.md`.

## Requirements

1. **Always read `feature-dictionary.md` first** — it defines the canonical Feature ID (`F-*`) and all valid sub-feature IDs (`FEAT-suffix`).
2. Explain how the feature behaves end-to-end.
3. Document edge cases, constraints, and operational risks.
4. Reference **sub-feature IDs** from `feature-matrix.md` (all must be from the unified feature dictionary).
5. Include clear conclusions: strengths, limitations, unknowns.
6. Keep findings source-backed.
7. Add a `Navigation` section linking product report, feature matrix, feature dictionary, and comparison reports.

## Output constraints

- Use `Sub-feature ID` in tables (not `Capability ID`).
- Sub-feature IDs must exactly match the dictionary.
