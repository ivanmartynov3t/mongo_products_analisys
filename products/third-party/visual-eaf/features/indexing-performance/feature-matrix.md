# VisuaLeaf — Indexing & Performance Feature Matrix

| ID | Capability | Status | Detail | Source |
|---|---|---|---|---|
| IDX-001 | Index type: Ascending | **confirmed** | Direction: 1; for sorting, filtering, range queries | https://visualeaf.com/docs/index-management |
| IDX-002 | Index type: Descending | **confirmed** | Direction: -1; for reverse sorting | https://visualeaf.com/docs/index-management |
| IDX-003 | Index type: Compound | **confirmed** | Multiple fields; ESR (Equality-Sort-Range) rule guidance | https://visualeaf.com/docs/index-management |
| IDX-004 | Index type: Text | **confirmed** | Type "text"; full-text search, stemming, stop words; max 1 text index per collection; wildcard: $** | https://visualeaf.com/docs/index-management |
| IDX-005 | Index type: Hashed | **confirmed** | Type "hashed"; equality queries and sharding keys; no range queries | https://visualeaf.com/docs/index-management |
| IDX-006 | Index type: 2D | **confirmed** | Type "2d"; flat coordinate systems; [x,y] arrays or {x,y} objects | https://visualeaf.com/docs/index-management |
| IDX-007 | Index type: 2D Sphere | **confirmed** | Type "2dsphere"; Earth-based lat/lng, GeoJSON; supports $geoNear, $geoWithin, $geoIntersects | https://visualeaf.com/docs/index-management |
| IDX-008 | Index type: Wildcard | **confirmed** | Key: $** or fieldName.$**; for flexible/dynamic schemas | https://visualeaf.com/docs/index-management |
| IDX-009 | Index type: TTL | **confirmed** | Single Date field + expireAfterSeconds; auto-delete ~every 60s; use cases: session data, tokens | https://visualeaf.com/docs/index-management |
| IDX-010 | Option: Index Name | **confirmed** | String; auto-generated default (e.g., email_1_status_-1) | https://visualeaf.com/docs/index-management |
| IDX-011 | Option: Unique | **confirmed** | Boolean; default false; enforce value uniqueness | https://visualeaf.com/docs/index-management |
| IDX-012 | Option: Sparse | **confirmed** | Boolean; default false; only index documents containing the field | https://visualeaf.com/docs/index-management |
| IDX-013 | Option: Background | **confirmed** | Boolean; default false; less critical in MongoDB 4.2+ (foreground by default) | https://visualeaf.com/docs/index-management |
| IDX-014 | Option: Hidden | **confirmed** | Boolean; default false; requires MongoDB 4.4+ | https://visualeaf.com/docs/index-management |
| IDX-015 | Option: Expire After Seconds (TTL) | **confirmed** | Integer; seconds after which indexed documents expire | https://visualeaf.com/docs/index-management |
| IDX-016 | Collation Tab: Enable/disable toggle | **confirmed** | Toggle collation options on/off per index | https://visualeaf.com/docs/index-management |
| IDX-017 | Collation Tab: Locale | **confirmed** | 60+ ICU locales (en, fr, de, es, zh, ja, ar, and more) | https://visualeaf.com/docs/index-management |
| IDX-018 | Collation Tab: Strength | **confirmed** | Levels 1–5 (Primary to Identical) | https://visualeaf.com/docs/index-management |
| IDX-019 | Collation Tab: Case Level | **confirmed** | Boolean; case sensitivity at strength 1 or 2 | https://visualeaf.com/docs/index-management |
| IDX-020 | Collation Tab: Case First | **confirmed** | Options: off / upper / lower | https://visualeaf.com/docs/index-management |
| IDX-021 | Collation Tab: Numeric Ordering | **confirmed** | Boolean; sort numbers as numeric values rather than strings | https://visualeaf.com/docs/index-management |
| IDX-022 | Collation Tab: Alternate | **confirmed** | Options: non-ignorable / shifted | https://visualeaf.com/docs/index-management |
| IDX-023 | Collation Tab: Max Variable | **confirmed** | Options: punct / space | https://visualeaf.com/docs/index-management |
| IDX-024 | Collation Tab: Backwards | **confirmed** | Boolean; sort secondary differences from end of string | https://visualeaf.com/docs/index-management |
| IDX-025 | Text Index Tab: Default Language | **confirmed** | 16 languages: none, danish, dutch, english, finnish, french, german, hungarian, italian, norwegian, portuguese, romanian, russian, spanish, swedish, turkish | https://visualeaf.com/docs/index-management |
| IDX-026 | Text Index Tab: Language Override | **confirmed** | Per-document language field name for multi-language collections | https://visualeaf.com/docs/index-management |
| IDX-027 | Text Index Tab: Text Index Version | **confirmed** | Versions 1–3; default 3 (Unicode 8.0 case folding) | https://visualeaf.com/docs/index-management |
| IDX-028 | Text Index Tab: Field Weights | **confirmed** | Custom weight per field; range 1–99,999 | https://visualeaf.com/docs/index-management |
| IDX-029 | Geospatial Tab: Min Value | **confirmed** | Default -180; configurable lower bound for 2d index | https://visualeaf.com/docs/index-management |
| IDX-030 | Geospatial Tab: Max Value | **confirmed** | Default 180; configurable upper bound for 2d index | https://visualeaf.com/docs/index-management |
| IDX-031 | Geospatial Tab: Bits (Geohash precision) | **confirmed** | Default 26; range 1–32; 26 bits ≈ 60cm spatial precision | https://visualeaf.com/docs/index-management |
| IDX-032 | Geospatial Tab: 2dsphere Version | **confirmed** | Default version 3 | https://visualeaf.com/docs/index-management |
| IDX-033 | Advanced Tab: Partial Filter Expression | **confirmed** | JSON editor for partial index filter expression | https://visualeaf.com/docs/index-management |
| IDX-034 | Advanced Tab: Wildcard Projection | **confirmed** | Include/exclude specific fields in a wildcard index | https://visualeaf.com/docs/index-management |
| IDX-035 | Advanced Tab: Storage Engine settings | **confirmed** | Per-index storage engine configuration options | https://visualeaf.com/docs/index-management |
| IDX-036 | Advanced Tab: Commit Quorum | **confirmed** | Replica set commit quorum setting for index build | https://visualeaf.com/docs/index-management |
| IDX-037 | Advanced Tab: Clustered index | **confirmed** | Clustered collection index option | https://visualeaf.com/docs/index-management |
| IDX-038 | Quick Action: Wildcard Text Index | **confirmed** | One-click: $**: text | https://visualeaf.com/docs/index-management |
| IDX-039 | Quick Action: Wildcard Index | **confirmed** | One-click: $**: 1 | https://visualeaf.com/docs/index-management |
| IDX-040 | Quick Action: _id index | **confirmed** | One-click: _id: 1 | https://visualeaf.com/docs/index-management |
| IDX-041 | Quick Action: createdAt index | **confirmed** | One-click: createdAt: -1 | https://visualeaf.com/docs/index-management |
| IDX-042 | Query Profiler: Slow Query Threshold | **confirmed** | Default 100ms; configurable | https://visualeaf.com/docs/query-profiler |
| IDX-043 | Query Profiler: Profiling Levels | **confirmed** | Level 0 (off), 1 (slow queries only), 2 (all queries) | https://visualeaf.com/docs/query-profiler |
| IDX-044 | Query Profiler: Sample Rate | **confirmed** | Default 100%; configurable | https://visualeaf.com/docs/query-profiler |
| IDX-045 | Query Profiler: Max Log Size | **confirmed** | Default 10,000 queries retained | https://visualeaf.com/docs/query-profiler |
| IDX-046 | Query Profiler: Query grouping by shape | **confirmed** | Groups similar queries by query shape for pattern analysis | https://visualeaf.com/docs/query-profiler |
| IDX-047 | Query Profiler: Time range filter | **confirmed** | Filter range: 30 minutes to 30 days | https://visualeaf.com/docs/query-profiler |
| IDX-048 | Query Profiler: COLLSCAN warnings | **confirmed** | COLLSCAN operations prominently flagged in results | https://visualeaf.com/docs/query-profiler |
| IDX-049 | Query Profiler: Export | **confirmed** | Export profiler data as CSV or JSON | https://visualeaf.com/docs/query-profiler |
| IDX-050 | Query Profiler: Percentile lines | **confirmed** | P50, P95, P99 percentile lines on query timeline scatter plot | https://visualeaf.com/docs/query-profiler |
| IDX-051 | Query Profiler: Index recommendations | **confirmed** | Types: Missing Index, Compound Index, Covered Query, Unused Index | https://visualeaf.com/docs/query-profiler |
| IDX-052 | Query Profiler: Explain modes | **confirmed** | queryPlanner, executionStats, allPlansExecution | https://visualeaf.com/docs/query-profiler |
| IDX-053 | Query Profiler: Execution stage types | **confirmed** | COLLSCAN, IXSCAN, FETCH, SORT, PROJECTION | https://visualeaf.com/docs/query-profiler |
| IDX-054 | Query Profiler: Live monitoring | **confirmed** | Current running operations; kill query button; auto-refresh; filter by operation type | https://visualeaf.com/docs/query-profiler |

## Navigation

- [← Product Report](../../product-report.md)
- [Feature Report](feature-report.md)
- [← Schema Validation Matrix](../schema-validation/feature-matrix.md)
- [→ Data Import/Export Matrix](../data-import-export/feature-matrix.md)
- [→ Visual Schema Matrix](../visual-schema/feature-matrix.md)
- [→ Shell Matrix](../shell/feature-matrix.md)
- [→ AI Assistant Matrix](../ai-assistant/feature-matrix.md)
- [→ Security & Governance Matrix](../security-governance/feature-matrix.md)
