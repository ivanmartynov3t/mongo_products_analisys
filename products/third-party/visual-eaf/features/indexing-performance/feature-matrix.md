# Feature Matrix — VisuaLeaf / Indexing & Performance

## Navigation

- [← Product Report](../../product-report.md)
- [Feature Report](feature-report.md)
- [← Schema Matrix](../schema/feature-matrix.md)
- [→ Data Transfer Matrix](../data-transfer/feature-matrix.md)
- [→ Shell Matrix](../shell/feature-matrix.md)
- [→ AI Matrix](../ai/feature-matrix.md)
- [→ Governance Matrix](../governance/feature-matrix.md)
- [→ Task Scheduler Matrix](../task-scheduler/feature-matrix.md)

## Source index

- S1: https://visualeaf.com/docs/index-management
- S2: https://visualeaf.com/docs/query-profiler

## Capability matrix

| Sub-feature ID | Capability | Status | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| IDX-inventory | Index inventory | confirmed | Index list with name, type, and usage statistics; implied by index management UI. Auto-generated default index names (e.g., email_1_status_-1). | — | confirmed | S1 |
| IDX-type-single | Single-field indexes (Ascending/Descending) | confirmed | Ascending: direction 1; for sorting, filtering, range queries. Descending: direction -1; for reverse sorting. | — | confirmed | S1 |
| IDX-type-compound | Compound index | confirmed | Multiple fields; ESR (Equality-Sort-Range) rule guidance provided. | — | confirmed | S1 |
| IDX-type-text | Text index | confirmed | Type "text"; full-text search with stemming and stop words; maximum 1 text index per collection; wildcard: $**. | — | confirmed | S1 |
| IDX-type-hashed | Hashed index | confirmed | Type "hashed"; equality queries and sharding keys; no range queries. | — | confirmed | S1 |
| IDX-type-2d | 2D index | confirmed | Type "2d"; flat coordinate systems; [x,y] arrays or {x,y} objects. | — | confirmed | S1 |
| IDX-type-2dsphere | 2DSphere index | confirmed | Type "2dsphere"; Earth-based lat/lng and GeoJSON; supports $geoNear, $geoWithin, $geoIntersects. | — | confirmed | S1 |
| IDX-type-wildcard | Wildcard index | confirmed | Key: $** or fieldName.$**; for flexible/dynamic schemas. | — | confirmed | S1 |
| IDX-type-ttl | TTL index | confirmed | Single Date field + expireAfterSeconds; documents auto-deleted approximately every 60s; use cases: session data, tokens. Option: Expire After Seconds (integer). | — | confirmed | S1 |
| IDX-props-unique-sparse | Unique and Sparse options | confirmed | Unique: boolean, default false; enforces value uniqueness. Sparse: boolean, default false; only indexes documents containing the field. | — | confirmed | S1 |
| IDX-props-hidden | Hidden index option | confirmed | Boolean; default false; requires MongoDB 4.4+. Allows hiding an index from the query planner without dropping it. | MongoDB 4.4+ required | confirmed | S1 |
| IDX-props-partial | Partial index | confirmed | Partial Filter Expression: JSON editor for partial index filter expression (Advanced Tab). | — | confirmed | S1 |
| IDX-build-mode | Background build mode | confirmed | Boolean; default false; less critical in MongoDB 4.2+ (foreground by default). | — | confirmed | S1 |
| IDX-hide-unhide | Hide/unhide index for planner testing | unknown/unverified | Hide/unhide workflow for planner A/B testing not explicitly documented in VisuaLeaf docs. | — | unknown/unverified | S1 |
| IDX-collation-opts | Collation options | confirmed | Enable/disable toggle; 60+ ICU locales (en, fr, de, es, zh, ja, ar, and more); Strength 1–5 (Primary to Identical); Case Level (boolean); Case First (off/upper/lower); Numeric Ordering (boolean); Alternate (non-ignorable/shifted); Max Variable (punct/space); Backwards (boolean). | — | confirmed | S1 |
| IDX-text-opts | Text index options | confirmed | Default Language: 16 languages (none, danish, dutch, english, finnish, french, german, hungarian, italian, norwegian, portuguese, romanian, russian, spanish, swedish, turkish); Language Override: per-document field name; Text Index Version: 1–3 (default 3, Unicode 8.0); Field Weights: custom weight per field, range 1–99,999. | — | confirmed | S1 |
| IDX-geo-opts | Geospatial index options | confirmed | Min Value: default -180; Max Value: default 180; Bits (geohash precision): default 26, range 1–32 (26 bits ≈ 60cm precision); 2dsphere Version: default 3. | — | confirmed | S1 |
| IDX-advanced-opts | Advanced index options | confirmed | Partial Filter Expression: JSON editor; Wildcard Projection: include/exclude specific fields in wildcard index; Storage Engine config: per-index storage engine options; Commit Quorum: replica set commit quorum for index build; Clustered index: clustered collection index option. | — | confirmed | S1 |
| IDX-quick-actions | Quick action templates | confirmed | Wildcard Text ($**: text); Wildcard ($**: 1); _id (_id: 1); createdAt (createdAt: -1). | — | confirmed | S1 |
| IDX-profiler-config | Query profiler configuration | confirmed | Slow Query Threshold: default 100ms; Profiling Levels: 0 (off), 1 (slow queries only), 2 (all queries); Sample Rate: default 100%; Max Log Size: default 10,000 queries retained. | — | confirmed | S2 |
| IDX-profiler-analysis | Query profiler analysis | confirmed | Query grouping by shape for pattern analysis; time range filter (30 minutes to 30 days); COLLSCAN operations prominently flagged; P50/P95/P99 percentile lines on timeline scatter plot; index recommendations (4 types: Missing Index, Compound Index, Covered Query, Unused Index); execution stage types: COLLSCAN, IXSCAN, FETCH, SORT, PROJECTION. | — | confirmed | S2 |
| IDX-profiler-drilldown | Profiler explain drilldown | confirmed | Explain modes per query: queryPlanner, executionStats, allPlansExecution. | — | confirmed | S2 |
| IDX-profiler-export | Profiler data export | confirmed | Export profiler data as CSV or JSON. | — | confirmed | S2 |
| IDX-explain-brief | Explain — queryPlanner mode | confirmed | queryPlanner: shows winning plan without executing; fastest explain mode. | — | confirmed | S2 |
| IDX-explain-full | Explain — executionStats and allPlansExecution | confirmed | executionStats: executes winning plan and returns runtime stats; allPlansExecution: runs all candidate plans, returns stats for each. | — | confirmed | S2 |
| IDX-profiler-live | Live operations monitoring | confirmed | Current running operations list; auto-refresh; filter by operation type. | — | confirmed | S2 |
| IDX-stop-ops | Kill running operation | confirmed | Kill button for individual running operations from live monitoring view. | — | confirmed | S2 |
