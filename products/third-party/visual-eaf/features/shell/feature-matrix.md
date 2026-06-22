# VisuaLeaf — MongoDB Shell Feature Matrix

| ID | Capability | Status | Detail | Source |
|---|---|---|---|---|
| SHL-001 | Monaco editor (VS Code engine) | **confirmed** | Same editor engine as VS Code; full JavaScript/MongoDB syntax highlighting | https://visualeaf.com/docs/mongodb-shell |
| SHL-002 | Monaco minimap | **confirmed** | Code minimap panel for navigation in large scripts | https://visualeaf.com/docs/mongodb-shell |
| SHL-003 | Auto-complete: db. namespace | **confirmed** | db. triggers collection list + db-level methods | https://visualeaf.com/docs/mongodb-shell |
| SHL-004 | Auto-complete: db.collection. namespace | **confirmed** | db.collection. triggers find(), aggregate(), insertOne(), etc. | https://visualeaf.com/docs/mongodb-shell |
| SHL-005 | Auto-complete: field names from schema | **confirmed** | Field name suggestions within query contexts derived from collection schema | https://visualeaf.com/docs/mongodb-shell |
| SHL-006 | Real-time syntax validation | **confirmed** | Syntax errors highlighted in real time as user types | https://visualeaf.com/docs/mongodb-shell |
| SHL-007 | Error line highlighting | **confirmed** | Line with error highlighted in red upon execution failure | https://visualeaf.com/docs/mongodb-shell |
| SHL-008 | Run All (F5) | **confirmed** | Executes all scripts top-to-bottom; auto-splits into sequential commands | https://visualeaf.com/docs/mongodb-shell |
| SHL-009 | Run Selected (Ctrl+F5) | **confirmed** | Executes only the highlighted/selected text | https://visualeaf.com/docs/mongodb-shell |
| SHL-010 | Run to Line (Ctrl+Shift+F5) | **confirmed** | Executes from start of script to the cursor line | https://visualeaf.com/docs/mongodb-shell |
| SHL-011 | Executing line highlighting | **confirmed** | Currently executing line highlighted during Run All | https://visualeaf.com/docs/mongodb-shell |
| SHL-012 | Progress indicator | **confirmed** | "Running script X of Y" shown during Run All execution | https://visualeaf.com/docs/mongodb-shell |
| SHL-013 | Editor read-only during execution | **confirmed** | Editor locked during script execution to prevent concurrent modifications | https://visualeaf.com/docs/mongodb-shell |
| SHL-014 | Execution error stops run | **confirmed** | Execution halts on error; problematic line highlighted in red | https://visualeaf.com/docs/mongodb-shell |
| SHL-015 | Result tab: Shell Output | **confirmed** | Dedicated tab for print() / printjson() output, execution logs, error messages | https://visualeaf.com/docs/mongodb-shell |
| SHL-016 | Result tabs: per-query result tabs | **confirmed** | Each query returning data opens a separate tab (Result 1, Result 2, …) | https://visualeaf.com/docs/mongodb-shell |
| SHL-017 | Result tab view modes | **confirmed** | Tree View, Table View, BSON View with pagination in each result tab | https://visualeaf.com/docs/mongodb-shell |
| SHL-018 | Script: Save | **confirmed** | Save current script to a named file | https://visualeaf.com/docs/mongodb-shell |
| SHL-019 | Script: Save As | **confirmed** | Save current script under a new name | https://visualeaf.com/docs/mongodb-shell |
| SHL-020 | Script: Load | **confirmed** | Load a previously saved script | https://visualeaf.com/docs/mongodb-shell |
| SHL-021 | Script: Export as .json | **confirmed** | Export script as .json file | https://visualeaf.com/docs/mongodb-shell |
| SHL-022 | Script: Export as .js | **confirmed** | Export as .js file; portable to mongosh and MongoDB Compass | https://visualeaf.com/docs/mongodb-shell |
| SHL-023 | Script: Import | **confirmed** | Import script from external file | https://visualeaf.com/docs/mongodb-shell |
| SHL-024 | Query History | **confirmed** | Auto-saved history with search, filter, and preview capability | https://visualeaf.com/docs/mongodb-shell |
| SHL-025 | Sessions: Persistent variable scope | **confirmed** | Variables persist across executions within the same session tab | https://visualeaf.com/docs/mongodb-shell |
| SHL-026 | Sessions: Multiple shell sessions | **confirmed** | Multiple independent sessions via multiple Shell activity tabs | https://visualeaf.com/docs/mongodb-shell |
| SHL-027 | Sessions: Auto-reconnect | **confirmed** | Automatically reconnects on network interruption | https://visualeaf.com/docs/mongodb-shell |
| SHL-028 | Sessions: Background execution | **confirmed** | Script execution continues when user switches to other activity tabs | https://visualeaf.com/docs/mongodb-shell |

## Navigation

- [← Product Report](../../product-report.md)
- [Feature Report](feature-report.md)
- [← Visual Schema Matrix](../visual-schema/feature-matrix.md)
- [→ AI Assistant Matrix](../ai-assistant/feature-matrix.md)
- [→ Security & Governance Matrix](../security-governance/feature-matrix.md)
