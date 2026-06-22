# Feature Matrix — VisuaLeaf / Data Transfer

## Navigation

- [← Product Report](../../product-report.md)
- [Feature Report](feature-report.md)
- [← Indexing & Performance Matrix](../indexing-performance/feature-matrix.md)
- [→ Task Scheduler Matrix](../task-scheduler/feature-matrix.md)
- [→ Shell Matrix](../shell/feature-matrix.md)
- [→ AI Matrix](../ai/feature-matrix.md)
- [→ Governance Matrix](../governance/feature-matrix.md)

## Source index

- S1: https://visualeaf.com/docs/task-manager

## Capability matrix

| Sub-feature ID | Capability | Status | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| TRANSFER-export-json | Export: JSON | confirmed | Pretty-print optional; standard MongoDB Extended JSON. | — | confirmed | S1 |
| TRANSFER-export-csv | Export: CSV | confirmed | Configurable delimiters and headers. | — | confirmed | S1 |
| TRANSFER-export-bson | Export: BSON | confirmed | Native MongoDB BSON format; suitable for backup/restore. | — | confirmed | S1 |
| TRANSFER-export-sql-stmts | Export: SQL INSERT statements | confirmed | SQL INSERT statements; for relational database migration. | — | confirmed | S1 |
| TRANSFER-import-json | Import: JSON | confirmed | Import from JSON file. | — | confirmed | S1 |
| TRANSFER-import-csv | Import: CSV | confirmed | Import from CSV file. | — | confirmed | S1 |
| TRANSFER-import-bson | Import: BSON | confirmed | Import from BSON file. | — | confirmed | S1 |
| TRANSFER-field-mapping | Field mapping and restructuring | confirmed | Map source field names to destination field names; rename fields; restructure document shape on import. | — | confirmed | S1 |
| TRANSFER-transform-types | Transformation: data type conversion | confirmed | E.g., string → date conversion during import. | — | confirmed | S1 |
| TRANSFER-transform-filter | Transformation: document filtering | confirmed | Include/exclude documents by condition before import. | — | confirmed | S1 |
| TRANSFER-transform-js | Transformation: custom JavaScript | confirmed | User-defined JS transform functions applied per document. | — | confirmed | S1 |
| TRANSFER-transform-pipeline | Transformation: aggregation pipeline pre-export | confirmed | Apply $pipeline stages as server-side pre-export transform. | — | confirmed | S1 |
| TRANSFER-import-modes | Import modes | confirmed | Upsert mode: update existing documents or insert new ones based on a configurable match key. | — | confirmed | S1 |
| TRANSFER-task-save | Save import/export as schedulable task | confirmed | Import and export configurations can be saved as schedulable tasks managed in the Task Scheduler. | — | confirmed | S1 |
| TRANSFER-plan-limits | Plan limits for tasks | confirmed | Community: 0 tasks (no import/export automation); Basic: up to 2 tasks; Professional: unlimited tasks. | — | confirmed | S1 |
