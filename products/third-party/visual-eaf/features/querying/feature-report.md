# VisuaLeaf — Querying Feature Report

## Summary

VisuaLeaf's collection querying supports four view modes (Tree, Table, BSON, Explain), a full find()-style JSON editor with ACE syntax highlighting and schema-aware auto-complete (Ctrl+Space), and three progressive query-building tiers: a raw JSON editor (all plans), a Visual Query Builder with AND/OR nested logic and type-aware inputs (Basic+), and an AI-powered natural language query builder (Professional). Document editing covers inline editing in Tree View, dialog editing with full ACE, batch operations with MongoDB update operators in Table View, and context-menu field operations. Query history and saved queries (Basic+) enable reuse and team sharing.

---

## Strengths

- **Four view modes:** Tree (hierarchical, type-colored, inline edit), Table (sortable, resizable, multi-select), BSON (EJSON-aware), and Explain (index analysis) — more modes than most tools.
- **Bidirectional VQB/JSON sync:** Visual Query Builder and JSON editor stay in sync in real time; users can start visually and switch to JSON for precision edits.
- **Batch editing with MongoDB operators:** $set, $unset, $inc, $push, $pull all available in Table View batch update — uncommon in GUI tools.
- **Type-aware VQB inputs:** Date pickers, number sliders, boolean toggles prevent accidental type coercion mistakes.
- **Execution timer with amber/red thresholds:** 2s amber, 5s red — immediate performance signal without opening a profiler.
- **Multiple copy formats:** JSON, EJSON, value, field name, dot-notation path — essential for developer workflows.
- **AI query builder with 11 OpenAI models and explicit privacy control:** "Send Schema Only" mode for privacy-sensitive environments; plain-English explanation on every result.

---

## Limitations / Gaps

- **VQB requires Basic+ plan:** Community users have JSON editor only; no visual query building.
- **AI requires Professional plan:** $149/year step up for natural language queries.
- **Skip dropdown limited to 0/50/100:** No manual skip entry documented; large-collection offset navigation is constrained.
- **SQL Query Mode:** Referenced in "Open In" context menu but no documentation found — **unknown/unverified**.
- **Chart Builder:** Referenced in "Open In" but no dedicated chart documentation found — **unknown/unverified**.
- **findAndModify / replaceOne:** Replace-whole-document operation not directly exposed in the UI.

---

## Comparison Notes (vs MongoDB Compass baseline)

| Aspect | VisuaLeaf | MongoDB Compass |
|---|---|---|
| View modes | Tree, Table, BSON, Explain | JSON list, Table, List |
| Visual Query Builder | **confirmed** (Basic+) | **confirmed** (all plans) |
| AND/OR nested logic in VQB | **confirmed** (Basic+) | **confirmed** |
| AI query builder | **confirmed** (Professional) | not available |
| Batch editing with operators | **confirmed** ($set, $unset, $inc, $push, $pull) | limited |
| Query history | **confirmed** (Basic+) | **confirmed** (all plans) |
| Saved queries / export | **confirmed** (Basic+, JSON export) | **confirmed** (all plans) |
| EJSON copy | **confirmed** | **confirmed** |
| Inline document editing | **confirmed** (Tree View) | **confirmed** |
| Explain View (embedded) | **confirmed** | **confirmed** (separate Analysis tab) |
| Execution timer with thresholds | **confirmed** (2s/5s amber/red) | basic spinner only |
| Projection Builder (visual) | **confirmed** (VQB, Basic+) | **confirmed** |

---

## Navigation

- [← Product Report](../../product-report.md)
- [Feature Matrix](feature-matrix.md)
- [← Connectivity](../connectivity/feature-report.md)
- [→ Aggregation](../aggregation/feature-report.md)
- [→ Schema Validation](../schema-validation/feature-report.md)
- [→ Indexing & Performance](../indexing-performance/feature-report.md)
- [→ Data Import/Export](../data-import-export/feature-report.md)
- [→ Visual Schema Designer](../visual-schema/feature-report.md)
- [→ MongoDB Shell](../shell/feature-report.md)
- [→ AI Assistant](../ai-assistant/feature-report.md)
- [→ Security & Governance](../security-governance/feature-report.md)
