# Feature Report — TablePlus / Querying

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Scope

- Feature name: Querying
- Feature ID: F-QUERY (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Product: TablePlus
- Product group: third-party
- Analysis date: 2026-09-04

## Behavioral walkthrough

TablePlus browses MongoDB collections through the same spreadsheet-style data grid it uses for relational tables, with a secondary raw-JSON list view as the alternative. There is no hierarchical tree view — the source is explicit that TablePlus "struggles to cleanly render deeply nested BSON structures" as a consequence. Simple MQL filters are entered through a top-level search bar to narrow results by primary document fields; the source does not describe a dedicated MongoDB filter-condition builder, projection panel, or sort control distinct from this search bar.

Selecting a cell and editing its value stages the change as a "pending" edit (highlighted yellow) rather than writing it immediately — this staged-commit behavior is documented under [F-GOV](../governance/feature-report.md) since it is an operational-safety mechanism, not a query-authoring one. Pressing Space over a cell opens an "Inspector & Quick Look" side panel that expands complex JSON objects, long strings, or binary data for readability — the source frames this as a viewing convenience rather than confirming it also supports schema-validated in-place document editing.

TablePlus's general "Multi-Condition Filtering" visual filter builder (AND/OR stacked rules across columns) is described once, in the product's cross-engine feature list, but is never named again in the MongoDB-specific capability comparison table — which instead describes only the plain MQL search bar. This is treated as an open question rather than assumed parity, since a generic marketing feature list describing "columns" does not clearly establish that the same visual builder understands MongoDB's document/array field model.

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| QUERY-view-table | Spreadsheet grid is the primary document-browsing mode. | Familiar to relational-database users; the source frames this as a weakness for deeply nested BSON. | S1 Section 5 |
| QUERY-view-tree | No tree view exists for MongoDB documents. | A materially thinner document-inspection surface than Compass, VisuaLeaf, or Studio 3T's three-mode viewers. | S1 Section 5 (comparison table) |
| QUERY-filter-bar | Simple MQL filters via a top-level search bar. | Adequate for basic field lookups; no confirmed support for complex nested-field or operator-heavy filters. | S1 Section 5 |
| QUERY-inline-edit | Grid cells support inline editing, staged as pending changes. | Reduces accidental-write risk (see F-GOV) while still supporting quick data fixes. | S1 Sections 4, 5 |

## Constraints and risks

- No confirmed visual query/filter builder specific to MongoDB's document model — the one "visual filter builder" the source describes is presented as a general, cross-engine capability, and the MongoDB-specific capability table describes only a plain search bar.
- No confirmed projection, sort, or pagination controls dedicated to MongoDB queries.
- The source's own framing ("struggles to cleanly render deeply nested BSON structures") is a direct, if secondary-sourced, statement of a real usability limitation for complex documents.

## Interactions and dependencies

- Inline cell edits feed the staged "pending changes" review/commit workflow documented under [F-GOV](../governance/feature-report.md) (`GOV-staged-commit`).
- Document viewing is the only MongoDB-facing surface described in the source besides raw aggregation JSON authoring (see [F-AGG](../aggregation/feature-report.md)) — there is no separate visual query builder, shell, or SQL-translation layer feeding into it (see the product-report.md's list of omitted feature areas).

## Conclusions

### Strengths

- A functional, if basic, grid-and-JSON document browsing and simple-filter querying experience consistent with TablePlus's "fast, minimal" product positioning.

### Limitations

- No tree view (confirmed absent) and no confirmed advanced filter/projection/sort UI for MongoDB specifically.
- The general-purpose visual filter builder's applicability to MongoDB documents is unconfirmed, not assumed.

### Unknowns

- Whether the cross-engine visual filter builder supports MongoDB's array/nested-document field paths.
- Whether saved/favorite MongoDB queries, query history, or export-to-driver-language exist for MongoDB filters specifically.
- Full behavior of the "Inspector & Quick Look" panel — read-only preview vs. editable document dialog.
