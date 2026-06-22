# Create detailed feature matrix (low-level)

You are analyzing a single feature of a MongoDB-related product.

## Task

Create or update:

`products/<group>/<product-name>/features/<feature-folder>/feature-matrix.md`

Use `templates/feature-matrix-template.md`.

## Requirements

1. **Always read `feature-dictionary.md` first** — it defines the canonical feature ID (`F-*`), the exact folder name, and all valid sub-feature IDs (`FEAT-suffix`).
2. Work at low implementation level, not category-only level.
3. Sub-feature IDs in the matrix **must come from `feature-dictionary.md`**. Do not invent new IDs without first adding them to the dictionary.
4. Add one row per sub-feature with explicit behavior and constraints.
5. Distinguish:
   - confirmed behavior
   - roadmap/planned behavior
   - unknown/unverified behavior
6. Include source references for every major capability.
7. Column header should be `Sub-feature ID` (not `Capability ID`).
8. Add a `Navigation` section linking product report, feature report, feature dictionary, and low-level comparison.

## Output constraints

- Avoid generic statements.
- Keep matrix rows comparable across products using the same sub-feature IDs.
- Sub-feature IDs must match the dictionary exactly (case-sensitive).
