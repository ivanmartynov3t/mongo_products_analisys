# Feature Report — Studio 3T / Data Import & Export

**Last reviewed:** 2026-07-31 — see [research findings](../../../../../research/studio-3t-desktop-review-2026/06-data-transfer-findings.md)

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [High-level comparison](../../../../../reports/comparisons/high-level-product-comparison.md)

## Scope

This report covers Studio 3T's Import Wizard, Export Wizard, incremental export, and data masking — including the standalone masking tool and in-flight masking during import/export operations.

## Behavioral walkthrough

Studio 3T's Import Wizard supports five source formats: CSV, JSON, BSON/mongodump, SQL databases, and another MongoDB collection. Each format exposes format-specific options — CSV offers full control over delimiters, text qualifiers, date format parsing (8 format variants × 3 separators), empty field handling, and an option to disable nested document creation (the "flat doc" mode). JSON import adds a validation pre-scan option that catches malformed JSON before inserting any documents. BSON import delegates to a bundled mongorestore binary, with archive support and single-collection extraction from a full dump archive.

The SQL toolchain is broader than previously documented: per `t3/sqlnosql/SqlFormat.java`, Studio 3T's SQL migration/import/export layer supports **six relational database dialects** — MySQL, Microsoft SQL Server, Oracle, PostgreSQL, Sybase, and IBM DB2 (each with version-specific sub-variants, e.g. `MYSQL_5_7`, `MSSQL_2016`, `ORACLE_12C`). MySQL, MSSQL, Oracle, and PostgreSQL are available under Pro/Base+ licensing across both the Import Wizard, Export Wizard, and SQL Migration tool. Sybase and DB2 are real but Enterprise-license-gated (`AppFeatures.SYBASE_DB`/`DB2`) and asymmetric in scope: Sybase has no direct SQL-export-wizard target (`sqlExport=false`), and DB2 is migration-only — reachable via the SQL Migration tool but not the plain Import/Export Wizard SQL format (`sqlImport=false`, `sqlExport=false`). The "sole full SQL↔MongoDB migration/export toolchain" framing found elsewhere is an exclusivity claim about competitors that a source-code review cannot verify one way or the other; what is confirmed is that the underlying capability is broader (6 dialects) than the 4-dialect figure previously documented here.

The Export Wizard mirrors the Import Wizard's breadth on the output side: CSV, Excel (.xlsx), JSON, BSON/mongodump, SQL, and another MongoDB collection. The Export Wizard's direct SQL target list remains four databases (MySQL, Microsoft SQL Server, Oracle, PostgreSQL) — Sybase and DB2 are not reachable from this wizard (`sqlExport=false` for both), only from the broader SQL Migration tool. Export sources can be the entire collection, a view, a specific find/aggregation query result, or selected documents — with the query bar editable inside the Export unit tab so the export scope can be refined without leaving the wizard. Date/time placeholders in output file paths generate unique filenames per run, which is essential for scheduled recurring exports.

No Parquet, Avro, YAML, standalone XML, or PDF import/export capability was found anywhere in `t3/utils/export/` — these formats are confirmed absent from the current format set, not merely unverified.

Incremental export is a meaningful capability for data pipeline use cases. Studio 3T maintains state across export runs using a tracking field (default: _id). Each subsequent run adds a {$gt: last_seen_value} filter transparently, exporting only new documents. Up to five historical resume points are retained, allowing rollback to an earlier checkpoint. The limitation is explicit in the documentation: incremental export tracks inserts only, not updates to existing documents. This makes it suitable for append-only event streams but not for change-capture of mutable documents.

The data masking feature deserves attention as a first-class tool, not an afterthought. The standalone masking tool supports field-level rules across all BSON types with granular technique options per type: strings can be scrambled, truncated, regex-masked, or replaced; numerics can be shifted by percentage or substituted; dates can be replaced with random or fixed values. The JSON preview updates dynamically as masking rules are configured, giving immediate feedback on what output will look like. Masking can also be applied in-flight during import and export runs, ensuring sensitive data never touches the target without going through the masking rules.

