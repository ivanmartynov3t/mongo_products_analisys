# VisuaLeaf — MongoDB Shell Feature Report

## Summary

VisuaLeaf's MongoDB Shell embeds a Monaco (VS Code–engine) editor with full JavaScript/MongoDB syntax highlighting, a minimap, and schema-aware auto-complete at the `db.`, `db.collection.`, and field-name levels. Three execution modes (Run All F5, Run Selected Ctrl+F5, Run to Line Ctrl+Shift+F5) with per-step progress indicators enable flexible multi-command scripting. Results open in per-query tabs (Tree/Table/BSON views with pagination), and scripts export as .js files portable to mongosh. Session variables persist across executions within a tab; multiple shell sessions run as independent tabs with isolated scopes. Background execution continues while switching to other features.

---

## Strengths

- **Monaco editor:** VS Code–quality editing experience — syntax highlighting, minimap, real-time error highlighting.
- **Three execution modes:** Run All, Run Selected, Run to Line — uncommon per-line granularity in GUI tool shells.
- **Per-query result tabs:** Each returning query opens its own Result N tab with Tree/Table/BSON views and pagination — avoids result flooding in a single output pane.
- **mongosh-compatible .js export:** Scripts export as standard .js, runnable directly in mongosh or importable by Compass shell.
- **Persistent session variables:** Variables survive across executions within a session tab; multiple tabs provide isolated variable scopes.
- **Background execution:** Long scripts continue running while the user browses other tool features.
- **Auto-reconnect on network interruption:** Handles network instability gracefully.
- **Field-name auto-complete:** Schema-aware completion within query contexts reduces syntax errors.

---

## Limitations / Gaps

- **Not a confirmed full mongosh replacement:** mongosh helper methods (`use()`, `show databases`, `show collections`, etc.) not explicitly documented — **unknown/unverified** whether they work.
- **No collaborative scripting:** Scripts are local to the user; no shared script library or team script repository.
- **No multi-cursor or advanced Monaco features exposed:** Standard advanced Monaco features (regex find/replace, column selection) may not be enabled.
- **Export from result tabs:** Result tab data export (CSV, JSON) is not explicitly documented for Shell results — may require redirecting to the Query Activity export.

---

## Comparison Notes (vs MongoDB Compass baseline)

| Aspect | VisuaLeaf | MongoDB Compass |
|---|---|---|
| Shell editor engine | Monaco (VS Code) | CodeMirror (custom) |
| Auto-complete scope | db., db.collection., field names | db., db.collection. |
| Execution modes | Run All, Run Selected, Run to Line | Run (all) only |
| Per-query result tabs | **confirmed** (Tree/Table/BSON each) | single result panel |
| Script save/load | **confirmed** | not available (ad-hoc only) |
| Export as .js (mongosh-compatible) | **confirmed** | not available |
| Session variable persistence | **confirmed** (per session tab) | **confirmed** (within session) |
| Background execution | **confirmed** | not available |
| Auto-reconnect | **confirmed** | **confirmed** |
| Multiple isolated sessions | **confirmed** (multiple tabs) | single session |

---

## Navigation

- [← Product Report](../../product-report.md)
- [Feature Matrix](feature-matrix.md)
- [← Visual Schema Designer](../visual-schema/feature-report.md)
- [→ AI Assistant](../ai-assistant/feature-report.md)
- [→ Security & Governance](../security-governance/feature-report.md)
