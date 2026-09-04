# Feature Report — TablePlus / Aggregation

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Scope

- Feature name: Aggregation
- Feature ID: F-AGG (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Product: TablePlus
- Product group: third-party
- Analysis date: 2026-09-04

## Behavioral walkthrough

TablePlus does not offer a dedicated aggregation-pipeline workspace. A developer who needs to run a MongoDB aggregation types (or pastes) the full pipeline as a raw JSON array of stages directly into the same generic query window used for any other query — there is no stage list, no per-stage editor panel, no input/output preview between stages, and no execution-plan or performance profiling for the pipeline as a whole. The source states this plainly and repeats it across three separate sections (the MongoDB capability comparison table, the "Critical MongoDB Tooling Deficits" list, and the head-to-head competitive matrix against Studio 3T), each independently confirming the same absence rather than merely omitting the topic.

This is a materially different situation from a product like DataGrip, whose MongoDB access is SQL-to-JS translation with no ability to execute a native pipeline at all — TablePlus users genuinely can and do run `$match`/`$group`/`$unwind`/`$lookup` pipelines natively, just with none of the authoring or debugging tooling around them that a specialized MongoDB IDE provides.

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| AGG-editor-layout | No dedicated pipeline editor UI; pipelines are raw JSON in the generic query window. | Materially higher authoring friction and error risk for multi-stage pipelines compared to a visual, panel-based builder. | S1 Section 5 |
| AGG-stage-mgmt | No add/duplicate/move/delete stage tooling. | Every pipeline edit requires manually re-typing or restructuring the JSON array. | S1 Sections 5, 18, 21 |
| AGG-stage-preview | No per-stage input/output preview or validation. | Debugging a failing multi-stage pipeline requires trial-and-error full-pipeline execution rather than isolating the failing stage. | S1 Section 5 |
| AGG-code-gen | No code generation from pipelines to application languages. | Developers must hand-translate any pipeline logic into their application's driver code. | S1 Sections 5, 21 |

## Constraints and risks

- The confirmed absence of stage-level validation and preview means diagnosing a failing pipeline is a materially harder, slower workflow than in a tool with a visual debugger.
- No performance profiling for aggregation execution — users cannot identify which stage is the bottleneck without external tooling.
- All findings trace to one secondary-research file with no inline citation markers; the absences themselves are treated as confirmed per this plan's rule for direct, unambiguous "Absence of X" statements, but no positive claim in this area (e.g., that raw JSON pipelines execute correctly against sharded clusters) is independently verified.

## Interactions and dependencies

- Shares the same generic query window as [F-QUERY](../querying/feature-report.md) — there is no separate aggregation-specific surface at all.
- Aggregation output, once run, is subject to the same export capabilities described under [F-TRANSFER](../data-transfer/feature-report.md) (unconfirmed whether pipeline-specific export options exist beyond generic query-result export).

## Conclusions

### Strengths

- Native pipeline execution is genuinely supported (unlike products whose MongoDB access is SQL-translation-only) — a baseline capability, not a differentiator.

### Limitations

- No visual stage-by-stage builder, no per-stage preview/validation, no execution profiling, and no code generation — the entire visual/diagnostic tooling layer that distinguishes a MongoDB-specialist aggregation editor is confirmed absent.

### Unknowns

- Whether pipeline-level options (`allowDiskUse`, collation, `maxTimeMS`) are configurable through any UI element or must be embedded in the hand-written JSON.
- Whether `db.createView()` or saved/named pipeline libraries exist for TablePlus (not discussed in the source).
