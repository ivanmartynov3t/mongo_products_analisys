# Feature Report — Navicat / Schema

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Scope

- Feature name: Schema
- Feature ID: F-SCHEMA (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Product: Navicat
- Product group: third-party
- Analysis date: 2026-09-04

## Behavioral walkthrough

Navicat's visual Schema Analyzer samples documents from a schema-flexible collection to map its structural topography along three dimensions: field population frequency (what percentage of sampled documents contain each field), per-field data-type mix (revealing polymorphic fields that hold more than one BSON type across documents), and schema anomalies — outlier documents containing unexpected data types or deprecated fields, which are flagged for review. This third dimension, anomaly/outlier detection, is explicitly distinguished in the source from the bare frequency/type-mix display, which is exactly why it maps to the newly-added `SCHEMA-anomaly-detection` dictionary ID rather than being folded into `SCHEMA-field-prob`/`SCHEMA-type-prob`.

Separately, Navicat Data Modeler provides a full entity-relationship modeling environment — Physical, Logical, and Conceptual modeling paradigms across Relational, Dimensional, and Data Vault 2.0 methodologies, with reverse-engineering of live databases into ER diagrams and forward-engineering of diagram changes back to the target database via DDL generation. This is a mature, general-purpose capability for Navicat's relational engines. For MongoDB specifically, however, the source is explicit and direct: "its document schema modeling for MongoDB remains limited to read-only analysis" (Strategic Product Opportunities section) — meaning architects can view/analyze MongoDB document structure through the modeler, but cannot use it to forward-engineer schema changes onto a live MongoDB collection the way they can for relational DDL. The source frames this specifically as a gap Studio 3T's interactive "Reschema" engine could exploit.

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| SCHEMA-field-prob / SCHEMA-type-prob / SCHEMA-anomaly-detection | All three schema-analytics dimensions are individually and specifically described for the same Schema Analyzer tool. | A relatively complete schema-analytics implementation — comparable in breadth (though not necessarily in UI depth) to Compass's and Studio 3T's own schema explorers. | Research file narrative ("MongoDB Functionality" section) |
| SCHEMA-designer-canvas | ER/Data Vault 2.0 modeling is real and mature for relational engines; explicitly read-only-analysis-only for MongoDB. | Navicat cannot be used as a MongoDB schema-refactoring tool the way Studio 3T's Reschema can — a genuine, source-confirmed strategic gap, not merely unverified. | Research file's own Strategic Product Opportunities section |

## Constraints and risks

- Do not conflate the visual Schema Analyzer (read/analyze-only by design, and genuinely full-featured for that purpose) with the Data Modeler's MongoDB support (also read-only, but as an explicit *limitation* relative to what the Modeler can do for relational engines) — these are two different tools in the source, both landing on "read-only for MongoDB" but for different underlying reasons.
- Sample-size/mode configurability, histogram support, and schema documentation export are silent gaps, not confirmed absences.

## Interactions and dependencies

- The Schema Analyzer's anomaly-detection findings could plausibly feed a rename/repair workflow (as Studio 3T's schema tree does via `SCHEMA-rename-discover`), but no such workflow is described for Navicat in the source.
- Data Modeler's relational-engine ER capability is out of scope for this MongoDB-focused report except where it explicitly bears on MongoDB (the read-only-analysis constraint).

## Conclusions

### Strengths

- A three-part visual Schema Analyzer (field-population frequency, per-field type-mix, anomaly/outlier detection) — one of the more complete sampling-based schema-analytics implementations reviewed among this repository's third-party products.

### Limitations

- Navicat Data Modeler's MongoDB document schema modeling is confirmed, by direct statement, to be read-only analysis only — no forward-engineering of schema changes to a live MongoDB collection.
- No value histogram, schema documentation export, or $jsonSchema validation authoring/deployment workflow described.

### Unknowns

- Sample size/mode configurability for the Schema Analyzer.
- Whether Data Modeler's MongoDB "read-only analysis" extends to visualizing an ER-style diagram of MongoDB collections, or is limited to a narrower structural report.
