# Feature Matrix — TablePlus / Data Transfer

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: TablePlus
- Product group: third-party
- Feature ID: F-TRANSFER (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `data-transfer`
- Analysis date: 2026-09-04
- Version/release context: 2026 release line

## Source index

- S1: TablePlus Competitive Intelligence Analysis (secondary research file, no inline per-claim citation markers), `research/google_research/tableplus-competitive-intelligence-analysis/TablePlus Competitive Intelligence Analysis.md`

## Scope note: MongoDB applicability is largely unconfirmed

Section 9 ("Import, Export, & Data Mobility") describes TablePlus's data-mobility tooling generically across all supported engines. "SQL Dump Import and Export" is, by name, a relational-only capability with no MongoDB equivalent mentioned. "Structured Data Export" (CSV/JSON/JSONL) and "Connection-to-Connection Transfer" are described without naming a specific engine, and MongoDB query/collection results are a plausible source for a grid-based CSV/JSON export given TablePlus's own grid-based MongoDB browsing (see [F-QUERY](../querying/feature-matrix.md)) — but the source never states this explicitly for MongoDB. Every row below is scored Unverified for MongoDB-specific applicability even where general existence is described.

## Capability matrix (low-level)

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TRANSFER-export-csv | Export CSV | Unverified — per secondary source, no primary citation; MongoDB scope unconfirmed | S1 (Section 9): "Structured Data Export: Exports filtered subsets of query results or entire tables directly into CSV, JSON, or JSON lines (JSONL) formats." | Described generically ("tables"); MongoDB collection/query-result export not named explicitly. | Unverified | S1 | — |
| TRANSFER-export-json | Export JSON | Unverified — per secondary source, no primary citation; MongoDB scope unconfirmed | Same citation as above. | Same as above. | Unverified | S1 | — |
| TRANSFER-export-sql | Export SQL | Confirmed absent for MongoDB (relational-only by definition) | S1 (Section 9): "SQL Dump Import and Export: Exports full database schemas and data to uncompressed or compressed SQL dump files." | SQL dump format is inherently a relational-schema/data format; not applicable to MongoDB's document model. | Confirmed absent (MongoDB scope) | S1 | Marked confirmed-absent for MongoDB specifically, not for TablePlus generally — the capability exists for relational engines. |
| TRANSFER-import-mongo / TRANSFER-export-mongo | Import/export to MongoDB | Unverified — per secondary source, no primary citation; MongoDB scope unconfirmed | S1 (Section 9): "Connection-to-Connection Transfer: Enables direct data transfers between active database connections (e.g., migrating a local development database to a staging server) without writing intermediate dump files to disk." | The worked example given is a database-to-database migration; MongoDB-to-MongoDB (or MongoDB-to-relational) transfer is not explicitly named. | Unverified | S1 | — |
| TRANSFER-export-src | Export source selection | Unverified — per secondary source, no primary citation | S1 (Section 9): export sources described as "filtered subsets of query results or entire tables." | "Tables" wording again leaves collection-level export unconfirmed by name. | Unverified | S1 | — |

## Feature-level conclusion

### Confirmed strengths

- None reach the Confirmed bar for MongoDB specifically — the source describes real data-mobility tooling, but always in relational-flavored language ("tables," "database schemas") without ever naming a MongoDB collection or document export explicitly.

### Confirmed limitations

- SQL dump import/export is, by definition, not applicable to MongoDB's document model — confirmed absent for MongoDB specifically (not a limitation of TablePlus generally, which does support this for its relational connections).

### Open questions / unknowns

- Whether CSV/JSON/JSONL export applies to MongoDB collection or query-result data, given TablePlus's grid-based MongoDB browsing.
- Whether connection-to-connection transfer supports MongoDB-to-MongoDB collection copying.
- No data-masking, incremental-export, or field-mapping capability is discussed anywhere in the source for any engine, MongoDB included.
