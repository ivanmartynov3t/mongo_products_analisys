# VisuaLeaf — SQL Tools Feature Report

## Summary

VisuaLeaf's SQL Mode lets users query MongoDB collections using SQL syntax — SELECT, WHERE, ORDER BY, LIMIT, and aggregate functions (COUNT, SUM, AVG) — with a SQL Helper example library covering JOINs, GROUP BY, subqueries, and complex conditions. Results display in a spreadsheet-style grid, and a MongoDB translation view shows the equivalent aggregation pipeline. This was previously an unresolved gap in this repository (flagged as "referenced in Open In context menu but no documentation found" in the Querying feature report); it is now confirmed to exist as a documented Core Feature, though its plan-tier requirement remains unstated.

Unlike Studio 3T's F-SQL, which is a full SQL↔MongoDB migration toolchain (migration wizard, JOIN→$lookup mapping, schema restructuring, bidirectional relational export), VisuaLeaf's SQL Mode is a query-only capability against MongoDB — it does not migrate data from or export data to external relational databases as part of this feature (VisuaLeaf's separate SQL INSERT statement export, TRANSFER-export-sql-stmts, lives in the Data Transfer feature area, not here).

---

## Strengths

- **Familiar SQL syntax over MongoDB:** SELECT/WHERE/ORDER BY/LIMIT plus COUNT/SUM/AVG aggregates lower the barrier for SQL-background analysts and developers.
- **MongoDB translation view:** Shows the equivalent aggregation pipeline for an entered SQL query — useful both as a migration aid and a way to learn MongoDB's native query language.
- **SQL Helper example library:** One-click insertion of JOIN, GROUP BY, subquery, and complex-condition examples reduces the learning curve for advanced SQL-over-Mongo patterns.

---

## Limitations / Gaps

- **No SQL migration wizard:** VisuaLeaf does not import data from external relational databases into MongoDB via SQL Mode (contrast with Studio 3T's SQL-migration).
- **No visual JOIN→$lookup mapping tool:** JOIN support appears to be SQL-syntax-level (via SQL Helper examples) rather than a dedicated visual mapping UI.
- **Plan tier unspecified:** Neither the SQL Mode feature page nor the pricing page states which plan (Community/Basic/Professional) includes SQL Mode.
- **Vendor-flagged scope limit:** The source page directs users to the Aggregation Pipeline for "advanced transformations," implying SQL Mode is not intended for complex data reshaping.

---

## Comparison Notes (vs MongoDB Compass baseline)

| Aspect | VisuaLeaf | MongoDB Compass |
|---|---|---|
| SQL query syntax over MongoDB | **confirmed** (SELECT/WHERE/ORDER BY/LIMIT/aggregates) | not available |
| SQL → MongoDB translation view | **confirmed** | not available |
| SQL migration wizard (relational → MongoDB) | not supported | not available |
| JOIN → $lookup visual mapping | unknown/unverified | not available |
| SQL export (relational target) | not part of SQL Mode (see TRANSFER-export-sql-stmts) | not available |

---

## Navigation

- [← Product Report](../../product-report.md)
- [Feature Matrix](feature-matrix.md)
- [← Querying](../querying/feature-report.md)
- [← Aggregation](../aggregation/feature-report.md)
- [→ Security & Governance](../governance/feature-report.md)
