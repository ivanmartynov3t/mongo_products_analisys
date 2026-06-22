# VisuaLeaf — Querying Feature Matrix

| ID | Capability | Status | Detail | Source |
|---|---|---|---|---|
| QRY-001 | View Mode: Tree View | **confirmed** | Expand/collapse nested docs; color-coded BSON types; inline editing; 3 search modes (Field/Value/Both) | https://visualeaf.com/docs/mongo-query |
| QRY-002 | View Mode: Table View | **confirmed** | Sortable/resizable columns; show/hide columns; drag-to-reorder; multi-select rows; nested expansion | https://visualeaf.com/docs/mongo-query |
| QRY-003 | View Mode: BSON View | **confirmed** | Extended JSON syntax highlighting; copy as EJSON; preserves ObjectId/Date/Binary types | https://visualeaf.com/docs/mongo-query |
| QRY-004 | View Mode: Explain View | **confirmed** | Execution plan, index usage, docs examined vs returned, index suggestions | https://visualeaf.com/docs/mongo-query |
| QRY-005 | Query filter editor (find() style) | **confirmed** | JSON filter field; ACE editor with JSON syntax highlighting | https://visualeaf.com/docs/mongo-query |
| QRY-006 | Projection editor | **confirmed** | Include (1) / exclude (0) fields; JSON editor | https://visualeaf.com/docs/mongo-query |
| QRY-007 | Sort editor | **confirmed** | Ascending (1) / descending (-1) per field; JSON editor | https://visualeaf.com/docs/mongo-query |
| QRY-008 | Limit dropdown | **confirmed** | Options: 50, 100, 200, 300, 500 documents per page | https://visualeaf.com/docs/mongo-query |
| QRY-009 | Skip dropdown | **confirmed** | Options: 0, 50, 100 | https://visualeaf.com/docs/mongo-query |
| QRY-010 | ACE editor with JSON syntax highlighting | **confirmed** | Used for filter, projection, and sort fields | https://visualeaf.com/docs/mongo-query |
| QRY-011 | Auto-complete: Ctrl+Space for field names | **confirmed** | Triggers field name suggestions derived from collection schema | https://visualeaf.com/docs/mongo-query |
| QRY-012 | Execution timer with visual thresholds | **confirmed** | Timer turns amber at 2s, red at 5s; visual alert for slow queries | https://visualeaf.com/docs/mongo-query |
| QRY-013 | Run All Documents | **confirmed** | Executes find() with current filter/projection/sort/limit/skip | https://visualeaf.com/docs/mongo-query |
| QRY-014 | Run Find One | **confirmed** | Executes findOne() with current filter | https://visualeaf.com/docs/mongo-query |
| QRY-015 | Run Count | **confirmed** | Executes countDocuments() with current filter | https://visualeaf.com/docs/mongo-query |
| QRY-016 | Cancel running query | **confirmed** | Cancel button terminates in-flight query | https://visualeaf.com/docs/mongo-query |
| QRY-017 | Visual Query Builder panel | **confirmed** | Basic+ plan only; toggleable; resizable; width persisted per activity | https://visualeaf.com/docs/mongo-query |
| QRY-018 | VQB: Drag-and-drop fields from schema | **confirmed** | Drag fields from collection schema panel into builder conditions | https://visualeaf.com/docs/mongo-query |
| QRY-019 | VQB: Visual operator selection | **confirmed** | Operators: $eq, $ne, $gt, $gte, $lt, $lte, $in, $nin, $regex, and more | https://visualeaf.com/docs/mongo-query |
| QRY-020 | VQB: AND/OR logic with nested groups | **confirmed** | AND/OR logic builder; supports nested condition groups | https://visualeaf.com/docs/mongo-query |
| QRY-021 | VQB: Type-aware inputs | **confirmed** | Date pickers, number sliders, boolean toggles based on field BSON type | https://visualeaf.com/docs/mongo-query |
| QRY-022 | VQB: Projection Builder | **confirmed** | Visual field include/exclude checkboxes | https://visualeaf.com/docs/mongo-query |
| QRY-023 | VQB: Sort Builder | **confirmed** | Ascending/descending toggle per field | https://visualeaf.com/docs/mongo-query |
| QRY-024 | VQB: Real-time JSON preview (bidirectional) | **confirmed** | VQB changes update JSON editor; JSON editor changes update VQB | https://visualeaf.com/docs/mongo-query |
| QRY-025 | VQB: Plan requirement | **confirmed** | Requires Basic or Professional plan | https://visualeaf.com/docs/mongo-query |
| QRY-026 | AI Query Builder: NL → MongoDB query | **confirmed** | Professional plan only; natural language → find()-style query | https://visualeaf.com/docs/mongo-query |
| QRY-027 | AI Query Builder: Conversation context | **confirmed** | Prior turns used for follow-up refinements | https://visualeaf.com/docs/mongo-query |
| QRY-028 | AI Query Builder: Schema-aware | **confirmed** | Uses collection field names and BSON types; optionally sends sample documents | https://visualeaf.com/docs/mongo-query |
| QRY-029 | AI Query Builder: Plain-English explanation | **confirmed** | Every AI-generated query includes a plain-English explanation of what it does | https://visualeaf.com/docs/mongo-query |
| QRY-030 | AI Query Builder: 11 OpenAI models | **confirmed** | ChatGPT4o (recommended), ChatGPT4oMini, ChatGPTo3Mini, ChatGPTo1, ChatGPTo1Mini, ChatGPTo1Preview, ChatGPT41, ChatGPT41Mini, ChatGPT4Turbo, ChatGPT4, ChatGPT35Turbo | https://visualeaf.com/docs/mongo-query |
| QRY-031 | AI Query Builder: Privacy toggle | **confirmed** | "Send sample data" (Better Accuracy) vs "schema-only" (More Private) | https://visualeaf.com/docs/mongo-query |
| QRY-032 | Inline editing (Tree View) | **confirmed** | Click value → type-appropriate editor → Enter to save, Esc to cancel | https://visualeaf.com/docs/mongo-query |
| QRY-033 | Undo/Redo | **confirmed** | Ctrl+Z (undo) / Ctrl+Shift+Z (redo) | https://visualeaf.com/docs/mongo-query |
| QRY-034 | Dialog editing with full ACE editor | **confirmed** | Full ACE editor for entire document; validation before save | https://visualeaf.com/docs/mongo-query |
| QRY-035 | Batch editing (Table View) | **confirmed** | Select rows → Batch Update → operators ($set, $unset, $inc, $push, $pull) → preview count + example changes → confirm | https://visualeaf.com/docs/mongo-query |
| QRY-036 | Field operations via context menu | **confirmed** | Add Field, Rename Field ($rename), Delete Field ($unset), Edit Value | https://visualeaf.com/docs/mongo-query |
| QRY-037 | Copy options | **confirmed** | JSON, value, EJSON, field name, field path (dot notation) | https://visualeaf.com/docs/mongo-query |
| QRY-038 | Pagination: docs per page | **confirmed** | 50 / 100 / 200 / 300 / 500 documents per page | https://visualeaf.com/docs/mongo-query |
| QRY-039 | Query History (auto-saved per collection) | **confirmed** | Basic+ plan; auto-saved with timestamp and execution time | https://visualeaf.com/docs/mongo-query |
| QRY-040 | Query History: reload all parameters | **confirmed** | Filter, projection, sort, limit, skip all restored on click | https://visualeaf.com/docs/mongo-query |
| QRY-041 | Saved Queries: name and organize | **confirmed** | Basic+ plan; organize by collection or globally | https://visualeaf.com/docs/mongo-query |
| QRY-042 | Saved Queries: export/import as JSON | **confirmed** | Export/import saved query libraries as JSON files | https://visualeaf.com/docs/mongo-query |
| QRY-043 | Saved Queries: share with team | **confirmed** | Basic+ plan; team sharing via exported JSON | https://visualeaf.com/docs/mongo-query |
| QRY-044 | "Open In" context integration | **confirmed** | Opens collection context in: Aggregation Pipeline, MongoDB Shell, SQL Query Mode, Collection Statistics, Create Chart, Import Data, Export Data | https://visualeaf.com/docs/mongo-query |

## Navigation

- [← Product Report](../../product-report.md)
- [Feature Report](feature-report.md)
- [← Connectivity Matrix](../connectivity/feature-matrix.md)
- [→ Aggregation Matrix](../aggregation/feature-matrix.md)
- [→ Schema Validation Matrix](../schema-validation/feature-matrix.md)
- [→ Indexing & Performance Matrix](../indexing-performance/feature-matrix.md)
- [→ Data Import/Export Matrix](../data-import-export/feature-matrix.md)
- [→ Visual Schema Matrix](../visual-schema/feature-matrix.md)
- [→ Shell Matrix](../shell/feature-matrix.md)
- [→ AI Assistant Matrix](../ai-assistant/feature-matrix.md)
- [→ Security & Governance Matrix](../security-governance/feature-matrix.md)
