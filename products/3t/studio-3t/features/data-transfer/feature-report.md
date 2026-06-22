# Feature Report — Studio 3T / Data Import & Export

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [High-level comparison](../../../../../reports/comparisons/high-level-product-comparison.md)

## Scope

This report covers Studio 3T's Import Wizard, Export Wizard, incremental export, and data masking — including the standalone masking tool and in-flight masking during import/export operations.

## Behavioral walkthrough

Studio 3T's Import Wizard supports five source formats: CSV, JSON, BSON/mongodump, SQL databases (MySQL, PostgreSQL, Oracle, SQL Server), and another MongoDB collection. Each format exposes format-specific options — CSV offers full control over delimiters, text qualifiers, date format parsing (8 format variants × 3 separators), empty field handling, and an option to disable nested document creation (the "flat doc" mode). JSON import adds a validation pre-scan option that catches malformed JSON before inserting any documents. BSON import delegates to a bundled mongorestore binary, with archive support and single-collection extraction from a full dump archive.

The Export Wizard mirrors this breadth on the output side: CSV, Excel (.xlsx), JSON, BSON/mongodump, SQL (four database targets), and another MongoDB collection. Export sources can be the entire collection, a view, a specific find/aggregation query result, or selected documents — with the query bar editable inside the Export unit tab so the export scope can be refined without leaving the wizard. Date/time placeholders in output file paths generate unique filenames per run, which is essential for scheduled recurring exports.

Incremental export is a meaningful capability for data pipeline use cases. Studio 3T maintains state across export runs using a tracking field (default: _id). Each subsequent run adds a {$gt: last_seen_value} filter transparently, exporting only new documents. Up to five historical resume points are retained, allowing rollback to an earlier checkpoint. The limitation is explicit in the documentation: incremental export tracks inserts only, not updates to existing documents. This makes it suitable for append-only event streams but not for change-capture of mutable documents.

The data masking feature deserves attention as a first-class tool, not an afterthought. The standalone masking tool supports field-level rules across all BSON types with granular technique options per type: strings can be scrambled, truncated, regex-masked, or replaced; numerics can be shifted by percentage or substituted; dates can be replaced with random or fixed values. The JSON preview updates dynamically as masking rules are configured, giving immediate feedback on what output will look like. Masking can also be applied in-flight during import and export runs, ensuring sensitive data never touches the target without going through the masking rules.

## Capability findings

| Capability ID | Finding | Impact |
| --- | --- | --- |
| IMP-001 | CSV import supports 8 date format variants × 3 separators, which covers most real-world CSV date encoding patterns. | Reduces the need for pre-processing CSV files to normalize date columns before import. |
| IMP-003 | BSON import uses the bundled mongorestore binary, supporting single-collection extraction from full dump archives — not just full-restore. | Enables targeted collection restoration from full backups without restoring everything. |
| IMP-014 | Incremental export with up to 5 historical resume points is a practical pipeline primitive for append-only data feeds. | Enables repeatable partial exports for downstream pipelines without custom scripting. |
| IMP-015 | The data masking standalone tool provides BSON-type-aware masking with dynamic JSON preview — not just column-level redaction. | Production-quality masking that handles MongoDB's flexible schema, not just flat tabular data. |
| IMP-016 | Percentage-based numeric masking (add/subtract %) and substring regex masking for strings are unusually granular for a GUI tool. | Enables realistic anonymization that preserves statistical properties — useful for analytics and testing datasets. |
| IMP-017 | In-flight masking during import/export means the original source is never modified by the masking process. | Safe for production source data; masking is applied only to the output stream. |

## Constraints and risks

- SQL import/export (IMP-004, IMP-012), data masking (IMP-015 to IMP-017), and task scheduling (IMP-018) all require Pro/Base+ edition — significant capability gaps for Free edition users.
- Incremental export tracks inserts only; updates to existing documents are invisible to the incremental mechanism. Teams using this feature for CDC-like use cases must be aware of this limitation.
- BSON import relies on the bundled mongorestore binary — a version mismatch between the bundled tool and the target MongoDB server version can cause import failures.
- The "overwrite source" data masking mode is irreversible without a backup; Studio 3T does not enforce a pre-masking backup step.
- Excel export is capped by Excel's 1,048,576 row limit; collections exceeding this silently truncate without an in-tool warning in the documented behavior.

## Conclusion

Data import and export is one of Studio 3T's broadest feature areas. CSV, JSON, BSON, SQL (bidirectional), and cross-collection formats are all covered with format-specific options. Incremental export and in-flight data masking add operational depth not found in most competing tools. The main friction points are the Pro/Base+ edition gates on SQL, masking, and scheduling, and the insert-only limitation of the incremental export mechanism.
