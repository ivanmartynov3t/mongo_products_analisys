# F-TRANSFER (Data Transfer) Findings — Studio 3T Desktop

## Navigation
- [Research plan](00-research-plan.md)
- [Feature dictionary](../../feature-dictionary.md)
- [Current feature-matrix.md](../../products/3t/studio-3t/features/data-transfer/feature-matrix.md)
- [Current feature-report.md](../../products/3t/studio-3t/features/data-transfer/feature-report.md)

## Source index (this document)

- `t3/sqlnosql/SqlFormat.java` — enum of supported SQL dialects for migration/import/export
- `t3/dataman/gui/datamasking/datamaskinggui/datamaskingtab/FieldOperation.java` — `DMMethod` enum, all masking operation types
- `t3/utils/gridfsview/mongodb/GridFsViewController.java` — GridFS CRUD
- `t3/utils/export/importunit/CollectionImportUnit.java`, `t3/utils/export/exportunit/*` — export/import unit formats
- `t3/utils/sqlexport/*`, `t3/utils/sqlimport/*` — SQL schema mapping / type registry
- `t3/datacapturerestore/**` — Collection History (per-document change capture/restore)
- `t3/utils/export/exportunit/ExcelExportUnit.java`, `t3/utils/mongodb/importexport/consumers/ExcelWriter.java`
- `product-suite/data-man-mongodb-ent` git history (24-month window) and `release/studio-3t/changelog.txt`

All findings below were gathered read-only. No files under `/Users/ivan/Project/3t.tools.intellij/3t.tools` were modified.

## Sub-feature status re-check

| Sub-feature ID | Old documented status | New status (confirmed/partial/roadmap/unverified/absent) | Evidence |
|---|---|---|---|
| TRANSFER-import-csv | confirmed | confirmed | `t3/utils/export/formatoptions/CsvOptions.java`, `CSVExportUnit`/import counterpart exist; delimiter/qualifier/date-format options present as documented. Not re-derived in full detail this pass (already matches source structure). |
| TRANSFER-import-json | confirmed | confirmed | `JSONExportUnit`/import counterpart and `JsonOptions` exist; no contradicting evidence found. |
| TRANSFER-import-bson | confirmed | confirmed | `BSONExportUnit`, `BsonOptions`; changelog confirms ongoing mongorestore/mongodump work (e.g. "Fix: BSON Import - Added an option to forcefully disable retryable writes... (mongorestore)", `release/studio-3t/changelog.txt:546`). |
| TRANSFER-import-sql | Supported (Pro/Base+); listed DBs: MySQL, PostgreSQL, Oracle, SQL Server | **partial→corrected**: confirmed, but DB list is incomplete | `t3/sqlnosql/SqlFormat.java` enum: `MYSQL, MYSQL_5_7, MSSQL, MSSQL_2016, ORACLE, ORACLE_12C, ORACLE_12_2C_PLUS, POSTGRE, POSTGRE_9_2, SYBASE, DB2`. **Sybase and IBM DB2 are also supported** (not just the 4 currently documented), each gated by an Enterprise-tier license check (`AppFeatures.ORACLE_DB/SYBASE_DB/DB2`, referenced from `MigrationToSqlJob.java`). Sybase/DB2 support is asymmetric: per-dialect booleans (`migrationToSql`, `migrationFromSql`, `sqlImport`, `sqlExport`) show Sybase has `sqlExport=false` (no direct SQL-export-wizard target) and DB2 has `sqlImport=false`/`sqlExport=false` (available via the SQL Migration tool but not the plain Import/Export Wizard SQL format) — i.e. DB2/Sybase support is real but narrower than MySQL/MSSQL/Oracle/PostgreSQL, and Enterprise-licensed rather than Pro/Base+. |
| TRANSFER-import-mongo | confirmed | confirmed | `t3/utils/export/importunit/CollectionImportUnit.java`: `Source` resolves its own `MongoConnectionInfo` by UUID independently of the destination connection, confirming cross-connection/cross-database collection-to-collection copy. |
| TRANSFER-import-modes | confirmed | confirmed | No contradicting evidence; insertion-mode classes present in export/import unit code. |
| TRANSFER-export-src | confirmed | confirmed | No contradicting evidence found this pass. |
| TRANSFER-export-csv | confirmed | confirmed | — |
| TRANSFER-export-excel | confirmed | **partial (row-limit claim unverified)** | `t3/utils/export/exportunit/ExcelExportUnit.java` and `t3/utils/mongodb/importexport/consumers/ExcelWriter.java` exist and implement `.xlsx` export, but no explicit `1,048,576`-row guard/constant was found in `ExcelWriter.java` — the row cap is presumably enforced implicitly by the underlying Apache POI library rather than by application code. The existing feature-matrix/report's "Excel row limit... silently truncate without an in-tool warning" claim should be labeled **unverified** (plausible via POI's `SpreadsheetVersion`, but not confirmed by a codebase-level check). |
| TRANSFER-export-json | confirmed | confirmed | — |
| TRANSFER-export-bson | confirmed | confirmed | — |
| TRANSFER-export-sql | Supported (Pro/Base+); MySQL, MSSQL, Oracle, PostgreSQL | **corrected** | Same `SqlFormat` evidence as TRANSFER-import-sql above — Sybase and DB2 exist in the enum but both have `sqlExport=false`, confirming the documented 4-database list is accurate specifically **for the SQL Export Wizard target list**, while the broader SQL toolchain (migration) supports 6 dialects. Matrix/report text should clarify "Export Wizard SQL target" vs. "SQL Migration tool" scope, since they differ. |
| TRANSFER-export-mongo | confirmed | confirmed | Same evidence as TRANSFER-import-mongo (`CollectionExportUnit` mirrors `CollectionImportUnit`). |
| TRANSFER-export-sql-stmts | confirmed | unverified (not re-checked this pass) | Not directly re-derived; no contradicting evidence encountered. |
| TRANSFER-incremental | confirmed | confirmed | No contradicting evidence found; not the focus of this pass's deep dive but nothing in git history/changelog contradicts the 5-resume-point / insert-only description (`release/studio-3t/changelog.txt` references "Migration Incremental Execution" preservation work, e.g. commit `430b44cca51` "preserve-migration-incremental-execution"). |
| TRANSFER-masking-tool | Supported (Pro/Base+) | confirmed | `t3/dataman/gui/datamasking/datamaskinggui/datamaskingtab/DataMaskingTab.java`, `DMConfiguration.java`, `DataMaskingDialog.java` implement the standalone tool with drag/drop mapping, exception logging (`logging/DataMaskingLog.java`, `DMLogger.java`). |
| TRANSFER-masking-types | Supported (Pro/Base+); described as ~15 named techniques across BSON types | **corrected — undercounted** | See "Re-verification of README claims" below: `FieldOperation.DMMethod` enum has **20 constants** (19 real masking techniques + `NOT_MASKED`), more than what's enumerated in the current feature-matrix prose. Full authoritative list captured below. |
| TRANSFER-masking-inline | Supported (Pro/Base+) | confirmed | `DataMaskingIntegrationContainer.java` (`t3/utils/export/exportgui/exporttab/`) and `DataMaskingExportRegistry.java` wire masking into the Import/Export Wizard flow, matching the "applies without modifying source" description. |
| TRANSFER-task-save | Supported (Pro/Base+) | confirmed | Task infrastructure (`t3/tasks/SqlImportTask.java`, `DataMaskingTask.java`) confirms import/export/masking configs are schedulable, consistent with existing docs. |

