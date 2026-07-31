# Feature Report — Studio 3T / Indexing & Performance

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [High-level comparison](../../../../../reports/comparisons/high-level-product-comparison.md)

**Last reviewed:** 2026-07-31 — see [research findings](../../../../../research/studio-3t-desktop-review-2026/05-indexing-performance-findings.md)

## Scope

This report covers Studio 3T's Index Manager, all supported index types and properties, Visual Explain (Brief and Full modes), the Query Profiler including its drill-down and tool integration capabilities, and — newly documented as of this review — the real-time server monitoring capability (live server-status charts and a Current Operations view) surfaced under a separate tab rather than the Index Manager or Query Profiler.

## Behavioral walkthrough

Studio 3T's index management UI covers the full MongoDB index type catalog: single field, compound, multikey (array), text, wildcard, 2d, 2dsphere, and the deprecated geoHaystack. Each index type exposes its type-specific options in the Add Index dialog — text indexes show version, default language, language override, and per-field weights; 2d indexes show lower/upper bound and bit precision. The Index Manager lists usage counts alongside each index (requiring the $indexStats privilege), making it immediately visible which indexes are unused and candidates for removal.

The Hide/Unhide feature is particularly valuable for safe index impact testing. Rather than dropping an index to measure its absence, users can hide it — removing it from the query planner's consideration while leaving the index data intact and constraints enforced. If the hidden index turns out to be needed, Unhide restores it instantly, with no rebuild cost. This feature requires MongoDB ≥ 4.4 with featureCompatibilityVersion set accordingly.

Visual Explain operates in two modes to balance usability with information depth. Brief mode renders a query plan diagram with no server round-trip — it shows the plan structure (COLLSCAN vs IXSCAN, stages, sort positions) without executing the query. This is the safe default for ad-hoc inspection. Full mode adds runtime statistics: per-stage document counts, execution time in milliseconds, and estimated bytes processed. Each stage block in the diagram supports right-click for description and raw JSON scoping, enabling precise diagnosis of specific pipeline segments. The "View JSON" button exposes the complete query plan document for advanced analysis.

Visual Explain is available across five Studio 3T tools: Collection Tab, IntelliShell Query Assist tabs, SQL Query tool, Aggregation Editor, and Query Profiler. This cross-tool availability means performance analysis is reachable from any query authoring context without switching tools.

The Query Profiler reads from MongoDB's system.profile collection. Studio 3T surfaces profile entries with two grouping modes: exact query (groups by unique field names + values, making each parameterized query variant a separate entry) and query shape (groups by logical structure regardless of values, showing the queryHash). This distinction helps identify both specific slow queries and recurring slow query patterns. Drill-down from a profiler entry can open the query in Collection Tab, IntelliShell, or Aggregation Editor, or embed the Visual Explain plan directly — creating a triage-to-action workflow within a single interface.

Index Manager also supports copying an index definition from one collection and pasting it onto another — including a target collection on an **entirely different connection**, not just a different collection on the same connection. This is confirmed by the copy/paste plumbing taking independent `Connection` objects for source and target. It is a genuine differentiator for replicating index strategy across environments (e.g., dev → staging), but it is gated to **Professional edition and above** (`AppFeatures.COPY_INDEX`) — it is not available on Free or Community (Robo) editions.

### Real-time performance monitoring (mongostat / currentOp equivalent)

Beyond the Index Manager and Query Profiler, Studio 3T ships a real-time server monitoring capability that is easy to overlook because it lives under a separate tab rather than either of those two tools — but it is a substantive, notable differentiator worth documenting on its own. Two independent pieces were verified directly in source:

1. **Live server-status charts** (a mongostat-equivalent) poll `serverStatus` on a timer and render live time-series charts of aggregate server-wide metrics: operation counters (query/getmore/insert/update/delete), connection counts (current/available/totalCreated), and network throughput (requests, bytes in/out). The refresh interval is configurable.
2. **Current Operations view** (a currentOp/killOp-equivalent) lists in-flight server operations in real time and lets a user kill a selected operation directly from the view, reachable from the connection tree and database context menu.

