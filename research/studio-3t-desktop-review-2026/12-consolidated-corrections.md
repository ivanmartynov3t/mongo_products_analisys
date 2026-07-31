# Consolidated Corrections — 2026-07-31 Studio 3T Desktop Source-Code Review

## Navigation

- [Research plan](00-research-plan.md)
- [Feature dictionary](../../feature-dictionary.md)
- [Studio 3T product report](../../products/3t/studio-3t/product-report.md)

This file consolidates every correction and addition produced by the full re-audit of Studio 3T Desktop (`products/3t/studio-3t/`) against its real source code (`product-suite/data-man-mongodb-ent/`), for use when updating downstream reports (`reports/cumulative-report.md`, both gap-analysis reports, both comparison reports). Per-feature-area detail, citations, and full reasoning live in `01-connectivity-findings.md` through `11-task-scheduler-findings.md` and the corresponding `products/3t/studio-3t/features/*/feature-matrix.md`/`feature-report.md` files (each now has a "Last reviewed: 2026-07-31" line). Do not re-derive citations here — cite the per-feature findings file or feature-matrix.md instead.

## 1. New sub-feature IDs added to `feature-dictionary.md` (17 total)

| ID | Feature | Name |
|---|---|---|
| CONN-session-restore | F-CONN | Session Restore |
| CONN-git-repo-sharing | F-CONN | Git-backed connection sharing |
| CONN-access-manager-integration | F-CONN | Access Manager tree integration |
| QUERY-value-search | F-QUERY | Cross-collection value search |
| TRANSFER-gridfs-crud | F-TRANSFER | GridFS file CRUD |
| TRANSFER-collection-history | F-TRANSFER | Collection History |
| SHELL-destructive-guard | F-SHELL | Destructive command detection & warning |
| SHELL-result-tab-limit | F-SHELL | Result tab count limit |
| SHELL-bookmarks | F-SHELL | Script bookmarks |
| SHELL-oidc-auth | F-SHELL | OIDC authentication for shell connections |
| SHELL-storedjs-rename | F-SHELL | Stored JS rename |
| AI-agentic-mode | F-AI | AI Helper Plus — agentic tool-calling mode |
| AI-offline-mcp | F-AI | Bundled offline MongoDB MCP server |
| AI-tab-context | F-AI | Global Tab Context Registry |
| AI-chart-render | F-AI | AI Helper response chart rendering |
| AI-multi-conversation | F-AI | AI Helper — multiple named conversations |
| AI-guardrail-layer | F-AI | AI Helper mismatch/guard-rail apply layer |

All 17 are Studio 3T Desktop only (not verified/claimed for any other product) — for the coverage/comparison reports, treat as Studio-3T-confirmed and blank/unverified for every other product unless that product's own docs already say otherwise.

## 2. F-SCHEMA — biggest correction: gap-analysis "13 confirmed absent" must become 9

Studio 3T Desktop **does** have a real, mature collection-validator authoring/deployment feature (JSON editor, Validation Level off/strict/moderate, Action error/warn, "Validate JSON" check, MongoDB ≥3.6 scope limits, validator-copy-on-collection-copy since 2022.5.0). Move these from confirmed-absent to **confirmed** (present on Studio 3T Desktop, and therefore present somewhere in the 3T portfolio):
- `SCHEMA-validation-model`
- `SCHEMA-validation-strictness`
- `SCHEMA-validation-ui`
- `SCHEMA-deploy-validator`
- `SCHEMA-validation-limits` (was "unverified", now confirmed — not one of the original 13, but upgrade it too)

**Still genuinely confirmed-absent** (9 IDs, claim holds — no code found anywhere in `t3`):
- `SCHEMA-geo-analysis`
- `SCHEMA-json-editor`
- `SCHEMA-bson-types`
- `SCHEMA-field-constraints`
- `SCHEMA-designer-canvas`
- `SCHEMA-designer-auto`
- `SCHEMA-designer-links`
- `SCHEMA-designer-color`
- `SCHEMA-designer-portability`

Any report text describing "the one confirmed gap across the whole 3T portfolio is schema validation/JSON-schema-editor/visual-ERD" must be corrected to describe only the JSON-Schema-tree-editor and visual-ERD/canvas cluster as the real gap — validator authoring/deployment is not part of it.

## 3. F-SCHED — task-scheduler completeness moved DOWN (more absent/partial than previously documented)