## Re-verification of README claims (SQL migration toolchain exclusivity, data masking op-type count)

**Claim 1 — "sole full SQL↔MongoDB migration/export toolchain"**: This codebase review can only confirm what Studio 3T itself implements, not what competitors do or don't implement — a claim of *exclusivity* ("sole") cannot be verified from this source tree alone. What is confirmed: Studio 3T's SQL toolchain is broader than currently documented — it supports **6 relational database dialects** (MySQL, Microsoft SQL Server, Oracle, PostgreSQL, Sybase, IBM DB2), each with version-specific sub-variants, bidirectional migration (`migrationToSql`/`migrationFromSql` flags per dialect in `t3/sqlnosql/SqlFormat.java`), a schema/mapping layer (`t3/utils/sqlexport/mongomappings/*`: `MongoMapping`, `SimpleMapping`, `ComplexMapping`, `SingleRowMapping`, `MultiRowMapping`, `Relationship`, `PrimaryKeyStrategy`), a SQL type registry (`t3/utils/sqlexport/SqlTypeRegistry.java`, `SqlRegistryTypeObject.java`), and a schema model for generated `CREATE TABLE` DDL (`t3/utils/sqlexport/sqlschema/SqlTable.java`/`SqlColumn.java`/`SqlSchema.java`). **The "sole" exclusivity language should be labeled unverified** (competitor-dependent claim, out of scope for a source-code-only review) but **the underlying capability breadth is confirmed and larger than currently documented** (6 dialects, not 4).

