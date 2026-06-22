# VisuaLeaf — Aggregation Feature Report

## Summary

VisuaLeaf's Aggregation Pipeline Builder provides a visual, dual-mode stage editor with 37+ MongoDB pipeline stages. Each stage can be configured in Form Mode (visual dropdowns with schema auto-complete and a Visual Query Builder integration for $match) or MongoDB Editor mode (Monaco with IntelliSense), switchable per-stage with preference saved. A real-time input/output split preview panel shows 20 sampled documents per stage. Pipelines export to .js files (mongosh-compatible), can be imported back, and results export to JSON/CSV/BSON/SQL. Saved pipelines are organized in folder hierarchies tagged by connection, database, and collection.

---

## Strengths

- **37+ stages:** Complete coverage including modern stages like $densify, $fill, $setWindowFields, $graphLookup, $facet, $search (Atlas), $merge, $out, $documents, and diagnostic stages ($collStats, $indexStats, $planCacheStats, $listSearchIndexes).
- **Dual-mode per stage:** Form Mode for guided input; Monaco Editor for power users — mode preference persisted per stage, not globally.
- **Monaco IntelliSense:** Field names, operators, and MongoDB function auto-complete in each stage's JSON editor — same engine as VS Code.
- **Per-stage input/output preview:** Side-by-side split view with 20-doc sample; auto-preview updates on every config change.
- **mongosh-compatible .js export:** Pipelines export as `db.collection.aggregate([…])`, runnable directly in mongosh or importable by Compass.
- **Bidirectional JSON code view:** Edit raw JSON pipeline and sync changes back to the visual stage builder.
- **Accumulator expression builder:** Visual builder for $sum, $avg, $max, $min, $first, $last, $push, $addToSet in $group — eliminates manual accumulator syntax errors.
- **Result export to 4 formats:** JSON, CSV, BSON, SQL INSERT — covers migration and analytics export needs.

---

## Limitations / Gaps

- **Atlas-only stages without guards:** $search and $listSearchIndexes will error on non-Atlas deployments; no documented warning or guard in the UI.
- **$out/$merge preview disabled:** Cannot preview terminal stage effects before execution — expected by design, but noted.
- **Allow Disk Use defaults to false:** Large aggregations on unindexed data will hit memory limits without manually toggling.
- **Max Time default 300s:** Long-running analytical pipelines may time out without manual adjustment.
- **Chart Builder not documented:** "Create Chart" referenced in export but no dedicated documentation found — **unknown/unverified** implementation.
- **No AI assistance in aggregation builder directly:** AI-generated aggregation pipelines are available through the AI Assistant (Professional), not from within the visual pipeline builder itself.

---

## Comparison Notes (vs MongoDB Compass baseline)

| Aspect | VisuaLeaf | MongoDB Compass |
|---|---|---|
| Stage count in palette | 37+ | ~30 (varies by version) |
| Per-stage mode (visual vs JSON) | **confirmed** (switchable per stage) | JSON editor per stage only |
| Editor engine for stages | Monaco (VS Code) | CodeMirror |
| Per-stage IntelliSense | **confirmed** (fields, operators, functions) | limited |
| Per-stage input/output preview | **confirmed** (auto-preview, 20 docs) | **confirmed** (20-doc preview) |
| Export to .js (mongosh format) | **confirmed** | **confirmed** |
| Import pipeline from .js | **confirmed** | **confirmed** |
| Save/load pipelines | **confirmed** (folder hierarchy) | **confirmed** (no folders) |
| Allow Disk Use toggle | **confirmed** | **confirmed** |
| Export results to CSV | **confirmed** | **confirmed** |
| Export results to SQL INSERT | **confirmed** | not available |
| $search (Atlas) stage | **confirmed** | **confirmed** |
| $densify / $fill / $setWindowFields | **confirmed** | **confirmed** (newer versions) |
| Accumulator expression visual builder | **confirmed** ($sum, $avg, $max, $min, $first, $last, $push, $addToSet) | not available |

---

## Navigation

- [← Product Report](../../product-report.md)
- [Feature Matrix](feature-matrix.md)
- [← Querying](../querying/feature-report.md)
- [→ Schema Validation](../schema-validation/feature-report.md)
- [→ Indexing & Performance](../indexing-performance/feature-report.md)
- [→ Data Import/Export](../data-import-export/feature-report.md)
- [→ Visual Schema Designer](../visual-schema/feature-report.md)
- [→ MongoDB Shell](../shell/feature-report.md)
- [→ AI Assistant](../ai-assistant/feature-report.md)
- [→ Security & Governance](../security-governance/feature-report.md)