The masking operation count previously documented here ("8 op types") is corrected: `FieldOperation.DMMethod` (`t3/dataman/gui/datamasking/datamaskinggui/datamaskingtab/FieldOperation.java`) defines **20 enum constants — 19 real masking operations plus `NOT_MASKED` as the no-op default state**. The full, representative list by BSON-type category:

- **String (7):** show only first N characters; show only last N characters; mask entire string; mask substrings matching regex; scramble characters; replace entire field with fixed string; replace field value with random string.
- **Numeric — Double/Int32/Int64/Decimal128 (3):** substitute with fixed number; add percentage to number; subtract percentage from number.
- **Date (2):** substitute with random date/time; substitute with fixed date/time.
- **Boolean (2):** negate boolean value; substitute with fixed boolean value.
- **Array (1):** empty contents of the array.
- **ObjectId (1):** substitute with new ObjectId.
- **All types (3):** null out field; exclude field; shuffle.

This is roughly 2.4x the previously documented count. Where "8" was intended as a category count rather than an operation count, the actual category count is 6 (String, Numeric, Date, Boolean, Array, ObjectId), still not a clean match — the recommended correction is to state "19 operation types across 6 BSON-type categories," cited to `FieldOperation.java`.

## GridFS file CRUD (undocumented capability — proposed `TRANSFER-gridfs-crud`)

`t3/utils/gridfsview/mongodb/GridFsViewController.java` implements a full GridFS file-management surface — upload (`addFiles`), download (`writeOutFiles`), delete (`removeFiles`), rename (`renameFile`), and metadata edit (`updateMetaData`) — plus retrieval by name, id, date, or size. This is a substantive, independently-usable data-transfer capability (moving binary files in and out of MongoDB via GridFS), but it currently has no dedicated `TRANSFER-*` (or other) sub-feature ID in `feature-dictionary.md`. The only existing dictionary reference is `QUERY-view-gridfs`, which is scoped to browsing/viewing GridFS content, not the CRUD/transfer operations themselves. GridFS actions are disabled on read-only connections (per commit `KONG-10731`), consistent with the read-only-mode governance behavior documented elsewhere. A new sub-feature ID, `TRANSFER-gridfs-crud`, is proposed pending a dictionary-owner decision (see the matrix row marked PENDING DICTIONARY ADDITION).

## Collection History (undocumented capability — proposed `TRANSFER-collection-history`)

