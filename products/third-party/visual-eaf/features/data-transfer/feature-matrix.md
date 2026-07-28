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
- S2: https://visualeaf.com/features/mongosync/

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
| TRANSFER-import-mongo | Import: cross-server/cluster MongoDB (MongoSync) | confirmed | MongoSync: "moves data wherever you need it" between local MongoDB instances, MongoDB Atlas, one cluster to another, across different databases, or between any saved VisuaLeaf connections. Guided workflow copies collections, indexes, and documents; selective sync (choose databases/collections, apply a query filter to sync only matching documents); optional name remapping or merge into existing collections; field filtering to exclude sensitive fields; transformation mappings (auto-detected fields incl. nested paths/BSON types, type casting, value scripts). Companion verification: Collection Compare shows a document-level diff before/after a sync (see GOV-collection-compare — a distinct, complementary capability, not the same feature). | Plan tier not explicitly stated; page mentions Pro tier availability. | confirmed | S2 |
| TRANSFER-export-mongo | Export: cross-server/cluster MongoDB (MongoSync) | confirmed | Same MongoSync workflow as TRANSFER-import-mongo, in the export direction (VisuaLeaf connection → another MongoDB instance/cluster/Atlas). | Plan tier not explicitly stated; page mentions Pro tier availability. | confirmed | S2 |
| TRANSFER-field-mapping | Field mapping and restructuring | confirmed | Map source field names to destination field names; rename fields; restructure document shape on import. | — | confirmed | S1 |
| TRANSFER-transform-types | Transformation: data type conversion | confirmed | E.g., string → date conversion during import. | — | confirmed | S1 |
| TRANSFER-transform-filter | Transformation: document filtering | confirmed | Include/exclude documents by condition before import. | — | confirmed | S1 |
| TRANSFER-transform-js | Transformation: custom JavaScript | confirmed | User-defined JS transform functions applied per document. | — | confirmed | S1 |
| TRANSFER-transform-pipeline | Transformation: aggregation pipeline pre-export | confirmed | Apply $pipeline stages as server-side pre-export transform. | — | confirmed | S1 |
| TRANSFER-import-modes | Import modes | confirmed | Upsert mode: update existing documents or insert new ones based on a configurable match key. MongoSync (cross-server MongoDB copy, see TRANSFER-import-mongo) additionally documents insert-new, upsert-on-match, and skip-existing conflict-handling options — unclear whether these extend to the general Task Manager import path or are scoped to MongoSync specifically. | — | confirmed | S1, S2 |
| TRANSFER-task-save | Save import/export as schedulable task | confirmed | Import and export configurations can be saved as schedulable tasks managed in the Task Scheduler. | — | confirmed | S1 |
| TRANSFER-plan-limits | Plan limits for tasks | confirmed | Community: 0 tasks (no import/export automation); Basic: up to 2 tasks; Professional: unlimited tasks. | — | confirmed | S1 |
