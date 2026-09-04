# Feature Matrix — DBeaver / Data Transfer

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: DBeaver
- Product group: third-party
- Feature ID: F-TRANSFER (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `data-transfer`
- Analysis date: 2026-09-04
- Version/release context: DBeaver 25.x–26.x line

## Source index

- S1: DBeaver Competitive Intelligence Analysis (secondary research file), `research/google_research/dbeaver-competitive-intelligence-analysis/DBeaver Competitive Intelligence Analysis.md`

## Capability matrix (low-level)

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TRANSFER-import-csv | Import CSV | Unverified — per secondary source, no primary citation | S1's MongoDB capability table lists DBeaver's "Bi-Directional Migration Engine" as "CSV/Table Import and Export Wizards," contrasted against Studio 3T's full SQL-to-Mongo engine. No primary source (docs page, release note) is cited for this specific wizard. | — | Unverified | S1 | The claim is plausible (DBeaver is well known generally for CSV import/export) but not tied to a primary citation in this file's Works Cited list for MongoDB specifically. |
| TRANSFER-export-csv | Export CSV | Unverified — per secondary source, no primary citation | Same source row as above. | — | Unverified | S1 | — |
| TRANSFER-import-sql | Import from SQL | Unverified | S1 separately describes generic "File-as-a-Database Drivers" (Parquet, XML, JSON, CSV, Excel) and cross-engine data transfer generally, but does not state that a relational-to-MongoDB import path exists analogous to Studio 3T's SQL migration wizard. | — | Unverified | S1 | Do not conflate DBeaver's generic multi-engine transfer capability with a MongoDB-targeted SQL migration wizard — the source does not claim the latter exists. |
| TRANSFER-export-sql-stmts | Export SQL INSERT | Unverified | Not discussed for MongoDB specifically. | — | Unverified | S1 | — |

## Feature-level conclusion

### Confirmed strengths

- None confirmed to a primary-source standard; DBeaver's CSV/table import-export wizards are asserted by the secondary research file but not traced to a specific vendor documentation page or release note for MongoDB in particular.

### Confirmed limitations

- The source's own comparative framing states Studio 3T offers a "Full SQL-to-Mongo & Mongo-to-SQL Engine" managing "type mappings, relational un-nesting, index creation, and schema transformations during migrations," implicitly contrasting this with DBeaver's narrower CSV/table wizard-based approach — but this is the secondary source's own comparative assertion, not independently confirmed against DBeaver's own documentation.

### Open questions / unknowns

- Whether DBeaver's CSV/table import-export wizards work against MongoDB collections at all, or only against its relational/tabular engines — the source's MongoDB capability table implies the former but does not cite a MongoDB-specific primary source.
- Whether any data masking, incremental export, or custom-transform capability exists for MongoDB data transfer in DBeaver — not discussed in the source and therefore omitted from this matrix.
