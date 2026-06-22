# Feature Matrix — Studio 3T / Querying

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Shell feature](../shell/feature-matrix.md) — IntelliShell capabilities (SHELL-*)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Source index

- S1: https://studio3t.com/knowledge-base/articles/query-mongodb/
- S2: https://studio3t.com/knowledge-base/articles/table-view/
- S3: https://studio3t.com/knowledge-base/articles/collections-tab/
- S4: https://studio3t.com/knowledge-base/articles/date-tags/

## Capability matrix

| Capability ID | Capability | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| QUERY-filter-bar | Collection tab query bar | Supported | Five fields: Query, Projection, Sort, Skip, Limit. Auto-completion for {, [, " pairs; field names; operators; BSON type wrappers; Ctrl+Space trigger. Syntax coloring. Shorthand expansions: bare ObjectId hex → ObjectId("...") query, bare UUID, bare number, bare quoted string. Query JSON Editor with Validate button. Run variants: find(), findOne(), count(). | Query must be valid JSON (with BSON extensions). | confirmed | S1, S3 | All editions. |
| QUERY-history | Query history and save/load | Supported | Queries auto-saved every run to history. Manual save to local files or shared folders. Saved queries include connection + database + collection target details. Default query per collection (auto-runs on open). | Shared folder save requires Pro/Base+. | confirmed | S1 | History: all editions. Shared save: Pro/Base+. |
| QUERY-open-in | Open query in other tools | Supported | "Open in IntelliShell" sends current query. "Open in Aggregation Editor" converts find() filters and projections into equivalent pipeline stages ($match, $project). | Conversion to aggregation stages is best-effort; complex operators may need manual adjustment. | confirmed | S1 | All editions. |
| QUERY-view-table | Table View | Supported | Rows/columns result view. In-place editing via double-click. Sort by column headers. Column reorder via drag. Hide/show columns (Ctrl+T). Auto-size compact or full. Expand embedded fields with breadcrumb trail navigation. Step into arrays at column or cell level. Copy as CSV. Copy for Excel. BSON type coloring (configurable). Restore default view. | Very wide documents or deeply nested structures may require manual column configuration. | confirmed | S2 | All editions. |
| QUERY-view-tree | Tree View | Supported | Hierarchical document display. In-place editing. Multi-line editor (ellipsis button) for long values. | — | confirmed | S1 | All editions. |
| QUERY-view-json | JSON View and document editor | Supported | Scrollable JSON documents per result. Document JSON Editor (Ctrl+J) for full-document editing. Validate JSON before save. | — | confirmed | S1 | All editions. |
| QUERY-multi-update | In-place multi-document update | Supported | "Update Documents" dialog: equivalent to updateMany(); separate query tab and update tab; Collection History recording option; Validate JSON. | Requires write access to the collection. | confirmed | S1 | All editions. |
| QUERY-vqb-core | Visual Query Builder (VQB) | Supported | Drag-and-drop cells/fields from Table View (single) or Tree View (multi-select via Ctrl). VQB and Query Bar bidirectionally sync in real time. Standalone or alongside IntelliShell. Top-level combiners: Match all ($and), Match any ($or), Match none ($nor). Nested AND/OR groups. Per-field operator dropdown + value field with auto-detected BSON type (manually overridable). Multiline text editor for long strings. Advanced editors for Binary, Reference, Regex. Clone field rules (duplicate button). | Array querying requires stepping into array column via "Has array element(s) matching" option. | confirmed | S1 | All editions. |
| QUERY-vqb-proj-sort | VQB Projection and Sort sections | Supported | VQB has distinct Query, Projection, and Sort sections. Code generation (Query Code tab) updates in real time as VQB is edited. | — | confirmed | S1 | All editions. |
| QUERY-date-tags | Date Tags | Supported | Tags available in: Collection Tab query bar, IntelliShell, VQB, Aggregation Editor $match stages, Export queries. Absolute: #today, #yesterday, #tomorrow. Hour: #lasthour, #nexthour, #lastNhours, #nextNhours. Days/weeks/months/years: #lastNdays, #lastcalweek, #thismonth, #thisyear, etc. Open-ended: #uptonow, #fromnow, #beforetoday, #aftertoday. Each expands to {$gt: <start>, $lt: <end>} at runtime. | N must be a positive integer; tags are Studio 3T–specific and not valid native MongoDB syntax. | confirmed | S4 | All editions. |
| QUERY-manager | Query Manager | Supported | Organizes queries in folders (drag-and-drop). Filter by folder or search by name. Query preview panel. Create, edit (Quick edit), duplicate, delete. Supported query types: Collection query, IntelliShell script, SQL Query, Aggregation query. Auto-saved query history (separate store from saved queries). | SQL Query type requires Pro/Base+. | confirmed | S1 | All editions for collection/IntelliShell/aggregation; Pro/Base+ for SQL. |
