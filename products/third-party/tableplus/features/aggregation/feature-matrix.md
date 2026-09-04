# Feature Matrix — TablePlus / Aggregation

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: TablePlus
- Product group: third-party
- Feature ID: F-AGG (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `aggregation`
- Analysis date: 2026-09-04
- Version/release context: 2026 release line

## Source index

- S1: TablePlus Competitive Intelligence Analysis (secondary research file, no inline per-claim citation markers), `research/google_research/tableplus-competitive-intelligence-analysis/TablePlus Competitive Intelligence Analysis.md`

## Judgment call: why this area gets a (minimal) matrix rather than pure prose

Unlike DataGrip, whose source states its MongoDB access is SQL-to-JS translation with **no ability to execute a native aggregation pipeline at all**, TablePlus's source confirms developers can and do execute native MongoDB aggregation pipelines — just without any visual tooling around it: "Developers must author complex `$match`, `$group`, `$unwind`, and `$lookup` aggregations manually as JSON arrays in the query window without stage-level validation, previewing, or performance profiling." That is a real (if minimal) capability — raw pipeline authoring and execution — distinct from DataGrip's confirmed inability to run native MQL pipelines at all. This matrix is therefore built, but scored almost entirely around confirmed absences plus one thin positive capability (raw JSON pipeline execution), consistent with how the dictionary's coverage matrix already flagged TablePlus F-AGG as "partial."

## Capability matrix (low-level)

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AGG-editor-layout | Editor layout | Confirmed absent (no dedicated multi-panel pipeline editor) | S1 (Section 5): "Developers must author complex $match, $group, $unwind, and $lookup aggregations manually as JSON arrays in the query window" — pipelines are typed into the same generic query window used for any query, not a dedicated stage-list/editor/output multi-panel layout. | — | Confirmed absent | S1 | Raw JSON array authoring in the general query window is the only confirmed mechanism. |
| AGG-stage-mgmt | Stage management | Confirmed absent | S1 (Section 5, 21): "Absence of a Visual Aggregation Pipeline Editor: TablePlus lacks a stage-by-stage aggregation pipeline builder." | — | Confirmed absent | S1 | — |
| AGG-stage-preview | Stage preview | Confirmed absent | S1 (Section 5): aggregations are authored "without stage-level validation, previewing, or performance profiling." | — | Confirmed absent | S1 | Direct, explicit statement. |
| AGG-code-gen | Code generation | Confirmed absent | S1 (Section 5, comparison table): "Application Code Generation | Not Supported | ...Developers must manually translate queries into application code." (This row applies to query/aggregation code generation generally, not aggregation-specific, but is stated without carve-out.) | — | Confirmed absent | S1 | Cross-referenced: the same absence applies to F-SHELL's "Lack of... Code Generation Engine" statement. |
| AGG-clipboard | Clipboard paste | Unverified — per secondary source, no primary citation | Raw JSON pipeline arrays are typed/pasted into the query window per S1's description; standard text-editor copy/paste is presumed but not explicitly confirmed as a distinct pipeline-clipboard feature. | — | Unverified | S1 | Inferred from the general "JSON arrays in the query window" description, not a dedicated statement. |
| AGG-mapreduce-editor | MapReduce editor | Confirmed absent (no evidence) | Not discussed anywhere in S1. | — | Unverified / no evidence | S1 | Omitted from strengths/limitations — absence not stated directly, simply not mentioned. |

## Feature-level conclusion

### Confirmed strengths

- None — the one positive capability (raw JSON pipeline authoring/execution in the query window) is a baseline execution mechanism, not a differentiated strength, and even it is not traceable to a primary-source citation.

### Confirmed limitations

- No stage-by-stage visual pipeline builder, no per-stage validation or preview, and no execution/performance profiling (all confirmed absent by direct statement in S1, Sections 5, 18, and 21).
- No code generation from aggregation pipelines to application-driver languages (confirmed absent).

### Open questions / unknowns

- Whether pipeline results can be exported directly (CSV/JSON/JSONL) the way general query results can — see [F-TRANSFER](../data-transfer/feature-matrix.md); the source does not distinguish aggregation-result export from query-result export.
- Whether `allowDiskUse`, collation, or `maxTimeMS` pipeline-level options are configurable, or must be hand-written into the JSON array (not discussed in the source).
- MapReduce editor support is not discussed at all — not confirmed present or absent.
