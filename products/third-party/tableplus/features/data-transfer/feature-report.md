# Feature Report — TablePlus / Data Transfer

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Scope

- Feature name: Data Transfer
- Feature ID: F-TRANSFER (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Product: TablePlus
- Product group: third-party
- Analysis date: 2026-09-04

## Behavioral walkthrough

TablePlus describes three data-mobility mechanisms in its general (cross-engine) feature list: SQL dump import/export, structured CSV/JSON/JSONL export of query results or whole tables, and direct connection-to-connection transfer without an intermediate dump file. All three are described using relational-flavored terminology ("database schemas," "tables") rather than MongoDB-specific terms ("collections," "documents"). Because the source never states explicitly that any of these three mechanisms operates against MongoDB — and one of them (SQL dump) cannot by definition, since it is a relational schema/data format — this feature area is built with a strong scope caveat: general existence of the capability for TablePlus as a whole is fairly clear, but MongoDB-specific applicability is unconfirmed for everything except the one confirmed exclusion (SQL dump).

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| TRANSFER-export-csv / TRANSFER-export-json | CSV/JSON/JSONL export of "query results or entire tables" is described generically. | If it extends to MongoDB (unconfirmed), gives a basic path to move query output into common interchange formats. | S1 Section 9 |
| TRANSFER-export-sql | SQL dump export exists for relational engines. | Not applicable to MongoDB by format definition — confirmed absent for MongoDB specifically. | S1 Section 9 |
| TRANSFER-import-mongo / TRANSFER-export-mongo | Connection-to-connection transfer is described with a database-migration example, not a MongoDB-specific one. | If it extends to MongoDB (unconfirmed), would allow local-to-staging collection migration without an intermediate dump. | S1 Section 9 |

## Constraints and risks

- Every positive finding in this area carries the same MongoDB-scope caveat: the source's language is relational-flavored throughout Section 9, and no sentence in the source explicitly names a MongoDB collection or document as the subject of an import/export/transfer operation.
- No data-masking, field-mapping, type-conversion, or incremental-export capability is discussed for any engine in the source.

## Interactions and dependencies

- If CSV/JSON export does extend to MongoDB, it would most plausibly operate on the grid-based query results described under [F-QUERY](../querying/feature-report.md), since that is TablePlus's only confirmed MongoDB result-rendering surface.

## Conclusions

### Strengths

- A real (if MongoDB-scope-unconfirmed) structured export and connection-to-connection transfer capability exists at the product level.

### Limitations

- SQL dump import/export, TablePlus's most fully-described data-mobility mechanism, is confirmed inapplicable to MongoDB.
- No masking, incremental export, or field-mapping tooling of any kind is discussed for any engine.

### Unknowns

- Whether CSV/JSON/JSONL export and connection-to-connection transfer are actually usable against MongoDB collections, or are described only in the context of TablePlus's relational engines.