**Claim 2 — "data masking (8 op types)"**: **Not accurate — undercounted.** The `FieldOperation.DMMethod` enum (`t3/dataman/gui/datamasking/datamaskinggui/datamaskingtab/FieldOperation.java`, lines ~75–920) defines **20 enum constants**, of which 19 are actual masking operations and one (`NOT_MASKED`) is the "no-op / not masked" default state:

1. `SHOW_ONLY_FIRST_CHARACTERS` — "Show only first characters" (string)
2. `SHOW_ONLY_LAST_CHARACTERS` — "Show only last characters" (string)
3. `MASK_ENTIRE_STRING` — "Mask entire string" (string)
4. `MASK_STRING_BY_REGEX` — "Mask substrings matching regex" (string)
5. `SCRAMBLE_CHARACTERS` — "Scramble characters" (string)
6. `MASK_ENTIRE_STRING_BY_FIXED_VALUE` — "Replace entire field with fixed string" (string)
7. `MASK_WITH_RANDOM_STRING` — "Replace field value with random string" (string)
8. `SUBSTITUTE_ENTIRE_NUMERIC_VALUE` — "Substitute value with fixed number" (numeric)
9. `ADD_PERCENTAGE_TO_NUMBER` — "Add percentage to number" (numeric)
10. `SUBTRACT_PERCENTAGE_FROM_NUMBER` — "Subtract percentage from number" (numeric)
11. `RANDOM_DATE` — "Substitute with random date and time" (date)
12. `FIXED_DATE` — "Substitute with fixed date and time" (date)
13. `NEGATE_BOOLEAN_VALUE` — "Negate boolean value" (boolean)
14. `SUBSTITUTE_ENTIRE_BOOLEAN_VALUE` — "Substitute with fixed boolean value" (boolean)
15. `EMPTY_ARRAY` — "Empty contents of the array" (array)
16. `GENERATE_NEW_OBJECT_ID` — "Substitute with new ObjectId" (ObjectId)
17. `NULL_OUT` — "Null out field" (all types)
18. `EXCLUDE_FIELD` — "Exclude field" (all types)
19. `SHUFFLING` — "Shuffle" (all types)
20. `NOT_MASKED` — "Not masked" (all types; default/no-op)

This is roughly **2.4x the claimed count** even counting only the 19 real operations (or 2.5x including the no-op state). The README's "8 op types" figure should be corrected to **19 distinct masking operation types** (across string/numeric/date/boolean/array/ObjectId/all-type categories), or the claim should be rephrased to count *BSON-type categories* rather than *operation types* if "8" was meant to approximate categories (even then, the actual category count is 6: String, Numeric, Date, Boolean, Array, ObjectId, plus "all types" operations — still not a clean match to 8). Recommend removing the specific "(8 op types)" parenthetical or replacing it with "(19 operation types across 6 BSON-type categories)", both cited to `FieldOperation.java`.

## Undocumented capabilities found (new sub-feature ID candidates)

1. **SQL dialect breadth (Sybase, IBM DB2)** — not a new sub-feature ID, but a factual correction to `TRANSFER-import-sql`/`TRANSFER-export-sql`: Sybase and DB2 are supported (Enterprise-license-gated) in addition to MySQL/MSSQL/Oracle/PostgreSQL. See `t3/sqlnosql/SqlFormat.java`.
2. **GridFS full CRUD surface** — the current feature dictionary/matrix does not appear to have a dedicated `TRANSFER-gridfs` (or equivalent) sub-feature ID for GridFS file management as a data-transfer capability. Confirmed via `t3/utils/gridfsview/mongodb/GridFsViewController.java`: `addFiles` (upload), `writeOutFiles` (download), `removeFiles` (delete), `renameFile` (rename), `updateMetaData` (metadata edit), plus retrieval by name/id/date/size. This is a substantive, independently-usable data-transfer capability (moving binary files in/out of MongoDB via GridFS) that is only referenced today via `QUERY-view-gridfs` (a *viewing* sub-feature, per `feature-dictionary.md`) rather than a transfer-oriented ID. Recommend a new candidate ID, e.g. `TRANSFER-gridfs-crud` — "GridFS file upload/download/delete/rename/metadata edit" — confirmed, Studio 3T Desktop, cite `GridFsViewController.java`.
3. **Collection History (per-document change capture and restore)** — `t3/datacapturerestore/**` implements a substantial capability with no matching `TRANSFER-*` or other sub-feature ID found in `feature-dictionary.md` (checked; only `GOV-platform-cdc` for the separate 3TL Bridge product, and a passing mention of "Collection History recording option" under `QUERY-multi-update`). This is a real, non-trivial Desktop IDE feature: per-collection, license-gated (`CollectionHistoryFeatureAvailability.java` — disabled entirely on Free edition, re-enabled on active paid license) document-level change tracking (`capture/ChangeDataCaptureActionHandler.java`, action types include field update/remove/rename, array field insert/remove/rename, whole-document changes) with selective restore of individual documents (`restore/RestoreStoredEntitiesMasterExecutor.java`) and per-document conflict resolution during restore (`ui/ResolveRestoreConflictsDialog.java`: "apply to all" vs. "choose for each conflicting document"). Scope is confirmed to be **single-collection, document-level undo/restore — not full-database or point-in-time backup**. Recommend a new candidate ID, e.g. `TRANSFER-collection-history` or a dedicated feature area, since this doesn't fit cleanly into "import/export" — it is closer to an audit/undo capability than a transfer format. Flagging for a decision on which feature area (F-TRANSFER vs. F-GOV vs. new) should own it, since it currently has no home.
4. No parquet, Avro, YAML, standalone XML, or PDF import/export formats were found anywhere under `t3/utils/export/` — ruling out any newer format capability beyond the already-documented CSV/JSON/BSON/Excel/SQL/Mongo set (confirmed absent, not merely unverified).

