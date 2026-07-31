# Gap Analysis — Sub-features NOT on Studio 3T Desktop

This report checks **every sub-feature ID in [feature-dictionary.md](../feature-dictionary.md)** (328 unique IDs across all 11 feature areas) against whether it is confirmed present on the **Studio 3T Desktop IDE specifically** — as distinct from the broader 3T Software Labs product family (3T Explore, 3T MCP, 3T Lens, 3T Access, 3TL Bridge), which since 2026-07-29 are documented in their own product folders under `products/3t/` (see [products/3t/README.md](../products/3t/README.md)).

## Navigation

- [Cumulative report index](cumulative-report.md)
- [Low-level feature comparison](comparisons/low-level-feature-comparison.md)
- [High-level product comparison](comparisons/high-level-product-comparison.md)
- [Feature dictionary](../feature-dictionary.md)
- [Studio 3T product report](../products/3t/studio-3t/product-report.md)
- [Companion report: NOT on any 3T product](gap-analysis-not-on-3t-products.md)

**Last reviewed:** 2026-07-31 — corrections from [research/studio-3t-desktop-review-2026/](../research/studio-3t-desktop-review-2026/)

## Methodology

Same master checklist and status source as the [companion report](gap-analysis-not-on-3t-products.md#methodology) — the full 328-ID dictionary, checked against `low-level-feature-comparison.md`'s "Studio 3T" column (which represents the whole 3T product family as one merged column), with product `feature-matrix.md` files used to catch consolidation/aliasing false positives rather than as a literal row-by-row check.

Sections, in order of severity:

1. **Confirmed absent from the whole 3T portfolio** — identical to the companion report, since if no 3T product has it, Desktop doesn't either.
2. **Present in the portfolio, but not Desktop-native** — the section unique to this report: sub-features confirmed supported somewhere in the 3T family, but delivered by 3T Explore, 3T MCP, 3T Lens, 3T Access, or 3TL Bridge as a separate product, not by the Desktop IDE.
3. **Confirmed absent from Studio 3T Desktop specifically, portfolio-wide status unverified** — a category unique to this report: the 2026-07-31 source-code re-audit confirmed these sub-features are absent from Studio 3T Desktop's task scheduler, but whether an equivalent exists elsewhere in the 3T family (e.g. 3T Lens/3TL Bridge scheduling) was not confirmed either way.
4. **Unverified** and **dictionary aliases** — identical to the companion report.

## 1. Confirmed absent from the whole 3T portfolio (9)

All 9 are in **F-SCHEMA (Schema)**, scoped to the JSON-Schema-tree-editor and visual-ERD/canvas cluster — see the [companion report](gap-analysis-not-on-3t-products.md#confirmed-absent--no-3t-product-supports-this-9) for the full table. IDs: `SCHEMA-geo-analysis`, `SCHEMA-json-editor`, `SCHEMA-bson-types`, `SCHEMA-field-constraints`, `SCHEMA-designer-canvas`, `SCHEMA-designer-auto`, `SCHEMA-designer-links`, `SCHEMA-designer-color`, `SCHEMA-designer-portability`.

**Correction (2026-07-31):** the 2026-07-31 Studio 3T Desktop source-code re-audit found that `SCHEMA-validation-model`, `SCHEMA-validation-strictness`, `SCHEMA-validation-ui`, and `SCHEMA-deploy-validator` are in fact confirmed present on Studio 3T Desktop itself (a real, mature collection-validator authoring/deployment feature) — they have been removed from this list (was 13, now 9). `SCHEMA-validation-limits` (previously unverified) is likewise now confirmed present on Desktop and is not counted anywhere in this report. See [12-consolidated-corrections.md §2](../research/studio-3t-desktop-review-2026/12-consolidated-corrections.md#2-f-schema--biggest-correction-gap-analysis-13-confirmed-absent-must-become-9).

## 2. Present in the 3T portfolio, but NOT on Studio 3T Desktop (17)

These are **not gaps for 3T Software Labs as a company** — every one is confirmed supported by a named 3T product. They are gaps **for the Desktop IDE specifically**: a user who only has Studio 3T Desktop installed does not get these without adopting a separate product.

### F-AI — AI Features (3, via 3T MCP / 3T Explore)

| Sub-feature ID | Name | Delivered by |
| --- | --- | --- |
| AI-010 | 3T MCP standalone binary (stt-cli) | [3T MCP](../products/3t/3t-mcp/product-report.md) |
| AI-011 | 3T MCP capabilities (collection browsing, query, schema, PII scanner) | [3T MCP](../products/3t/3t-mcp/product-report.md) |
| AI-012 | 3T Explore AI Helper | [3T Explore](../products/3t/3t-explore/product-report.md) |

### F-GOV — Governance & Security (14, via 3T Lens / 3T Access / 3TL Bridge / 3T Explore)

| Sub-feature ID | Name | Delivered by |
| --- | --- | --- |
| GOV-platform-lens | 3T Lens centralized connection management | [3T Lens](../products/3t/3t-lens/product-report.md) |
| GOV-002 | 3T Lens compliance policy templates | [3T Lens](../products/3t/3t-lens/product-report.md) |
| GOV-003 | 3T Lens alert channels | [3T Lens](../products/3t/3t-lens/product-report.md) |
| GOV-004 | 3T Lens PII classification | [3T Lens](../products/3t/3t-lens/product-report.md) |
| GOV-005 | 3T Lens versioned field history and document diffs | [3T Lens](../products/3t/3t-lens/product-report.md) |
| GOV-006 | 3T Lens query performance suggestions | [3T Lens](../products/3t/3t-lens/product-report.md) |
| GOV-007 | 3T Lens MCP integration (59 tools) | [3T Lens](../products/3t/3t-lens/product-report.md) |
| GOV-platform-access | 3T Access identity and governance plane | [3T Access](../products/3t/3t-access/product-report.md) |
| GOV-platform-cdc | 3TL Bridge CDC pipeline engine | [3TL Bridge](../products/3t/3tl-bridge/product-report.md) |
| GOV-010 | 3TL Bridge Transform Studio | [3TL Bridge](../products/3t/3tl-bridge/product-report.md) |
| GOV-011 | 3TL Bridge real-time PII masking | [3TL Bridge](../products/3t/3tl-bridge/product-report.md) |
| GOV-012 | 3TL Bridge security and identity (multi-provider OIDC) | [3TL Bridge](../products/3t/3tl-bridge/product-report.md) |
| GOV-013 | 3TL Bridge deployment and scaling (Kubernetes Helm/Docker Compose) | [3TL Bridge](../products/3t/3tl-bridge/product-report.md) |
| GOV-platform-explore | 3T Explore browser IDE workspace (Workspace Switcher + Access Control) | [3T Explore](../products/3t/3t-explore/product-report.md) |

## 3. Confirmed absent from Studio 3T Desktop specifically, portfolio-wide status unverified (9)

The 2026-07-31 Studio 3T Desktop source-code re-audit (see [12-consolidated-corrections.md §3](../research/studio-3t-desktop-review-2026/12-consolidated-corrections.md#3-f-sched--task-scheduler-completeness-moved-down-more-absentpartial-than-previously-documented)) confirmed these F-SCHED (Task Scheduler) sub-features are genuinely absent from Studio 3T Desktop's scheduler implementation. Unlike section 1, this is **not** a portfolio-wide absence claim — whether an equivalent exists elsewhere in the 3T family (e.g. 3T Lens or 3TL Bridge scheduling/orchestration capabilities) was not checked in this pass and remains unverified. These IDs are therefore removed from the "unverified" bucket (section 4) but are not added to section 1 or section 2 either.

| Sub-feature ID | Name |
| --- | --- |
| SCHED-status-states | Task status states |
| SCHED-exec-config | Execution config |
| SCHED-retry | Retry policy |
| SCHED-concurrent | Concurrent execution |
| SCHED-batch | Batch size |
| SCHED-history | Execution history |
| SCHED-history-retention | History retention |
| SCHED-notifications | Notifications |
| SCHED-email | Email provider config |

## 4. Unverified — not confirmed present or absent on Studio 3T Desktop (54)

Mostly identical to the companion report's unverified list — see [gap-analysis-not-on-3t-products.md](gap-analysis-not-on-3t-products.md#unverified--not-confirmed-present-or-absent-78) for the full breakdown by feature area (F-CONN, F-QUERY, F-AGG, F-SCHEMA, F-IDX, F-TRANSFER, F-SHELL, F-AI, F-SQL, F-GOV, F-SCHED), **except** that for Studio 3T Desktop specifically the count is lower than the companion report's 78: 14 F-IDX sub-feature IDs that previously had no matrix row are now confirmed present on Studio 3T Desktop (real-time monitoring via `ServerStatusChartsTab.java`/`TaskMonitorTab.java` among them — see [12-consolidated-corrections.md §4](../research/studio-3t-desktop-review-2026/12-consolidated-corrections.md#4-f-idx--mostly-matrix-gaps-filled-in-14-new-rows-plus-two-factual-error-corrections-and-one-edition-gating-fix)), `SCHEMA-validation-limits` is now confirmed present (see section 1 correction note above), and the 9 F-SCHED IDs above have moved to section 3. Net: 78 − 14 (F-IDX, now confirmed present) − 1 (`SCHEMA-validation-limits`, now confirmed present) − 9 (F-SCHED, moved to section 3) = **54**.

## 5. Dictionary aliases excluded from the counts above (17)

Identical to the companion report — see [gap-analysis-not-on-3t-products.md](gap-analysis-not-on-3t-products.md#dictionary-aliases-excluded-from-the-counts-above-17) for the full table.

## Known gap in this analysis: Desktop-native governance is under-documented, not confirmed absent

Eight governance sub-feature IDs are referenced by the comparison reports **against Studio 3T specifically** (not the split-out platform products) but have no dedicated capability matrix backing them in `products/3t/studio-3t/features/governance/feature-matrix.md` — that file's content was entirely about the five platform products before the 2026-07-29 split (see its Scope note). These are a **pre-existing documentation gap**, not confirmed-absent or confirmed-present, and are intentionally excluded from sections 1–4 above (they're already counted as "implemented" in the coverage accounting below, based on the comparison report's own detail text, but no dedicated Desktop matrix row backs that classification):

| Sub-feature ID | Name | Comparison-report status for Studio 3T |
| --- | --- | --- |
| GOV-readonly-mode | Protect / destructive-write prevention mode | 🧪 partial |
| GOV-cred-protection | Credential protection mechanism | ✅ confirmed |
| GOV-rbac-users | RBAC user management dashboard | 🔌 via 3T Access platform |
| GOV-rbac-roles | RBAC role configuration | 🔌 via 3T Access platform |
| GOV-audit-log | Audit logging | 🔌 via 3T Lens platform |
| GOV-collection-compare | Collection compare | 💼 Pro/Base+ |
| GOV-collection-sync | Collection sync | 💼 Pro/Base+ |
| GOV-data-masking | Data masking | 💼 Pro/Base+ |

If Studio 3T Desktop's own governance UI is ever independently deep-analyzed (as opposed to reasoning from the comparison report's summary claims), this list is where that work should start.

## Coverage accounting

328 dictionary IDs = 239 implemented somewhere in the 3T portfolio, of which **222 are Desktop-native** and **17 are portfolio-only (section 2)** + 9 confirmed absent portfolio-wide (section 1) + 9 confirmed absent from Studio 3T Desktop specifically, portfolio-wide unverified (section 3) + 54 unverified (section 4) + 17 dictionary-alias redundancies (section 5).

(Reconciliation from the previous 311/203/186/13/78 figures: +17 new dictionary IDs, all Studio-3T-Desktop-confirmed, added to Desktop-native present; +4 F-SCHEMA IDs and +1 `SCHEMA-validation-limits` moved from absent/unverified to Desktop-native present; +14 F-IDX IDs moved from unverified to Desktop-native present; 9 F-SCHED IDs split out of unverified into the new section-3 bucket. See [12-consolidated-corrections.md](../research/studio-3t-desktop-review-2026/12-consolidated-corrections.md) for full detail.)
