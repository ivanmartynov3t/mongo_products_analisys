# Feature Matrix — Studio 3T / Indexing & Performance

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Source index

- S1: https://studio3t.com/knowledge-base/articles/mongodb-index-strategy/
- S2: https://studio3t.com/knowledge-base/articles/mongodb-explain-visualized/
- S3: https://studio3t.com/knowledge-base/articles/mongodb-query-performance/

## Capability matrix

| Capability ID | Capability | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| IDX-inventory | Index Manager display | Supported | Lists all indexes for a collection: name (expandable to fields + sort order), type, size, usage count. Total index size displayed in bottom-right. Usage count = times used since index creation or last server restart. Side-by-side index view across databases. | Usage display requires the $indexStats privilege on the MongoDB user. | confirmed | S1 | All editions. |
| IDX-type-single | Index type — Single field | Supported | Single field with sort order (1 ascending, -1 descending). Sort order is irrelevant for single-field queries but matters for range queries and sort operations. Studio 3T surfaces this context in the Add Index dialog. | — | confirmed | S1 | All editions. |
| IDX-type-compound | Index type — Compound | Supported | Multiple fields; Studio 3T recommends ESR (Equality, Sort, Range) field ordering. Sort order per field configurable. | ESR ordering is a recommendation, not enforcement. | confirmed | S1 | All editions. |
| IDX-type-multikey | Index type — Multikey | Supported | Array field: MongoDB automatically creates a key per array element. Compound multikey restrictions apply (at most one array field in a compound multikey index). | — | confirmed | S1 | All editions. |
| IDX-type-text | Index type — Text | Supported | Version 1/2/3 (default 3). Default language (English). Language override field. Per-field weights. One text index per collection enforced by MongoDB. | Only one text index per collection is a hard MongoDB constraint, not a Studio 3T limit. | confirmed | S1 | All editions. |
| IDX-type-wildcard | Index type — Wildcard | Supported | $** (all fields) or specific dotted path. Designed for collections with unknown or dynamic field names. | Wildcard indexes have performance trade-offs on large collections; Studio 3T does not warn about these. | confirmed | S1 | All editions. |
| IDX-type-2d | Index type — 2D | Supported | Flat-geometry 2d index; configurable lower/upper bound and bit precision (default 26 bits ≈ 60 cm resolution). | — | confirmed | S1 | All editions. |
| IDX-type-2dsphere | Index type — 2DSphere | Supported | Earth-sphere GeoJSON geospatial index. | — | confirmed | S1 | All editions. |
| IDX-type-haystack | Index type — geoHaystack | Supported with constraints | Bucket size configurable. Deprecated in MongoDB 4.4, removed in MongoDB 5.0. Studio 3T still surfaces this option. | Only useful on MongoDB < 5.0. Creating a geoHaystack index on MongoDB ≥ 5.0 will fail. Studio 3T does not warn about deprecation status. | confirmed | S1 | All editions. Deprecated in MongoDB 4.4; removed in 5.0. |
| IDX-props-unique-sparse | Index properties — Unique & Sparse | Supported | Unique: rejects duplicate field values. Sparse: skips documents missing the indexed field. | — | confirmed | S1 | All editions. |
| IDX-props-hidden | Index properties — Hidden | Supported | Index excluded from query planner but constraints still enforced; requires MongoDB ≥ 4.4 and featureCompatibilityVersion ≥ 4.4. | Requires MongoDB ≥ 4.4 and featureCompatibilityVersion ≥ 4.4. | confirmed | S1 | All editions. |
| IDX-type-ttl | Index type — TTL | Supported | Single-field date-type index with automatic document expiry in seconds. | TTL requires a Date-type field. | confirmed | S1 | All editions. |
| IDX-props-partial | Index properties — Partial | Supported | Filter expression to index only matching documents. | Requires a valid filter expression. | confirmed | S1 | All editions. |
| IDX-props-collation | Index properties — Collation (case-insensitive) | Supported | Case-insensitive index via collation (locale required; strength 1 or 2). | Locale must be specified; case-insensitivity requires strength ≤ 2. | confirmed | S1 | All editions. |
| IDX-build-mode | Background vs foreground index creation | Supported | Unchecked = foreground (compact index, blocks reads + writes during build). Checked = background (non-blocking build, less compact, size converges over time). | Foreground creation is blocking — avoid on production with active traffic. Background index is deprecated in favor of concurrent builds in MongoDB 4.4+. | confirmed | S1 | All editions. |
| IDX-copy-paste | Index operations — Copy / Paste across collections | Supported | Copy index definition from one collection, paste to another collection (even on a different connection). Useful for replicating index strategies across environments. | Destination collection must exist and be writable. | confirmed | S1 | All editions. |
| IDX-hide-unhide | Index operations — Hide / Unhide | Supported | Hide removes the index from query planner consideration without dropping it. Unhide restores it. Allows safe index impact testing. | Requires MongoDB ≥ 4.4 and featureCompatibilityVersion ≥ 4.4. | confirmed | S1 | All editions. |
| IDX-explain-brief | Visual Explain — Brief mode | Supported | Default mode: plan diagram only with no runtime statistics. Always fast and always available regardless of query complexity or collection size. Suitable for plan type verification (COLLSCAN vs IXSCAN). | Brief mode does not show execution time or document counts. | confirmed | S2 | All editions. |
| IDX-explain-full | Visual Explain — Full mode | Supported | Click "Run full explain" to add runtime statistics per stage: output document count, execution time (ms) per stage and total, estimated bytes processed per stage. Hover tooltips on arrows and stage blocks. Per-stage detail: right-click → "What's this?" for description; "View original JSON fragment" for raw JSON scoped to that stage. View full query plan JSON ("View JSON" button). | Full mode executes the query against the database; avoid on expensive queries in production. | confirmed | S2 | All editions. |
| IDX-explain-sources | Visual Explain integration points | Supported | Available in: Collection Tab, IntelliShell (Query Assist tabs), SQL Query tool, Aggregation Editor, and Query Profiler. | IntelliShell Visual Explain only available in Query Assist mode (not Shell mode). | confirmed | S2 | All editions. |
| IDX-profiler-config | Query Profiler | Supported | Reads from MongoDB's system.profile collection. Profiling levels: Level 0 (Off), Level 1 (slow queries > 100ms), Level 2 (all). Studio 3T toggles Level 0 ↔ Level 1. Query grouping: Exact query (unique groups by field names + values) or Query shape (groups by structure; shows queryHash column). Filters by collection and timeframe (e.g., last 30 days). | Requires MongoDB Database Profiler enabled; $indexStats privilege required for usage display. Level 2 profiling can significantly impact server performance. | confirmed | S3 | All editions. |
| IDX-profiler-drilldown | Query Profiler drill-down and integration | Supported | Per-execution detail: Duration, Timestamp, Keys Examined, planSummary. Actions: View Full JSON (system.profile document), Query Code tab (MongoDB Shell syntax), "Open in IntelliShell", "Open in Collection Tab" (find queries), "Open in Aggregation Editor" (aggregation), Explain plan tab (embedded Visual Explain). Right-click context → "Add Index on collection" shortcut. | "Open in Collection Tab" and "Open in Aggregation Editor" require the relevant query type. | confirmed | S3 | All editions. |
