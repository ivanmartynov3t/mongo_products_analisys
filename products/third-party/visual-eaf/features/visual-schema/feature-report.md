# VisuaLeaf — Visual Schema Designer Feature Report

## Summary

VisuaLeaf's Visual Schema Designer provides an infinite canvas with drag-and-drop collection placement, free positioning, auto-arrange, and graph-theory–based automatic relationship detection. Collections can be color-coded (11 presets via right-click), and relationship links can be found or removed individually or in bulk via multi-selection. Schema diagrams can be auto-generated from the live database and exported/imported for sharing. Requires Basic+ plan.

---

## Strengths

- **Infinite canvas with free positioning:** Unrestricted layout; supports very large schemas with many collections.
- **Graph theory relationship detection:** Automatic relationship inference beyond simple key-name string matching.
- **Auto-generate from database:** One-click diagram generation from all live collections — no manual collection-by-collection setup.
- **Auto-arrange:** Instant organized layout from a cluttered free-form canvas.
- **Multi-selection bulk operations:** Color, find links, remove links, delete — across multiple collections simultaneously.
- **11 color presets:** Visual grouping by domain, service, or team ownership.
- **Export/import diagrams:** Save and restore canvas layouts across sessions or share with team members.

---

## Limitations / Gaps

- **Export format not documented:** The file format for exported diagrams is **unknown/unverified** — prevents assessing portability or toolchain compatibility.
- **Relationship metadata not documented:** How relationships are persisted (field name, type, cardinality) is **unknown/unverified**.
- **No formal ER notation:** No documented support for formal ER/UML cardinality notation (1:1, 1:N, M:N) on relationship lines.
- **Relationship detection heuristic undocumented:** "Graph theory–based" is stated but the specific heuristic (field name matching, ObjectId type matching, naming convention, etc.) is not detailed.
- **Basic+ plan required:** Community users cannot access schema visualization.
- **No multi-database diagram:** Whether collections from different databases or connections can appear on the same canvas is **unknown/unverified**.

---

## Comparison Notes (vs MongoDB Compass baseline)

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
- [← Data Import/Export](../data-import-export/feature-report.md)
- [→ MongoDB Shell](../shell/feature-report.md)
- [→ AI Assistant](../ai-assistant/feature-report.md)
- [→ Security & Governance](../security-governance/feature-report.md)
