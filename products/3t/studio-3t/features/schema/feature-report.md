# Feature Report — Studio 3T / Schema Explorer

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [High-level comparison](../../../../../reports/comparisons/high-level-product-comparison.md)

## Scope

This report covers Studio 3T's Schema Explorer: sample configuration, schema tree analysis (field probability and type distribution), value visualizations, documentation export, the rename-on-discover workflow, and the View Editor.

## Behavioral walkthrough

The Schema Explorer analyzes a collection sample and builds a field-level schema tree showing what fields exist, how frequently they appear, and what BSON types they carry. This three-layer view (field → presence probability → type probability) is particularly valuable for MongoDB's schemaless documents, where a field named `status` might be a string in 80% of documents, null in 15%, and missing entirely in 5%. Without a tool like Schema Explorer, discovering such patterns requires writing ad-hoc aggregation queries.

Sample configuration gives the user control over how the analysis is performed: the four modes (Random, First, Last, All) and a configurable sample size allow balancing analysis accuracy against execution time. The "Omit individual array elements" checkbox (on by default) prevents array-heavy collections from inflating element-level statistics and obscuring the true field structure. Adding a query filter further scopes the analysis to a specific document subset — useful for segmenting schema by tenant, region, or status code.

Visualizations add quantitative context to the schema tree. Numeric fields show value histograms for distribution analysis. String fields show top-value frequency charts, which can reveal unexpected nulls, typos, or category fragmentation. Date fields show density distributions across four time granularities — daily, weekly, monthly, and all-time — making ingestion gap detection and time-series pattern analysis straightforward.

The rename-on-discover workflow is a notable integration between schema analysis and data operations. When the schema tree reveals a field with inconsistent naming (e.g., `usr_name` vs `username`), the user can right-click, explore the affected documents, and launch a Rename Field operation against all matching documents directly from the schema analysis session. This turns a discovery step into an immediate remediation action.

The View Editor wraps MongoDB's db.createView() in a visual pipeline builder. It reuses the Aggregation Editor's stage management UI, pre-populates a $match stage, and handles the createView call. Views created here appear in the Connection Tree's Views folder and are treated as queryable objects across all Studio 3T tools (Collection Tab, Export Wizard, etc.).

## Capability findings

| Capability ID | Finding | Impact |
| --- | --- | --- |
| SCH-001 | Four sample modes with query filter support give fine-grained control over analysis scope and performance. | Prevents slow Schema Explorer runs on multi-billion-document collections. |
| SCH-003 | Per-field type probabilities expose polymorphic fields directly in the schema tree — no aggregation query required. | Speeds up schema audit and data quality investigations. |
| SCH-007 | Date distribution across hourly/daily/weekly/monthly granularities is a unique built-in visualization for time-series schema analysis. | Practical for IoT, analytics, and event log collections. |
| SCH-010 | Rename-on-discover workflow closes the loop between schema analysis and remediation in a single session. | Reduces context switching and eliminates the need to write a separate updateMany. |
| SCH-011 | View Editor reuses the Aggregation Editor UI for pipeline authoring, creating a consistent interaction model across both tools. | Reduces learning overhead for view creation. |

## Constraints and risks

- Schema probabilities are relative to the sample, not the full collection — small samples on large collections with sparse fields may produce misleading probabilities.
- Comments annotated in the Statistics tab are local to the Studio 3T installation and are not stored in MongoDB or shared with team members.
- The rename-on-discover write path requires collection write access and is irreversible without a backup.
- Views created via the View Editor require MongoDB ≥ 3.4 and create real database objects — accidental view creation is not undoable from within Studio 3T.

## Conclusion

Schema Explorer provides meaningful schema analysis with actionable integrations: direct explore navigation, rename-on-discover, and view creation from the same session. The combination of type-level probability analysis and date distribution visualizations covers most schema audit and data quality use cases without requiring custom aggregation pipelines.
