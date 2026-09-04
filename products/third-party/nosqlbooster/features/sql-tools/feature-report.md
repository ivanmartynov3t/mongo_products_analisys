# Feature Report — NoSQLBooster / SQL Tools

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Scope

- Feature name: SQL Tools
- Feature ID: F-SQL (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Product: NoSQLBooster
- Product group: third-party
- Analysis date: 2026-09-04

## Behavioral walkthrough

NoSQLBooster's SQL engine parses standard relational SQL syntax — `SELECT`, `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`, `LIMIT`, `DISTINCT`, INNER/LEFT equi-JOINs, and uncorrelated subqueries — and transpiles it into native MongoDB `find()` queries or aggregation pipelines. Unlike DBeaver's and DataGrip's SQL surfaces, which are each product's *sole* MongoDB access path (both products lack any native document query workspace, per this repository's own DBeaver and DataGrip product reports), NoSQLBooster's SQL engine is one option alongside a native find/aggregate query surface (F-QUERY), a native shell (F-SHELL), and a Visual Query Builder — it is a convenience/familiarity bridge for SQL-background developers, not the product's only way to query MongoDB. The engine also exposes a programmatic `mb.runSQLQuery()` function, letting a SQL statement be embedded and executed directly inside an otherwise-normal mongosh JavaScript script — a distinctive fusion of the SQL and shell surfaces that neither DBeaver nor DataGrip's more SQL-first architectures replicate the same way.

A separate schema-restructuring tool ("Collection re-schema tool"), first introduced in the 2021 v7.0 release, generates a `$convert`-based aggregation pipeline (using MongoDB's update-via-aggregation-pipeline capability, available since MongoDB 4.2) to convert a field's BSON type across a collection — the vendor's own Feature Tour page frames it explicitly as a code-generation tool: it produces an editable script (with a reusable `convertFieldType` code template) the user can extend with more complex business logic, rather than a one-click black-box operation. This is mapped to `SQL-reschema` rather than to F-SCHEMA, matching this dictionary's own existing placement of schema-restructuring capability under SQL Tools.

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| SQL-expressions / SQL-join-mapping | A genuinely capable SQL dialect (not just `SELECT`/`WHERE`) confirmed across both files, but JOIN authoring is plain-text SQL only, with no visual mapping editor described. | Comparable expressiveness to DataGrip's SQL-to-JS translation layer, but delivered as one authoring option among several rather than the sole MongoDB access path. | S1, S2 |
| SQL-reschema | A working, code-generating schema-restructuring tool with a MongoDB-version prerequisite (4.2+) explicitly documented. | Gives NoSQLBooster a schema-restructuring capability neither DBeaver nor DataGrip is documented as having (both products' F-SCHEMA/F-SQL areas are confirmed to lack native schema-analysis/restructuring surfaces per this repository's other product reports). | S1, P1 |

## Constraints and risks

- Whether the SQL engine or the re-schema tool are themselves gated by license tier is not confirmed by either source file — S1's pricing table names other capabilities (multi-language code conversion, CLI, scheduling) as explicitly gated but is silent on the SQL engine and re-schema tool specifically.
- No SQL migration wizard (relational → MongoDB) or Mongo-to-relational-database export target is described — NoSQLBooster's relational-direction capability stops at plain-text SQL INSERT-statement export (F-TRANSFER) and SQL table import (also F-TRANSFER), not a full bidirectional migration toolchain.

## Interactions and dependencies

- `mb.runSQLQuery()` bridges F-SQL and F-SHELL directly — SQL statements execute inside otherwise-normal JavaScript scripts, meaning the interactive debugger (`SHELL-debugger`) can step through code that includes embedded SQL calls.
- The SQL engine's internal aggregation-pipeline output is not exposed as an editable pipeline in the F-AGG visual sense (which is confirmed absent) — the console log panel shows the generated MongoDB query for inspection, per S2, but this is a read-only preview, not a hand-off into an aggregation editor.

## Conclusions

### Strengths

- A capable SQL-to-MongoDB translation engine plus a script-embeddable `mb.runSQLQuery()` API, and a working, code-generating schema re-schema tool — together a genuinely differentiated F-SQL surface among the third-party products this repository has reviewed to date.

### Limitations

- JOIN authoring is text-only, with no visual mapping editor.
- No SQL migration wizard or full relational-database export target.

### Unknowns

- License-tier gating of the SQL engine and re-schema tool specifically.
- Whether compound (multi-condition) JOINs are supported.
