# Low-Level Feature Comparison Template

## Navigation

- [Cumulative report index](../reports/cumulative-report.md)
- [High-level comparison](../reports/comparisons/high-level-product-comparison.md)
- [Feature dictionary](../feature-dictionary.md)

## How to use this template

Sub-feature IDs in the `Sub-feature ID` column must come from the [unified feature dictionary](../feature-dictionary.md).
One row per sub-feature per feature group. Products not supporting a sub-feature get `Not supported` or `Not assessed`.

## Normalized sub-feature comparison

| Feature ID | Sub-feature ID | Sub-feature name | MongoDB Compass | VisuaLeaf | Studio 3T | Gap type | Sources |
| --- | --- | --- | --- | --- | --- | --- | --- |
| F-CONN | CONN-topology |  |  |  |  |  |  |
| F-CONN | CONN-auth-std |  |  |  |  |  |  |
| F-QUERY | QUERY-filter-bar |  |  |  |  |  |  |
| F-AGG | AGG-editor-layout |  |  |  |  |  |  |

## Gap taxonomy

- `Missing` — capability absent from that product
- `Partial` — capability exists but with significant constraints
- `Mismatch` — behavioral difference between products
- `Constraint` — present but requires specific edition, version, or deployment
- `Roadmap` — planned but not yet available

## Notes

- Keep rows explicit and source-backed.
- Use sub-feature IDs exactly as defined in the feature dictionary.
- Add new sub-feature IDs to the dictionary before using them here.