Moved to **confirmed absent** (previously roadmap/partial/unverified in various matrices):
- `SCHED-status-states`, `SCHED-exec-config`, `SCHED-retry`, `SCHED-concurrent`, `SCHED-batch` (absent at scheduler level), `SCHED-history`, `SCHED-history-retention`, `SCHED-notifications`, `SCHED-email`

Downgraded to **partial**:
- `SCHED-actions`, `SCHED-task-actions` (no Pause/Resume, no View History action)

`SCHED-cron` reworded: real cron-like matching engine exists internally, but there is no free-form cron-string UI field — only structured day/hour/minute pickers under "Custom." Tasks fire asynchronously with no concurrency cap (code comment: "tasks are launched asynchronously, avalanche is possible" — an acknowledged design characteristic).

`SCHED-task-types` corrected: 13 concrete task types (import splits into 6 separate types), not the previously documented count.

## 4. F-IDX — mostly matrix gaps filled in (14 new rows), plus two factual-error corrections and one edition-gating fix

- Two factual errors corrected: Studio 3T **does** show an in-UI geoHaystack deprecation warning (`IndexGeoOptionsSubTab.java:215`) and **does** explain the background/foreground index-build tradeoff and MongoDB 4.2+ locking change in-UI — both were previously (incorrectly) documented as absent/not-flagged.
- `IDX-copy-paste` (cross-connection index copy/paste): corrected from "All editions" to **Professional tier and above** (`AppFeatures.COPY_INDEX`). The capability itself remains a genuine differentiator vs. Compass/VisuaLeaf — only the free-tier availability claim was wrong.
- 14 previously-dictionary-only IDs now have matrix rows with confirmed/absent status (notably: real-time monitoring — a mongostat/currentOp equivalent via `ServerStatusChartsTab.java`/`TaskMonitorTab.java` — is confirmed and is a notable, previously underdocumented differentiator). Full list in `products/3t/studio-3t/features/indexing-performance/feature-matrix.md`.
- Confirmed genuinely absent (no change): Atlas Search index management, Vector Search index management, ESR guidance text, commit quorum option, wildcard projection UI, profiler CSV/JSON export, performance advisor/insights, sharding-distribution stats, explicit multikey UI.

## 5. F-TRANSFER — data masking op-count correction (8 → 19) and SQL dialect expansion (4 → 6)

- **Data masking**: previously documented/claimed as "8 op types" (README, product-report). Actual: **19 real masking operations** (+1 no-op state = 20 constants total in `FieldOperation.java`/`DMMethod` enum), across 6 BSON-type categories. This correction must propagate to any report stating an "8" figure.
- **SQL migration dialects**: previously documented as 4 (MySQL, PostgreSQL, Oracle, SQL Server). Actual: **6** (adds Sybase, IBM DB2 — both Enterprise-gated and asymmetric: Sybase has no direct SQL-export-wizard target; DB2 is migration-only).
- Two new capabilities added to dictionary (see §1): GridFS full CRUD (`TRANSFER-gridfs-crud`) and Collection History / per-document restore (`TRANSFER-collection-history`).
- Confirmed genuinely absent: Parquet, Avro, YAML, standalone XML, PDF import/export.
- The README/product-report "sole full SQL↔MongoDB migration/export toolchain" *exclusivity* wording is unverifiable from a source-only review (it depends on competitor capabilities) — label as unverified claim, not confirmed/denied, if a report repeats it.

## 6. F-QUERY / F-AGG — edition-gating corrections and the VQB "bidirectional sync" correction