`t3/datacapturerestore/**` implements a per-collection, document-level change-capture and restore capability with no matching sub-feature ID anywhere in `feature-dictionary.md` today (the only related dictionary entries are `GOV-platform-cdc`, which covers the separate 3TL Bridge product's CDC pipeline, and a passing mention of a "Collection History recording option" under `QUERY-multi-update`). Key characteristics, confirmed from source:

- Change tracking at the field level: update, remove, and rename of scalar fields; insert, remove, and rename of array fields; and whole-document changes (`capture/ChangeDataCaptureActionHandler.java`).
- Selective restore of individual documents, not a bulk/all-or-nothing rollback (`restore/RestoreStoredEntitiesMasterExecutor.java`).
- Per-document conflict resolution during restore, offering "apply to all" or "choose for each conflicting document" (`ui/ResolveRestoreConflictsDialog.java`).
- License-gated: disabled entirely on the Free edition, re-enabled with an active paid license (`CollectionHistoryFeatureAvailability.java`).
- Scope is confirmed single-collection, document-level undo/restore — explicitly **not** a full-database or point-in-time backup mechanism.

Because this doesn't fit cleanly into "import/export," it is closer to an audit/undo capability than a transfer format. A new sub-feature ID, `TRANSFER-collection-history`, is proposed pending a decision on which feature area (F-TRANSFER vs. F-GOV vs. a new area) should own it long-term (see the matrix row marked PENDING DICTIONARY ADDITION).

## Capability findings

| Capability ID | Finding | Impact |
| --- | --- | --- |
| IMP-001 | CSV import supports 8 date format variants × 3 separators, which covers most real-world CSV date encoding patterns. | Reduces the need for pre-processing CSV files to normalize date columns before import. |
| IMP-003 | BSON import uses the bundled mongorestore binary, supporting single-collection extraction from full dump archives — not just full-restore. | Enables targeted collection restoration from full backups without restoring everything. |
| IMP-014 | Incremental export with up to 5 historical resume points is a practical pipeline primitive for append-only data feeds. | Enables repeatable partial exports for downstream pipelines without custom scripting. |
| IMP-015 | The data masking standalone tool provides BSON-type-aware masking with dynamic JSON preview — not just column-level redaction, and covers 19 distinct operation types (not 8 as previously documented). | Production-quality masking that handles MongoDB's flexible schema, not just flat tabular data. |
| IMP-016 | Percentage-based numeric masking (add/subtract %) and substring regex masking for strings are unusually granular for a GUI tool. | Enables realistic anonymization that preserves statistical properties — useful for analytics and testing datasets. |
| IMP-017 | In-flight masking during import/export means the original source is never modified by the masking process. | Safe for production source data; masking is applied only to the output stream. |
| IMP-019 | The SQL toolchain supports 6 relational dialects (MySQL, MSSQL, Oracle, PostgreSQL, Sybase, DB2), not 4 as previously documented; Sybase/DB2 are Enterprise-gated and asymmetric (Sybase: no direct SQL-export-wizard target; DB2: SQL Migration tool only). | Broader competitive footprint for Enterprise customers with legacy Sybase/DB2 estates than previously credited. |
| IMP-020 | GridFS file management (upload/download/delete/rename/metadata edit) is a full CRUD surface with no dedicated data-transfer sub-feature ID today. | Undocumented capability gap — GridFS file transfer is a real feature that isn't currently represented in comparison/gap-analysis reports. |
| IMP-021 | Collection History provides per-document change capture and selective restore/undo, license-gated, single-collection scope. | Undocumented audit/undo capability with no current home in the feature dictionary; may be under-credited in competitive comparisons. |

## Constraints and risks

- SQL import/export (IMP-004, IMP-012, IMP-019), data masking (IMP-015 to IMP-017), and task scheduling (IMP-018) all require Pro/Base+ edition — significant capability gaps for Free edition users; Sybase/DB2 SQL support additionally requires Enterprise-tier licensing.
- Incremental export tracks inserts only; updates to existing documents are invisible to the incremental mechanism. Teams using this feature for CDC-like use cases must be aware of this limitation.
- BSON import relies on the bundled mongorestore binary — a version mismatch between the bundled tool and the target MongoDB server version can cause import failures.
- The "overwrite source" data masking mode is irreversible without a backup; Studio 3T does not enforce a pre-masking backup step.
- Excel export is capped by Excel's 1,048,576 row limit; the exact enforcement point (explicit application check vs. implicit Apache POI library behavior) is unverified — no explicit row-guard constant was found in `ExcelWriter.java` — so the "silently truncates without an in-tool warning" claim should be treated as plausible but unconfirmed pending a dedicated POI-behavior check.
- Collection History and GridFS CRUD are both real, license-relevant capabilities (see subsections above) that currently have no sub-feature ID in `feature-dictionary.md` — they are absent from gap-analysis and comparison reports as a structural consequence, not because they don't exist.

## Conclusion

Data import and export is one of Studio 3T's broadest feature areas. CSV, JSON, BSON, SQL (bidirectional, 6 dialects), and cross-collection formats are all covered with format-specific options, and 19 masking operation types across 6 BSON-type categories give data masking real depth. Incremental export and in-flight data masking add operational depth not found in most competing tools. Two additional capabilities — GridFS file CRUD and Collection History (per-document change capture/restore) — are real and substantive but currently lack a home in the feature dictionary; see the dedicated subsections above. The main friction points are the Pro/Base+ (and, for Sybase/DB2, Enterprise) edition gates on SQL, masking, and scheduling, and the insert-only limitation of the incremental export mechanism.
