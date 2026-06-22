# Feature Matrix — MongoDB Compass / Querying

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Source index

- S1: https://www.mongodb.com/docs/compass/query/filter/
- S2: https://www.mongodb.com/docs/compass/query/project/
- S3: https://www.mongodb.com/docs/compass/query/sort/
- S4: https://www.mongodb.com/docs/compass/query/skip/
- S5: https://www.mongodb.com/docs/compass/query/limit/
- S6: https://www.mongodb.com/docs/compass/query/collation/
- S7: https://www.mongodb.com/docs/compass/query/maxtimems/
- S8: https://www.mongodb.com/docs/compass/query/recent/
- S9: https://www.mongodb.com/docs/compass/query/queries/
- S10: https://www.mongodb.com/docs/compass/export-query-to-language/

## Capability matrix

| Capability ID | Capability | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| QUERY-filter-bar | Filter query bar | Supported | MongoDB filter syntax in UI with examples and field-to-query shortcuts. | Query correctness depends on user syntax. | Unknown | S1 | Supports nested paths and operators. |
| QUERY-projection | Projection controls | Supported | Include/exclude fields with project document controls. | Validation required for valid projection document. | Unknown | S2 | `_id` included by default unless excluded. |
| QUERY-sort | Sort controls | Supported | Per-query sort document in query bar options. | Overrides default sort settings. | Unknown | S3 | Supports multi-field sort ordering. |
| QUERY-skip-limit | Skip and limit | Supported | Offset and result-size controls in query bar options. | Large result views may use subset behavior. | Unknown | S4, S5 | Useful for pagination/testing. |
| QUERY-collation | Collation-aware querying | Supported | Query-level collation document with locale rules. | Locale field is required. | Unknown | S6 | Language-specific compare behavior. |
| QUERY-max-time | maxTimeMS control | Supported | Time cap for query operations with timeout interruption. | May require tuning for large/complex operations. | Unknown | S7 | Default documented as 60000 ms. |
| QUERY-history | Recent query history | Supported | Recent query list with save/copy/remove actions and autocomplete integration. | History depth is capped. | Unknown | S8 | Helps iteration speed. |
| QUERY-saved | Saved/favorite query workflows | Supported | Saved queries and saved aggregations are reusable in My Queries and favorites views. | Scope is per collection context. | Unknown | S9 | Includes bulk update favorites support. |
| QUERY-export-lang | Query export to driver languages | Supported | Exports query syntax to Java, Node, C#, Python, Ruby, Go, Rust, PHP. | Export quality depends on valid source query/options. | Unknown | S10 | Optional import statements and driver syntax. |
