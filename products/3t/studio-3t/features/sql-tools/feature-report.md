# Feature Report — Studio 3T / SQL Tools

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [High-level comparison](../../../../../reports/comparisons/high-level-product-comparison.md)

**Last reviewed:** 2026-07-31 — see [research findings](../../../../../research/studio-3t-desktop-review-2026/09-sql-tools-findings.md)

## Scope

This report covers Studio 3T's SQL tooling suite: the SQL Query tool (including joins and code generation), SQL → MongoDB migration, MongoDB → SQL migration, and Reschema. All capabilities in this feature area require Pro/Base or Ultimate edition.

**Scope-mismatch note (flagged by the 2026-07-31 source-code audit, not resolved here):** this feature area, as currently structured in both `feature-dictionary.md` (F-SQL) and this folder, bundles two things that are implemented in entirely separate parts of the codebase and arguably belong to different Feature IDs: (1) the SQL **query** engine — `SQL-expressions`, `SQL-join-mapping`, `SQL-code-gen`, `SQL-query-manager` — an ANTLR-based SQL-to-MongoDB-aggregation-pipeline translator (`t3/utils/mongodb/sql`, `t3/dataman/gui/sqltab`); and (2) the SQL **migration/reschema** toolchain — `SQL-migration*`, `SQL-export-*`, `SQL-reschema` — JDBC-based import/export/mapping wizards (`t3/sqlnosql`, `t3/dataman/gui/sqlimport`, `t3/dataman/gui/sqlexport`, `t3/dataman/gui/reschema`), which is conceptually data transfer (F-TRANSFER), not SQL querying. The audit only re-verified the query-engine sub-features in depth; the migration/export/reschema rows below are left as previously documented (not re-verified in this pass) — that is F-TRANSFER's remit. This scope question is left open for whoever owns `feature-dictionary.md` to resolve; no files have been moved or IDs changed as part of this update.

## Behavioral walkthrough

Studio 3T's SQL Query tool translates SQL syntax into MongoDB aggregation pipelines, enabling SQL-proficient users to query MongoDB without learning MongoDB Query Language. This is **not** a MySQL dialect: per the 2026-07-31 source-code audit, the parser is an ANTLR4-based grammar that is a heavily 3T-modified fork of the public `sqlite-parser` grammar. The supported SQL surface is broad but bounded: SELECT with projection, WHERE with nested field access using dot notation, INNER and LEFT JOIN (both translated to $lookup), GROUP BY / HAVING with aggregate functions (COUNT, SUM, AVG, MIN, MAX, and the previously undocumented STDEV/STDEVP), LIMIT, OFFSET, ORDER BY, LIKE/GLOB/REGEXP with % and _ wildcards and optional ESCAPE, IN (literal list only, not a subquery), BETWEEN, RAND/RANDINT/RANDDOUBLE random-value functions, and BSON type constructors (ObjectId, ISODate, NumberDecimal, MaxKey, MinKey, Symbol, Undefined, NumberLong, etc.). The use of BSON type constructors in WHERE clauses — for example, filtering by ObjectId("...") — is a critical capability that allows SQL queries to express MongoDB-native types without string coercion. Notably absent, and confirmed so by the audit rather than merely undocumented: `CASE/WHEN`, `CAST`, `COLLATE`, `RAISE`, `MATCH`, all subqueries (including `IN (SELECT ...)` and `EXISTS`), `WITH`/CTEs, and compound `SELECT ... UNION/INTERSECT/EXCEPT`.

Joins are implemented via MongoDB's $lookup stage and support INNER JOIN, LEFT JOIN, CROSS JOIN, self-join (via aliases), and multiple chained joins in a single query. There is no visual JOIN-mapping editor for the query tool — joins are authored as plain SQL text (`JOIN ... ON ...`), and only a single equality comparison per JOIN clause is supported; compound AND-ed join conditions throw an error at query time. The Query Code tab generates the equivalent aggregation pipeline in eight target languages (including all three Java driver API generations), making the SQL tool a pipeline generation engine as much as a query tool.

The SQL → MongoDB migration wizard addresses the common enterprise scenario of moving relational data to MongoDB. It allows multiple import units (table or custom SQL query per unit, with JOIN and UNION support at the SQL query level), schema manipulation per unit (rename, reorder, add, remove fields; create nested objects from flat columns; move fields by drag-and-drop), and two relationship mapping modes: one-to-one (embed related table fields as a nested object) and one-to-many (embed as an array of objects). FK auto-detection reduces manual mapping work for standard relational schemas.

