# Stage 1 — Candidate Long-List

## Navigation

- [← Research plan](01-research-plan.md)
- [← Data inventory & source tiers](02-data-inventory.md)
- [Next stage: scored long-list →](04-scored-longlist.md)

## Method executed

- **1a.** Extracted all 108 tracked IDs from `gap-analysis-not-on-3t-desktop.md` / `gap-analysis-not-on-3t-products.md` (13 confirmed-absent + 17 present-elsewhere-in-3T-family + 78 unverified), grouped by feature area.
- **1b.** Re-derived every explicit "should build X" / gap statement from all 21 `google_research` files (both from `overview.md`'s condensed summaries and, where a recommendation needed more context, the full source file).
- **1c.** Pulled Studio 3T's own `product-report.md` "Strategic risks/gaps" and "Open questions."
- **1d.** Tagged all 7 VoC pilot records as missing-capability vs. bug-in-existing-feature.
- **1e.** Ran 5 fresh compliant web searches to check for drift since the `google_research` analysis dates (~mid-2026) — findings noted inline below and flagged where they affect a candidate's status.

## 1e. Fresh web research — drift findings (2026-07-30)

| Finding | Source | Affects |
|---|---|---|
| Studio 3T 2026.4 (25-Feb-2026) added "local file support, enabling users to save and load MongoDB and SQL connections from the local file system, **including Git-backed folders**" | [Studio 3T changelog](https://files.studio3t.com/changelog/changelog.txt) | **Candidate 3 (Git integration)** — this is evidence Studio 3T already ships *some* Git-adjacent capability (connection configs in git-backed folders). Whether this extends to queries/pipelines/scheduler configs with a commit/diff/PR workflow, or is limited to connection files, is **unverified** and must be checked directly in Stage 3 before scoring this candidate further. |
| Studio 3T 2026.10 shipped a new local MCP server; 2026.5 improved AI Helper (runtime model fetching); OIDC token caching now optional | [Studio 3T changelog](https://files.studio3t.com/changelog/changelog.txt) | Confirms AI-007 (Local MCP Server) and AI Helper are actively evolving; does not resolve the "no bundled LLM, external API key required" strategic risk noted in the product report. |
| No GUI competitor (DBeaver, DataGrip, Navicat) was found in 2026 comparison articles to have shipped a named "index advisor" / "query optimizer" feature; MongoDB's own Atlas Performance Advisor is a **platform** (Atlas cloud), not a **GUI client**, capability | [DataGrip vs DBeaver 2026 – QueryGlow](https://queryglow.com/blog/datagrip-vs-dbeaver), [Bytebase Navicat alternatives 2026](https://www.bytebase.com/blog/top-navicat-alternative/) | **Candidate 1 (AI query/index advisor)** — lowers Competitive Urgency (nobody's shipped this at the GUI-client layer yet) but *raises* its fit for the "widen the lead" objective specifically: this would be a first-to-market move among MongoDB desktop GUIs, not a catch-up. Scored explicitly with this nuance in Stage 2. |
| MongoDB Compass confirmed to expose In-Use Encryption (view encrypted fields under Advanced Connection options); Queryable Encryption (QE) is the recommended forward path, CSFLE is being superseded | [MongoDB QE/CSFLE docs](https://www.mongodb.com/docs/v8.0/core/queryable-encryption/about-qe-csfle/), [CSFLE→QE migration guide](https://oneuptime.com/blog/post/2026-03-31-mongodb-migrate-csfle-to-queryable-encryption/view) | **Candidate 9 (QE/CSFLE key-vault UI)** — confirms Compass's exclusivity claim from `cumulative-report.md` still holds in 2026; also means if built, Studio 3T should target **QE specifically**, not legacy CSFLE, since MongoDB itself is steering customers off CSFLE. |
| Secrets-vault market (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault) in 2026 centers on **dynamic, short-lived credentials** and automatic rotation, not just static retrieval | [HashiCorp Vault vs AWS Secrets Manager 2026](https://sanj.dev/post/hashicorp-vault-aws-secrets-azure-key-vault-comparison/) | **Candidate 5 (secrets vault integration)** — if built, the bar is dynamic/rotating credential support, not a simple "read a static secret" integration; raises the effort estimate. |
| A direct search of `community.studio3t.com` for Git/version-control requests around aggregation/queries surfaced no explicit thread (only general Aggregation Editor feature discussions) | community.studio3t.com search | No additional Tier C corroboration found for Candidate 3 beyond the changelog finding above — noted as an evidence gap, not treated as absence of demand. |

## 1d. VoC pilot record tagging

| # | Record (see `voice-of-customer-metrics.md`) | Tag |
|---|---|---|
| 1 | Array masking bug (only first object in array masked) | **Bug in existing feature** — out of scope (TRANSFER-masking-types already implemented; this is a defect, not a missing capability) |
| 2 | No way to trigger a saved export task from outside Studio 3T with runtime parameters | **Missing capability** — direct corroboration for **Candidate 4 (Headless CLI/CI-CD automation)** |
| 3 | Shell executable fails to start in Community Edition | **Bug in existing feature** — out of scope |
| 4 | All non-authenticated stored connections broke after an update, required full reinstall | **Bug in existing feature** — out of scope |
| 5 | IntelliShell doesn't honor proxy settings the GUI does | **Bug in existing feature** — out of scope (though it touches CONN-proxy, a dictionary ID already marked implemented for the GUI; the gap is IntelliShell-specific inconsistency, not a net-new capability) |
| 6 | Confusing "Query Failed" on sort of 1.3M-doc collection until "Allow disk use" was found in Find Query Options | **Existing capability, discoverability problem** — out of scope (the capability exists; this is a UX/defaults issue) |
| 7 | Catastrophic loss of 20+ saved connections with no explanation | **Bug in existing feature** — out of scope |

Only VoC record #2 represents a genuine missing-capability candidate; the other six are defects or discoverability problems in already-implemented features, which this decision explicitly excludes per the agreed candidate-universe rule. This is a real finding worth surfacing on its own: **6 of 7 real, cited customer pain points in our only direct-quote data source are about reliability/UX of existing features, not missing capabilities** — noted for the memo's limitations/context section, since it's a meaningful signal even though it falls outside this specific decision's scope.

## Headline candidates (full Research Result Cards in Stage 2)

Long-list table — 20 headline candidates, each converging from 2+ independent sources (the bar for "headline" vs. "atomic gap" below).

| # | Candidate | Feature area | Source tags | Segment hint |
|---|---|---|---|---|
| 1 | AI-driven query/index performance advisor (autonomous explain-plan analysis + index recommendations) | F-IDX (`IDX-perf-insights`, unverified) + new F-AI tie-in | B: studio-3t-review-mining, nosqlbooster-competitive-analysis, nosqlbooster-competitive-intelligence-analysis, mongodb-ai-automation-opportunities, mongodb-evolution-and-roadmap; D: competitor drift search | Both |
| 2 | IntelliShell interactive script debugger (breakpoints, step execution, variable inspection) | F-SHELL — NEW (no dictionary ID) | B: nosqlbooster-competitive-analysis, nosqlbooster-competitive-intelligence-analysis | Individual devs primarily, some startup |
| 3 | Native Git/version-control integration for queries, pipelines, scheduler configs (commit/diff/PR workflow) | F-QUERY/F-AGG/F-SCHED — NEW, partially overlaps `mongodb-developer-workflow-automation`'s "declarative migration frameworks" | B: studio-3t-missing-integrations, mongodb-developer-workflow-automation; D: Studio 3T 2026.4 changelog (partial prior art — connections only) | Both |
| 4 | Headless CLI / CI-CD pipeline automation (trigger Task Scheduler, masking, Data Compare from GitHub Actions/GitLab CI/Jenkins) | F-SCHED/F-TRANSFER/F-GOV — NEW | B: studio-3t-missing-integrations; **C: VoC record #2 (direct customer ask, 3T staff confirmed absent)** | Both — enterprise CI/CD teams and startups with automated pipelines alike |
| 5 | Secrets vault integration (HashiCorp Vault / AWS Secrets Manager / Azure Key Vault) for dynamic credential retrieval | F-CONN/F-GOV — NEW | B: studio-3t-enterprise-gap-analysis, studio-3t-missing-integrations; D: 2026 secrets-management market search | Enterprise/regulated primarily |
| 6 | Centralized SIEM/audit-log export (Splunk/Datadog/Grafana) at the Desktop level | F-GOV — NEW (distinct from 3T Lens's own separate audit trail) | B: studio-3t-enterprise-gap-analysis, studio-3t-missing-integrations | Enterprise/regulated |
| 7 | Just-In-Time temporary access + dynamic query-layer data masking (governance control-plane features) | F-GOV — NEW (distinct from existing static `TRANSFER-masking-tool`) | B: studio-3t-enterprise-gap-analysis | Enterprise/regulated |
| 8 | Desktop app-level SSO / IdP federation (Entra ID/Okta) — distinct from MongoDB-cluster OIDC auth already supported | F-CONN/F-GOV — NEW | B: studio-3t-enterprise-gap-analysis | Enterprise/regulated |
| 9 | Queryable Encryption (QE)/CSFLE key-vault configuration UI | F-CONN (`CONN-in-use-enc`, unverified) | A: gap-analysis (unverified); B: mongodb-evolution-and-roadmap, mongodb-gui-technology-trends; product-report cumulative-report.md (confirmed Compass-exclusive); D: QE/CSFLE 2026 confirmation | Enterprise/regulated (compliance-driven) |
| 10 | Native BI/dashboard builder ("3T Insights" style) | F-QUERY (`QUERY-charts-dashboards`, unverified) | A: gap-analysis (unverified, added from VisuaLeaf's own confirmed feature); B: navicat-competitive-intelligence-analysis | Both |
| 11 | Visual ERD designer / JSON-Schema editor / validation-rule authoring UI | F-SCHEMA (13 confirmed-absent IDs) | **A: gap-analysis (confirmed absent, portfolio-wide)**; B: navicat-competitive-intelligence-analysis, mongodb-gui-competitor-landscape-analysis | Both — but this is the "close the gap" candidate the stated objective (widen the lead) explicitly deprioritizes; kept in long-list per the "both" scope decision |
| 12 | AI-driven schema anti-pattern/health advisor (detect unbounded arrays, excessive `$lookup`, unindexed patterns) | F-SCHEMA/F-AI — NEW, distinct from #11 (diagnostics vs. design/validation UI) | B: mongodb-ai-automation-opportunities | Both |
| 13 | Synthetic/constrained test-data generator for CI/CD (compliance-safe edge-case data) | F-TRANSFER/F-AI — NEW | B: mongodb-ai-automation-opportunities | Enterprise/regulated (compliance testing), also startups doing CI |
| 14 | Federated cross-database querying (MongoDB + external relational join) | F-SQL/F-CONN — NEW | B: datagrip-competitive-analysis | Both, but likely large effort |
| 15 | VS Code / JetBrains companion IDE extension | New product surface — NEW | B: studio-3t-missing-integrations | Individual devs, startups |
| 16 | Deeper Vector Search tooling (index profiler, hybrid vector+scalar query builder) | F-IDX (`IDX-vector-search`, unverified) | A: gap-analysis (unverified); B: datagrip-competitive-analysis, mongodb-evolution-and-roadmap, mongodb-gui-technology-trends | Both — AI/RAG-building startups and enterprise alike |
| 17 | Enterprise AI gateway / centrally-managed SSO for AI Helper (replace per-user external API keys) | F-AI — NEW | B: studio-3t-missing-integrations; **A: Studio 3T product-report's own "Strategic risks/gaps" (AI Helper requires external API keys, no bundled LLM)** | Enterprise/regulated |
| 18 | Slack/Teams/Jira/PagerDuty webhook notifications for Task Scheduler/compliance alerts | F-SCHED/F-GOV — proven concept elsewhere in 3T family | **A: gap-analysis "present-elsewhere" (`GOV-003`, built into 3T Lens, not Desktop)**; B: studio-3t-missing-integrations | Both |
| 19 | Automated PII classification/discovery (auto-scan collections, flag likely-PII fields) | F-GOV — proven concept elsewhere in 3T family, twice | **A: gap-analysis "present-elsewhere" (`GOV-004` via 3T Lens, `AI-011` PII scanner via 3T MCP)** | Enterprise/regulated primarily |
| 20 | Schema drift detection / versioned field history (diff schema across snapshots) | F-SCHEMA/F-GOV — proven concept elsewhere in 3T family | **A: gap-analysis "present-elsewhere" (`GOV-005` via 3T Lens)** | Both |

## Atomic dictionary gaps — triaged, not individually carded

The remaining dictionary-tracked IDs not absorbed into a headline candidate above are single-checkbox-sized items (one UI control, one option, one format) rather than a cohesive "feature to widen the lead." Carrying each of the ~78 unverified + remaining confirmed-absent/present-elsewhere IDs as a full 5-axis card would misrepresent their scale relative to the 20 headline candidates. They are listed here in full for completeness (the "don't silently drop coverage" principle), grouped by feature area, and are **not** expected to survive to the shortlist on Reach/Severity grounds alone — Stage 2 gives them a single blanket assessment rather than 78 individual ones.

<details>
<summary>Full list of 78 unverified + non-headline present-elsewhere IDs (click to expand)</summary>

**F-CONN (9 unverified):** CONN-uri-export, CONN-multi-active, CONN-in-use-enc *(→ absorbed into Candidate 9)*, CONN-role-docs, CONN-test-steps, CONN-search-nav, CONN-compat-docdb, CONN-compat-cosmos, CONN-compat-redis

**F-QUERY (9 unverified):** QUERY-collation, QUERY-max-time, QUERY-run-variants, QUERY-cancel, QUERY-perf-timer, QUERY-undo-redo, QUERY-view-gridfs, QUERY-view-split, QUERY-charts-dashboards *(→ absorbed into Candidate 10)*

**F-AGG (4 unverified):** AGG-pagination, AGG-timer-cancel, AGG-chart-builder, AGG-stage-count

**F-SCHEMA (2 unverified, distinct from the 13 confirmed-absent):** SCHEMA-validation-limits, SCHEMA-designer-layouts *(both effectively sub-items of Candidate 11 if it proceeds)*

**F-IDX (10 unverified):** IDX-type-hashed, IDX-atlas-search, IDX-vector-search *(→ absorbed into Candidate 16)*, IDX-advanced-opts, IDX-quick-actions, IDX-profiler-export, IDX-profiler-live, IDX-perf-insights *(→ absorbed into Candidate 1)*, IDX-realtime-perf, IDX-stop-ops

**F-TRANSFER (4 unverified):** TRANSFER-export-sql-stmts, TRANSFER-transform-filter, TRANSFER-transform-js, TRANSFER-transform-pipeline

**F-SHELL (4 unverified, excluding 3 pure dictionary aliases):** SHELL-minimap, SHELL-sessions-vars, SHELL-reconnect, SHELL-background

**F-AI (7 unverified, excluding 5 pure dictionary aliases):** AI-explanation, AI-schema-aware, AI-sample-context, AI-conversation, AI-privacy, AI-key-storage, AI-multi-config

**F-SQL (1 unverified):** SQL-query-manager

**F-GOV (11 unverified, excluding 1 pure dictionary alias; 4 present-elsewhere absorbed into headline candidates):** GOV-network-policy, GOV-telemetry, GOV-startup-policy, GOV-cli-policy, GOV-ai-controls, GOV-cred-storage-os, GOV-isolated-edition, GOV-air-gapped, GOV-rbac-inheritance, GOV-rbac-tree, GOV-rbac-actions — plus present-elsewhere GOV-002 (Lens policy templates, folded into Candidate 7's governance theme), GOV-006 (Lens query performance suggestions, folded into Candidate 1), GOV-007 (Lens MCP integration — not carried forward, redundant with Desktop's own AI Helper/MCP), GOV-platform-lens/access/cdc/explore and GOV-010/012/013 (each represents porting an entire separate product's function to Desktop — out of scope by definition of the effort ceiling)

**F-SCHED (7 unverified, excluding 1 pure dictionary alias):** SCHED-timezone, SCHED-exec-config, SCHED-progress, SCHED-plan-limits

**Present-elsewhere, not carried forward:** AI-010/AI-011 (3T MCP binary — Desktop already has its own Local MCP Server; distinct transport/deployment model, not a missing capability for Desktop users), AI-012 (3T Explore AI Helper — Desktop already has its own AI Helper)

</details>

## Long-list count check

20 headline candidates + 1 grouped "atomic gaps" entry = **21 line items**, satisfying the "15+" exhaustive-canvass target while keeping the long-list navigable. Every one of the 108 dictionary-tracked gap IDs is accounted for (either absorbed into a headline candidate or listed in the triaged group above) — none silently dropped.
