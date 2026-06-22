# Feature Matrix — VisuaLeaf / Querying

## Navigation

- [← Product Report](../../product-report.md)
- [Feature Report](feature-report.md)
- [← Connectivity Matrix](../connectivity/feature-matrix.md)
- [→ Aggregation Matrix](../aggregation/feature-matrix.md)
- [→ Schema Matrix](../schema/feature-matrix.md)
- [→ Indexing & Performance Matrix](../indexing-performance/feature-matrix.md)
- [→ Data Transfer Matrix](../data-transfer/feature-matrix.md)
- [→ Shell Matrix](../shell/feature-matrix.md)
- [→ AI Matrix](../ai/feature-matrix.md)
- [→ Governance Matrix](../governance/feature-matrix.md)
- [→ Task Scheduler Matrix](../task-scheduler/feature-matrix.md)

## Source index

- S1: https://visualeaf.com/docs/mongo-query

## Capability matrix

| Sub-feature ID | Capability | Status | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| QUERY-view-tree | Tree View | confirmed | Expand/collapse nested docs; color-coded BSON types; inline editing; 3 search modes (Field/Value/Both). | — | confirmed | S1 |
| QUERY-view-table | Table View | confirmed | Sortable/resizable columns; show/hide columns; drag-to-reorder; multi-select rows; nested expansion. | — | confirmed | S1 |
| QUERY-view-json | BSON View | confirmed | Extended JSON syntax highlighting; copy as EJSON; preserves ObjectId/Date/Binary types. | — | confirmed | S1 |
| QUERY-view-explain | Explain View | confirmed | Execution plan, index usage, docs examined vs returned, index suggestions. | — | confirmed | S1 |
| QUERY-filter-bar | Query filter editor | confirmed | JSON filter field (find() style); ACE editor with JSON syntax highlighting; Ctrl+Space triggers field name autocomplete derived from collection schema. | — | confirmed | S1 |
| QUERY-projection | Projection editor | confirmed | Include (1) / exclude (0) fields; JSON editor. | — | confirmed | S1 |
| QUERY-sort | Sort editor | confirmed | Ascending (1) / descending (-1) per field; JSON editor. | — | confirmed | S1 |
| QUERY-skip-limit | Skip and limit controls | confirmed | Limit dropdown: 50, 100, 200, 300, 500 documents per page. Skip dropdown: 0, 50, 100. | — | confirmed | S1 |
| QUERY-perf-timer | Execution timer with visual thresholds | confirmed | Timer turns amber at 2s, red at 5s; visual alert for slow queries. | — | confirmed | S1 |
| QUERY-run-variants | Run variants | confirmed | Run All: executes find() with current filter/projection/sort/limit/skip. Run Find One: executes findOne() with current filter. Run Count: executes countDocuments() with current filter. | — | confirmed | S1 |
| QUERY-cancel | Cancel running query | confirmed | Cancel button terminates in-flight query. | — | confirmed | S1 |
| QUERY-vqb-core | Visual Query Builder — core | confirmed | Basic+ plan only; toggleable; resizable panel; width persisted per activity. Drag fields from collection schema panel into conditions. Operator selection: $eq, $ne, $gt, $gte, $lt, $lte, $in, $nin, $regex, and more. AND/OR logic builder with nested condition groups. Type-aware inputs: date pickers, number sliders, boolean toggles based on field BSON type. | Basic or Professional plan required | confirmed | S1 |
| QUERY-vqb-proj-sort | VQB Projection and Sort Builders | confirmed | Projection Builder: visual field include/exclude checkboxes. Sort Builder: ascending/descending toggle per field. | Basic or Professional plan required | confirmed | S1 |
| QUERY-vqb-bidirectional | VQB bidirectional JSON sync | confirmed | VQB changes update JSON editor in real time; JSON editor changes update VQB. | — | confirmed | S1 |
| QUERY-vqb-plan | VQB plan requirement | confirmed | Requires Basic or Professional plan. | Basic or Professional plan | confirmed | S1 |
| QUERY-ai-builder | AI Query Builder | confirmed | Professional plan only. Natural language → find()-style query and full multi-stage aggregation pipeline. Every AI-generated query includes a plain-English explanation. Uses collection field names and BSON types; optionally sends sample documents ("Send sample data ON" = Better Accuracy; OFF = More Private). Prior conversation turns used for follow-up refinements. 11 OpenAI models: ChatGPT4o (recommended/gpt-4o), ChatGPT4oMini (gpt-4o-mini), ChatGPTo3Mini (o3-mini), ChatGPTo1 (o1), ChatGPTo1Mini (o1-mini), ChatGPTo1Preview (o1-preview), ChatGPT41 (gpt-4.1), ChatGPT41Mini (gpt-4.1-mini), ChatGPT4Turbo (gpt-4-turbo), ChatGPT4 (gpt-4), ChatGPT35Turbo (gpt-3.5-turbo). Privacy toggle available. | Professional plan required | confirmed | S1 |
| QUERY-inline-edit | Inline editing and field operations | confirmed | Tree View inline edit: click value → type-appropriate editor → Enter to save, Esc to cancel. Field context menu: Add Field, Rename Field ($rename), Delete Field ($unset), Edit Value. | — | confirmed | S1 |
| QUERY-undo-redo | Undo/Redo | confirmed | Ctrl+Z (undo) / Ctrl+Shift+Z (redo). | — | confirmed | S1 |
| QUERY-doc-dialog | Dialog editing with full ACE editor | confirmed | Full ACE editor for entire document; validation before save. | — | confirmed | S1 |
| QUERY-batch-edit | Batch editing (Table View) | confirmed | Select rows → Batch Update → operators ($set, $unset, $inc, $push, $pull) → preview count + example changes → confirm. | — | confirmed | S1 |
| QUERY-copy-options | Copy options | confirmed | JSON, value, EJSON, field name, field path (dot notation). | — | confirmed | S1 |
| QUERY-pagination | Pagination | confirmed | 50 / 100 / 200 / 300 / 500 documents per page. | — | confirmed | S1 |
| QUERY-history | Query history | confirmed | Basic+ plan; auto-saved per collection with timestamp and execution time. Reload restores all parameters: filter, projection, sort, limit, skip. | Basic or Professional plan required | confirmed | S1 |
| QUERY-saved | Saved queries | confirmed | Basic+ plan; name and organize by collection or globally. Export/import saved query libraries as JSON files. Team sharing via exported JSON. | Basic or Professional plan required | confirmed | S1 |
| QUERY-open-in | "Open In" context integration | confirmed | Opens collection context in: Aggregation Pipeline, MongoDB Shell, SQL Query Mode, Collection Statistics, Create Chart, Import Data, Export Data. | — | confirmed | S1 |
