# VisuaLeaf — Schema Feature Report

## Summary

VisuaLeaf's Schema feature combines two distinct capabilities: **Schema Validation** and **Visual Schema Designer**. The validation module provides a tree-based $jsonSchema editor with full BSON type support (15 types including Decimal128), polymorphic fields, import-from-collection auto-generation, direct deployment to MongoDB, and live verification against collection data. The visual designer provides an infinite canvas with auto-generated ERD diagrams, graph-theory relationship detection, 11 color presets, named layouts, and diagram portability. Both require Basic or Professional plan.

---

## Schema Validation

### Strengths

- **Full BSON type coverage:** 15 BSON types including Decimal128, ObjectId, BinData, Timestamp — beyond what standard JSON Schema alone supports.
- **Polymorphic field support:** Multiple types per field (e.g., `string | null`) correctly reflected in `$jsonSchema` `bsonType` arrays.
- **Import schema from live collection:** Auto-generates schema by analyzing 100 documents — useful for documenting and enforcing structure on legacy collections.
- **Verification against live data:** Runs `$jsonSchema` query filter and surfaces all non-matching documents in a new activity tab — one-click data quality audit.
- **Direct deployment to MongoDB:** Push schema as `collMod` validator from UI without manual shell commands.
- **Two-tab manager separation:** Saved Schemas (local library) vs MongoDB Schemas (live collection validators) aids workflow clarity.
- **Export as $jsonSchema-compatible JSON:** Works with `db.runCommand({collMod})` and external schema registries; follows JSON Schema Draft 4 + BSON extensions.

### Limitations / Gaps

- **Requires Basic+ plan:** Community users have no access to schema validation.
- **Sample size fixed at 100 docs for import:** May not accurately represent collections with highly diverse schemas (e.g., multi-tenant collections).
- **JSON Schema Draft 4 only:** Modern keywords (if/then/else, $ref, $defs, anyOf beyond bsonType arrays) are **unknown/unverified** — likely not supported.
- **additionalProperties UI detail unclear:** Whether the UI generates `additionalProperties: false` or merely informs the user is not explicitly documented.
- **No schema versioning:** No built-in version history or diff between schema revisions.
- **Validation action (error vs. warn) not surfaced:** MongoDB 5.0+ supports `validationAction: "warn"` in addition to `"error"` — whether the UI exposes this is **unknown/unverified**.

### Comparison Notes (vs MongoDB Compass)

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

## Visual Schema Designer

### Strengths

- **Infinite canvas with free positioning:** Unrestricted layout; supports very large schemas with many collections.
- **Graph theory relationship detection:** Automatic relationship inference beyond simple key-name string matching.
- **Auto-generate from database:** One-click diagram generation from all live collections — no manual collection-by-collection setup.
- **Auto-arrange:** Instant organized layout from a cluttered free-form canvas.
- **Multi-selection bulk operations:** Color, find links, remove links, delete — across multiple collections simultaneously.
- **11 color presets:** Visual grouping by domain, service, or team ownership.
- **Export/import diagrams:** Save and restore canvas layouts across sessions or share with team members.

### Limitations / Gaps

- **Export format not documented:** The file format for exported diagrams is **unknown/unverified** — prevents assessing portability or toolchain compatibility.
- **Relationship metadata not documented:** How relationships are persisted (field name, type, cardinality) is **unknown/unverified**.
- **No formal ER notation:** No documented support for formal ER/UML cardinality notation (1:1, 1:N, M:N) on relationship lines.
- **Relationship detection heuristic undocumented:** "Graph theory–based" is stated but the specific heuristic (field name matching, ObjectId type matching, naming convention, etc.) is not detailed.
- **Basic+ plan required:** Community users cannot access schema visualization.
- **No multi-database diagram:** Whether collections from different databases or connections can appear on the same canvas is **unknown/unverified**.

### Comparison Notes (vs MongoDB Compass)

| Aspect | VisuaLeaf | MongoDB Compass |
|---|---|---|
| Visual schema diagram | **confirmed** (infinite canvas) | not available (Schema Analysis tab shows field types, not ER diagram) |
| Auto-generate from database | **confirmed** | n/a |
| Automatic relationship detection | **confirmed** (graph theory) | not available |
| Color coding collections | **confirmed** (11 presets) | not available |
| Export/import diagram | **confirmed** | not available |
| Multi-selection bulk operations | **confirmed** | not available |
| Plan required | Basic+ | N/A |

---

## Navigation

- [← Product Report](../../product-report.md)
- [Feature Matrix](feature-matrix.md)
- [← Aggregation](../aggregation/feature-report.md)
- [→ Indexing & Performance](../indexing-performance/feature-report.md)
- [→ Data Transfer](../data-transfer/feature-report.md)
- [→ MongoDB Shell](../shell/feature-report.md)
- [→ AI Features](../ai/feature-report.md)
- [→ Governance](../governance/feature-report.md)
