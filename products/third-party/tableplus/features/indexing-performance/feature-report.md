# Feature Report — TablePlus / Indexing & Performance

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Scope

- Feature name: Indexing & Performance
- Feature ID: F-IDX (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Product: TablePlus
- Product group: third-party
- Analysis date: 2026-09-04

## Behavioral walkthrough

TablePlus lets a developer view an existing collection's indexes and add a basic index directly from the UI ("Developers can... add basic indexes"). Beyond that, the source's own head-to-head comparison table is explicit that this is the extent of the capability: TablePlus's row reads "Basic index listing & creation," directly contrasted in the adjacent column against Studio 3T's "Visual Explain plans & index performance analyzer," with the strategic-impact column calling this a "Moderate" limitation ("TablePlus offers limited index optimization tools"). No Explain-plan viewer, execution-stats mode, or index-performance analyzer of any kind is named for TablePlus anywhere in the source.

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| IDX-inventory | Basic index listing exists. | Sufficient for simple index housekeeping; no confirmed detail (usage counts, size) beyond a bare list. | S1 Section 5 |
| IDX-type-single | Basic index creation is supported. | Covers the common case of adding a single-field index without leaving the app. | S1 Section 5 |
| IDX-explain-brief / IDX-explain-full | No Explain plan of any kind. | Developers cannot diagnose slow MongoDB queries from within TablePlus — a genuine, source-confirmed gap versus specialized tools. | S1 Section 5 (comparison table) |
| IDX-perf-insights | No index-performance analyzer. | No in-app guidance on missing or redundant indexes. | S1 Section 5 |

## Constraints and risks

- The comparison table's "limited index optimization tools" framing is a direct, if secondary-sourced, statement — treated as confirmed-absent for Explain plans and performance insights specifically, consistent with this plan's rule for direct absence statements.
- No confirmed depth on index types (compound, text, geospatial, TTL, wildcard, hashed) or properties (unique, sparse, partial) — these are neither confirmed present nor confirmed absent, simply not itemized.

## Interactions and dependencies

- No dependency on or cross-reference to a shell, profiler, or aggregation surface for index diagnostics — the source describes index tooling as isolated to basic listing/creation only.

## Conclusions

### Strengths

- Basic index visibility and creation exist without requiring a separate tool or raw command.

### Limitations

- No Explain plan, no execution-stats view, and no index-performance analyzer of any kind (confirmed absent) — a materially thinner index-tuning surface than Compass, Studio 3T, Navicat, or NoSQLBooster.

### Unknowns

- Exact index-type and index-property coverage available through the creation UI.
- Whether any real-time operational-performance monitoring exists for MongoDB connections.
