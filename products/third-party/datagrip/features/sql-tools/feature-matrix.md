# Feature Matrix — DataGrip / SQL Tools

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: DataGrip
- Product group: third-party
- Feature ID: F-SQL (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `sql-tools`
- Analysis date: 2026-09-04
- Version/release context: DataGrip 2025.3–2026.2 line

## Source index

- S1: DataGrip Competitive Analysis Studio 3T (secondary research file), `research/google_research/datagrip-competitive-analysis/DataGrip Competitive Analysis Studio 3T.md`
- S2: SQL for MongoDB | DataGrip Documentation, https://www.jetbrains.com/help/datagrip/sql-for-mongodb.html (S1 Works Cited #22 — JetBrains' own canonical reference for this exact feature)
- S3: DataGrip 2020.3 EAP 3: SQL for MongoDB - The JetBrains Blog, https://blog.jetbrains.com/datagrip/2020/10/22/datagrip-2020-3-eap-3-sql-for-mongodb/ (S1 Works Cited #23 — original feature announcement)
- S4: What's New in DataGrip 2026.2, https://www.jetbrains.com/datagrip/whatsnew/ (S1 Works Cited #5)
- S5: [Design] Cross-DB JOIN UX: console, data source, and syntax discoverability — DBE-26268, https://youtrack.jetbrains.com/projects/DBE/issues/DBE-26268 (S1 Works Cited #6 — JetBrains' own issue tracker)

## Capability matrix (low-level)

This is DataGrip's primary MongoDB query-authoring surface (see [product-report.md](../../product-report.md) for why F-QUERY was not created as a separate folder — the same reasoning DBeaver's entry applied).

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SQL-expressions | SQL expressions | Confirmed | S1: DataGrip's "custom JavaScript-SQL translation layer... allows developers to write standard SQL queries against MongoDB collections," supporting "SELECT queries utilizing WHERE, GROUP BY, HAVING, ORDER BY, LIMIT, OFFSET, INNER JOIN, and LEFT JOIN clauses." Independently corroborated by JetBrains' own "SQL for MongoDB" documentation page (S2), which is the vendor's canonical reference for this exact feature. | Only SELECT-family syntax; SQL aggregate functions (AVG/SUM/MIN/MAX) cannot be used outside explicit GROUP BY blocks, and nested aggregate calls are prohibited. | Unverified (whether the exact clause list has expanded since the version documented) | S1, S2 | Strongest primary-source-backed claim in this feature area — matches the same pattern that made DBeaver's `SQL-expressions` row its strongest citation. |
| SQL-code-gen | Code generation | Confirmed | S1 shows a worked example: a SQL `SELECT ... WHERE ... ORDER BY ... LIMIT` statement is transpiled automatically into `db.users.find({...}, {...}).sort({...}).limit(10)` MongoDB shell syntax, inspectable via a "Show JS Script" context action. This is the origin feature announced in DataGrip 2020.3 EAP 3 (S3) and documented canonically in S2. | Generates MongoDB shell (JavaScript) syntax specifically, not a driver-language (Java/Python/C#/Node.js/PHP) code artifact — see product-report.md constraints for the explicit contrast with Studio 3T's Aggregations-to-Code. | Not planned (no driver-language code-gen claimed anywhere in the source) | S1, S2, S3 | The literal mechanism DataGrip's MongoDB support is built around; two independent primary sources (a dedicated help page and the original announcement blog post) back this claim. |
| SQL-join-mapping | JOIN mapping | Not supported (confirmed absent) | S1: "JOIN statements in SQL for MongoDB are restricted to a single condition within the ON clause using equality operators (= or ==). Subqueries inside JOIN clauses and USING syntax are unsupported." No visual JOIN-condition editor exists — all SQL, including JOINs, is authored as plain text in the SQL console. | Single equality-comparison condition only; even narrower than DBeaver's plain-SQL-text JOIN support (which was itself never confirmed to have a visual mapping editor for MongoDB). | Not planned | S1 | Confirmed-absent by direct statement in the source (not merely a silence-based inference). |
| SQL-migration | SQL migration wizard | Not supported (confirmed absent, per contrast) | S1's side-by-side comparison table row "SQL Engine for MongoDB" credits Studio 3T alone with "Full SQL query translation engine with bi-directional SQL-to-MongoDB data migration tools," explicitly contrasting DataGrip's "Custom SQL-to-JS translation engine (supports SELECT, WHERE, GROUP BY, JOIN)." | — | Not planned | S1 | Same direct-contrast pattern used to confirm DBeaver's `SQL-migration` absence. |
| SQL-federated-query | Federated cross-database query | Confirmed (general cross-relational-database capability); Unverified (MongoDB-specific scope) | S1 describes `dg_cross`, a DuckDB-backed engine letting one SQL query join tables across multiple `$data_source`-qualified connections, with a worked example joining `$postgresql_production` and `$sqlserver_warehouse`. Confirmed as a real, launched feature via DataGrip's own 2026.2 release notes (S4) and a JetBrains-internal YouTrack design issue discussing its console/UX (S5). | The source's own technical walkthrough and worked SQL example name only relational engines (PostgreSQL, SQL Server, MySQL) as join targets. MongoDB is mentioned only in the source's separate "Strategic Opportunities" section as something Studio 3T should build to *match* DataGrip — not as a confirmed existing MongoDB-inclusive `dg_cross` capability. | Unverified (MongoDB scope) | S1, S4, S5 | Direct evidentiary basis for the new dictionary ID `SQL-federated-query` (added 2026-09-04). Important nuance flagged explicitly: do not read this row as "DataGrip can federate-join a MongoDB collection today" — that specific claim is not made anywhere in the source. |

## Feature-level conclusion

### Confirmed strengths

- The SQL-to-MongoDB translation engine (`SQL-expressions`, `SQL-code-gen`) is independently corroborated by two JetBrains primary sources (a dedicated help-center page and the original 2020 feature-announcement blog post) — a stronger evidentiary basis than most claims reviewed elsewhere in this repository's third-party product entries.
- `dg_cross` is a real, shipped, primary-source-confirmed feature (2026.2 release notes) — a genuine architectural differentiator versus every other product compared in this repository, even setting aside the MongoDB-scope question.

### Confirmed limitations

- No SQL migration wizard or SQL-to-MongoDB-driver-language code generation comparable to Studio 3T's toolchain — confirmed absent by the source's own direct comparison table.
- JOIN support against MongoDB is confirmed-absent for anything beyond a single equality condition; no visual JOIN-mapping editor exists at all (SQL, including JOINs, is always authored as text).
- No SQL-based INSERT/UPDATE/DELETE against MongoDB — write operations require native MongoDB shell syntax or cell-by-cell data-grid edits (see product-report.md).

### Open questions / unknowns

- Whether `dg_cross` can include a MongoDB collection as a federated join target — the only worked technical example in the source joins two relational engines.
- Exact SQL syntax subset supported against MongoDB beyond the enumerated clause list (e.g., whether newer DataGrip versions have expanded past SELECT/WHERE/GROUP BY/HAVING/ORDER BY/LIMIT/OFFSET/single-equality JOIN).