The MongoDB → SQL migration wizard goes in the reverse direction with equal depth. Four field mapping types handle the structural mismatch between MongoDB's document model and SQL's flat table model: Column (primitive to column), Object Fields (embedded doc to flat columns), Array Elements to Rows (array to rows), and Array Elements to Columns (array to columns). Four relationship types control how sub-documents and arrays become SQL tables. Live export monitoring, SQL statement preview, and revert capability reduce the risk of irreversible migrations.

Reschema completes the SQL tools picture: it applies in-place schema transformations to existing MongoDB collections (add, delete, rename, reorder, flatten, extract fields and arrays) without requiring a migration script. It is schedulable via the Task Scheduler.

## Capability findings

| Capability ID | Finding | Impact |
| --- | --- | --- |
| SQL-001 | BSON type constructors in SQL WHERE clauses (ObjectId, ISODate, NumberDecimal, etc.) enable type-correct filtering — not just string matching. | Critical for correctness when querying typed MongoDB fields via SQL syntax. |
| SQL-002 | INNER JOIN and LEFT JOIN translate to MongoDB $lookup natively — users get relational join semantics without rewriting queries as aggregation pipelines. Joins are authored as plain SQL text (no visual mapping editor) and are limited to a single equality comparison per JOIN clause. | Significant productivity gain for SQL-proficient users who need to join MongoDB collections, within the single-equality-condition limit. |
| SQL-003 | Code generation from SQL queries exposes the underlying aggregation pipeline in 8 languages — SQL becomes a pipeline authoring shortcut. | Useful learning tool and a bridge from SQL to MongoDB aggregation concepts. |
| SQL-007 | One-to-many relationship mapping in SQL → MongoDB with array content options (objects, scalars, custom) covers the most common relational→document embedding patterns. | Reduces manual post-migration reshaping of imported data. |
| SQL-008 | Four field mapping types (Column, Object Fields, Array→Rows, Array→Columns) in MongoDB → SQL directly address MongoDB's structural polymorphism. | Without these mapping types, arrays and embedded documents would silently drop or corrupt SQL output. |
| SQL-012 | Reschema provides in-place structural transformation without migration scripts — schedulable as a recurring task. | Enables schema evolution as a first-class operational workflow rather than a one-off scripting event. |

## Constraints and risks

- All SQL tools (SQL Query, SQL migration both directions, Reschema) require Pro/Base+ edition — unavailable in Free.
- SQL JOIN performance depends on collection indexes; no automatic join optimization is noted in the documentation.
- SQL → MongoDB one-to-many embedding creates potentially large arrays with no automatic size warning — this can cause MongoDB document size limit (16 MB) violations.
- MongoDB → SQL auto-type detection is based on the last 50 documents; sparse or heterogeneous collections may produce inaccurate SQL type assignments.
- Reschema is an in-place write operation and is irreversible without a backup; Studio 3T does not enforce a pre-operation backup step.
- IBM DB2 and Sybase are MongoDB → SQL export targets only; they are not available as SQL → MongoDB import sources.
- SQL JOIN clauses support only a single equality comparison per join (no compound/AND-ed join conditions); there is no visual JOIN-mapping editor for the query tool — see `SQL-join-mapping` correction in the feature matrix.
- The SQL Query tool does not support CASE/WHEN, CAST, COLLATE, RAISE, MATCH, any subquery form, WITH/CTEs, or compound SELECT (UNION/INTERSECT/EXCEPT) — treat these as confirmed absent, not merely undocumented, when scoping customer questions or comparisons.

## Stability

The 2026-07-31 source-code audit found the SQL query engine has been stable for at least the last 24 months: no commits touched the SQL grammar files (`SQLiteParser.g4`/`SQLiteLexer.g4`) in that window, and of the ~27 commits touching the relevant source tree, only a targeted NPE bugfix (`KONG-11118`) and a cosmetic removal of a stale "Pro-edition" label suffix (`KONG-10223`, not an actual licensing change) were user-facing. No changelog entries in the same window announced new SQL Query expressions, functions, or join behavior — release-note activity in this window was entirely on the migration side (virtual-column handling, array preview limits, a dialog fix) plus one connection-storage improvement (local file-based connection save/load) applicable to SQL connections generally.

## Conclusion

SQL Tools is Studio 3T's most distinctive feature cluster relative to competing MongoDB GUIs. The SQL Query tool with BSON type constructors and JOIN support, the bidirectional migration wizards with relationship mapping, and Reschema together address the full lifecycle of SQL-to-MongoDB and MongoDB-to-SQL data movement. The entire feature area is behind the Pro/Base+ paywall, but for teams that need it, there is no close competitor in the GUI tool space.
