# Feature Matrix — Navicat / Indexing & Performance

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: Navicat
- Product group: third-party
- Feature ID: F-IDX (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `indexing-performance`
- Analysis date: 2026-09-04
- Version/release context: Navicat 17 line

## Source index

- S1: Navicat Competitive Intelligence Analysis (secondary research file), `research/google_research/navicat-competitive-intelligence-analysis/Navicat Competitive Intelligence Analysis.md`

## Capability matrix (low-level)

This matrix is intentionally thin relative to Navicat's overall feature richness: the source confirms index management and Visual Explain exist, but does not itemize index types, profiler configuration depth, or performance-monitoring detail the way it does for the aggregation and schema features.

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| IDX-inventory | Index inventory | Confirmed (existence); Unverified (detail) | S1 (MongoDB Object Management, Feature Inventory): "Graphical designers for Collections, Views, Functions, Indexes, Aggregation Pipelines, GridFS file buckets, and MapReduce jobs." | Name/type/size/usage-count columns are not itemized. | Unverified | S1 | — |
| IDX-type-single | Single-field index | Unverified | Implied by "Graphical designers for... Indexes" but no per-type enumeration given. | — | Unverified | S1 | — |
| IDX-type-compound | Compound index | Unverified | Same as above — not itemized. | — | Unverified | S1 | — |
| IDX-explain-full | Explain — full stats | Confirmed | S1: "Visual Explain renders query execution plans graphically, detailing stage-by-stage document scanning metrics, index utilization (IXSCAN vs. COLLSCAN), execution times, and returned document counts." Also (MongoDB Functionality section): "Visual Explain utilities render query execution plans graphically, exposing index scans, collection scans, and execution timings to aid index optimization." | — | Unverified | S1 | Described twice in the source with consistent, specific detail (IXSCAN/COLLSCAN distinction, execution timing, returned document counts) — one of the better-evidenced F-IDX capabilities. |
| IDX-profiler-config | Profiler configuration | Unverified | S1: "Navicat integrates Visual Explain tools alongside MongoDB Profiler interfaces" — a single, brief mention with no detail on profiling level, threshold, or sample-rate configuration. | — | Unverified | S1 | Existence only; configuration depth entirely unverified. |
| IDX-profiler-analysis | Profiler analysis | Unverified | Same single brief mention as above; no query grouping, percentile, or COLLSCAN-flagging detail given. | — | Unverified | S1 | — |
| IDX-realtime-perf | Real-time performance | Confirmed (as general server monitoring); Unverified (MongoDB-specific mongostat/mongotop/currentOp-style scope) | S1: "System performance is tracked through the Server Monitor interface, which displays active connections, running processes, CPU and memory utilization, and lock statuses across database instances." | Server Monitor appears to be a general, engine-wide monitoring tool (not MongoDB-specific mongostat/mongotop/currentOp equivalents); no pause/play or per-operation drill-down described. | Unverified | S1 | Imperfect-fit mapping: `IDX-realtime-perf`'s dictionary description is "live operational metrics (mongostat/mongotop/currentOp) with pause/play," while Server Monitor reads as a general server-health dashboard (connections/processes/CPU/memory/locks) rather than a MongoDB-query-operation-specific live-ops view. Flagged here as the closest existing ID rather than treated as a confident match. |
| IDX-stop-ops | Stop operations | Unverified | Not discussed — no kill/terminate-operation capability mentioned alongside Server Monitor. | — | Unverified | S1 | — |

## Feature-level conclusion

### Confirmed strengths

- Visual Explain is well and consistently described: graphical execution-plan rendering distinguishing index scans (IXSCAN) from collection scans (COLLSCAN), plus execution timings and returned document counts — described twice in the source with consistent specificity.
- A graphical index designer exists as part of Navicat's broader "MongoDB Object Management" suite.

### Confirmed limitations

- No itemized breakdown of supported index types (single, compound, multikey, text, wildcard, geospatial, hashed, TTL) — the source only confirms a graphical index designer exists, not its type coverage.
- MongoDB Profiler integration is mentioned in a single brief clause with no configuration detail (profiling level, threshold, sample rate) — a materially thinner picture than VisuaLeaf's or Studio 3T's profiler documentation in this repository's other product reports.
- Server Monitor is a general, engine-wide performance dashboard (connections, processes, CPU/memory, locks) rather than a confirmed MongoDB-specific real-time operations view (mongostat/mongotop/currentOp-equivalent) — mapped cautiously to `IDX-realtime-perf` as the closest existing ID, flagged as an imperfect fit.

### Open questions / unknowns

- Full index-type coverage and any advanced index options (partial filter expressions, wildcard projections, collation) — not itemized in the source.
- Whether MongoDB Profiler interfaces in Navicat support configurable profiling levels, slow-query thresholds, or drill-down into individual slow operations.
- Whether Server Monitor can kill/terminate long-running MongoDB operations, or is read-only/observational.
