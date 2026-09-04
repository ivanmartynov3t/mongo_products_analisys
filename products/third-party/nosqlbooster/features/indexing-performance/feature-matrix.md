# Feature Matrix — NoSQLBooster / Indexing & Performance

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: NoSQLBooster
- Product group: third-party
- Feature ID: F-IDX (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `indexing-performance`
- Analysis date: 2026-09-04
- Version/release context: v11.0–v11.1 line

## Source index

- S1: NoSQLBooster Competitive Analysis
- S2: NoSQLBooster Competitive Intelligence Analysis
- P1: nosqlbooster.com/features (primary; fetched directly by this review)
- P2: nosqlbooster.com/compareEditions (primary; fetched directly by this review)

## Capability matrix (low-level)

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| IDX-explain-full | Explain — full stats | Confirmed | S2: "a Visual Explain Plan interface that parses MongoDB execution plans into a hierarchical graphical flow diagram. This tool supports legacy query engines as well as the Slot-Based Query Execution (SBE) engine introduced in MongoDB 7.0." S1: "breaks down execution stages, index coverage, and document scanning metrics." | — | N/A | S1, S2 | SBE-engine awareness is a specific, differentiated claim not made for most other products reviewed in this repository. |
| IDX-log-parser | Log file parser | Confirmed | S2: "a dedicated MongoDB Log Parser capable of processing active mongod event streams as well as historical external log files. The parser categorizes entries by severity, timestamp, component, and operational context, and allows structured log lines to be saved directly into a MongoDB collection." S1 corroborates: "converts local or external mongod log files into queryable collections." | — | N/A | S1, S2 | Direct, near-exact-definition evidentiary match for the `IDX-log-parser` dictionary ID. |
| IDX-realtime-perf | Real-time performance | Confirmed | S1: "real-time server dashboards track mongostat, mongotop, active connections, and slow operations (CurrentOp)." S2: "graphical wrappers around mongostat and mongotop, alongside an In-Progress Operations Viewer." | — | N/A | S1, S2 | — |
| IDX-stop-ops | Stop operations | Confirmed | S2: "an In-Progress Operations Viewer that allows administrators to inspect running queries and issue commands to kill long-running operations." | — | N/A | S2 | — |
| IDX-inventory | Index inventory | Confirmed (existence only) | Neither S1 nor S2 discusses index creation, listing, or management at all. P2's edition-comparison table lists a plain "Index Management" row (present across all tiers) directly under "Object Explorer/Management," confirming an index inventory/management surface exists. | — | N/A | P2 | Confirmed via primary source fetched directly by this review; neither research file itemizes this. Index-type coverage (single/compound/multikey/text/wildcard/geospatial/hashed/TTL) and configuration depth remain unconfirmed — P2's row is a bare "Index Management" label with no itemization. |
| IDX-perf-insights | Performance insights | Unverified | P2's edition-comparison table lists a "Suggest Index / Create Index From Query" row (present across all tiers), suggesting some index-recommendation capability. | — | N/A | P2 | Weak evidentiary basis (a bare feature-matrix row label, no explanatory text in either research file or on the Feature Tour page) — marked Unverified rather than Confirmed given how thin this is relative to the dictionary ID's "system-level modeling/indexing improvement suggestions" definition. |

## Feature-level conclusion

### Confirmed strengths

- A genuinely differentiated Visual Explain Plan that is explicitly SBE-engine-aware (MongoDB 7.0+), plus a dedicated MongoDB Log Parser (mongod live-tail and external file parsing, with results savable back into a MongoDB collection for further querying) — the direct evidentiary basis for this effort's `IDX-log-parser` dictionary ID.
- Real-time mongostat/mongotop/CurrentOp monitoring with the ability to kill long-running operations.
- An index-management surface and an index-suggestion row exist per the vendor's own edition-comparison page, though neither research file discusses either at all.

### Confirmed limitations

- Neither research file discusses index type coverage, index creation/management UI, or query-profiler configuration (levels, thresholds, drill-down) at all — this is a genuine evidentiary gap in the source material, not a confirmed absence of the capability itself. The primary-source fetch confirms bare existence of index management and index suggestions but not their depth.

### Open questions / unknowns

- Index-type coverage and profiler configuration depth — entirely unconfirmed by either research file or the primary source fetched.
