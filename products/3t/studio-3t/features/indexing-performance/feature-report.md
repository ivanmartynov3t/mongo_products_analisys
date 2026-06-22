# Feature Report — Studio 3T / Indexing & Performance

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [High-level comparison](../../../../../reports/comparisons/high-level-product-comparison.md)

## Scope

This report covers Studio 3T's Index Manager, all supported index types and properties, Visual Explain (Brief and Full modes), and the Query Profiler including its drill-down and tool integration capabilities.

## Behavioral walkthrough

Studio 3T's index management UI covers the full MongoDB index type catalog: single field, compound, multikey (array), text, wildcard, 2d, 2dsphere, and the deprecated geoHaystack. Each index type exposes its type-specific options in the Add Index dialog — text indexes show version, default language, language override, and per-field weights; 2d indexes show lower/upper bound and bit precision. The Index Manager lists usage counts alongside each index (requiring the $indexStats privilege), making it immediately visible which indexes are unused and candidates for removal.

The Hide/Unhide feature is particularly valuable for safe index impact testing. Rather than dropping an index to measure its absence, users can hide it — removing it from the query planner's consideration while leaving the index data intact and constraints enforced. If the hidden index turns out to be needed, Unhide restores it instantly, with no rebuild cost. This feature requires MongoDB ≥ 4.4 with featureCompatibilityVersion set accordingly.

Visual Explain operates in two modes to balance usability with information depth. Brief mode renders a query plan diagram with no server round-trip — it shows the plan structure (COLLSCAN vs IXSCAN, stages, sort positions) without executing the query. This is the safe default for ad-hoc inspection. Full mode adds runtime statistics: per-stage document counts, execution time in milliseconds, and estimated bytes processed. Each stage block in the diagram supports right-click for description and raw JSON scoping, enabling precise diagnosis of specific pipeline segments. The "View JSON" button exposes the complete query plan document for advanced analysis.

Visual Explain is available across five Studio 3T tools: Collection Tab, IntelliShell Query Assist tabs, SQL Query tool, Aggregation Editor, and Query Profiler. This cross-tool availability means performance analysis is reachable from any query authoring context without switching tools.

The Query Profiler reads from MongoDB's system.profile collection. Studio 3T surfaces profile entries with two grouping modes: exact query (groups by unique field names + values, making each parameterized query variant a separate entry) and query shape (groups by logical structure regardless of values, showing the queryHash). This distinction helps identify both specific slow queries and recurring slow query patterns. Drill-down from a profiler entry can open the query in Collection Tab, IntelliShell, or Aggregation Editor, or embed the Visual Explain plan directly — creating a triage-to-action workflow within a single interface.

## Capability findings

| Capability ID | Finding | Impact |
| --- | --- | --- |
| IDX-009 | All six standard index properties (Unique, Sparse, Hidden, TTL, Partial, Case-insensitive) are configurable via UI without shell commands. | Reduces index creation errors from manual option document construction. |
| IDX-012 | Hide/Unhide index is a first-class UI action — supports safe index impact testing without drop risk. | Eliminates the risk of costly index rebuilds during impact analysis. |
| IDX-013 | Brief mode Visual Explain is always available and fast — no query execution overhead for plan structure inspection. | Makes explain accessible for exploratory inspection, not just formal debugging. |
| IDX-015 | Visual Explain available in SQL Query tool, not just MongoDB query tools — enables explain for SQL-translated aggregation pipelines. | Unique cross-language explain coverage not seen in comparable tools. |
| IDX-016 | Query Profiler with query shape grouping (queryHash) and exact query grouping in the same UI is more analytical than Compass's profiler. | Enables both pattern-level and instance-level slow query triage. |
| IDX-017 | Profiler drill-down → "Add Index on collection" shortcut bridges performance triage to index remediation without leaving the profiler. | Reduces the steps between identifying a slow query and creating the fix. |

## Constraints and risks

- geoHaystack index type (IDX-008) is deprecated in MongoDB 4.4 and removed in 5.0; Studio 3T surfaces it without a deprecation warning — users on newer MongoDB versions will encounter a server error on creation.
- Usage count display requires the $indexStats privilege — teams using least-privilege MongoDB roles may not see usage data.
- Full mode Visual Explain executes the query against the database; running it against expensive queries on production collections can cause load spikes.
- Background index creation (IDX-010) is itself deprecated in MongoDB 4.4 in favor of concurrent builds; Studio 3T does not flag this deprecation in the UI.
- Level 2 profiling captures all operations and can significantly degrade server performance on busy deployments; Studio 3T does not warn the user before enabling Level 2.

## Conclusion

Index management and performance tooling in Studio 3T is comprehensive. The Index Manager covers all MongoDB index types with type-specific options, the Hide/Unhide workflow enables safe impact testing, and Visual Explain spans five query entry points. The Query Profiler's two grouping modes and drill-down integration with other tools create a practical performance triage workflow. The main risks are around deprecated index types not being flagged in the UI and the performance impact of Full mode explain and Level 2 profiling.
