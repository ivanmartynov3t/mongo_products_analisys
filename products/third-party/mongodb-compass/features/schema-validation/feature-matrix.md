# Feature Matrix — MongoDB Compass / Schema Validation

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Source index

- S1: https://www.mongodb.com/docs/compass/schema/
- S2: https://www.mongodb.com/docs/compass/sampling/
- S3: https://www.mongodb.com/docs/compass/schema/export/
- S4: https://www.mongodb.com/docs/compass/validation/
- S5: https://www.mongodb.com/docs/compass/add-validation-rules/
- S6: https://www.mongodb.com/docs/compass/edit-validation-rules/
- S7: https://www.mongodb.com/docs/compass/generate-validation-rules/

## Capability matrix

| Capability ID | Capability | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SCH-001 | Sampling-based schema profiling | Supported | Schema analysis is based on sampled documents for speed and statistical approximation. | Defaults and quality depend on sample behavior. | Unknown | S1, S2 | Sampling documented as 1000 docs via `$sample`. |
| SCH-002 | Rich field analysis visuals | Supported | Displays type distributions, cardinality, histograms, ranges, and nested shape analysis. | Complex collections may require tuning max time. | Unknown | S1 | Includes mixed-type visibility. |
| SCH-003 | Geospatial schema analysis | Supported | Map-backed analysis for geo fields with interactive filter drawing and generated geo queries. | Requires map features/network availability. | Unknown | S1 | Useful for location-heavy datasets. |
| SCH-004 | Schema export | Supported with constraints | Exports analyzed schema in multiple formats (standard/MongoDB/expanded). | Export fails if schema has >1000 distinct fields. | Unknown | S3 | Useful for sharing and review. |
| SCH-005 | Validation rule authoring model | Supported | Validation supports `$jsonSchema` and query-operator style rules. | Some operators excluded from validation context. | Unknown | S4 | Includes action/level semantics. |
| SCH-006 | Validation strictness controls | Supported | Supports `warn`/`error` action and `strict`/`moderate` level behavior. | Needs alignment with runtime data quality policy. | Unknown | S4 | Enforcement behavior is configurable. |
| SCH-007 | Validation workflows | Supported | Add/edit/generate/preview/apply flows are provided in UI. | Readonly mode limits edit capabilities. | Unknown | S5, S6, S7 | Consistent user flow across pages. |
| SCH-008 | Validation scope limits | Supported with constraints | Validation UI unavailable for Atlas Data Federation; validation size constraints apply. | Distinct field count >1000 blocks validation/export workflows. | Unknown | S4 | Important for very wide schemas. |