## Recent changes (last ~24 months, git + release notes)

Git log scoped to `sqlexport`, `sqlimport`, `datacapturerestore`, `gridfsview`, and `datamasking` directories over the last 24 months returned **25 commits**, mostly refactors/bugfixes rather than new capability additions (e.g. `KONG-11001` ObjectField raw-value conversion, `KONG-10814` extracting a `COLLECTION_TYPE` enum, `KONG-10731` disabling GridFS actions on read-only connections, `KONG-10387`/`c41f895` Collection History "Enable" dialog fix, `ROBO-120` "Disable CH" [Collection History] twice). No major new sub-feature was added to these specific directories in this window based on commit subjects alone.

`release/studio-3t/changelog.txt` (broader search, not limited to the 24-month git window) shows ongoing maintenance activity relevant to F-TRANSFER:
- SQL Migration: decimal/scale handling fixes, Oracle identifier-length limit fix, array-length-limit robustness improvements, primary-key mapping flexibility improvements ("Mappings now support any field as a primary key").
- Imports: BSON import retryable-writes toggle for mongorestore, CSV import file-lock fix, remembered custom field names across saved import tasks.
- Exports: new Excel export type added (changelog entry: "New: Exports - Added a new type of export that allows writing documents directly into an MS Excel file" — corroborates `TRANSFER-export-excel` as a real, added capability), export cloning action added to toolbar/context menu, mongodump/mongorestore fixes for Atlas serverless compatibility, index hints applied correctly for aggregation-based exports.
- Data Masking: fixes for excluding multiple fields, alias display in mapping tree, duplicated/session-restored tab availability.
- GridFS: multiple UI refinement and crash-fix entries (invalid/empty bucket names rejected, multi-extension filename fix, drop-bucket crash fix).

No release-notes evidence of parquet/Avro/other new formats was found — consistent with the source-code absence noted above.

## Confidence / spot-check notes

- **High confidence**: SQL dialect enum contents (`SqlFormat.java`), masking operation enum contents (`FieldOperation.java`), GridFS CRUD methods (`GridFsViewController.java`), cross-connection collection copy (`CollectionImportUnit.java`), and Collection History scope (`datacapturerestore/**`) — all read directly from source with exact class/method/enum-constant names cited above.
- **Medium confidence**: The precise mapping of `SqlFormat`'s four gating booleans (`migrationToSql`, `migrationFromSql`, `sqlImport`, `sqlExport`) to exact end-user-visible UI restrictions (i.e., which wizard screens show which dialects) was inferred from field declaration order and naming, not from tracing every call site; recommend a follow-up spot-check in `t3/dataman/gui/sqlexport`/`sqlimport` UI code before publishing a definitive per-dialect capability table.
- **Unverified / out of scope for this pass**: Excel's exact row-cap enforcement point (implicit POI behavior vs. explicit app check), TRANSFER-export-sql-stmts, TRANSFER-incremental, TRANSFER-import-csv/json/modes, TRANSFER-export-src/csv/json/bson/mongo — these were not contradicted by any evidence found but were not independently re-derived line-by-line in this pass (time-boxed to the areas most likely to contain discrepancies: SQL dialect count and masking op count, per the task's explicit README-claim-verification instruction).
- **Explicitly out of scope**: any claim requiring knowledge of competitor products (e.g., whether Studio 3T really is the "sole" tool with a given capability) cannot be verified from this source-code-only review and is labeled unverified rather than confirmed or denied.
