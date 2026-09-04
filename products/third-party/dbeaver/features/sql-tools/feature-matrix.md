# Feature Matrix — DBeaver / SQL Tools

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: DBeaver
- Product group: third-party
- Feature ID: F-SQL (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `sql-tools`
- Analysis date: 2026-09-04
- Version/release context: DBeaver 25.x–26.x line

## Source index

- S1: DBeaver Competitive Intelligence Analysis (secondary research file), `research/google_research/dbeaver-competitive-intelligence-analysis/DBeaver Competitive Intelligence Analysis.md`
- S2: Connect from DBeaver - SQL Interface - MongoDB Docs, https://www.mongodb.com/docs/sql-interface/dbeaver/connect/ (S1 Works Cited #28 — MongoDB's own documentation of DBeaver as a SQL Interface client)
- S3: DBeaver: MongoDB JDBC Driver returns error: com.mongodb.jdbc.MongoConnection.setAutoCommit - MongoDB Community Hub, https://www.mongodb.com/community/forums/t/dbeaver-mongodb-jdbc-driver-returns-error-com-mongodb-jdbc-mongoconnection-setautocommit/277465 (S1 Works Cited #34)
- S4: Mongo limit native query · Issue #23205 - GitHub, https://github.com/dbeaver/dbeaver/issues/23205 (S1 Works Cited #11)

## Capability matrix (low-level)

This is DBeaver's primary MongoDB query-authoring surface (see [product-report.md](../../product-report.md) for why F-QUERY was not created as a separate folder).

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SQL-expressions | SQL expressions | Confirmed | S1's MongoDB capability table lists DBeaver's "Primary Database Paradigm" as "SQL-First over MongoDB / Basic Shell," via a "SQL Console and Auto-Completion Engine" described as a "context-aware code completion engine that analyzes schema metadata to prioritize foreign key joins, multi-line execution variable bindings, transaction management, visual explain plans, and inline ORDER BY syntax parsing." Independently confirmed by MongoDB's own documentation, which lists DBeaver as a supported "SQL Interface" client. | Requires MongoDB's SQL Interface / a SQL-to-Mongo JDBC bridge (e.g., MongoDB's own MongoSQL JDBC driver, per S3) — not DBeaver's native MongoDB NoSQL driver alone. | Unverified (exact SQL syntax subset supported) | S1, S2 | Strongest primary-source-backed claim in this feature area: MongoDB's own docs (S2) independently corroborate DBeaver's SQL-over-MongoDB integration. |
| SQL-join-mapping | JOIN mapping | Unverified | S1 separately describes a generic "Visual Query Builder (VQB): Drag-and-drop builder enabling users to construct complex SQL join trees" for DBeaver, but does not confirm this VQB is usable against MongoDB connections specifically (as opposed to relational engines only). | — | Unverified | S1 | Do not conflate DBeaver's generic relational VQB with a MongoDB-$lookup-mapping capability — the source does not make that connection explicitly. |
| SQL-migration | SQL migration wizard | Not supported (confirmed absent, per contrast) | S1's MongoDB capability table row "Bi-Directional Migration Engine" lists DBeaver as "CSV/Table Import and Export Wizards" only, explicitly contrasted with Studio 3T's "Full SQL-to-Mongo & Mongo-to-SQL Engine ... manages type mappings, relational un-nesting, index creation, and schema transformations during migrations." | — | Not planned | S1 | Confirmed-absent by direct contrast in the source's own comparison table. |
| SQL-code-gen | Code generation | Not supported (confirmed absent, per contrast) | Same comparison logic as SQL-migration — no MongoDB-query-from-SQL code generation is claimed for DBeaver anywhere in the source. | — | Not planned | S1 | — |

## Feature-level conclusion

### Confirmed strengths

- DBeaver's SQL-over-MongoDB capability is the one MongoDB-facing claim in this entire research file independently corroborated by MongoDB's own official documentation (S2), not just the secondary competitive-intelligence write-up — a materially stronger evidentiary basis than most other claims in this product's coverage.
- Generic SQL editor features (context-aware auto-completion prioritizing FK joins, transaction management, visual explain plans) are inherited by the MongoDB SQL Console from DBeaver's broader relational tooling.

### Confirmed limitations

- No SQL migration wizard or SQL-to-Mongo code generation comparable to Studio 3T's toolchain — confirmed absent by the source's own direct product-comparison table.
- A specific engine-level bug (GitHub #23205) shows DBeaver's query parser expects relational SQL syntax and throws a `NullPointerException` on native MongoDB method-chain queries — direct evidence of the SQL-first architecture's friction with MongoDB's native query model.
- A MongoDB Community Hub forum thread (S3) documents integration failures between DBeaver and MongoDB's own MongoSQL JDBC driver (`MongoConnection.setAutoCommit` exceptions), because the driver enforces a read-only state that conflicts with DBeaver's default auto-commit connection loop.

### Open questions / unknowns

- Exact SQL syntax subset supported against MongoDB (which JOIN types, aggregate functions, subquery forms).
- Whether the generic relational Visual Query Builder is usable against a MongoDB SQL-Interface connection.
