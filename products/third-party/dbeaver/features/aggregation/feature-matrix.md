# Feature Matrix — DBeaver / Aggregation

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: DBeaver
- Product group: third-party
- Feature ID: F-AGG (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `aggregation`
- Analysis date: 2026-09-04
- Version/release context: DBeaver 25.x–26.x line

## Source index

- S1: DBeaver Competitive Intelligence Analysis (secondary research file), `research/google_research/dbeaver-competitive-intelligence-analysis/DBeaver Competitive Intelligence Analysis.md`
- S2: Mongo limit native query · Issue #23205 - GitHub, https://github.com/dbeaver/dbeaver/issues/23205 (S1 Works Cited #11)

## Capability matrix (low-level)

This matrix is intentionally thin: the source material describes DBeaver's MongoDB aggregation surface as a single undifferentiated capability ("text-based JSON array console"), not a multi-panel stage-by-stage builder. Per [feature-dictionary.md](../../../../../feature-dictionary.md), DBeaver's F-AGG cell in the coverage matrix is marked "partial — see notes" for exactly this reason.

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AGG-editor-layout | Editor layout | Confirmed, limited | S1: "Aggregation Pipeline Engineering | Text-based JSON array console." Pipelines are authored as a single raw JSON array of stage documents, not a multi-panel UI (no separate stage list / stage editor / I/O panel regions). | No dedicated aggregation UI outside of what the generic SQL Console/JSON editor provides. | Not planned (per S1's own recommendation that Studio 3T exploit this gap) | S1 | Contrast: Studio 3T/Compass/VisuaLeaf all have a dedicated multi-panel pipeline editor (see [low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)). |
| AGG-stage-mgmt | Stage management | Not supported (confirmed absent) | S1: "DBeaver lacks a dedicated stage-by-stage visual aggregation builder. Complex $lookup, $unwind, and $facet pipelines must be written manually as JSON arrays, increasing syntax errors for developers." | — | Not planned | S1 | — |
| AGG-code-gen | Code generation | Unverified | Not discussed in S1 for MongoDB aggregation output. | — | Unverified | S1 | Omitted from broader comparison rows pending evidence. |
| AGG-create-view | Create view | Unverified | Not discussed in S1. | — | Unverified | S1 | — |

## Feature-level conclusion

### Confirmed strengths

- None specific to aggregation — the source frames this as a competitive weakness for DBeaver, not a strength, and Studio 3T's own strategic-response section (Pillar 1) explicitly targets this gap.

### Confirmed limitations

- No dedicated stage-by-stage visual aggregation pipeline builder for MongoDB; pipelines are authored as raw JSON arrays in a generic text console.
- A specific GitHub issue (#23205) documents that native MongoDB method-chain syntax (e.g., `db.getCollection("user_profile").find().limit(10)`) throws a `NullPointerException` in DBeaver's query engine because its parser expects relational SQL syntax — evidence that DBeaver's query/aggregation tooling is architecturally SQL-first, not MongoDB-native.

### Open questions / unknowns

- Whether any per-stage preview, stage enable/disable toggle, or pipeline execution options (allowDiskUse, collation) exist at all for the JSON-array aggregation console — not discussed in the source.
- Whether pipeline output can be exported in any structured format from the JSON console — not discussed.
