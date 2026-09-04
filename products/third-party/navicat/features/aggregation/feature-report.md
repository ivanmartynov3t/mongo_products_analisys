# Feature Report — Navicat / Aggregation

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Scope

- Feature name: Aggregation
- Feature ID: F-AGG (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Product: Navicat
- Product group: third-party
- Analysis date: 2026-09-04

## Behavioral walkthrough

Navicat's aggregation pipeline builder is a genuine visual, drag-and-drop, stage-by-stage editor: developers drag named operators ($match, $group, $project, $lookup, $unwind, etc.) into a sequential pipeline, and the editor renders a preview of the *output* documents at each stage as transformation rules are applied. This was introduced during the Navicat 12–15 release cycle, per the source's release-history narrative, making it one of the longer-standing capabilities in the current feature set (as opposed to the AI features and BI workspace, which are Navicat 17-era additions).

The source's own head-to-head comparison table against Studio 3T draws an explicit, direct line at what Navicat's builder does *not* do: it lacks "deep stage-by-stage input/output document inspection" (Navicat shows output preview only, not a combined input+output debugging view) and it lacks "instant driver code generation across multiple programming languages (e.g., C#, Java, Python, JavaScript, PHP, Ruby)" that Studio 3T's Aggregation Editor provides. Both of these are confirmed-absent by direct, repeated statement in the source rather than silent gaps.

Separately from the aggregation pipeline, Navicat provides a dedicated MapReduce editor: a form-based workflow to author, test, and debug map/reduce functions against sampled document sets before committing to a full-cluster job run. This is architecturally distinct from the aggregation pipeline builder (different execution model — MapReduce vs. the aggregation framework) and different UI (forms for authoring/testing vs. drag-and-drop stage operators), which is why it maps to its own dictionary ID (`AGG-mapreduce-editor`, newly added in this same effort) rather than being folded into the pipeline builder's sub-features.

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| AGG-editor-layout / AGG-stage-modes | Visual, drag-and-drop stage builder confirmed, introduced in the Navicat 12–15 cycle. | Materially better authoring ergonomics than DBeaver's raw-JSON-array console; roughly comparable in kind (though shallower in depth) to Compass/VisuaLeaf/Studio 3T. | Research file narrative + release history |
| AGG-stage-preview | Per-stage *output* preview confirmed; combined input+output ("IO") inspection explicitly not present. | Developers can verify results as they build a pipeline, but cannot inspect what each stage received as input the way Studio 3T's debugger allows. | Research file's own head-to-head comparison table |
| AGG-code-gen | Confirmed absent — no multi-language driver code generation from a pipeline. | Developers must hand-translate a working pipeline into application code themselves; a real, source-confirmed competitive gap versus Studio 3T. | Research file (user feedback section + comparison table) |
| AGG-mapreduce-editor | A distinct author/test/debug workflow for MapReduce scripts, working against sampled document sets before full-cluster execution. | Gives Navicat a MapReduce-specific development workflow that neither the aggregation pipeline builder nor a generic shell would provide. | Research file narrative |

## Constraints and risks

- The source frames the aggregation builder's "output preview only, no code-gen" limitation as a *competitive weakness* for Navicat relative to Studio 3T, not as a strength — treat the F-AGG area overall as "real capability, materially shallower than the deepest competitors reviewed in this repository," not as a full-parity implementation.
- Stage-toggle, pipeline execution options (allowDiskUse/collation/maxTimeMS), and JSON pipeline import/export are silent gaps in the source (not discussed either way) and are omitted from the matrix rather than marked absent.

## Interactions and dependencies

- The BI workspace ([F-QUERY](../querying/feature-report.md)'s `QUERY-charts-dashboards`) draws on "visual query tools" and "aggregations" as its data source — implying some integration between the aggregation surface and the BI/dashboard surface, though the exact mechanism is not detailed.
- MapReduce (this feature) is a separate execution path from the aggregation pipeline; both are listed together under "Graphical designers for... Aggregation Pipelines... and MapReduce jobs" in the source's Feature Inventory.

## Conclusions

### Strengths

- A genuine, drag-and-drop visual stage-by-stage aggregation pipeline builder with per-stage output preview.
- A dedicated MapReduce author/test/debug editor, distinct from the pipeline builder, working against sampled data before full-cluster execution.

### Limitations

- No deep stage input/output inspection (output preview only) — confirmed by direct statement in the source's own comparison table.
- No multi-language driver code generation from a pipeline — confirmed absent by direct, repeated statement.

### Unknowns

- Stage enable/disable toggling, pipeline execution options, keyboard shortcuts, JSON pipeline import/export, and total supported stage-type count are not discussed in the source in either direction.
- Whether a MongoDB view can be created directly from a saved pipeline.
