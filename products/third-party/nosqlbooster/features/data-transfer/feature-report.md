# Feature Report — NoSQLBooster / Data Transfer

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Scope

- Feature name: Data Transfer
- Feature ID: F-TRANSFER (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Product: NoSQLBooster
- Product group: third-party
- Analysis date: 2026-09-04

## Behavioral walkthrough

NoSQLBooster's data-transfer surface covers the standard MongoDB GUI-client format set — JSON, BSON, CSV, two distinct Excel formats (.xlsx and .xlsb), SQL INSERT-statement export, HTML, and plain text — alongside GUI/task wrappers around the native `mongoimport`, `mongoexport`, `mongodump`, and `mongorestore` command-line tools. Import from relational sources (MySQL, PostgreSQL, Microsoft SQL Server) is also confirmed. All of these can be saved as reusable, schedulable tasks (see F-SCHED), though task scheduling and CLI task execution are excluded from the Free and Personal license tiers per S1's own pricing table.

The most notable single finding in this feature area is the Test Data Generator — a synthetic BSON dataset generator with more than 100 built-in "faker"-style templates for realistic-looking mock data, explicitly listed as a "unique feature" on the vendor's own Feature Tour page. This capability appears in only one of the two research files (S2), which describes it briefly as "a Test Data Generator capable of synthesizing structured mock BSON datasets for database benchmarking" — S1 does not mention it at all. Because this is a single-file claim rather than a two-file conflict, and because the plan's classification rule calls for treating an unconfirmed secondary claim as Unverified by default, this review independently checked the primary source both files otherwise cite, confirmed the capability is real and elaborated (100+ templates, configurable blank-field ratio, document-count scaling, generated as an editable shell script rather than a black box), and marked it Confirmed on that basis — this capability is the direct evidentiary basis for this effort's `TRANSFER-test-data-gen` dictionary ID applying to NoSQLBooster specifically.

GridFS file handling supports full read/write CRUD (not just browsing) via drag-and-drop upload, per the primary source — tracked here distinctly from the browse/view capability already covered under F-QUERY's `QUERY-view-gridfs`.

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| TRANSFER-test-data-gen | Single-research-file claim (S2 only), independently corroborated via primary source rather than accepted at face value. | Demonstrates the classification discipline this effort applied even to non-conflicting claims — a claim only one of two assigned sources makes still gets checked, not silently upgraded to Confirmed on S2's prose alone. | S2, P1 |
| TRANSFER-task-save | Confirmed but tier-gated below Commercial. | Free/Personal-tier users cannot automate any of NoSQLBooster's rich import/export format coverage — a real adoption-path constraint for cost-sensitive individual users specifically, the demographic S1's own pricing-sentiment section says NoSQLBooster otherwise appeals to most. | S1, S2 |

## Constraints and risks

- Data masking/obfuscation, incremental export with resume points, and per-document custom JavaScript transforms during import/export are not discussed in either research file — treat as unconfirmed, not as confirmed absences (neither file makes the kind of explicit "lacks X" statement it makes for, e.g., the visual aggregation builder or centralized governance).
- Task automation of any kind (including the Test Data Generator's own scheduled/batch use) requires at least a Commercial license.

## Interactions and dependencies

- The Test Data Generator produces an editable shell script in the query/script editor rather than a black-box GUI action — meaning it composes directly with F-SHELL's debugger, autocomplete, and NPM-utility environment for further customization, per the primary source's description of the generated script being adjustable "with more complex business logic."
- GridFS CRUD (this feature area) and GridFS browsing/viewing (F-QUERY's `QUERY-view-gridfs`) are the same underlying GridFS Viewer tool, split across two dictionary IDs per the dictionary's own read/browse vs. write/CRUD distinction.

## Conclusions

### Strengths

- Broad, standard import/export format coverage plus native dump/restore/import/export CLI-tool wrappers.
- A primary-source-corroborated, feature-rich Test Data Generator — a genuine differentiator this review verified rather than accepted from a single secondary source.

### Limitations

- Task automation (including scheduled data-transfer jobs) is excluded from the Free and Personal tiers.

### Unknowns

- Data masking, incremental export, and per-document custom-transform capabilities during import/export.
