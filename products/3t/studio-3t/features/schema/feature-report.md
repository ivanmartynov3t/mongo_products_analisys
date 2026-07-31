# Feature Report — Studio 3T / Schema Explorer

**Last reviewed:** 2026-07-31 — see [research findings](../../../../../research/studio-3t-desktop-review-2026/04-schema-findings.md)

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [High-level comparison](../../../../../reports/comparisons/high-level-product-comparison.md)

## Scope

This report covers Studio 3T's Schema Explorer (sample configuration, schema tree analysis, value visualizations, documentation export, the rename-on-discover workflow, and the View Editor) and Studio 3T's collection-validator authoring/deployment feature (validator rule editing, validation level/action configuration, and `collMod`-based deploy). It also documents the remaining confirmed-absent capabilities: the tree-based JSON Schema editor, structured BSON-type/field-constraint pickers, geo schema analysis, and the visual ERD/canvas cluster.

## Behavioral walkthrough

The Schema Explorer analyzes a collection sample and builds a field-level schema tree showing what fields exist, how frequently they appear, and what BSON types they carry. This three-layer view (field → presence probability → type probability) is particularly valuable for MongoDB's schemaless documents, where a field named `status` might be a string in 80% of documents, null in 15%, and missing entirely in 5%. Without a tool like Schema Explorer, discovering such patterns requires writing ad-hoc aggregation queries.

Sample configuration gives the user control over how the analysis is performed: the four modes (Random, First, Last, All) and a configurable sample size allow balancing analysis accuracy against execution time. The "Omit individual array elements" checkbox (on by default) prevents array-heavy collections from inflating element-level statistics and obscuring the true field structure. Adding a query filter further scopes the analysis to a specific document subset — useful for segmenting schema by tenant, region, or status code.

Visualizations add quantitative context to the schema tree. Numeric fields show value histograms for distribution analysis. String fields show top-value frequency charts, which can reveal unexpected nulls, typos, or category fragmentation. Date fields show density distributions across four time granularities — daily, weekly, monthly, and all-time — making ingestion gap detection and time-series pattern analysis straightforward.

The rename-on-discover workflow is a notable integration between schema analysis and data operations. When the schema tree reveals a field with inconsistent naming (e.g., `usr_name` vs `username`), the user can right-click, explore the affected documents, and launch a Rename Field operation against all matching documents directly from the schema analysis session. This turns a discovery step into an immediate remediation action.

The View Editor wraps MongoDB's db.createView() in a visual pipeline builder. It reuses the Aggregation Editor's stage management UI, pre-populates a $match stage, and handles the createView call. Views created here appear in the Connection Tree's Views folder and are treated as queryable objects across all Studio 3T tools (Collection Tab, Export Wizard, etc.).

### Collection validator authoring and deployment

A source-code audit (2026-07-31) found that Studio 3T Desktop has a real, mature MongoDB collection-validator authoring and deployment feature — this had previously been documented in this repo's comparisons as entirely unsupported, which was incorrect. The corrected picture:

- **Editing surface**: right-clicking a collection in the Connection Tree offers "Add Validator", which opens the Edit Validator dialog. The dialog is a JSON editor — the user pastes or writes the validator document directly. It works equally with `$jsonSchema`-style rules or plain query-operator-style rules, since the editor treats the document generically rather than parsing a specific schema syntax. A "Validator" tab in the Add Collection dialog offers the same editing surface at collection-creation time.
- **Validation Level / Action**: the dialog exposes a Validation Level dropdown (`off` / `strict` / `moderate`) and a Validation Action dropdown (`error` / `warn`), matching MongoDB's native validator semantics.
- **Syntax check**: a "Validate JSON" button parses the entered document and reports JSON-syntax errors before the user attempts to save, though this is a syntax check only — there is no semantic preview of which existing documents would pass or fail the rule.
- **Deploy path**: saving runs a `collMod` command against the live collection with the `validator`, `validationLevel`, and `validationAction` fields — a real, direct deployment path, not a local-only draft.
- **Scope limits**: validators require MongoDB 3.6 or later, and are blocked against the `admin`, `local`, and `config` databases and any `system.*` collection — these are enforced in code, not just documented as constraints.
- **Copy behavior**: since release 2022.5.0, validators are copied along with a collection or database when either is copied, so a validator survives a copy-collection operation.
- **Maturity**: changelog entries referencing this feature date back to 2020, and it has received no feature-level changes in the last 24 months — it is a stable, long-standing capability, not a recent addition.
- **Gap that remains real**: this is a JSON-text-entry workflow, not a tree-based visual schema editor. There is no distinct "Generate" step to auto-derive a validator from Schema Explorer's sampled results, and no "Preview" step separate from the syntax check — so it is narrower than a competitor's full add/edit/generate/preview/apply flow, even though the underlying add/edit/deploy capability is real.

