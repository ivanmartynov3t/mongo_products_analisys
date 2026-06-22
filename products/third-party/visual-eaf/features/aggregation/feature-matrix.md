# Feature Matrix — VisuaLeaf / Aggregation

## Navigation

- [← Product Report](../../product-report.md)
- [Feature Report](feature-report.md)
- [← Querying Matrix](../querying/feature-matrix.md)
- [→ Schema Matrix](../schema/feature-matrix.md)
- [→ Indexing & Performance Matrix](../indexing-performance/feature-matrix.md)
- [→ Data Transfer Matrix](../data-transfer/feature-matrix.md)
- [→ Shell Matrix](../shell/feature-matrix.md)
- [→ AI Matrix](../ai/feature-matrix.md)
- [→ Governance Matrix](../governance/feature-matrix.md)
- [→ Task Scheduler Matrix](../task-scheduler/feature-matrix.md)

## Source index

- S1: https://visualeaf.com/docs/aggregation

## Capability matrix

| Sub-feature ID | Capability | Status | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| AGG-stage-count | Supported stage types | confirmed | 37+ stages in palette: $match, $limit, $skip, $sample, $count, $project, $addFields, $set, $unset, $sort, $unwind, $replaceRoot, $replaceWith, $redact, $densify, $fill, $setWindowFields, $group, $bucket, $bucketAuto, $sortByCount, $lookup, $graphLookup, $unionWith, $facet, $out, $merge, $geoNear, $search (Atlas), $documents, $collStats, $indexStats, $planCacheStats, $listSearchIndexes. | — | confirmed | S1 |
| AGG-editor-layout | Pipeline editor layout | confirmed | Visual pipeline canvas with stage cards; stages displayed sequentially; each card shows stage type, collapsed/expanded config, and per-stage preview. | — | confirmed | S1 |
| AGG-stage-mgmt | Stage management | confirmed | Add stage; reorder via drag-and-drop; duplicate stage (Ctrl+D); delete stage (Delete key). | — | confirmed | S1 |
| AGG-stage-modes | Stage configuration modes | confirmed | Form Mode: field dropdowns with schema autocomplete; Visual Query Builder integration for $match; data-type validation. Accumulator Expression Builder: visual builder for $group accumulators ($sum, $avg, $max, $min, $first, $last, $push, $addToSet). MongoDB Editor (raw JSON): Monaco editor per stage with MongoDB-aware syntax highlighting; IntelliSense auto-complete for field names, operators, MongoDB functions (Ctrl+Space); real-time error detection and highlighting. Form Mode ↔ MongoDB Editor toggle per individual stage; preference saved per stage. | — | confirmed | S1 |
| AGG-stage-preview | Stage preview | confirmed | Input/Output split-view panel; side-by-side stage input and output documents; 20-document sample for quick per-stage preview; Auto-Preview mode (updates on every config change, toggleable); preview disabled for $out and $merge (would write to collection); input and output panels individually resizable; doc count shown. | — | confirmed | S1 |
| AGG-stage-toggle | Stage enable/disable toggle | unknown/unverified | No explicit per-stage enable/disable toggle documented in VisuaLeaf docs. | — | unknown/unverified | S1 |
| AGG-pipeline-opts | Pipeline execution options | confirmed | Allow Disk Use: default false; toggle to allow large in-memory sort overflow to disk. Max Time: default 300 seconds; configurable. Auto Collapse: default false; collapses all stage cards for pipeline overview. | — | confirmed | S1 |
| AGG-timer-cancel | Execution timer and cancel | confirmed | Real-time execution timer with cancel button to abort pipeline. | — | confirmed | S1 |
| AGG-pagination | Result pagination | confirmed | First / Previous / Next / Last navigation for paginated results. | — | confirmed | S1 |
| AGG-keyboard | Keyboard shortcuts | confirmed | Ctrl+Enter: execute pipeline; Ctrl+S: save current pipeline; Delete: remove selected stage; Ctrl+D: duplicate selected stage; Ctrl+Space: trigger IntelliSense in MongoDB Editor mode. | — | confirmed | S1 |
| AGG-js-import-export | Pipeline .js import/export | confirmed | Export pipeline as .js file (mongosh format: db.collection.aggregate([…])). Import pipeline from previously exported .js file. | — | confirmed | S1 |
| AGG-code-tab | Query Code tab | confirmed | Bidirectional JSON view of the pipeline; Format Code button; Apply Code Changes syncs edits back to visual builder. | — | confirmed | S1 |
| AGG-export-results | Export pipeline results | confirmed | Export pipeline output in 4 formats: JSON; CSV; BSON; SQL INSERT statements. | — | confirmed | S1 |
| AGG-chart-builder | Create Chart from pipeline | confirmed | Opens Chart Builder using the pipeline output as data source. | — | confirmed | S1 |
| AGG-save-load | Save/load pipelines | confirmed | Save with name, folder, description; tagged with connection/DB/collection; quick load by double-click. | — | confirmed | S1 |
| AGG-code-gen | Export pipeline to driver languages | unknown/unverified | No source found in VisuaLeaf docs for export to driver languages (Java, Python, Node.js, etc.). | — | unknown/unverified | S1 |
| AGG-create-view | Create view from pipeline output | unknown/unverified | Not documented in VisuaLeaf aggregation docs. | — | unknown/unverified | S1 |
| AGG-clipboard | Copy/paste full pipeline JSON | unknown/unverified | Not explicitly documented; Query Code tab may provide equivalent capability. | — | unknown/unverified | S1 |
