# Feature Matrix — NoSQLBooster / SQL Tools

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: NoSQLBooster
- Product group: third-party
- Feature ID: F-SQL (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `sql-tools`
- Analysis date: 2026-09-04
- Version/release context: v11.0–v11.1 line

## Source index

- S1: NoSQLBooster Competitive Analysis
- S2: NoSQLBooster Competitive Intelligence Analysis
- P1: nosqlbooster.com/features (primary; fetched directly by this review)

## Capability matrix (low-level)

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SQL-expressions | SQL expressions | Confirmed | S1: "parses relational SQL queries (SELECT, WHERE, GROUP BY, HAVING, ORDER BY, LIMIT)." S2: "SELECT statements... INNER and LEFT equi-JOINs, uncorrelated subqueries... GROUP BY aggregations, HAVING filters, DISTINCT operators, standard string and date functions." P1's edition-comparison page lists a matching row set. | — | N/A | S1, S2, P1 | — |
| SQL-join-mapping | JOIN mapping | Confirmed, text-only (no visual mapping editor) | S1: "supports SQL equi-JOINs and uncorrelated sub-queries across separate collections." S2: "INNER and LEFT equi-JOINs, uncorrelated subqueries." | Plain SQL text syntax; no drag-and-drop visual JOIN-condition editor is described anywhere in either source. | N/A | S1, S2 | Same "confirmed but text-only, no visual editor" characterization this repository applied to DBeaver's and DataGrip's own SQL JOIN support. |
| SQL-code-gen | Code generation | Confirmed | S1: "translates them into MongoDB aggregation pipelines and db.collection.find() queries." S2: "The equivalent generated MongoDB query can be inspected in real time via the integrated console log panel." | — | N/A | S1, S2 | This is the SQL→MQL transpilation itself, distinct from `QUERY-export-lang`'s SQL→driver-language-code generation (also confirmed, in F-QUERY). |
| SQL-reschema | Schema restructuring | Confirmed | S1 (2021 release history): "a GUI Collection Re-Schema Tool using `$convert` aggregation pipelines." P1 elaborates: uses the `$convert` operator and MongoDB's update-via-aggregation-pipeline capability, requires MongoDB Server 4.2+, and provides a `convertFieldType` code template. | Requires MongoDB Server 4.2 or above. | N/A | S1, P1 | Mapped here rather than to F-SCHEMA per this dictionary's existing placement of schema-restructuring capability under SQL Tools (`SQL-reschema`'s definition: "merge, split, rename, type-change operations"), matching this repository's convention. |

## Feature-level conclusion

### Confirmed strengths

- A genuine SQL-to-MongoDB translation engine (SELECT/JOIN/GROUP BY/HAVING/subqueries) with a programmatic `mb.runSQLQuery()` API letting SQL statements be embedded directly inside JavaScript scripts — a distinctive combination not offered the same way by DBeaver or DataGrip (whose SQL surfaces are their *primary* MongoDB access path, not one option alongside a native document workspace and shell).
- A working, MongoDB-4.2+-gated schema-restructuring (re-schema) tool using `$convert`-based aggregation pipelines with a generated, user-editable code template.

### Confirmed limitations

- SQL JOIN authoring is plain-text SQL syntax only, with equi-JOINs and uncorrelated subqueries confirmed but no visual/drag-and-drop JOIN-mapping editor described.
- Neither source file describes a SQL migration wizard (relational schema/data → MongoDB collections) or a Mongo→SQL relational-export target beyond the already-confirmed SQL INSERT-statement text export (tracked under F-TRANSFER's `TRANSFER-export-sql-stmts`) — unlike Studio 3T's full bidirectional SQL migration toolchain.

### Open questions / unknowns

- Whether compound (multi-condition) JOINs are supported, or — as with DataGrip's and Studio 3T's own SQL JOIN implementations documented elsewhere in this repository — only single equality-condition JOINs work; neither file specifies this level of detail.
- Whether the SQL query surface is available identically across all license tiers or is itself gated (S1's pricing table gates multi-language code conversion and CLI/scheduling explicitly, but does not name the SQL engine itself as tier-restricted).
