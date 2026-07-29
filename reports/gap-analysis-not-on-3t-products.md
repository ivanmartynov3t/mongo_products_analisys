# Gap Analysis — Sub-features NOT on Any 3T Product

This report compiles every dictionary sub-feature that is **not confirmed present on any product made by 3T Software Labs** — Studio 3T (Desktop IDE), 3T Explore, 3T MCP, 3T Lens, 3T Access, and 3TL Bridge, collectively. It is derived from the "Studio 3T" column of [low-level-feature-comparison.md](comparisons/low-level-feature-comparison.md), which represents the whole 3T product family as a single comparison column (per [products/3t/README.md](../products/3t/README.md)).

## Navigation

- [Cumulative report index](cumulative-report.md)
- [Low-level feature comparison](comparisons/low-level-feature-comparison.md)
- [High-level product comparison](comparisons/high-level-product-comparison.md)
- [Feature dictionary](../feature-dictionary.md)
- [Companion report: NOT on 3T Desktop specifically](gap-analysis-not-on-3t-desktop.md)

## Methodology

- Source: the "Detailed iconized" sub-feature comparison table in [low-level-feature-comparison.md](comparisons/low-level-feature-comparison.md), which covers 307 comparison rows across all 11 feature areas.
- **Confirmed absent** = the Studio 3T column shows ❌ ("not supported"). Per this repo's icon legend, this means the gap has been positively confirmed, not just undocumented.
- **Unverified** = the Studio 3T column shows ❓ ("unknown/unverified"). This means no 3T product's own documentation confirms the capability either way — it is not a confirmed gap, just an open question.
- Every row in the low-level report (307 total) was cross-checked directly against Studio 3T's, MongoDB Compass's, and VisuaLeaf's own `feature-matrix.md` files, not just the comparison report itself, as of 2026-07-29. Six data-entry errors were found and fixed (one for Studio 3T, five for VisuaLeaf) and one missing row was added (`SQL-query-manager`, previously absent from the comparison report entirely). Full list in the low-level report's ["2026-07-29 deep-file verification pass"](comparisons/low-level-feature-comparison.md#2026-07-29-deep-file-verification-pass) note. The one fix relevant to this file: `CONN-auth-enterprise` was wrongly marked ❌ for Studio 3T — corrected to 🏢 (enterprise-tier-only, confirmed in Studio 3T's own connectivity matrix) — so it is excluded from the confirmed-absent list below.

## Confirmed absent — no 3T product supports this (13)

All 13 are in **F-SCHEMA (Schema)**. No other feature area has a single confirmed 3T-wide gap.

| Sub-feature ID | Name | Held by (for contrast) |
| --- | --- | --- |
| SCHEMA-geo-analysis | Geo field map-backed analysis | MongoDB Compass |
| SCHEMA-validation-model | Validation rule model ($jsonSchema / query-operator rules) | MongoDB Compass, VisuaLeaf |
| SCHEMA-validation-ui | Validation UI workflow (add/edit/generate/preview/apply) | MongoDB Compass, VisuaLeaf (paid tier) |
| SCHEMA-validation-strictness | Validation action (warn/error) and level (strict/moderate) | MongoDB Compass |
| SCHEMA-deploy-validator | Deploy validator to collection | MongoDB Compass, VisuaLeaf |
| SCHEMA-json-editor | JSON schema tree editor | VisuaLeaf |
| SCHEMA-bson-types | BSON type support in schema editor | VisuaLeaf |
| SCHEMA-field-constraints | Field-level constraint options (minLength/pattern/etc.) | MongoDB Compass, VisuaLeaf |
| SCHEMA-designer-canvas | Visual ERD canvas | VisuaLeaf (paid tier) |
| SCHEMA-designer-auto | Auto-generate ERD from all collections | VisuaLeaf |
| SCHEMA-designer-links | Relationship detection (graph-theory) | VisuaLeaf |
| SCHEMA-designer-color | ERD node color coding | VisuaLeaf |
| SCHEMA-designer-portability | ERD export/import and named layouts | VisuaLeaf |

**Takeaway:** the entire 3T product family's one confirmed capability gap versus competitors is schema **validation authoring/deployment** and the **visual ERD / JSON-schema-editor** cluster — both owned exclusively by MongoDB Compass and/or VisuaLeaf in this comparison.

## Unverified — not confirmed present or absent on any 3T product (83)

These are open research questions, not confirmed gaps. No 3T product's own documentation states support, and none states non-support either.

### F-AI — AI Features (13)
| Sub-feature ID | Name |
| --- | --- |
| AI-explanation | Plain-English explanation always included |
| AI-models | User-selectable model per config |
| AI-sample-context | "Send sample data" privacy toggle / Sample context |
| AI-conversation | Conversation turns for iterative refinement / Conversation context |
| AI-multi-config | Multiple named AI configurations / Multiple configs |
| AI-key-storage | API key storage security |
| AI-schema-aware | Schema and field names injected as AI context / Schema-aware |
| AI-plan-req | Plan requirement |
| AI-privacy | Privacy mode |

### F-GOV — Governance & Security (13)
| Sub-feature ID | Name |
| --- | --- |
| GOV-network-policy | Network access policy |
| GOV-telemetry | Telemetry opt-out/configuration / Telemetry controls |
| GOV-startup-policy | Startup policy enforcement (EJSON/YAML) |
| GOV-cli-policy | CLI policy enforcement |
| GOV-isolated-edition | Isolated / air-gapped edition |
| GOV-ai-controls | AI feature controls with human approval gate |
| GOV-rbac-tree | RBAC visual role inheritance tree |
| GOV-air-gapped | Air-gapped deployment support |
| GOV-cred-storage-os | OS credential storage |
| GOV-rbac-actions | Privilege actions |
| GOV-rbac-inheritance | Role inheritance |
| GOV-readonly-mode | Read-only mode (as a distinct dimension from GOV-readonly-mode's protect-mode row, which IS confirmed 🧪) |

### F-CONN — Connectivity (9)
| Sub-feature ID | Name |
| --- | --- |
| CONN-multi-active | Multiple concurrent connections |
| CONN-uri-export | URI export from form fields |
| CONN-search-nav | Connection search and keyboard navigation |
| CONN-in-use-enc | In-use encryption (QE/CSFLE) |
| CONN-role-docs | Required roles documentation |
| CONN-test-steps | Step-by-step connection test |
| CONN-compat-docdb | DocumentDB compatibility |
| CONN-compat-cosmos | Cosmos DB compatibility |
| CONN-compat-redis | Redis compatibility |

### F-IDX — Indexing & Performance (10)
| Sub-feature ID | Name |
| --- | --- |
| IDX-type-hashed | Hashed index |
| IDX-advanced-opts | Advanced index options (commit quorum, clustered) |
| IDX-quick-actions | Quick-action index templates |
| IDX-atlas-search | Atlas Search index creation |
| IDX-vector-search | Vector Search index creation |
| IDX-profiler-export | Export profiler data |
| IDX-profiler-live | Live running operations view |
| IDX-stop-ops | Kill/stop running operations |
| IDX-realtime-perf | Real-time performance monitoring |
| IDX-perf-insights | Performance insights / advisory |

### F-QUERY — Querying (9)
| Sub-feature ID | Name |
| --- | --- |
| QUERY-collation | Collation |
| QUERY-max-time | Max execution time |
| QUERY-perf-timer | Performance timer with color thresholds |
| QUERY-run-variants | Run variants (findOne, count) |
| QUERY-cancel | Cancel in-flight query |
| QUERY-undo-redo | Undo/redo edits |
| QUERY-view-gridfs | GridFS viewer |
| QUERY-view-split | Split panel views |
| QUERY-charts-dashboards | Charts & dashboards |

### F-SCHED — Task Scheduler (10)
| Sub-feature ID | Name |
| --- | --- |
| SCHED-timezone | Timezone-aware scheduling with DST |
| SCHED-exec-config | Execution configuration options / Retry policy / Concurrent execution / Batch size |
| SCHED-notifications | Email notification provider |
| SCHED-actions | Task actions |
| SCHED-history-retention | History retention |
| SCHED-progress | Progress monitoring |
| SCHED-types-time | Time-based schedules |

### F-SHELL — Shell (8)
| Sub-feature ID | Name |
| --- | --- |
| SHELL-background | Background script execution |
| SHELL-reconnect | Auto-reconnect on connection drop |
| SHELL-minimap | Code minimap in editor |
| SHELL-sessions-vars | Persistent session variables across runs / Session variable scope |
| SHELL-sessions-multi | Multiple sessions |

### F-TRANSFER — Data Transfer (4)
| Sub-feature ID | Name |
| --- | --- |
| TRANSFER-export-sql-stmts | Export as SQL INSERT statements |
| TRANSFER-transform-filter | Document filter condition before import |
| TRANSFER-transform-js | User-defined JS transform per document |
| TRANSFER-transform-pipeline | Server-side $pipeline pre-export transform |

### F-AGG — Aggregation (4)
| Sub-feature ID | Name |
| --- | --- |
| AGG-stage-count | Number of supported pipeline stages |
| AGG-chart-builder | Open pipeline output in Chart Builder |
| AGG-timer-cancel | Execution timer + cancel button |
| AGG-pagination | Pipeline output pagination |

### F-SCHEMA — Schema (2, distinct from the confirmed-absent list above)
| Sub-feature ID | Name |
| --- | --- |
| SCHEMA-designer-layouts | Named layouts |
| SCHEMA-validation-limits | Validation limits |

### F-SQL — SQL Tools (1)
| Sub-feature ID | Name |
| --- | --- |
| SQL-query-manager | SQL query manager (save/organize/rerun SQL queries with target collection binding) — Studio 3T's general Query Manager includes an "SQL Query" type, but equivalence to this dictionary ID is unconfirmed |

## Feature areas with zero gaps

Every one of the 11 feature areas has at least one confirmed-absent or unverified row for the 3T portfolio — F-SQL is the smallest, with a single unverified row (`SQL-query-manager`).
