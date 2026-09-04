# Feature Matrix — Navicat / Data Transfer

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: Navicat
- Product group: third-party
- Feature ID: F-TRANSFER (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `data-transfer`
- Analysis date: 2026-09-04
- Version/release context: Navicat 17 line

## Source index

- S1: Navicat Competitive Intelligence Analysis (secondary research file), `research/google_research/navicat-competitive-intelligence-analysis/Navicat Competitive Intelligence Analysis.md`

## Capability matrix (low-level)

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TRANSFER-import-csv | Import CSV | Confirmed | S1: "Supported source formats include TXT, CSV, XML, JSON, Microsoft Access, Microsoft Excel, and external ODBC data sources." "The wizard guides users through delimiter selection, character encoding, field mapping, data type conversion, and import execution modes." | — | Unverified | S1 | — |
| TRANSFER-import-json | Import JSON | Confirmed | Same Import Wizard sentence as above; JSON explicitly named. | — | Unverified | S1 | — |
| TRANSFER-import-bson | Import BSON | Confirmed | S1: "graphical wrappers for mongodump and mongorestore utilities, enabling logical backups and restores directly within the GUI"; also "native wrappers for mongoimport and mongoexport command-line utilities." | — | Unverified | S1 | mongorestore = BSON archive import; mongoimport = JSON/CSV import (already covered above). |
| TRANSFER-import-sql | Import from SQL | Confirmed (Navicat Premium only) | S1: "Cross-DBMS migration is supported through the Data Transfer engine in Navicat Premium. This enables migrations between different database paradigms, such as moving tables from MySQL or PostgreSQL into MongoDB document collections with automatic column-to-BSON field mapping." | Requires Navicat Premium (multi-engine tier), not available in the standalone Navicat for MongoDB SKU. | Unverified | S1 | — |
| TRANSFER-import-modes | Insertion modes | Confirmed | S1: "import execution modes (append, update, replace, or skip existing records)." | — | Unverified | S1 | — |
| TRANSFER-export-csv | Export CSV | Confirmed | S1: "The Export Wizard allows users to extract data from collections, views, tables, or custom query results into formats including CSV, Excel, Access, TXT, XML, and JSON." | — | Unverified | S1 | — |
| TRANSFER-export-excel | Export Excel | Confirmed | Same Export Wizard sentence; Excel explicitly named. | — | Unverified | S1 | — |
| TRANSFER-export-json | Export JSON | Confirmed | Same Export Wizard sentence; JSON explicitly named. Also: "native wrappers for... mongoexport command-line utilities." | — | Unverified | S1 | — |
| TRANSFER-export-bson | Export BSON | Confirmed | S1: "graphical wrappers for mongodump and mongorestore utilities, enabling logical backups and restores directly within the GUI." | Backup tasks "can be encrypted, compressed, and assigned automated retention policies using the scheduler." | Unverified | S1 | mongodump = BSON archive export. |
| TRANSFER-export-mongo | Export to MongoDB | Confirmed | S1 (Data Transfer engine): "Executes high-throughput data migration across local, remote, or cloud-hosted database connections." Cross-server/cross-database MongoDB-to-MongoDB copy is implied by "local, remote, or cloud-hosted database connections" applying to same-engine transfers, consistent with the general Data Transfer description. | — | Unverified | S1 | — |
| TRANSFER-field-mapping | Field mapping | Confirmed | S1: "with configurable field mapping rules" (Data Transfer engine); also "field mapping" named explicitly in the Import Wizard description. | — | Unverified | S1 | — |
| TRANSFER-gridfs-crud | GridFS file CRUD | Confirmed | S1: "Users can browse, stream, upload, and download files within GridFS buckets." | — | Unverified | S1 | Upload/download = CRUD; browsing/streaming is also tracked under `QUERY-view-gridfs` in [F-QUERY](../querying/feature-matrix.md) per the dictionary's own distinction between the two IDs. Delete/rename/metadata-edit specifically are not itemized. |
| TRANSFER-masking-tool | Data masking tool | Not supported (confirmed absent) | S1: "No Field-Level Data Obfuscation or Masking: Navicat lacks native dynamic data masking or field-level obfuscation tools. Developers pulling production data down to staging environments cannot automatically sanitize sensitive fields (such as credit card numbers or personally identifiable information) during export or migration operations." | — | Not planned | S1 | Confirmed-absent by direct, explicit statement — a named weakness in the source's own Strengths/Weaknesses table. |
| TRANSFER-test-data-gen | Synthetic test data generator | Unverified | S1 (Release History): "The Navicat 16 release cycle introduced a user interface overhaul with full Dark Mode support, added native connectivity for Redis key-value stores, updated data generation tools, introduced Collection Profiles for MongoDB..." | The phrase "updated data generation tools" implies a pre-existing data-generation capability that was updated in v16; no detail on whether it is schema-aware, constrained, or faker-style, nor whether it applies to MongoDB specifically. | Unverified | S1 | This is the thinnest possible evidentiary basis in this Navicat report for the new dictionary ID `TRANSFER-test-data-gen` — a single passing phrase in a release-history bullet, with no elaboration anywhere else in the source. Included because it is the closest and only plausible match, not because the claim is well-evidenced. |

## Feature-level conclusion

### Confirmed strengths

- A comprehensive Import/Export Wizard pair covering TXT, CSV, XML, JSON, Access, Excel, and ODBC formats, plus native mongoimport/mongoexport and mongodump/mongorestore GUI wrappers.
- A dedicated cross-DBMS Data Transfer engine (Navicat Premium) supporting relational-to-MongoDB migration with automatic column-to-BSON field mapping — though see the Constraints/prerequisites column: this is an object-to-object copy utility, not a JOIN-to-embedded-document/`$lookup` translation engine (see [product-report.md](../../product-report.md)).
- Native GridFS file CRUD (upload/download, complementing the browsing/streaming half tracked under F-QUERY).

### Confirmed limitations

- No field-level data masking/obfuscation of any kind — confirmed absent by direct, explicit statement, named as a specific weakness in the source's own analysis.
- The Data Transfer engine's cross-DBMS capability is confirmed to be an object-to-object copy utility, not an intelligent schema-restructuring migration tool: S1 states directly that Navicat's migration tool "lacks advanced, bi-directional SQL-to-MongoDB schema translation algorithms, such as automatically converting relational foreign key JOIN relationships into embedded sub-documents or $lookup array references."

### Open questions / unknowns

- Whether the "updated data generation tools" mentioned for Navicat 16 constitute a schema-aware synthetic/constrained dataset generator (as the new `TRANSFER-test-data-gen` dictionary ID describes) or something narrower (e.g., simple placeholder/lorem-ipsum-style filler data, or a relational-only feature) — the source gives no further detail.
- Exact scope of incremental export, custom JavaScript per-document transforms, and server-side pre-export pipeline transforms — none of these are discussed for Navicat.
- Whether GridFS delete/rename/metadata-edit operations (as opposed to upload/download) are supported.