### What remains genuinely absent

The following schema capabilities were re-confirmed as absent from Studio 3T Desktop by the same source-code audit — no code found in `schemaexplorer/` or `dataman/gui/collection/`:

- **Tree-based JSON Schema editor** (`SCHEMA-json-editor`): the validator editor is a flat JSON text box, not an expandable tree with per-node add/delete/duplicate/reorder actions.
- **Structured BSON type picker** (`SCHEMA-bson-types`) and **field-level constraint widgets** (`SCHEMA-field-constraints`): BSON types and constraints (minLength, pattern, minimum/maximum, etc.) can only be hand-typed into the validator JSON; no dedicated UI surfaces them.
- **Geo schema analysis** (`SCHEMA-geo-analysis`): no map-backed field analysis or interactive geo filter drawing exists.
- **Visual ERD / canvas cluster** (`SCHEMA-designer-canvas`, `-auto`, `-links`, `-color`, `-portability`): no canvas, diagram, or collection-relationship-graph code exists anywhere in the source tree.

## Capability findings

| Capability ID | Finding | Impact |
| --- | --- | --- |
| SCH-001 | Four sample modes with query filter support give fine-grained control over analysis scope and performance. | Prevents slow Schema Explorer runs on multi-billion-document collections. |
| SCH-003 | Per-field type probabilities expose polymorphic fields directly in the schema tree — no aggregation query required. | Speeds up schema audit and data quality investigations. |
| SCH-007 | Date distribution across hourly/daily/weekly/monthly granularities is a unique built-in visualization for time-series schema analysis. | Practical for IoT, analytics, and event log collections. |
| SCH-010 | Rename-on-discover workflow closes the loop between schema analysis and remediation in a single session. | Reduces context switching and eliminates the need to write a separate updateMany. |
| SCH-011 | View Editor reuses the Aggregation Editor UI for pipeline authoring, creating a consistent interaction model across both tools. | Reduces learning overhead for view creation. |
| SCH-012 | Collection validator authoring (add/edit) and `collMod`-based deploy is a real, long-standing (2020+) capability confirmed by source-code audit — `EditValidatorDialog`, `AddCollectionDialog`, `AppController.addValidator()`. Previously misdocumented as entirely unsupported. | Corrects a significant prior gap-analysis inaccuracy; Studio 3T is not behind on basic validator authoring/deployment. |
| SCH-013 | No tree-based JSON Schema editor, structured BSON-type picker, field-constraint widgets, geo schema analysis, or visual ERD/canvas cluster exist (re-confirmed absent by source-code audit). | These remain the genuine schema-capability gap versus competitors, not validator authoring/deployment. |

## Constraints and risks

- Schema probabilities are relative to the sample, not the full collection — small samples on large collections with sparse fields may produce misleading probabilities.
- Comments annotated in the Statistics tab are local to the Studio 3T installation and are not stored in MongoDB or shared with team members.
- The rename-on-discover write path requires collection write access and is irreversible without a backup.
- Views created via the View Editor require MongoDB ≥ 3.4 and create real database objects — accidental view creation is not undoable from within Studio 3T.
- The validator editor is free-text JSON with only a syntax check, not a semantic preview — a validator with correct JSON syntax but incorrect logic (e.g., a typo'd field name) will deploy without warning and silently fail to catch the intended bad documents.
- Validators cannot be applied against MongoDB < 3.6, or against `admin`/`local`/`config` databases or `system.*` collections — attempts outside this scope are blocked in code.
- The tree-based JSON Schema editor, structured BSON-type/constraint pickers, geo schema analysis, and the visual ERD/canvas cluster remain genuinely unimplemented — this is a real, confirmed capability gap versus competitors offering those specific UIs.

## Conclusion

Schema Explorer provides meaningful schema analysis with actionable integrations: direct explore navigation, rename-on-discover, and view creation from the same session. The combination of type-level probability analysis and date distribution visualizations covers most schema audit and data quality use cases without requiring custom aggregation pipelines. A source-code audit further confirmed that Studio 3T's collection-validator authoring and deployment feature — add/edit via a JSON editor, Validation Level/Action configuration, syntax checking, and `collMod`-based deploy — is real and has existed since at least 2020; prior documentation in this repo incorrectly described it as entirely unsupported. The genuine remaining schema gap versus competitors is narrower than previously documented: it is limited to the tree-based JSON Schema editor, structured BSON-type/constraint pickers, geo schema analysis, and the visual ERD/canvas cluster — not validator authoring/deployment itself.
