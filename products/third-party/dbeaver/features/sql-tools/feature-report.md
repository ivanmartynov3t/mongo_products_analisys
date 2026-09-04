# Feature Report — DBeaver / SQL Tools

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Scope

- Feature name: SQL Tools
- Feature ID: F-SQL (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Product: DBeaver
- Product group: third-party
- Analysis date: 2026-09-04

## Behavioral walkthrough

Where Compass, VisuaLeaf, and Studio 3T all offer a MongoDB-native filter bar / query builder as their primary query surface, DBeaver's primary MongoDB query surface is SQL text run through a "SQL Console and Auto-Completion Engine" — a generic, engine-agnostic editor shared with every relational database DBeaver connects to. MongoDB's own documentation independently confirms this integration, listing DBeaver among the clients supported by its "SQL Interface" (a MongoDB-provided SQL-to-Mongo translation layer, distinct from DBeaver's separate native MongoDB NoSQL driver used for JDBC/BSON access).

This SQL-first design is also the direct cause of several confirmed friction points. A MongoDB Community Hub forum thread documents `MongoConnection.setAutoCommit` errors when using MongoDB's own MongoSQL JDBC driver with DBeaver, because the driver enforces a read-only connection state that conflicts with DBeaver's default auto-commit connection loop. Separately, GitHub issue #23205 shows that native MongoDB method-chain syntax (`db.getCollection(...).find().limit(10)`) throws a `NullPointerException`, because DBeaver's query parser expects relational SQL and cannot handle MongoDB's own native query language.

DBeaver has no SQL migration wizard or SQL-to-MongoDB code generator comparable to Studio 3T's toolchain — the research file's own MongoDB capability comparison table explicitly draws this contrast, crediting Studio 3T alone with a "Full SQL-to-Mongo & Mongo-to-SQL Engine" that handles type mapping, relational un-nesting, index creation, and schema transformation during migration.

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| SQL-expressions | SQL-over-MongoDB is independently confirmed by MongoDB's own documentation, not just the secondary research file. | The strongest-evidenced MongoDB-facing claim for DBeaver in this entire product entry. | MongoDB Docs "Connect from DBeaver - SQL Interface" (S1 Works Cited #28) |
| SQL-migration, SQL-code-gen | No SQL↔MongoDB migration wizard or code-gen tool; confirmed absent by the source's own direct comparison table. | Materially narrower toolchain than Studio 3T for relational-to-document migration scenarios. | Research file's MongoDB Capability Matrix |

## Constraints and risks

- Requires a SQL-to-Mongo translation bridge (MongoDB's own SQL Interface / MongoSQL JDBC driver) in addition to, or instead of, DBeaver's native MongoDB NoSQL driver — the exact relationship between the two connection paths is not fully specified in the source.
- Confirmed integration friction (auto-commit conflicts, native-syntax parser crashes) suggests the SQL bridge is not a seamless drop-in replacement for MongoDB's native query language.

## Interactions and dependencies

- Shares its editor surface with [F-AGG](../aggregation/feature-report.md) (the same JSON-array/text console is used for aggregation authoring) and receives AI-generated SQL from [F-AI](../ai/feature-report.md).
- Depends on [F-CONN](../connectivity/feature-report.md)'s MongoDB connection type, which requires a paid DBeaver tier.

## Conclusions

### Strengths

- Independently confirmed (by MongoDB's own docs) SQL-over-MongoDB integration — the most solidly evidenced MongoDB capability for DBeaver in this repository.
- Inherits DBeaver's broader SQL editor sophistication (schema-aware auto-completion, transaction management, visual explain plans).

### Limitations

- No SQL migration wizard, no SQL-to-MongoDB-driver-language code generation.
- Confirmed integration friction between DBeaver and MongoDB's own SQL JDBC driver (auto-commit conflicts) and between DBeaver's parser and MongoDB's native query syntax (NullPointerException on method chains).

### Unknowns

- Full supported SQL syntax subset against MongoDB (JOIN types, aggregate functions, subqueries).
- Whether the generic relational Visual Query Builder can be used against a MongoDB SQL-Interface connection.
