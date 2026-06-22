# Feature Matrix — MongoDB Compass / Indexing Performance

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Source index

- S1: https://www.mongodb.com/docs/compass/indexes/
- S2: https://www.mongodb.com/docs/compass/indexes/create-search-index/
- S3: https://www.mongodb.com/docs/compass/indexes/create-vector-search-index/
- S4: https://www.mongodb.com/docs/compass/query-plan/
- S5: https://www.mongodb.com/docs/compass/manage-data/performance-insights/
- S6: https://www.mongodb.com/docs/compass/performance/

## Capability matrix

| Capability ID | Capability | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| IDX-inventory | Index inventory and usage visibility | Supported | Lists index metadata, properties, and usage counters in index tab. | Usage metrics reflect connected node, not full cluster-wide truth. | Unknown | S1 | Docs recommend `$indexStats` for full-node coverage. |
| IDX-type-single | Single-field index creation | Supported | Create ascending or descending single-field indexes. | Index strategy impacts write performance; must be tuned. | Unknown | S1 | |
| IDX-type-compound | Compound index creation | Supported | Create multi-field compound indexes with key ordering. | Index strategy impacts write performance; must be tuned. | Unknown | S1 | Includes compound key authoring. |
| IDX-type-ttl | TTL index creation | Supported | Create TTL (auto-expiry) indexes on Date fields with configurable expiry time. | Requires a Date-type field. | Unknown | S1 | |
| IDX-props-unique-sparse | Unique and sparse properties | Supported | Apply unique constraint and sparse (skip missing field) properties to indexes. | Unique constraint enforcement on existing data requires pre-validation. | Unknown | S1 | |
| IDX-props-partial | Partial index | Supported | Create index with a filter expression to index only matching documents. | Partial filter expression must be valid query syntax. | Unknown | S1 | |
| IDX-hide-unhide | Hide/unhide indexes | Supported | Supports index hide/unhide for planner-impact testing before drop. | Requires MongoDB 4.4+; use with operational caution in production. | Unknown | S1 | Useful risk-mitigation workflow. |
| IDX-props-hidden | Hidden index property | Supported | Hidden index property available at creation time; index invisible to query planner. | Requires MongoDB 4.4+. | Unknown | S1 | |
| IDX-atlas-search | Atlas Search index workflow | Supported with constraints | Search index creation from Compass supported for eligible Atlas/local setups, including status tracking. | Atlas M10+ (or Atlas-CLI local) and MongoDB 7.0+ requirements. | Unknown | S2 | Status tracking included. |
| IDX-vector-search | Vector Search index workflow | Supported with constraints | Vector search index creation supports vector config fields and status checks. | Same deployment/version constraints as Search index flow. | Unknown | S3 | Supports semantic-search scenarios. |
| IDX-explain-brief | Explain plan — plan mode | Supported | Plan-only explain showing query plan without execution; fast and always available. | Interpretation quality depends on query/index understanding. | Unknown | S4 | Key debugging surface for query tuning. |
| IDX-explain-full | Explain plan — full stats | Supported | Full execution-stats explain with per-stage timing, document counts, and scan characteristics. | Interpretation quality depends on query/index understanding. | Unknown | S4 | Key debugging surface for query tuning. |
| IDX-perf-insights | Performance insights recommendations | Supported | System suggests modeling/indexing improvements for problematic patterns. | Suggestions are generic and must be validated against workload reality. | Unknown | S5 | Advisory, not auto-remediation. |
| IDX-realtime-perf | Real-time performance tab | Supported with constraints | Live operational metrics (`mongostat`, `mongotop`, `currentOp`) and slow-op drill-down; includes pause/play visualization control. | Limited detail via `mongos`; QE collections have limitations. | Unknown | S6 | Includes pause/play visualization control. |
| IDX-stop-ops | Stop long operations | Supported with constraints | Allows stopping operations from performance view. | Stopping non-owned ops requires `killop` privilege. | Unknown | S6 | Privilege-gated control. |
