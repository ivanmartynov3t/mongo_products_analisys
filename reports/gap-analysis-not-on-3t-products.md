# Gap Analysis — Sub-features NOT on Any 3T Product

This report checks **every sub-feature ID in [feature-dictionary.md](../feature-dictionary.md)** (311 unique IDs across all 11 feature areas) against whether it is confirmed present on any product made by 3T Software Labs — Studio 3T (Desktop IDE), 3T Explore, 3T MCP, 3T Lens, 3T Access, and 3TL Bridge, collectively.

## Navigation

- [Cumulative report index](cumulative-report.md)
- [Low-level feature comparison](comparisons/low-level-feature-comparison.md)
- [High-level product comparison](comparisons/high-level-product-comparison.md)
- [Feature dictionary](../feature-dictionary.md)
- [Companion report: NOT on 3T Desktop specifically](gap-analysis-not-on-3t-desktop.md)

## Methodology

- **Master checklist:** every sub-feature ID defined in feature-dictionary.md's Sub-feature registry (311 total, including the "Supplemental aliases" section).
- **Status source:** the "Studio 3T" column of [low-level-feature-comparison.md](comparisons/low-level-feature-comparison.md)'s iconized sub-feature table, which represents the whole 3T product family as one merged column. That report was itself cross-checked directly against every product's own `feature-matrix.md` files as of 2026-07-29 (six corrections made — see its ["2026-07-29 deep-file verification pass"](comparisons/low-level-feature-comparison.md#2026-07-29-deep-file-verification-pass) note).
- **Why not check product `feature-matrix.md` files directly, ID-by-ID?** Tried that first and rejected it: product matrices frequently consolidate several dictionary IDs into one descriptive row (e.g. Studio 3T's `QUERY-filter-bar` row covers `QUERY-projection`, `QUERY-sort`, and `QUERY-skip-limit` in its prose without giving them separate rows), and some capabilities are cross-referenced under a *different* ID depending on which feature area views them (e.g. `GOV-readonly-mode` and `CONN-readonly-lock` are the same capability). A literal "does this exact ID have its own row" check produced false positives for "not implemented" — e.g. it would have flagged basic projection/sort support as missing from Studio 3T, which is false. The comparison report's status column already reconciles this.
- **Confirmed absent** = comparison report shows ❌ for every row matching that ID.
- **Unverified** = comparison report shows ❓ (no positive status anywhere for that ID), or the ID doesn't appear in the comparison report at all and isn't a near-duplicate of an ID that does.
- **Dictionary aliases** = IDs that don't appear in the comparison report but are near-duplicates of an ID that does, and that duplicate is confirmed implemented — these are dictionary redundancy from earlier research passes, not real gaps, and are excluded from every count.

## Confirmed absent — no 3T product supports this (13)

All 13 are in **F-SCHEMA (Schema)**. No other feature area has a single confirmed 3T-wide gap.

| Sub-feature ID | Name |
| --- | --- |
| SCHEMA-geo-analysis | Geo schema analysis |
| SCHEMA-validation-model | Validation rule model |
| SCHEMA-validation-strictness | Validation strictness |
| SCHEMA-validation-ui | Validation UI workflows |
| SCHEMA-json-editor | JSON schema editor |
| SCHEMA-deploy-validator | Deploy validator |
| SCHEMA-bson-types | BSON type coverage |
| SCHEMA-field-constraints | Field constraints |
| SCHEMA-designer-canvas | Visual canvas |
| SCHEMA-designer-auto | Auto-generate diagram |
| SCHEMA-designer-links | Relationship detection |
| SCHEMA-designer-color | Color coding |
| SCHEMA-designer-portability | Diagram portability |

**Takeaway:** the entire 3T product family's one confirmed capability gap versus competitors is schema **validation authoring/deployment** and the **visual ERD / JSON-schema-editor** cluster — both owned exclusively by MongoDB Compass and/or VisuaLeaf in the comparison reports.

## Unverified — not confirmed present or absent (78)

Open research questions, not confirmed gaps. Grouped by feature area.

### F-CONN — Connectivity (9)
| Sub-feature ID | Name |
| --- | --- |
| CONN-uri-export | URI export |
| CONN-multi-active | Multiple active |
| CONN-in-use-enc | In-use encryption |
| CONN-role-docs | Role/privilege docs |
| CONN-test-steps | Connection test |
| CONN-search-nav | Search & keyboard nav |
| CONN-compat-docdb | Amazon DocumentDB |
| CONN-compat-cosmos | Azure Cosmos DB |
| CONN-compat-redis | Redis |

### F-QUERY — Querying (9)
| Sub-feature ID | Name |
| --- | --- |
| QUERY-collation | Collation |
| QUERY-max-time | Max time |
| QUERY-run-variants | Run variants |
| QUERY-cancel | Cancel query |
| QUERY-perf-timer | Execution timer |
| QUERY-undo-redo | Undo/redo |
| QUERY-view-gridfs | GridFS viewer |
| QUERY-view-split | Split panel views |
| QUERY-charts-dashboards | Charts & dashboards |

### F-AGG — Aggregation (4)
| Sub-feature ID | Name |
| --- | --- |
| AGG-pagination | Result pagination |
| AGG-timer-cancel | Timer & cancel |
| AGG-chart-builder | Chart builder |
| AGG-stage-count | Stage catalog |

### F-SCHEMA — Schema (2, distinct from the confirmed-absent list above)
| Sub-feature ID | Name |
| --- | --- |
| SCHEMA-validation-limits | Validation limits |
| SCHEMA-designer-layouts | Named layouts |

### F-IDX — Indexing & Performance (10)
| Sub-feature ID | Name |
| --- | --- |
| IDX-type-hashed | Hashed index |
| IDX-atlas-search | Atlas Search index |
| IDX-vector-search | Vector Search index |
| IDX-advanced-opts | Advanced index opts |
| IDX-quick-actions | Quick-action presets |
| IDX-profiler-export | Profiler export |
| IDX-profiler-live | Live monitoring |
| IDX-perf-insights | Performance insights |
| IDX-realtime-perf | Real-time performance |
| IDX-stop-ops | Stop operations |

### F-TRANSFER — Data Transfer (4)
| Sub-feature ID | Name |
| --- | --- |
| TRANSFER-export-sql-stmts | Export SQL INSERT |
| TRANSFER-transform-filter | Import filter |
| TRANSFER-transform-js | Custom JS transform |
| TRANSFER-transform-pipeline | Pipeline pre-export |

### F-SHELL — Shell (7)
| Sub-feature ID | Name |
| --- | --- |
| SHELL-minimap | Minimap |
| SHELL-sessions-vars | Session variable scope |
| SHELL-reconnect | Auto-reconnect |
| SHELL-background | Background execution |
| SHELL-background-exec | Background execution (dictionary alias of `SHELL-background`, itself unverified) |
| SHELL-auto-reconnect | Auto reconnect (dictionary alias of `SHELL-reconnect`, itself unverified) |
| SHELL-persistent-vars | Persistent variables (dictionary alias of `SHELL-sessions-vars`, itself unverified) |

### F-AI — AI Features (12)
| Sub-feature ID | Name |
| --- | --- |
| AI-explanation | Query explanation |
| AI-schema-aware | Schema-aware |
| AI-sample-context | Sample context |
| AI-conversation | Conversation context |
| AI-privacy | Privacy mode |
| AI-key-storage | API key storage |
| AI-multi-config | Multiple configs |
| AI-sample-data-toggle | Sample data toggle (dictionary alias of `AI-sample-context`, itself unverified) |
| AI-context-turns | Conversation turns (dictionary alias of `AI-conversation`, itself unverified) |
| AI-named-configs | Named AI configs (dictionary alias of `AI-multi-config`, itself unverified) |
| AI-schema-context | Schema context (dictionary alias of `AI-schema-aware`, itself unverified) |
| AI-model-chooser | Model chooser (dictionary alias of `AI-models` — that ID's "specific models available" aspect is ✅ confirmed, but its "user-selectable model per config" aspect, which is what this ID means, is ❓ unverified) |

### F-SQL — SQL Tools (1)
| Sub-feature ID | Name |
| --- | --- |
| SQL-query-manager | SQL query manager (Studio 3T's general Query Manager includes an "SQL Query" query type, but whether that satisfies this dictionary ID's intent — save/organize/rerun with target collection binding — is unconfirmed) |

### F-GOV — Governance & Security (12)
| Sub-feature ID | Name |
| --- | --- |
| GOV-network-policy | Network policy |
| GOV-telemetry | Telemetry controls |
| GOV-startup-policy | Startup policy |
| GOV-cli-policy | CLI policy |
| GOV-ai-controls | AI data controls |
| GOV-cred-storage-os | OS credential storage |
| GOV-isolated-edition | Isolated edition |
| GOV-air-gapped | Air-gapped support |
| GOV-rbac-inheritance | Role inheritance |
| GOV-rbac-tree | Privilege tree view |
| GOV-rbac-actions | Privilege actions |
| GOV-telemetry-config | Telemetry configuration (dictionary alias of `GOV-telemetry`, itself unverified) |

### F-SCHED — Task Scheduler (8)
| Sub-feature ID | Name |
| --- | --- |
| SCHED-timezone | Timezone support |
| SCHED-exec-config | Execution config |
| SCHED-progress | Progress monitoring |
| SCHED-retry | Retry policy (dictionary alias of `SCHED-exec-config`, itself unverified) |
| SCHED-concurrent | Concurrent execution (dictionary alias of `SCHED-exec-config`, itself unverified) |
| SCHED-batch | Batch size (dictionary alias of `SCHED-exec-config`, itself unverified) |
| SCHED-email | Email provider config (dictionary alias of `SCHED-notifications` — that ID's "task completion notifications" aspect is ✅ confirmed, but its "email notification provider" aspect, which is what this ID means, is ❓ unverified) |
| SCHED-plan-limits | Scheduler plan limits (no matching row found anywhere in the comparison report — not an alias of anything else; a genuine open question) |

## Dictionary aliases excluded from the counts above (17)

These 17 dictionary IDs are near-duplicates of an already-implemented ID (same underlying capability, documented under a different name from an earlier research pass — six of them are explicitly labeled "Supplemental aliases" in the dictionary itself). They are **not** additional gaps.

A verification pass on the first draft of this table caught 3 IDs that had been placed here incorrectly — `AI-model-chooser`, `SCHED-email`, and `SCHED-plan-limits` — because their target ID's *specific* matching row was actually ❓ or (for `SCHED-plan-limits`) didn't exist at all; those three now live in the Unverified section above.

| Sub-feature ID | Name | Duplicate of (confirmed implemented) |
| --- | --- | --- |
| CONN-color-coding | Color coding | `CONN-org-folders` |
| AGG-result-formats | Export format range | `AGG-export-results` |
| AI-local-mcp | Local MCP server | `AI-007` |
| AI-mcp-client | MCP client support | `AI-009` |
| AI-mcp-tools | MCP tools count | `AI-008` |
| AI-stt-cli | stt-cli + PII scanner | `AI-010` |
| AI-plan-gate | AI plan gate | `AI-plan-req` |
| GOV-platform-bridge | Platform bridge integration | `GOV-platform-cdc` |
| GOV-platform-k8s | Platform Kubernetes deployment | `GOV-013` |
| GOV-platform-oidc | Platform OIDC providers | `GOV-012` |
| GOV-protect-mode | Protect mode | `GOV-readonly-mode` |
| SCHED-preset-types | Preset schedule types | `SCHED-types-time` |
| SCHED-task-actions | Task management actions | `SCHED-actions` |
| SCHED-task-save | Task save from tools | `TRANSFER-task-save` |
| SCHED-history | Execution history | `SCHED-history-retention` |
| SHELL-open-from | Open in shell from tools | `SHELL-integrations` |
| SHELL-sessions | Shell sessions | `SHELL-sessions-multi` |

## Coverage accounting

311 dictionary IDs = 203 implemented (excluded from this report) + 13 confirmed absent + 78 unverified + 17 dictionary-alias redundancies.
