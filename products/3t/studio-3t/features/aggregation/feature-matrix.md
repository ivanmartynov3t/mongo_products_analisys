# Feature Matrix — Studio 3T / Aggregation

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Source index

- S1: https://studio3t.com/knowledge-base/articles/query-mongodb/

## Capability matrix

| Capability ID | Capability | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AGG-001 | Pipeline editor layout | Supported | Five-region UI: (1) Pipeline panel (top-left) — all stages listed with enable/disable checkboxes; (2) Stage editor (top-right) — code editor for current stage with auto-named or custom stage name; (3) Stage input/output (bottom) — Run button per panel, Count Documents, vertical/horizontal layout toggle; (4) Pipeline output (bottom tab) — full pipeline result; (5) Query Code tab and Explain tab. | — | confirmed | S1 | All editions. |
| AGG-002 | Stage management | Supported | Add stage (Shift+Ctrl+N), Add before/after selected stage, Duplicate stage, Move up (Shift+F8), Move down (F8), Enable/disable via checkbox or right-click, Delete. Run entire pipeline (F5), Run selection, Refresh (Ctrl+R). | — | confirmed | S1 | All editions. |
| AGG-003 | Enable / disable individual stages | Supported | Each stage has a checkbox; disabled stages are skipped in pipeline execution without deletion. Also accessible via right-click context menu. | — | confirmed | S1 | All editions. |
| AGG-004 | Pipeline options | Supported | allowDiskUse toggle (writes to _tmp subdirectory of dbPath when memory limit exceeded); custom collation (language-specific string comparison with locale and strength settings); index hint (choose collection scan, specify index name, or define index specification document). | allowDiskUse requires sufficient disk space on MongoDB server. Collation must match server locale support. | confirmed | S1 | All editions. |
| AGG-005 | Code generation — multi-language | Supported | Query Code tab generates: JavaScript (Node.js), Java 2.x driver API, Java 3.x driver API, Java 4.x driver API (separate sub-tabs), C#, Python, PHP, Ruby, MongoDB Shell (mongosh syntax). "Open in IntelliShell" button for MongoDB Shell target. | Generated code reflects current pipeline state; manual review recommended before production use. | confirmed | S1 | All editions. |
| AGG-006 | Export from pipeline | Supported | Export Wizard can be launched from Pipeline output or from individual Stage I/O panels. Exports the document set as seen at that pipeline stage. | Export target format and options follow the same Export Wizard configuration as standard exports. | confirmed | S1 | All editions. |
| AGG-007 | Save and load pipelines | Supported | Save as Studio 3T query (with optional saved target: connection + database + collection) or as a .js file. Load from Query Manager or .js file. | .js save omits target details; Studio 3T query format stores full context. | confirmed | S1 | All editions. |
| AGG-008 | Create view from pipeline | Supported | "Create view from aggregate query" option generates a db.createView() call using the current pipeline. View appears in Connection Tree under the source database > Views folder. | Requires MongoDB ≥ 3.4 for view support. Requires write access to the database. | confirmed | S1 | All editions. |
| AGG-009 | Side-by-side with Visual Query Builder | Supported | Open Aggregation Editor alongside VQB; changes in VQB $match stages sync bidirectionally to the equivalent Aggregation Editor stage. | VQB sync applies specifically to $match and $project stages generated from VQB conditions. | confirmed | S1 | All editions. |
| AGG-010 | Change source collection / database / connection | Supported | Toolbar allows switching the target collection, database, or connection mid-session without losing the current pipeline. | The pipeline must be re-run after switching target. Field names in stages may no longer match if schema differs. | confirmed | S1 | All editions. |
| AGG-011 | Date Tags in $match stages | Supported | Date Tag syntax (#today, #lastNdays, #lastcalmonth, etc.) usable in $match stage conditions; expands to {$gt, $lt} date range at execution time. | Date Tags are Studio 3T–specific; pipeline exported as .js will include the expanded literal values at save time. | confirmed | S1 | All editions. |
| AGG-012 | Copy / paste entire aggregate query | Supported | Full pipeline JSON can be copied to clipboard and pasted into another Aggregation Editor session or IntelliShell. | — | confirmed | S1 | All editions. |
