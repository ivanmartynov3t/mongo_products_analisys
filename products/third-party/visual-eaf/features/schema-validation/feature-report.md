# VisuaLeaf — Schema Validation Feature Report

## Summary

VisuaLeaf's Schema Validation module provides a tree-based, visually navigable $jsonSchema editor. It supports all 15 BSON types with per-type validation constraints, polymorphic fields (multiple types per field), and full nested object/array handling. Schemas are organized in a local library with folder hierarchy, can be imported from the database via a 100-document sample analysis, deployed directly as collection validators, verified against live collection data, and exported as standard $jsonSchema-compatible JSON. Requires Basic+ plan.

---

## Strengths

- **Full BSON type coverage:** 15 BSON types including Decimal128, ObjectId, BinData, Timestamp — beyond what standard JSON Schema alone supports.
- **Polymorphic field support:** Multiple types per field (e.g., `string | null`) correctly reflected in `$jsonSchema` `bsonType` arrays.
- **Import schema from live collection:** Auto-generates schema by analyzing 100 documents — useful for documenting and enforcing structure on legacy collections.
- **Verification against live data:** Runs `$jsonSchema` query filter and surfaces all non-matching documents in a new activity tab — a one-click data quality audit.
- **Direct deployment to MongoDB:** Push schema as `collMod` validator from UI without manual shell commands.
- **Two-tab manager separation:** Saved Schemas (local library) vs MongoDB Schemas (live collection validators) aids workflow clarity.
- **Export as $jsonSchema-compatible JSON:** Works with `db.runCommand({collMod})` and external schema registries; follows JSON Schema Draft 4 + BSON extensions.

---

## Limitations / Gaps

- **Requires Basic+ plan:** Community users have no access to schema validation.
- **Sample size fixed at 100 docs for import:** May not accurately represent collections with highly diverse schemas (e.g., multi-tenant collections).
- **JSON Schema Draft 4 only:** Modern keywords (if/then/else, $ref, $defs, anyOf beyond bsonType arrays) are **unknown/unverified** — likely not supported.
- **additionalProperties UI detail unclear:** Whether the UI generates `additionalProperties: false` or merely informs the user is not explicitly documented.
- **No schema versioning:** No built-in version history or diff between schema revisions.
- **Validation action (error vs. warn) not surfaced:** MongoDB 5.0+ supports `validationAction: "warn"` in addition to `"error"` — whether the UI exposes this is **unknown/unverified**.

---

## Comparison Notes (vs MongoDB Compass baseline)

| Aspect | VisuaLeaf | MongoDB Compass |
|---|---|---|
| Schema validation editor | **confirmed** (tree-based, per-field constraints) | JSON editor only (via `$jsonSchema` raw JSON) |
| BSON type coverage | 15 types including Decimal128, ObjectId, BinData | full BSON via raw $jsonSchema |
| Import schema from collection | **confirmed** (100-doc sample analysis) | not available |
| Deploy validator to collection | **confirmed** (direct from UI) | requires raw `runCommand` or Documents tab |
| Verify schema against live data | **confirmed** (opens non-matching docs tab) | not built-in |
| Export as .json | **confirmed** | copy from JSON editor |
| Polymorphic fields | **confirmed** (visual multi-type) | **confirmed** (manual JSON) |
| Plan required | Basic+ | all plans |

---

## Navigation

- [← Product Report](../../product-report.md)
- [Feature Matrix](feature-matrix.md)
- [← Aggregation](../aggregation/feature-report.md)
- [→ Indexing & Performance](../indexing-performance/feature-report.md)
- [→ Data Import/Export](../data-import-export/feature-report.md)
- [→ Visual Schema Designer](../visual-schema/feature-report.md)
- [→ MongoDB Shell](../shell/feature-report.md)
- [→ AI Assistant](../ai-assistant/feature-report.md)
- [→ Security & Governance](../security-governance/feature-report.md)
