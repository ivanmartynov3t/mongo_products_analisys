# Studio 3T Documentation Changelog

## Navigation

- [Product report](product-report.md)
- [Feature dictionary](../../../feature-dictionary.md)
- [Research plan & findings](../../../research/studio-3t-desktop-review-2026/)

This file records every edit made to Studio 3T's documentation in this repository, dated, with the reason. It exists so a future reviewer can see what changed and why without diffing every file by hand. It does not track changes to Studio 3T Desktop the product (see `product-suite/`'s own git history for that) — only changes to *this repo's documentation about it*.

---

## 2026-07-31 — Full source-code re-audit

**Trigger:** a full review of `products/3t/studio-3t/` against the real Studio 3T Desktop source code (`product-suite/data-man-mongodb-ent/`), requested to (a) add features implemented but undocumented, and (b) correct completeness status of already-documented features. Method, scope guardrail, and methodology: [research plan](../../../research/studio-3t-desktop-review-2026/00-research-plan.md). Full per-feature findings: [research/studio-3t-desktop-review-2026/01-connectivity-findings.md](../../../research/studio-3t-desktop-review-2026/01-connectivity-findings.md) through [11-task-scheduler-findings.md](../../../research/studio-3t-desktop-review-2026/11-task-scheduler-findings.md). Consolidated correction list: [12-consolidated-corrections.md](../../../research/studio-3t-desktop-review-2026/12-consolidated-corrections.md).

### New sub-feature IDs added to `feature-dictionary.md` (17)

| ID | Feature | Name |
|---|---|---|
| `CONN-session-restore` | F-CONN | Session Restore |
| `CONN-git-repo-sharing` | F-CONN | Git-backed connection sharing |
| `CONN-access-manager-integration` | F-CONN | Access Manager tree integration |
| `QUERY-value-search` | F-QUERY | Cross-collection value search |
| `TRANSFER-gridfs-crud` | F-TRANSFER | GridFS file CRUD |
| `TRANSFER-collection-history` | F-TRANSFER | Collection History |
| `SHELL-destructive-guard` | F-SHELL | Destructive command detection & warning |
| `SHELL-result-tab-limit` | F-SHELL | Result tab count limit |
| `SHELL-bookmarks` | F-SHELL | Script bookmarks |
| `SHELL-oidc-auth` | F-SHELL | OIDC authentication for shell connections |
| `SHELL-storedjs-rename` | F-SHELL | Stored JS rename |
| `AI-agentic-mode` | F-AI | AI Helper Plus — agentic tool-calling mode |
| `AI-offline-mcp` | F-AI | Bundled offline MongoDB MCP server |
| `AI-tab-context` | F-AI | Global Tab Context Registry |
| `AI-chart-render` | F-AI | AI Helper response chart rendering |
| `AI-multi-conversation` | F-AI | AI Helper — multiple named conversations |
| `AI-guardrail-layer` | F-AI | AI Helper mismatch/guard-rail apply layer |

### Major status corrections

