# Feature Report — DBeaver / Aggregation

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Scope

- Feature name: Aggregation (partial)
- Feature ID: F-AGG (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Product: DBeaver
- Product group: third-party
- Analysis date: 2026-09-04

## Behavioral walkthrough

DBeaver has no MongoDB-specific aggregation pipeline builder. Because MongoDB access is mediated by a relational/JDBC abstraction, complex operations like `$lookup`, `$unwind`, and `$facet` must be hand-written as a raw JSON array of stage documents inside the same generic SQL Console used for querying (see [F-SQL](../sql-tools/feature-report.md)). There is no stage list, no per-stage editor region, no per-stage input/output preview, and no code-generation path from an aggregation pipeline to a driver language — all capabilities that Compass, VisuaLeaf, and Studio 3T provide natively (per the [low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)).

A specific, primary-sourced data point reinforces this: GitHub issue #23205 documents a `NullPointerException` when a user runs a native MongoDB method-chain query (`db.getCollection(...).find().limit(10)`) in DBeaver, because the underlying query parser expects relational SQL syntax rather than MongoDB's native query language.

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| AGG-editor-layout | Single raw-JSON-array console; no multi-panel stage UI. | Materially higher authoring friction and syntax-error risk for complex pipelines versus competitors' visual builders. | Research file narrative |
| AGG-stage-mgmt | No stage-by-stage add/duplicate/move/delete UI. | Confirmed structural gap — the research file itself frames this as Studio 3T's Pillar 1 competitive opportunity. | Research file narrative |

## Constraints and risks

- This is a genuinely thin feature area for DBeaver — most AGG- sub-feature IDs (stage toggle, stage preview, pipeline options, code generation, chart builder, etc.) are not discussed at all in the source material and are therefore omitted rather than marked "not supported" with false confidence.
- Do not read the matrix's silence on unlisted sub-features as "confirmed absent" — it means "not evidenced either way" per this repository's unverified-by-default rule.

## Interactions and dependencies

- Aggregation pipelines are authored through the same console as [F-SQL](../sql-tools/feature-report.md)'s SQL Console — there is no separate aggregation-specific editor surface.

## Conclusions

### Strengths

- None evidenced.

### Limitations

- No dedicated visual aggregation pipeline builder; JSON-array-only authoring increases syntax-error risk.
- A confirmed engine-level bug (GitHub #23205) shows native MongoDB method-chain syntax is not correctly parsed, underscoring the SQL-first architecture's friction with MongoDB's native query model.

### Unknowns

- Stage preview, stage toggling, pipeline execution options, and code generation for MongoDB aggregation are not discussed in the source and remain unverified in either direction.
