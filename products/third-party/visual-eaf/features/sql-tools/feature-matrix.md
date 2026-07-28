# Feature Matrix — VisuaLeaf / SQL Tools

## Navigation

- [← Product Report](../../product-report.md)
- [Feature Report](feature-report.md)
- [← Querying Matrix](../querying/feature-matrix.md)
- [← Aggregation Matrix](../aggregation/feature-matrix.md)
- [→ Governance Matrix](../governance/feature-matrix.md)

## Source index

- S1: https://visualeaf.com/features/sql-mode/
- S2: https://visualeaf.com/ (homepage — "SQL Mode" listed under Core Features)

## Capability matrix

| Sub-feature ID | Capability | Status | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| SQL-expressions | SQL SELECT/WHERE/ORDER BY/LIMIT/aggregates | confirmed | "Write familiar SQL SELECT statements to query MongoDB. Use WHERE clauses, ORDER BY, LIMIT, and aggregate functions like COUNT, SUM, and AVG." SQL Helper provides an example library (JOINs, GROUP BY, subqueries, complex conditions) with one-click insertion. Results shown in a grid view with spreadsheet-style sort/filter/edit. | SQL Mode targets MongoDB collections only — it is not a client for VisuaLeaf's other supported database engines (PostgreSQL, MySQL, etc.). Vendor guidance directs users to the Aggregation Pipeline for "advanced transformations," implying SQL Mode has scope limits versus full pipeline authoring. | confirmed | S1 |
| SQL-code-gen | SQL query → MongoDB translation view | confirmed | A "MongoDB translation view" shows the aggregation-pipeline equivalent of the entered SQL query. | Whether this generates driver-language code (Java/Python/Node/etc.), or only the MongoDB pipeline/query shape, is not specified. | confirmed | S1 |
| SQL-join-mapping | SQL JOIN → $lookup mapping | unknown/unverified | The SQL Helper example library includes JOIN syntax, but no visual JOIN-to-$lookup mapping tool (comparable to Studio 3T's dedicated JOIN mapping UI) is documented. | — | unknown/unverified | S1 |
| SQL-query-manager | SQL query manager | unknown/unverified | Not documented specifically for SQL Mode. VisuaLeaf's general Saved Queries feature (QUERY-saved, Basic+) may or may not extend to SQL Mode queries. | — | unknown/unverified | S1 |
| SQL-migration | SQL migration wizard | not supported | No SQL-database-to-MongoDB migration wizard is documented for VisuaLeaf. SQL Mode queries MongoDB via SQL syntax; it does not migrate data from relational sources into MongoDB. | — | not supported | S1 |
| SQL-migration-schema | Auto-map SQL schema to MongoDB schema | not supported | Not documented; no migration wizard exists (see SQL-migration). | — | not supported | S1 |
| SQL-migration-1to1 | 1-to-1 table to collection migration | not supported | Not documented. | — | not supported | S1 |
| SQL-migration-1to-many | 1-to-N relational to embedded document | not supported | Not documented. | — | not supported | S1 |
| SQL-export-field-map | SQL export field mapping modes | unknown/unverified | Not documented for SQL Mode specifically. VisuaLeaf's general SQL INSERT statement export (TRANSFER-export-sql-stmts, in the Data Transfer feature area) is a separate capability from SQL Mode querying. | — | unknown/unverified | S1 |
| SQL-export-relations | SQL export relational structure options | unknown/unverified | Not documented. | — | unknown/unverified | S1 |
| SQL-export-monitor | SQL export live preview | unknown/unverified | Not documented. | — | unknown/unverified | S1 |
| SQL-export-targets | SQL export database targets | unknown/unverified | Not documented for SQL Mode. See TRANSFER-export-sql-stmts for VisuaLeaf's confirmed SQL INSERT statement export capability. | — | unknown/unverified | S1 |
| SQL-reschema | In-place MongoDB schema migration | not supported | Not documented. VisuaLeaf's schema restructuring capability, if any, is not part of SQL Mode. | — | not supported | S1 |

## Feature-level conclusion

### Confirmed strengths

- SQL Mode lets users query MongoDB collections with familiar SQL syntax (SELECT/WHERE/ORDER BY/LIMIT/aggregate functions), lowering the entry barrier for SQL-background users joining a MongoDB team.
- A MongoDB translation view (showing the equivalent aggregation pipeline) helps users learn MongoDB's native query language from SQL, similar in spirit to Studio 3T's SQL→MongoDB code generation.

### Confirmed limitations

- SQL Mode is scoped to querying MongoDB only — it is not a SQL-to-MongoDB migration tool, unlike Studio 3T's F-SQL, which includes a full migration wizard, JOIN→$lookup mapping, and bidirectional relational export.
- The vendor's own documentation directs users to the Aggregation Pipeline for advanced transformations, suggesting SQL Mode is intended for straightforward querying rather than complex data reshaping.

### Open questions / unknowns

- Which VisuaLeaf plan tier (Community/Basic/Professional) includes SQL Mode — not stated on the source pages.
- Whether SQL Mode queries can be saved/organized via the same Saved Queries mechanism as JSON queries.
- Whether a visual JOIN-to-$lookup mapping tool exists beyond the SQL Helper's example snippets.
