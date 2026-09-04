# Feature Matrix — NoSQLBooster / Data Transfer

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: NoSQLBooster
- Product group: third-party
- Feature ID: F-TRANSFER (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `data-transfer`
- Analysis date: 2026-09-04
- Version/release context: v11.0–v11.1 line

## Source index

- S1: NoSQLBooster Competitive Analysis
- S2: NoSQLBooster Competitive Intelligence Analysis
- P1: nosqlbooster.com/features (primary; fetched directly by this review)

## Capability matrix (low-level)

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TRANSFER-import-csv | Import CSV | Confirmed | S2: "File-based import and export formats encompass JSON, BSON, CSV, Excel (.xlsx, .xlsb), HTML, and plain text." | — | N/A | S2 | — |
| TRANSFER-import-json | Import JSON | Confirmed | Same S2 citation. | — | N/A | S2 | — |
| TRANSFER-import-bson | Import BSON | Confirmed | S2 lists BSON among formats; also "native integrations for mongoimport, mongoexport, mongodump, and mongorestore." | — | N/A | S2, S1 | — |
| TRANSFER-import-sql | Import from SQL | Confirmed | S2: "Data integration capabilities support direct table imports from relational database management systems, including MySQL, PostgreSQL, and Microsoft SQL Server." | — | N/A | S2 | Oracle is not named (unlike the dictionary description's illustrative example list); only MySQL/PostgreSQL/SQL Server are confirmed. |
| TRANSFER-export-excel | Export Excel | Confirmed | S2 lists "Excel (.xlsx, .xlsb)" export explicitly. | — | N/A | S2 | Two distinct Excel formats (.xlsx and .xlsb) is a specific, differentiated claim. |
| TRANSFER-export-sql-stmts | Export SQL INSERT | Confirmed | S1: "data export options cover JSON, BSON, CSV, Excel (.xlsx/.xlsb), SQL scripts, and HTML tables." | — | N/A | S1 | — |
| TRANSFER-task-save | Save as task | Confirmed | S2: "Users can define recurring workflows for database backups, data migrations, script executions, and export tasks." | Gated: S1's pricing table states the Personal tier "cannot run tasks in CLI, have no task scheduling"; unlocked at Commercial tier. | N/A | S2, S1 (gating) | Cross-referenced with `SCHED-task-save`/`SCHED-task-types` in F-SCHED. |
| TRANSFER-test-data-gen | Synthetic test data generator | Confirmed (S2 only, corroborated by primary source) | S2: "a Test Data Generator capable of synthesizing structured mock BSON datasets for database benchmarking." P1 independently confirms and elaborates: "Test Data Generator (Mock Data)... more than 100 templates to create random faked 'real' data... generate mock data with incredibly large size," listed as a "unique feature" on the vendor's own site. | — | N/A | S2, P1 | S1 does not mention this capability at all — this is a genuine S1/S2 coverage gap (not a contradiction) rather than a conflict; this review confirmed it independently via the primary source both files' Works Cited otherwise point to, so it is marked Confirmed rather than Unverified-single-source. This is the direct evidentiary basis for this effort's `TRANSFER-test-data-gen` dictionary ID being applicable to NoSQLBooster. |
| TRANSFER-gridfs-crud | GridFS file CRUD | Confirmed | P1: "With our GridFS Viewer, you can read and write to GridFS collections. Files can be added quickly with drag and drop." S1 more generally: "binary storage is managed through a graphical GridFS viewer." | — | N/A | P1, S1 (general) | Distinct from `QUERY-view-gridfs` (browsing/viewing), tracked in F-QUERY — this row covers the read/write/upload CRUD depth specifically. |

## Feature-level conclusion

### Confirmed strengths

- Broad import/export format coverage (JSON, BSON, CSV, dual Excel formats, SQL scripts, HTML, plain text) plus native `mongoimport`/`mongoexport`/`mongodump`/`mongorestore` wrappers.
- A genuine, primary-source-confirmed Test Data Generator (100+ faker-style templates, large-scale synthetic BSON dataset generation) — notable because it appears in only one of the two research files (S2), and this review independently corroborated it via the vendor's own Feature Tour page rather than accepting a single-source secondary claim at face value.
- GridFS file CRUD (read/write/upload via drag-and-drop), distinct from browse-only viewing.

### Confirmed limitations

- Task-save-to-scheduler is confirmed gated below Commercial tier, per S1's pricing table.
- Neither research file describes a field-level data-masking/obfuscation tool, incremental export with resume points, or per-document custom JavaScript transforms during import/export — these remain unconfirmed rather than assumed absent, since neither file makes an explicit absence claim the way both files do for governance or aggregation-builder gaps.

### Open questions / unknowns

- Whether the Test Data Generator's 100+ templates are user-extensible/customizable beyond the built-in set, and whether generated datasets can target existing collections with existing documents (append) versus new collections only.
- Data-masking, incremental-export, and custom-JS-transform capabilities during import/export — not discussed in either source file.
