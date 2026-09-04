# Feature Report — NoSQLBooster / Schema

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Scope

- Feature name: Schema
- Feature ID: F-SCHEMA (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Product: NoSQLBooster
- Product group: third-party
- Analysis date: 2026-09-04

## Behavioral walkthrough

Both research files independently confirm NoSQLBooster ships a sampling-based Schema Analyzer — S1 and S2 both reference it specifically while explaining what it *doesn't* do (no ERD, no cross-database visual schema comparison), which is itself useful evidence that the tool exists and does document sampling. The vendor's own Feature Tour page fills in the operational detail neither research file itemizes: users choose a sample mode (random, first, last, or all records) and a sample count (or the whole collection, at the cost of longer analysis time on large collections), and the resulting report shows per-field population probability and per-field type-percentage breakdowns, plus a display of any existing `$jsonSchema` document-validation rule with click-to-highlight field navigation. The report can be exported to Word, PDF, HTML, JSON, TXT, CSV, or a Mongoose.js schema file.

What is confirmed absent, by direct and independent statement in both source files, is any visual Entity-Relationship Diagram (ERD) or drag-and-drop schema-design canvas — S1 lists this under a dedicated "Visual ERD & Schema Design Environment" missing-functionality heading, and S2 names Navicat and DbSchema by name as competitors that do have this. Also notably absent from every source reviewed (including the vendor's own Feature Tour page) is any anomaly/outlier-flagging capability distinct from the bare probability/type-mix display — this stands in direct contrast to Navicat's Schema Analyzer (documented in this repository's Navicat product report), which explicitly does flag outlier documents, and which is the actual evidentiary basis for this effort's `SCHEMA-anomaly-detection` dictionary ID addition. This matrix deliberately does not force that ID onto NoSQLBooster despite the superficial similarity of "sampling-based schema analyzer" between the two products.

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| SCHEMA-sampling / SCHEMA-field-prob / SCHEMA-type-prob | A real three-part sampling analytics implementation, though the "type probabilities" and precise sampling-mode detail come from the primary source rather than either research file's own narrative. | Comparable in breadth to Compass's and Studio 3T's own schema explorers on this specific dimension. | S1, S2, P1 |
| SCHEMA-doc-export | Multi-format export (Word/PDF/HTML/JSON/TXT/CSV/Mongoose.js) confirmed via primary source only. | A genuine documentation-generation strength, useful for handoff/compliance documentation workflows. | P1 |
| SCHEMA-designer-canvas | Confirmed absent, independently, in both research files. | A real, named competitive gap versus Navicat (and, per this repository's other reports, VisuaLeaf). | S1, S2 |

## Constraints and risks

- The Schema Analyzer's sample size vs. accuracy tradeoff is explicitly acknowledged in the primary source ("it may take a long time to finish if the collection has millions of records or thousands of fields") — consistent with both research files' independently-documented UI-freezing complaints on large clusters (see `product-report.md`).
- No anomaly/outlier detection, no value histogram, and no schema-comparison-across-databases capability are confirmed — treat these as genuine gaps, not merely thin evidence, given the specificity of both files' "missing functionality" sections on this exact point.

## Interactions and dependencies

- The Schema Analyzer's field/type metadata is the same metadata the AI Helper can optionally send to its backend model for schema-aware query generation (`AI-schema-aware` in F-AI) — the two features draw on a shared underlying schema-introspection mechanism, per both files' descriptions.
- The separate "Collection re-schema tool" ($convert-based field-type conversion) is tracked under F-SQL's `SQL-reschema`, not under F-SCHEMA, matching the dictionary's own placement of schema-restructuring capability under SQL Tools.

## Conclusions

### Strengths

- A real, multi-dimensional sampling-based Schema Analyzer (probability, type-mix, multi-format export) confirmed across both research files and the primary source.

### Limitations

- No visual ERD/schema-design canvas — confirmed absent by direct, independent statement in both files.
- No anomaly/outlier detection distinct from bare probability display, unlike Navicat's equivalent tool.

### Unknowns

- Value histogram / date-distribution chart support.
- Exact scope of the "document validation" display (whether it supports a full `SCHEMA-verify`-style non-conforming-document workflow or is read-only display only).
