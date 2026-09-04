# Feature Report — NoSQLBooster / Indexing & Performance

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Scope

- Feature name: Indexing & Performance
- Feature ID: F-IDX (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Product: NoSQLBooster
- Product group: third-party
- Analysis date: 2026-09-04

## Behavioral walkthrough

NoSQLBooster's diagnostics-and-tuning surface is confirmed real but narrow relative to what the research files document elsewhere in the product: a Visual Explain Plan renders `.explain("executionStats")` output as an interactive, hierarchical tree — S2 specifically calls out that it is aware of MongoDB 7.0's Slot-Based Query Execution (SBE) engine, not just the legacy explain format, a differentiated claim among the products this repository has reviewed to date. A dedicated MongoDB Log Parser handles two distinct input modes — live-tailing the most recent in-memory `mongod` log events, and parsing an external log file — categorizing entries by severity, timestamp, component, and context, with the option to persist parsed entries back into a MongoDB collection for further ad hoc querying. Real-time server monitoring wraps `mongostat` and `mongotop` in graphical dashboards, complemented by an In-Progress Operations Viewer that can kill long-running operations directly.

What neither research file discusses at all is index management proper: index type coverage, index creation/editing UI, or query profiler configuration (levels, slow-query thresholds, drill-down detail). This is a genuine gap in the source material's coverage of the product, not a confirmed absence — this review's incidental primary-source glance (made while resolving the two flagged S1/S2 conflicts elsewhere) did turn up "Index Management" and "Suggest Index / Create Index From Query" rows on the vendor's own edition-comparison page, but per this plan's scope this matrix does not lean on that beyond flagging it as an open question, since neither assigned research file itself makes the claim.

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| IDX-explain-full | SBE-engine-aware Visual Explain is a specific, differentiated claim. | Signals engineering investment keeping pace with MongoDB's own query-engine evolution, similar in spirit to S2's broader "day-one MongoDB Server support" narrative. | S2 |
| IDX-log-parser | Direct, close-to-exact match for this effort's newly-added `IDX-log-parser` dictionary ID, including the "save parsed entries back to a collection" detail the ID's description anticipates. | NoSQLBooster is the clearest evidentiary basis among the five products reviewed in this effort for this specific dictionary ID. | S1, S2 |

## Constraints and risks

- The confirmed UI-thread-freezing issue on large clusters (see `product-report.md`) is specifically reported in the context of "the left connection tree pane handling a server with 800 databases" — a connectivity/sidebar-rendering issue, not specifically an F-IDX one, but relevant context for any performance-monitoring workflow against a large deployment.

## Interactions and dependencies

- The Log Parser's "save to collection" output creates a normal MongoDB collection that can then be queried, aggregated, or exported through every other F-QUERY/F-AGG/F-TRANSFER capability — a deliberate design choice per S1's description.

## Conclusions

### Strengths

- SBE-aware Visual Explain and a dual-mode (live + external-file) Log Parser that persists results back into MongoDB for further querying.

### Limitations

- Index management and query-profiler configuration depth are simply not discussed in either research file.

### Unknowns

- Index type coverage, index creation/edit UI, and profiler level/threshold configuration.
