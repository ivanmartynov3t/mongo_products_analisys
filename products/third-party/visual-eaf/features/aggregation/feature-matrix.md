# VisuaLeaf — Aggregation Feature Matrix

| ID | Capability | Status | Detail | Source |
|---|---|---|---|---|
| AGG-001 | Stage: $match | **confirmed** | Filter stage; uses Visual Query Builder or raw JSON | https://visualeaf.com/docs/aggregation |
| AGG-002 | Stage: $limit | **confirmed** | Filter stage; integer limit on document count | https://visualeaf.com/docs/aggregation |
| AGG-003 | Stage: $skip | **confirmed** | Filter stage; skip N documents | https://visualeaf.com/docs/aggregation |
| AGG-004 | Stage: $sample | **confirmed** | Filter stage; randomly selects N documents | https://visualeaf.com/docs/aggregation |
| AGG-005 | Stage: $count | **confirmed** | Filter stage; counts matching documents, outputs count field | https://visualeaf.com/docs/aggregation |
| AGG-006 | Stage: $project | **confirmed** | Transformation stage; include/exclude/compute fields | https://visualeaf.com/docs/aggregation |
| AGG-007 | Stage: $addFields | **confirmed** | Transformation stage; add computed fields | https://visualeaf.com/docs/aggregation |
| AGG-008 | Stage: $set | **confirmed** | Transformation stage; alias for $addFields | https://visualeaf.com/docs/aggregation |
| AGG-009 | Stage: $unset | **confirmed** | Transformation stage; remove fields from documents | https://visualeaf.com/docs/aggregation |
| AGG-010 | Stage: $sort | **confirmed** | Transformation stage; sort ascending (1) or descending (-1) per field | https://visualeaf.com/docs/aggregation |
| AGG-011 | Stage: $unwind | **confirmed** | Transformation stage; deconstruct array fields | https://visualeaf.com/docs/aggregation |
| AGG-012 | Stage: $replaceRoot | **confirmed** | Transformation stage; promote subdocument to root | https://visualeaf.com/docs/aggregation |
| AGG-013 | Stage: $replaceWith | **confirmed** | Transformation stage; alias for $replaceRoot | https://visualeaf.com/docs/aggregation |
| AGG-014 | Stage: $redact | **confirmed** | Transformation stage; restrict document content per ACL rules | https://visualeaf.com/docs/aggregation |
| AGG-015 | Stage: $densify | **confirmed** | Transformation stage; fill gaps in numeric/date sequences | https://visualeaf.com/docs/aggregation |
| AGG-016 | Stage: $fill | **confirmed** | Transformation stage; fill null/missing field values | https://visualeaf.com/docs/aggregation |
| AGG-017 | Stage: $setWindowFields | **confirmed** | Transformation stage; window functions over ordered document sets | https://visualeaf.com/docs/aggregation |
| AGG-018 | Stage: $group | **confirmed** | Group stage; group by _id expression with accumulators | https://visualeaf.com/docs/aggregation |
| AGG-019 | Stage: $bucket | **confirmed** | Group stage; categorize documents into defined buckets | https://visualeaf.com/docs/aggregation |
| AGG-020 | Stage: $bucketAuto | **confirmed** | Group stage; auto-determine bucket boundaries | https://visualeaf.com/docs/aggregation |
| AGG-021 | Stage: $sortByCount | **confirmed** | Group stage; sort by occurrence count | https://visualeaf.com/docs/aggregation |
| AGG-022 | Stage: $lookup | **confirmed** | Join stage; left outer join with another collection | https://visualeaf.com/docs/aggregation |
| AGG-023 | Stage: $graphLookup | **confirmed** | Join stage; recursive graph traversal across collection | https://visualeaf.com/docs/aggregation |
| AGG-024 | Stage: $unionWith | **confirmed** | Join stage; union documents from another collection | https://visualeaf.com/docs/aggregation |
| AGG-025 | Stage: $facet | **confirmed** | Multi-pipeline stage; run multiple sub-pipelines simultaneously | https://visualeaf.com/docs/aggregation |
| AGG-026 | Stage: $out | **confirmed** | Output stage; write results to a collection (replaces existing) | https://visualeaf.com/docs/aggregation |
| AGG-027 | Stage: $merge | **confirmed** | Output stage; merge results into an existing collection | https://visualeaf.com/docs/aggregation |
| AGG-028 | Stage: $geoNear | **confirmed** | Geospatial stage; orders documents by geographic proximity | https://visualeaf.com/docs/aggregation |
| AGG-029 | Stage: $search (Atlas) | **confirmed** | Atlas Search stage; full-text search via Lucene indexes | https://visualeaf.com/docs/aggregation |
| AGG-030 | Stage: $documents | **confirmed** | Literal stage; returns a hardcoded sequence of documents | https://visualeaf.com/docs/aggregation |
| AGG-031 | Stage: $collStats | **confirmed** | Stats stage; collection-level statistics | https://visualeaf.com/docs/aggregation |
| AGG-032 | Stage: $indexStats | **confirmed** | Stats stage; index usage statistics | https://visualeaf.com/docs/aggregation |
| AGG-033 | Stage: $planCacheStats | **confirmed** | Stats stage; query plan cache statistics | https://visualeaf.com/docs/aggregation |
| AGG-034 | Stage: $listSearchIndexes | **confirmed** | Atlas stage; list Atlas Search indexes on a collection | https://visualeaf.com/docs/aggregation |
| AGG-035 | Total stage count | **confirmed** | 37+ stages in palette | https://visualeaf.com/docs/aggregation |
| AGG-036 | Stage config: Form Mode (Visual) | **confirmed** | Field dropdowns with schema auto-complete; Visual Query Builder integration for $match; data type validation | https://visualeaf.com/docs/aggregation |
| AGG-037 | Stage config: Accumulator expression builder | **confirmed** | Visual builder for $sum, $avg, $max, $min, $first, $last, $push, $addToSet in $group | https://visualeaf.com/docs/aggregation |
| AGG-038 | Stage config: MongoDB Editor (Raw JSON) | **confirmed** | Monaco editor per stage with MongoDB-aware syntax highlighting | https://visualeaf.com/docs/aggregation |
| AGG-039 | Stage config: Monaco IntelliSense | **confirmed** | Field names, operators, MongoDB functions auto-complete in Monaco editor | https://visualeaf.com/docs/aggregation |
| AGG-040 | Stage config: Real-time validation | **confirmed** | Real-time error detection and highlighting in Monaco editor | https://visualeaf.com/docs/aggregation |
| AGG-041 | Stage config: Mode switch per stage | **confirmed** | Form Mode ↔ MongoDB Editor toggleable per individual stage; preference saved per stage | https://visualeaf.com/docs/aggregation |
| AGG-042 | Stage Preview: Input/Output split view | **confirmed** | Side-by-side panel showing stage input and output documents | https://visualeaf.com/docs/aggregation |
| AGG-043 | Stage Preview: Auto-Preview mode | **confirmed** | Updates stage preview on every config change; toggleable on/off | https://visualeaf.com/docs/aggregation |
| AGG-044 | Stage Preview: Sample limit | **confirmed** | 20 documents sampled for quick per-stage preview | https://visualeaf.com/docs/aggregation |
| AGG-045 | Stage Preview: Disabled for terminal stages | **confirmed** | $out and $merge stages have preview disabled (would write to collection) | https://visualeaf.com/docs/aggregation |
| AGG-046 | Stage Preview: Resizable panels | **confirmed** | Input and output panels are individually resizable; doc count shown | https://visualeaf.com/docs/aggregation |
| AGG-047 | Execution: Allow Disk Use toggle | **confirmed** | Default: false; toggle to allow large in-memory sort overflow to disk | https://visualeaf.com/docs/aggregation |
| AGG-048 | Execution: Max Time | **confirmed** | Default: 300 seconds; configurable maximum execution time | https://visualeaf.com/docs/aggregation |
| AGG-049 | Execution: Auto Collapse stages | **confirmed** | Default: false; collapses all stage cards for pipeline overview | https://visualeaf.com/docs/aggregation |
| AGG-050 | Execution: Pagination for large results | **confirmed** | First / Previous / Next / Last navigation for paginated results | https://visualeaf.com/docs/aggregation |
| AGG-051 | Execution: Live timer + cancel | **confirmed** | Real-time execution timer with cancel button to abort pipeline | https://visualeaf.com/docs/aggregation |
| AGG-052 | Keyboard: Ctrl+Enter execute | **confirmed** | Execute pipeline | https://visualeaf.com/docs/aggregation |
| AGG-053 | Keyboard: Ctrl+S save | **confirmed** | Save current pipeline | https://visualeaf.com/docs/aggregation |
| AGG-054 | Keyboard: Delete stage | **confirmed** | Delete key removes selected stage | https://visualeaf.com/docs/aggregation |
| AGG-055 | Keyboard: Ctrl+D duplicate stage | **confirmed** | Duplicate selected stage | https://visualeaf.com/docs/aggregation |
| AGG-056 | Keyboard: Ctrl+Space auto-complete | **confirmed** | Triggers IntelliSense in MongoDB Editor mode | https://visualeaf.com/docs/aggregation |
| AGG-057 | Export: Pipeline to .js file | **confirmed** | Exports as mongosh format: db.collection.aggregate([…]) | https://visualeaf.com/docs/aggregation |
| AGG-058 | Import: Pipeline from .js file | **confirmed** | Reimport previously exported .js pipeline | https://visualeaf.com/docs/aggregation |
| AGG-059 | Query Code tab: bidirectional JSON | **confirmed** | Read-only or editable JSON; Format Code; Apply Code Changes syncs back to visual builder | https://visualeaf.com/docs/aggregation |
| AGG-060 | Export Results: JSON | **confirmed** | Export pipeline output as JSON | https://visualeaf.com/docs/aggregation |
| AGG-061 | Export Results: CSV | **confirmed** | Export pipeline output as CSV | https://visualeaf.com/docs/aggregation |
| AGG-062 | Export Results: BSON | **confirmed** | Export pipeline output as BSON | https://visualeaf.com/docs/aggregation |
| AGG-063 | Export Results: SQL INSERT | **confirmed** | Export pipeline output as SQL INSERT statements | https://visualeaf.com/docs/aggregation |
| AGG-064 | Create Chart from pipeline | **confirmed** | Opens Chart Builder using pipeline as data source | https://visualeaf.com/docs/aggregation |
| AGG-065 | Save/load pipelines with folder hierarchy | **confirmed** | Save with name, folder, description; tagged with connection/DB/collection; quick load by double-click | https://visualeaf.com/docs/aggregation |

## Navigation

- [← Product Report](../../product-report.md)
- [Feature Report](feature-report.md)
- [← Querying Matrix](../querying/feature-matrix.md)
- [→ Schema Validation Matrix](../schema-validation/feature-matrix.md)
- [→ Indexing & Performance Matrix](../indexing-performance/feature-matrix.md)
- [→ Data Import/Export Matrix](../data-import-export/feature-matrix.md)
- [→ Visual Schema Matrix](../visual-schema/feature-matrix.md)
- [→ Shell Matrix](../shell/feature-matrix.md)
- [→ AI Assistant Matrix](../ai-assistant/feature-matrix.md)
- [→ Security & Governance Matrix](../security-governance/feature-matrix.md)
