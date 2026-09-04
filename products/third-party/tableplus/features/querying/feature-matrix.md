# Feature Matrix — TablePlus / Querying

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: TablePlus
- Product group: third-party
- Feature ID: F-QUERY (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `querying`
- Analysis date: 2026-09-04
- Version/release context: 2026 release line

## Source index

- S1: TablePlus Competitive Intelligence Analysis (secondary research file, no inline per-claim citation markers), `research/google_research/tableplus-competitive-intelligence-analysis/TablePlus Competitive Intelligence Analysis.md`

## Capability matrix (low-level)

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| QUERY-view-table | Table view | Unverified — per secondary source, no primary citation | S1 (Section 5): "It supports browsing document collections in a spreadsheet-like grid or raw JSON list." A spreadsheet/grid rendering of documents is the primary document-browsing mode. | — | Unverified | S1 | Section 5's comparison table row: "Document Browsing: Spreadsheet grid & raw JSON view." |
| QUERY-view-json | JSON/BSON view | Unverified — per secondary source, no primary citation | Same S1 citation as above — raw JSON list is offered as an alternative browsing mode to the grid. | — | Unverified | S1 | — |
| QUERY-view-tree | Tree view | Confirmed absent | S1's comparison table (Section 5) contrasts TablePlus's "Spreadsheet grid & raw JSON view" against Studio 3T's "Tree view, Table view, & JSON view" — tree view is implicitly and explicitly not among TablePlus's two listed modes, and Section 5's prose adds: "TablePlus struggles to cleanly render deeply nested BSON structures," consistent with the absence of a hierarchical tree renderer. | — | Confirmed absent | S1 | Treated as confirmed-absent (not merely unverified) because the comparison table directly enumerates TablePlus's exactly two view modes, omitting tree view by name. |
| QUERY-inline-edit | Inline editing | Unverified — per secondary source, no primary citation | S1 (Sections 4, 5): "Spreadsheet Data Grid: Presents table records and document collections in a grid with inline cell editing." / "Developers can perform inline field edits." | Edits are staged as "pending changes," not applied immediately — see [F-GOV](../governance/feature-matrix.md) (`GOV-staged-commit`). | Unverified | S1 | — |
| QUERY-filter-bar | Filter bar | Unverified — per secondary source, no primary citation | S1 (Section 5): "Simple MQL filters can be submitted through the top-level search bar to query primary document fields." | Described as "simple" filters on "primary document fields" — depth (nested-field filters, operators) not itemized. | Unverified | S1 | — |
| QUERY-doc-dialog | Document dialog | Unverified — per secondary source, no primary citation | S1 (Section 4): "Inspector & Quick Look Panels: Pressing Space expands complex JSON objects, long text strings, or binary data into readable side panels." | Described as a read-oriented "Quick Look" inspector rather than confirmed as a full editable-document dialog. | Unverified | S1 | Mapped cautiously — the source does not confirm this panel supports in-place JSON-schema-validated editing the way `QUERY-doc-dialog` implies elsewhere in this dictionary; flagged here rather than assumed. |
| QUERY-vqb-core | Visual Query Builder core | Unverified — per secondary source, no primary citation, and MongoDB scope unconfirmed | S1 (Section 4): "Multi-Condition Filtering: A visual filter builder that supports stacked field rules (AND/OR) across columns without requiring raw query syntax." | This capability is described in the product's general "Data Editing and Workspace Management" feature list, which covers all engines; Section 5's MongoDB-specific comparison table does not mention a visual filter/query builder for MongoDB, only "Simple MQL filters... through the top-level search bar." | Unverified | S1 | Not marked Confirmed for MongoDB specifically — Section 5's own MongoDB capability table describes only the raw-MQL search bar, suggesting the general-purpose visual filter builder may not extend to MongoDB's document model. Flagged as an open question. |

## Feature-level conclusion

### Confirmed strengths

- None reach this repository's Confirmed bar (no inline per-claim citations in the source).

### Confirmed limitations

- No tree view for document browsing (confirmed absent — Section 5's comparison table names exactly two TablePlus view modes, and its prose states TablePlus "struggles to cleanly render deeply nested BSON structures").

### Open questions / unknowns

- Whether the general-purpose visual, stacked-condition filter builder (`QUERY-vqb-core`) described in Section 4 actually applies to MongoDB queries, or only to relational tables — Section 5's MongoDB-specific capability table describes only a plain top-level MQL search bar, which is a materially thinner capability than a visual AND/OR condition builder.
- Whether projection, sort, skip/limit, or collation controls exist as dedicated UI elements for MongoDB queries, or must be hand-written into the MQL filter — not discussed in the source.
- Whether saved/favorite queries (`QUERY-saved`) apply to MongoDB filters specifically — the source's "Execution History and Snippet Management" feature (Section 4) is described generically across engines.
