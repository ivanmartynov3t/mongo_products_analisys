# Feature Matrix — NoSQLBooster / Schema

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: NoSQLBooster
- Product group: third-party
- Feature ID: F-SCHEMA (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `schema`
- Analysis date: 2026-09-04
- Version/release context: v11.0–v11.1 line

## Source index

- S1: NoSQLBooster Competitive Analysis
- S2: NoSQLBooster Competitive Intelligence Analysis
- P1: nosqlbooster.com/features (primary; fetched directly by this review)

## Capability matrix (low-level)

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SCHEMA-sampling | Sampling config | Confirmed | S1 (Missing functionality section): "its Schema Analyzer evaluates collection structures via document sampling." S2 (Missing Functionality section): "a sampling-based text schema analyzer." P1 adds configuration detail: "sampled(random, first, last) N or all records." | — | N/A | S1, S2, P1 | — |
| SCHEMA-field-prob | Field probability | Confirmed | P1: "The document shows the probability of sampled objects" — corroborates S1/S2's general "structural analysis"/"document sampling" claims with the specific probability metric. | — | N/A | S1, S2 (general), P1 (specific) | — |
| SCHEMA-type-prob | Type probabilities | Confirmed | P1: "different types of percentages" shown per field. | — | N/A | P1 | Neither research file itemizes per-field type-mix specifically (only general "structural analysis") — confirmed via primary source. |
| SCHEMA-doc-export | Documentation export | Confirmed | P1: "You could export this document to the most popular document file types, like MS Word, PDF, HTML, along with JSON, TXT, and CSV. Mongoose.js schema file supported as well." | — | N/A | P1 | Not itemized in S1/S2 body text beyond the general "Schema Explorer" mention. |
| SCHEMA-designer-canvas | Visual canvas (ERD) | Confirmed absent | S1 (section heading): "Visual ERD & Schema Design Environment" listed under Missing Functionality. S2: "lacks visual Entity-Relationship Diagramming (ERD) and drag-and-drop schema modeling tools found in competitors like DbSchema or Navicat." | — | N/A | S1, S2 | Confirmed absent by direct statement in both files independently — not merely unmentioned. |
| SCHEMA-anomaly-detection | Field anomaly detection | Unverified — not discussed | Neither research file nor P1's Schema Analyzer section describes outlier/anomaly flagging distinct from the bare field-probability/type-probability display. | — | N/A | — | Deliberately **not** marked Confirmed despite this dictionary ID's addition being motivated by a similar-sounding Navicat capability — NoSQLBooster's Schema Analyzer, per all sources reviewed, stops at probability/type-mix display and does not flag outlier documents the way Navicat's does. |
| SCHEMA-histogram | Value histogram | Unverified — not discussed | Not described in any source reviewed. | — | N/A | — | — |

## Feature-level conclusion

### Confirmed strengths

- A genuine sampling-based Schema Analyzer with configurable sample mode (random/first/last/all) and count, field-population probability, per-field type-mix, and multi-format documentation export (Word/PDF/HTML/JSON/TXT/CSV, plus a Mongoose.js schema file) — a solid, if not exceptional, schema-analytics implementation confirmed jointly across both research files and the primary source.

### Confirmed limitations

- No visual ERD or schema-design canvas — confirmed absent by direct, independent statement in both S1 and S2, each naming Navicat and/or DbSchema as competitors that do have this.
- No confirmed anomaly/outlier detection distinct from the bare probability/type-mix display, unlike Navicat's Schema Analyzer (which this repository's other product report confirms does have this distinction, and which is the evidentiary basis for the `SCHEMA-anomaly-detection` dictionary ID).

### Open questions / unknowns

- Whether the Schema Analyzer surfaces a value histogram (numeric distribution) or date-distribution chart — not described anywhere in the sources reviewed.
- Whether the "document validation" window P1 describes (showing an existing collection's `$jsonSchema` validator, with click-to-highlight field navigation) amounts to a `SCHEMA-verify`-style "run validator, view non-conforming documents" workflow, or is a narrower read-only display — the primary-source wording ("shows document validation of the collection... a validator window showing below the document") reads closer to the latter, so `SCHEMA-verify` is not marked Confirmed here.
