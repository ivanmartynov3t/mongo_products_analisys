# Feature Matrix — MongoDB Compass / Indexing Performance

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
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
| IDX-001 | Index inventory and usage visibility | Supported | Lists index metadata, properties, and usage counters in index tab. | Usage metrics reflect connected node, not full cluster-wide truth. | Unknown | S1 | Docs recommend `$indexStats` for full-node coverage. |
| IDX-002 | Index creation options | Supported | Supports regular and special index options (unique, TTL, partial, wildcard, collation). | Index strategy impacts write performance; must be tuned. | Unknown | S1 | Includes compound key authoring. |
| IDX-003 | Hide/unhide indexes | Supported | Supports index hide/unhide for planner-impact testing before drop. | Requires operational caution in production. | Unknown | S1 | Useful risk-mitigation workflow. |
| IDX-004 | Atlas Search index workflow | Supported with constraints | Search index creation from Compass is supported for eligible Atlas/local setups. | Atlas M10+ (or Atlas-CLI local) and MongoDB 7.0+ requirements. | Unknown | S2 | Status tracking included. |
| IDX-005 | Vector Search index workflow | Supported with constraints | Vector search index creation supports vector config fields and status checks. | Same deployment/version constraints as Search index flow. | Unknown | S3 | Supports semantic-search scenarios. |
| IDX-006 | Query explain plan | Supported | Explain plan in visual and raw forms shows execution stats and scan characteristics. | Interpretation quality depends on query/index understanding. | Unknown | S4 | Key debugging surface for query tuning. |
| IDX-007 | Performance insights recommendations | Supported | System suggests modeling/indexing improvements for problematic patterns. | Suggestions are generic and must be validated against workload reality. | Unknown | S5 | Advisory, not auto-remediation. |
| IDX-008 | Real-time performance tab | Supported with constraints | Uses live operational metrics (`mongostat`, `mongotop`, `currentOp`) and slow-op drill-down. | Limited detail via `mongos`; QE collections have limitations. | Unknown | S6 | Includes pause/play visualization control. |
| IDX-009 | Stop long operations | Supported with constraints | Allows stopping operations from performance view. | Stopping non-owned ops needs `killop` privilege. | Unknown | S6 | Privilege-gated control. |
