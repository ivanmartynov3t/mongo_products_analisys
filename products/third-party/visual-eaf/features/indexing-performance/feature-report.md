# VisuaLeaf — Indexing & Performance Feature Report

## Summary

VisuaLeaf's index management provides a comprehensive index creation UI supporting all 9 MongoDB index types, each with type-specific configuration tabs: General (name, unique, sparse, background, hidden, TTL), Collation (60+ ICU locales, 5 strength levels, 8 sub-options), Text Index (16 languages, field weights 1–99,999, version), Geospatial (bits precision 1–32, min/max bounds, 2dsphere version), and Advanced (partial filter, wildcard projection, storage engine, commit quorum, clustered). The Query Profiler integrates performance analysis with P50/P95/P99 timeline visualization, query shape grouping, four index recommendation types, and live operation monitoring with kill capability.

---

## Strengths

- **All 9 index types covered:** Ascending, Descending, Compound, Text, Hashed, 2D, 2DSphere, Wildcard, TTL — complete taxonomy.
- **Collation configuration depth:** 60+ ICU locales, 5 strength levels, Case Level/First, Numeric Ordering, Alternate, Max Variable, Backwards — detailed enough for i18n-sensitive index design.
- **Text index weight configuration:** Per-field weights (1–99,999) with 16 language options and language override field — full text index lifecycle management.
- **Geospatial precision control:** Bits (geohash precision) configurable 1–32 with default 26 (≈60cm) — unusual granularity in GUI tools.
- **Partial filter expression JSON editor:** Enables partial index creation without manual shell commands.
- **P50/P95/P99 percentiles on profiler timeline:** Statistical distribution beyond simple max/average — required for SLA analysis.
- **Four index recommendation types:** Missing Index, Compound Index, Covered Query, Unused Index — actionable guidance surfaced automatically.
- **Live operation kill:** Terminate in-flight queries from the profiler UI without requiring a separate shell session.
- **Query shape grouping:** Pattern-level analysis groups similar queries, reducing noise from individual query variation.

---

## Limitations / Gaps

- **No index size / memory footprint display:** Index memory consumption per index not shown in the index list.
- **Background build flag UI:** Less relevant since MongoDB 4.2 (foreground builds no longer block) but still surfaced — may confuse users on modern clusters.
- **Commit Quorum and Clustered index options underdocumented:** Advanced tab fields present but not detailed in public documentation.
- **Query profiler requires system.profile:** Standard MongoDB prerequisite but no documented auto-enable or guided setup workflow.
- **COLLSCAN warning threshold fixed:** No documented customization of COLLSCAN warning vs. OK boundary (other than the slow query threshold).
- **Index usage statistics:** $indexStats-based visualization outside the aggregation stage ($indexStats) is not mentioned.

---

## Comparison Notes (vs MongoDB Compass baseline)

| Aspect | VisuaLeaf | MongoDB Compass |
|---|---|---|
| Index types | All 9 (including Wildcard, TTL, 2D, 2DSphere) | All 9 |
| Collation configuration | **confirmed** (60+ locales, 5 strengths, 8 options) | **confirmed** (basic collation options) |
| Text index field weights | **confirmed** (per-field, 1–99,999) | not available in UI |
| Geospatial bits precision | **confirmed** (1–32, default 26) | not exposed |
| Partial filter expression | **confirmed** (JSON editor) | **confirmed** |
| Hidden index (MongoDB 4.4+) | **confirmed** | **confirmed** |
| Query Profiler | **confirmed** (built-in, P50/P95/P99, shape grouping) | **confirmed** (basic profiler) |
| Index recommendations | **confirmed** (4 types) | **confirmed** (index suggestions) |
| Live kill query | **confirmed** | not available |
| P50/P95/P99 percentile lines | **confirmed** | not available |
| Export profiler data | **confirmed** (CSV, JSON) | not available |

---

## Navigation

- [← Product Report](../../product-report.md)
- [Feature Matrix](feature-matrix.md)
- [← Schema Validation](../schema/feature-report.md)
- [→ Data Import/Export](../data-transfer/feature-report.md)
- [→ Schema Designer](../schema/feature-report.md)
- [→ MongoDB Shell](../shell/feature-report.md)
- [→ AI Assistant](../ai/feature-report.md)
- [→ Security & Governance](../governance/feature-report.md)