- **F-SCHEMA** — Studio 3T Desktop has a full, mature collection-validator authoring/deployment feature that was documented as absent. Moved `SCHEMA-validation-model`, `SCHEMA-validation-strictness`, `SCHEMA-validation-ui`, `SCHEMA-deploy-validator`, `SCHEMA-validation-limits` from absent/unverified to **confirmed**. This overturned the repo's own gap-analysis claim that schema validation was "the sole confirmed gap across the whole 3T portfolio" — the real gap is narrower (JSON-Schema-tree-editor + visual-ERD/canvas cluster, 9 IDs, not 13).
- **F-SCHED** — corrected in the opposite direction: execution history/retention, notifications/email, retry/concurrency/batch config, and a persistent status-state machine were documented as present/partial but have **no supporting code**. Moved 9 IDs to confirmed-absent, 2 to partial. Tasks fire asynchronously with no concurrency cap by design (source comment: "avalanche is possible").
- **F-AI** — as of Studio 3T release **2026.12.0** (17-Jul-2026), AI Helper is now **disabled by default** (opt-in), reversing the previously-documented default-enabled model. MCP tool names corrected (`find_documents`, `get_collection_stats`). The "no validation" claim for applying AI results was wrong — a real guard-rail layer exists.
- **F-IDX** — two outright factual errors fixed (Studio 3T *does* show geoHaystack and background-index-build deprecation warnings in-UI). 14 dictionary sub-feature IDs that had no matrix row were filled in, most confirmed — including a previously-undocumented real-time performance monitoring capability (mongostat/currentOp equivalent).
- **F-TRANSFER** — data masking corrected from "8 op types" to **19** (`FieldOperation.java`/`DMMethod`, 6 BSON-type categories). SQL migration dialect support corrected from 4 to **6** (adds Sybase, IBM DB2 — both Enterprise-gated, asymmetric between import and export).
- **F-QUERY / F-AGG** — the Visual Query Builder's "real-time bidirectional sync" claim was wrong; it's a **one-way handoff**. Aggregation code generation corrected from an "eight languages / Java sub-tabs" framing to 9 generators / 7 target languages via a single dropdown. `AGG-stage-modes` corrected (no form/wizard mode, raw JSON only). `QUERY-view-split` and `QUERY-charts-dashboards` (added 2026-07-28 from marketing pages) have zero corroborating source code — downgraded pending re-verification.
- **F-SQL** — no visual JOIN-mapping editor exists (plain SQL text, single equality-comparison JOINs only). Dialect is an ANTLR4 fork of `sqlite-parser`, not MySQL.
- **F-GOV** — audit logging narrowed significantly: only Connection Manager actions are logged, off by default, Windows-GPO-only activation; a built HTTP audit-sender to 3T Access has zero call sites (unwired). Credential storage corrected (local BouncyCastle keystore, not OS Keychain). Startup policy corrected (Windows GPO/registry, not EJSON/YAML). `GOV-cli-policy` and `GOV-isolated-edition` confirmed absent. Studio 3T's governance `feature-matrix.md`, previously an unauthored placeholder, is now a full 20-ID table.
- **F-CONN** — edition names resolved definitively: Free / Community Edition / Professional / Ultimate ("Pro/Base" was an internal alias, not a SKU). Several "All editions" claims corrected to Professional+ (SSH Profiles, color-coding, read-only lock, cross-connection index copy/paste). `CONN-compat-redis` has zero code evidence — flagged as a likely documentation error.

### Files touched in this pass

- `feature-dictionary.md` — 17 new sub-feature IDs, `PROP-schema-erd-cluster` linkage corrected (13→9 IDs), F-GOV coverage note updated, changelog entry added.
- `products/3t/studio-3t/product-report.md` — edition names, masking count, SQL dialect count, VQB sync claim, index copy/paste tier, AI Helper opt-in reversal, audit-logging scope, task-scheduler operational maturity, F-GOV status, open questions.
- `products/3t/studio-3t/features/*/feature-matrix.md` and `feature-report.md` (all 11 feature areas) — status corrections and new capability sections, each with a "Last reviewed: 2026-07-31" line linking to its findings file.
- `README.md` (repo root) — masking op-count and edition-name corrections in the Studio 3T summary bullet.
- `reports/gap-analysis-not-on-3t-products.md` — confirmed-absent count 13→9, unverified 78→77, coverage arithmetic recomputed for 328 total IDs.
- `reports/gap-analysis-not-on-3t-desktop.md` — same F-SCHEMA correction, plus a new bucket for the 9 F-SCHED IDs (Desktop-confirmed-absent, portfolio-wide status unverified), unverified count 78→54.
- `reports/cumulative-report.md` — masking/SQL-dialect counts, sub-feature-ID total (311→328), stale-count flags preserved rather than silently resolved.
- `reports/comparisons/high-level-product-comparison.md` — VQB sync, SQL join-mapping, masking count, audit-log scope, index-copy-paste tier, and a softened Compass "only product with real-time monitoring" claim (Studio 3T has it too).
- `reports/comparisons/low-level-feature-comparison.md` — row-level corrections across all of the above, plus 17 new rows for the new sub-feature IDs.
- `products/3t/studio-3t/CHANGELOG.md` — this file, new.

### Explicitly out of scope for this pass

- The `product-suite/` source repo itself — read-only throughout; nothing there was modified.
- Full row-level reconciliation of the "257+ sub-feature rows" figure in `reports/cumulative-report.md` against the low-level comparison report's actual row count — flagged as a separate, not-yet-reconciled number.
- The F-SQL/F-TRANSFER scope overlap (SQL query engine vs. SQL migration toolchain both currently live under `sql-tools`) — flagged for a future dictionary clarification, not resolved here.
- Whether the 9 F-SCHED IDs confirmed absent from Studio 3T Desktop are also absent from 3T Lens/3TL Bridge (portfolio-wide) — left unverified.
