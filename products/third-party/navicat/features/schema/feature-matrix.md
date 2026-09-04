# Feature Matrix — Navicat / Schema

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: Navicat
- Product group: third-party
- Feature ID: F-SCHEMA (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `schema`
- Analysis date: 2026-09-04
- Version/release context: Navicat 17 line

## Source index

- S1: Navicat Competitive Intelligence Analysis (secondary research file), `research/google_research/navicat-competitive-intelligence-analysis/Navicat Competitive Intelligence Analysis.md`
- S2: Navicat Data Modeler Release Note, https://www.navicat.com/en/products/navicat-data-modeler-release-note (S1 Works Cited #10 — general release-note index, not a specific dated entry)

## Capability matrix (low-level)

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SCHEMA-sampling | Sampling config | Confirmed (existence); Unverified (configurability) | S1: "The tool samples collection documents to map structural topography, plotting field population frequencies, data type mix per key, and schema anomalies." | Sample mode/count/filter controls are not itemized — only that sampling occurs. | Unverified | S1 | — |
| SCHEMA-field-prob | Field probability | Confirmed | S1: "a visual Schema Analyzer to help users understand structural variance within schema-flexible collections... plotting field population frequencies." | — | Unverified | S1 | — |
| SCHEMA-type-prob | Type probabilities | Confirmed | Same S1 sentence: "...data type mix per key..." | — | Unverified | S1 | — |
| SCHEMA-anomaly-detection | Field anomaly detection | Confirmed | S1: "...and schema anomalies. Outliers, such as documents containing unexpected data types or deprecated fields, are highlighted for review." | — | Unverified | S1 | This Navicat capability is the direct evidentiary basis for the new dictionary ID `SCHEMA-anomaly-detection` added in this same effort (2026-09-04) — the source explicitly distinguishes outlier/anomaly highlighting from the bare field-probability/type-probability display, matching the new ID's definition exactly. |
| SCHEMA-histogram | Value histogram | Unverified | Not discussed — S1 describes field population frequency and type mix, not a numeric-value frequency histogram. | — | Unverified | S1 | — |
| SCHEMA-doc-export | Documentation export | Unverified | Not discussed for the Schema Analyzer specifically. | — | Unverified | S1 | — |
| SCHEMA-designer-canvas | Visual canvas | Confirmed, heavily constrained for MongoDB | S1 (Data Modeling section): "The integrated modeling environment is based on the standalone Navicat Data Modeler application. It supports Physical, Logical, and Conceptual modeling paradigms across Relational, Dimensional, and Data Vault 2.0 methodologies. Architects can reverse-engineer live databases into graphical ER diagrams..." However, S1's Strategic Product Opportunities section states directly: "While Navicat Data Modeler offers strong ER modeling for relational and Data Vault 2.0 structures, its document schema modeling for MongoDB remains limited to read-only analysis." | The canvas/ER-diagramming capability is real and rich for Navicat's relational engines; for MongoDB specifically, it is read-only structural analysis only — no forward-engineering of schema changes back to a live MongoDB collection. | Not planned (per the source's own framing as a Studio 3T "Reschema" competitive opportunity) | S1 | Marked Confirmed-but-constrained per this plan's explicit instruction: the underlying canvas/ER capability is real and well-evidenced, but its applicability to MongoDB is explicitly narrowed by the source to read-only analysis, not full modeling. |
| SCHEMA-designer-auto | Auto-generate diagram | Confirmed (relational); Unverified (MongoDB) | S1 describes "automatic diagram layout generation" as part of the Data Modeler's general capability set, but does not confirm this applies to auto-generating a diagram from MongoDB collections given the read-only-analysis constraint above. | Same MongoDB read-only-analysis constraint as `SCHEMA-designer-canvas`. | Unverified (MongoDB scope) | S1 | — |
| SCHEMA-designer-links | Relationship detection | Unverified | Not specifically described for Navicat (no graph-theory or automatic relationship-detection algorithm mentioned, unlike VisuaLeaf's confirmed capability per this repository's other product reports). | — | Unverified | S1 | — |
| SCHEMA-verify | Schema verification | Unverified | Not discussed — no $jsonSchema validator authoring, deployment, or non-conforming-document verification workflow is described for Navicat. | — | Unverified | S1 | — |

## Feature-level conclusion

### Confirmed strengths

- A genuine sampling-based visual Schema Analyzer covering field population frequency, per-field type-mix, and — distinctly — outlier/anomaly detection (unexpected data types, deprecated fields flagged for review). This three-part combination (frequency + type-mix + anomaly flagging) is one of the more complete schema-analytics implementations reviewed among this repository's third-party competitors.
- A rich, general-purpose Data Modeler with Physical/Logical/Conceptual modeling across Relational, Dimensional, and Data Vault 2.0 methodologies, including reverse-engineering and forward-engineering for relational/DDL-based engines.

### Confirmed limitations

- Navicat Data Modeler's MongoDB document schema modeling is explicitly, directly stated to be limited to **read-only analysis** — it cannot forward-engineer schema changes back to a live MongoDB collection, unlike its relational-engine DDL modeling or Studio 3T's interactive "Reschema" engine (per the source's own Strategic Product Opportunities section, which frames this as a specific gap Studio 3T could exploit).
- No value histogram, schema documentation export, JSON Schema editor, or $jsonSchema validation authoring/deployment workflow is described for Navicat's Schema Analyzer.

### Open questions / unknowns

- Whether the Schema Analyzer's anomaly detection is purely statistical (frequency-based outlier flagging) or includes any rule-based/user-configurable anomaly definitions.
- Sample size/mode configurability for the Schema Analyzer.
- Whether the Data Modeler's "read-only analysis" constraint for MongoDB means it cannot render an ER-style diagram of MongoDB collections at all, or that it can visualize structure but not edit/forward-engineer it — the source's wording ("remains limited to read-only analysis") is closer to the latter reading, which is how this matrix has scored `SCHEMA-designer-canvas`, but the exact UI behavior is not detailed.