No dedicated mongotop-style per-collection read/write activity monitor was found — the closest equivalent is the existing per-collection stats views, which are point-in-time rather than live. Both the live charts and Current Operations are gated to **Professional edition and above** (`AppFeatures.SERVER_STATUS_CHARTS` and `AppFeatures.CURRENT_OPERATIONS` respectively), absent from Free and Community (Robo) editions.

## Capability findings

| Capability ID | Finding | Impact |
| --- | --- | --- |
| IDX-009 | All six standard index properties (Unique, Sparse, Hidden, TTL, Partial, Case-insensitive) are configurable via UI without shell commands. | Reduces index creation errors from manual option document construction. |
| IDX-012 | Hide/Unhide index is a first-class UI action — supports safe index impact testing without drop risk. | Eliminates the risk of costly index rebuilds during impact analysis. |
| IDX-013 | Brief mode Visual Explain is always available and fast — no query execution overhead for plan structure inspection. | Makes explain accessible for exploratory inspection, not just formal debugging. |
| IDX-015 | Visual Explain available in SQL Query tool, not just MongoDB query tools — enables explain for SQL-translated aggregation pipelines. | Unique cross-language explain coverage not seen in comparable tools. |
| IDX-016 | Query Profiler with query shape grouping (queryHash) and exact query grouping in the same UI is more analytical than Compass's profiler. | Enables both pattern-level and instance-level slow query triage. |
| IDX-017 | Profiler drill-down → "Add Index on collection" shortcut bridges performance triage to index remediation without leaving the profiler. | Reduces the steps between identifying a slow query and creating the fix. |
| IDX-018 | Real-time server-status charts (mongostat-equivalent) plus a Current Operations view with kill support (currentOp/killOp-equivalent) give live operational visibility beyond static stats snapshots. | Lets teams diagnose live load and terminate runaway operations without dropping to a shell. |

## Constraints and risks

- geoHaystack index type (IDX-008) is deprecated in MongoDB 4.4 and removed in 5.0. **Corrected 2026-07-31:** Studio 3T *does* warn about this in-UI — the "Bucket Size/geoHaystack is deprecated" text appears in the geo options sub-tab — and the option is version-gated to servers before 4.9. The prior claim that Studio 3T surfaces it "without a deprecation warning" was factually wrong.
- Usage count display requires the $indexStats privilege — teams using least-privilege MongoDB roles may not see usage data.
- Full mode Visual Explain executes the query against the database; running it against expensive queries on production collections can cause load spikes.
- Background index creation (IDX-010) is superseded by concurrent builds in MongoDB 4.4+. **Corrected 2026-07-31:** Studio 3T *does* explain the tradeoff in-UI — the "Create in background" checkbox is accompanied by text describing the MongoDB 4.2+ locking change and the background-build size/compactness tradeoff — though it does not use the literal word "deprecated." The prior claim that Studio 3T does not flag this at all was factually wrong.
- Level 2 profiling captures all operations and can significantly degrade server performance on busy deployments; Studio 3T does not warn the user before enabling Level 2.
- Index copy/paste (IDX-copy-paste), the real-time server-status charts, and the Current Operations/kill-operation view are all **Professional edition and above only** — teams on Free or Community (Robo) editions do not have access to these, which is a material caveat for anyone evaluating cross-connection index replication or live monitoring as a reason to choose Studio 3T.

## Conclusion

Index management and performance tooling in Studio 3T is comprehensive. The Index Manager covers all MongoDB index types with type-specific options (including hashed indexes and full collation/text/geo option sets not previously documented here), the Hide/Unhide workflow enables safe impact testing, and Visual Explain spans five query entry points. The Query Profiler's two grouping modes and drill-down integration with other tools create a practical performance triage workflow. Beyond these, Studio 3T also ships genuine real-time performance monitoring — live server-status charts and a Current Operations/kill-operation view — that is a notable differentiator worth surfacing on its own rather than leaving undocumented; it is, however, restricted to Professional edition and above, as is cross-connection index copy/paste. The main residual risks are the performance impact of Full mode explain and Level 2 profiling, and the edition gating on the Professional-tier features noted above.