- Several sub-features previously marked "All editions" are actually gated: query history, Query Manager (non-SQL types), and the Visual Query Builder core/projection-sort are Community-Edition-and-up or Professional-and-up (not Free). Cite `Edition.java`/`AppFeatures.java`.
- **`QUERY-vqb-bidirectional` / `AGG-vqb-sync` — corrected from "bidirectional sync" to "one-way handoff."** No VQB↔query-bar or VQB↔aggregation-editor live bidirectional sync exists in source; it's an "Open in aggregation editor"-style one-way action. This is a significant positioning correction — any report describing Studio 3T's VQB as "real-time bidirectional sync" needs this fix.
- `AGG-code-gen`: corrected from "Java 2.x/3.x/4.x sub-tabs"/"eight languages" framing to: one language dropdown, 9 registered generators (MongoDB Shell, JavaScript/Node.js, Java, C#, Python, PHP, Ruby, with Java offering 2.x/3.x/4.x driver-API variants within the single Java entry) — 7 distinct target languages, not 8, and no separate sub-tabs.
- `AGG-stage-modes`: corrected — no form/visual or wizard stage-editing mode exists; only a raw JSON editor per stage (with operator-insertion templates).
- `AGG-chart-builder`: confirmed absent (no evidence in code).
- `QUERY-view-split` and `QUERY-charts-dashboards` (both added 2026-07-28 from marketing-page review): **zero corroborating source code found**. Downgrade from confirmed/roadmap to absent/unverified pending re-verification; flag for whoever owns those dictionary entries.
- New capability: `QUERY-value-search` (F-QUERY, see §1) — cross-collection value/field-name search, Professional+.

## 7. F-SQL — dialect/scope corrections, no exclusivity claims affected

- The SQL query engine's dialect is an ANTLR4-based, heavily-modified fork of the public `sqlite-parser` grammar — **not MySQL** as might be assumed from naming.
- `SQL-join-mapping`: corrected — no visual/drag-drop JOIN mapping editor exists; joins are authored as plain SQL text, and only single equality-comparison JOIN conditions are supported (compound ANDed joins throw `NotImplementedException`). Any report implying a visual JOIN editor is wrong.
- Confirmed-absent SQL constructs (worth stating explicitly rather than leaving unstated): CASE/WHEN, CAST, COLLATE, RAISE, MATCH, all subqueries, WITH/CTEs, compound SELECT (UNION/INTERSECT/EXCEPT). No BI/ODBC/JDBC-server connectivity exists.
- Scope note: F-SQL's dictionary section and Studio 3T's `sql-tools` folder currently bundle two distinct things — the SQL **query** engine (`SQL-expressions`, `SQL-join-mapping`, `SQL-code-gen`, `SQL-query-manager`) and the SQL **migration/reschema** toolchain (which is really F-TRANSFER's remit). Not resolved in this pass; flagged for a future dictionary clarification, not something downstream reports need to fix themselves.

## 8. F-GOV — audit logging much narrower than documented; several claims corrected

- **`GOV-audit-log`**: narrowed. A real, shipped local audit trail exists (tamper-evident chained-MD5 `audit.log`) but only logs **Connection Manager actions** (create/edit/delete/duplicate/import connections) — not queries or document modifications — and is **off by default**, enabled only via Windows Group Policy/registry. A separately-built HTTP audit-event sender to 3T Access exists in code but has **zero call sites** — unwired scaffolding, not a shipped feature; treat as roadmap/unverified, not confirmed.
- `GOV-cred-storage-os`: corrected — real mechanism is a local BouncyCastle file-based keystore, **not** OS Keychain/Windows Credential Manager/Keytar.
- `GOV-startup-policy`: corrected — real mechanism is **Windows-only** Group Policy/registry/manifest, not EJSON/YAML config.
- `GOV-cli-policy`: **confirmed absent** (no supporting code — only one unrelated CLI flag exists).
- `GOV-protect-mode`: flagged as likely a duplicate of `GOV-readonly-mode` (no distinct code) — not deleted, just flagged.
- `GOV-isolated-edition`: **absent** for Studio 3T Desktop (only appears as a MongoDB Compass detection string in code).
- Confirmed accurate, no change: Ultimate-edition gating of Kerberos/LDAP/AWS IAM/OIDC, `GOV-network-policy` outbound kill switch, telemetry controls, RBAC (MongoDB server-side, Professional tier), data masking (Ultimate-gated, no PII classification/compliance templates — those remain 3T Lens/3TL Bridge only).
- Studio 3T's governance `feature-matrix.md` previously had **no real content** ("has not yet been authored" placeholder) — it is now fully authored with a 20-ID table. Any report describing Studio 3T's F-GOV matrix as "not yet authored" is now stale.

## 9. F-CONN — edition-gating corrections, one likely-erroneous entry, new capabilities

- Edition names resolved definitively: **Free / Community Edition / Professional / Ultimate** (no separate "Pro/Base" display name — internal alias only).
- Several sub-features previously marked "All editions" are actually Professional-tier+: SSH Profile management (`CONN-ssh`'s advanced form), connection color-coding (`CONN-color-coding`), and the read-only lock toggle (`CONN-readonly-lock`).
- `CONN-test-steps`: overstated — no step-by-step diagnostic wizard exists, just a single "Test Connection" button plus a telemetry-only error classifier.
- `CONN-compat-redis`: **zero code evidence found anywhere** in the module — likely a documentation error; downgrade to absent/unverified.
- No OS-native credential store (Keychain/Windows Credential Manager/libsecret) is used for connection **passwords** — only for TLS certificates (corroborates the F-GOV `GOV-cred-storage-os` finding independently).
- New capabilities added to dictionary (see §1): Session Restore, Git-backed connection sharing, Access Manager tree integration.

## 10. F-AI — most time-sensitive correction: AI Helper flipped to disabled-by-default

- **As of release 2026.12.0 (17-Jul-2026), AI Helper is disabled by default (opt-in)** — a reversal of the previously-documented default-enabled/opt-out model. Any report crediting Studio 3T with AI being "on by default" or lower-friction than competitors needs re-examination.
- MCP tool names corrected: `find_documents` (not `query`), `get_collection_stats` (not `get_collection_statistics`).
- `AI-004` ("no validation" claim): corrected — a real mismatch/guard-rail layer exists (`GlobalAiHelperChangeActionCoordinator`), see new `AI-guardrail-layer` ID.
- `AI-006` "Ctrl+Enter to send" flagged as possibly backwards (plain Enter sends, Ctrl+Enter inserts newline) — marked unverified pending manual UI check, not asserted definitively.
- Local MCP server details reconfirmed exactly as previously documented: port 27117, loopback-only, no auth, single-session, Ultimate-edition gate, 2026.9.0 ship date.
- Six new capabilities added to dictionary (see §1): AI Helper Plus agentic mode, bundled offline MCP server, tab-context registry, chart rendering, multi-conversation support, guard-rail layer.

## 11. F-SHELL — several corrections, five new capabilities

- "Monaco editor" claim flagged as likely incorrect (real editor is a custom Eclipse JFace/SWT `StyledText`-based component) — medium confidence, marked for follow-up rather than asserted as definitively wrong.
- "Save to Query Manager" for shell scripts: downgraded to unverified (only plain file Save/Open confirmed in code).
- `SHELL-reconnect`/auto-reconnect: downgraded to unverified (no IntelliShell-specific evidence found).
- Query Assist mode is silently force-disabled when a custom (non-bundled) mongosh path is set — an undocumented interaction worth surfacing.
- Five new capabilities added to dictionary (see §1): destructive-command detection/warning, result-tab count limit, script bookmarks, OIDC shell auth, Stored JS rename.

## What downstream reports need (for the agents applying this file)

1. **`reports/gap-analysis-not-on-3t-products.md`** and **`reports/gap-analysis-not-on-3t-desktop.md`**: fix the "13 confirmed absent (all in F-SCHEMA)" count → 9 (§2), and update the "Takeaway"/summary framing accordingly. `gap-analysis-not-on-3t-desktop.md` additionally check its "17 present elsewhere in 3T family" and "78 unverified" buckets for any of the F-SCHED items that moved to absent (§3) or F-IDX items now confirmed (§4) — those counts may shift too.
2. **`reports/cumulative-report.md`**: the feature-matrix count is already flagged stale (28 vs. real 35) — also note the sub-feature-ID count has grown from 311 to 328 (17 new IDs added, §1), and reflect the F-SCHEMA gap correction (§2) and F-SCHED completeness downgrade (§3) in the executive summary/coverage matrix if it discusses Studio 3T's completeness.
3. **`reports/comparisons/high-level-product-comparison.md`**: correct any Studio 3T row for F-AGG/F-QUERY (VQB "bidirectional sync" → one-way, §6), F-SQL (JOIN mapping, §7), F-TRANSFER (masking count, SQL dialects, §5), F-GOV (audit logging scope, §8), F-IDX (index copy-paste tier, §4), F-AI (opt-in reversal, §10).
4. **`reports/comparisons/low-level-feature-comparison.md`**: update the specific Studio 3T cells for every corrected/new sub-feature ID listed above (§§1-11) — this is the most granular report and needs the most row-level edits. Add rows for all 17 new sub-feature IDs (§1) with Studio 3T's confirmed status and other products left unverified/❓ unless independently known.

Do not touch `product-suite/` (already handled, read-only) or re-litigate findings — this file is the single source of truth for what changed; cite it (`research/studio-3t-desktop-review-2026/12-consolidated-corrections.md`) rather than re-deriving.
