# Feature Matrix — MongoDB Compass / Schema

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
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
| SCHEMA-sampling | Sampling-based schema profiling | Supported | Schema analysis based on sampled documents for speed and statistical approximation; defaults to 1000 docs via `$sample`. | Sampling quality depends on collection size and distribution. | Unknown | S1, S2 | Sampling documented as 1000 docs via `$sample`. |
| SCHEMA-field-prob | Field probability analysis | Supported | Displays per-field probability indicating the percentage of sampled documents containing that field. | Complex collections may require tuning max time. | Unknown | S1 | Helps identify sparse or optional fields. |
| SCHEMA-type-prob | Type probability analysis | Supported | Shows per-field type distribution, revealing polymorphic fields with mixed BSON types. | Complex collections may require tuning max time. | Unknown | S1 | Includes mixed-type visibility. |
| SCHEMA-histogram | Value histogram | Supported | Frequency histogram of numeric field value distributions and range analysis. | Complex collections may require tuning max time. | Unknown | S1 | Includes cardinality and range info. |
| SCHEMA-geo-analysis | Geospatial schema analysis | Supported | Map-backed analysis for geo fields with interactive filter drawing and generated geo queries. | Requires map features/network availability. | Unknown | S1 | Useful for location-heavy datasets. |
| SCHEMA-file-export | Schema file export | Supported with constraints | Exports analyzed schema in multiple formats (standard/MongoDB/expanded). | Export fails if schema has >1000 distinct fields. | Unknown | S3 | Useful for sharing and review. |
| SCHEMA-validation-model | Validation rule authoring model | Supported | Validation supports `$jsonSchema` and query-operator style rules with action and level semantics. | Some operators excluded from validation context. | Unknown | S4 | Includes action/level semantics. |
| SCHEMA-validation-strictness | Validation strictness controls | Supported | Supports `warn`/`error` action and `strict`/`moderate` level behavior. | Needs alignment with runtime data quality policy. | Unknown | S4 | Enforcement behavior is configurable. |
| SCHEMA-validation-ui | Validation UI workflows | Supported | Add/edit/generate/preview/apply validation rule flows provided in UI. | Readonly mode limits edit capabilities. | Unknown | S5, S6, S7 | Consistent user flow across pages. |
| SCHEMA-validation-limits | Validation scope limits | Supported with constraints | Validation UI unavailable for Atlas Data Federation; distinct field count >1000 blocks validation/export workflows. | Applies to very wide schemas. | Unknown | S4 | Important for very wide schemas. |
