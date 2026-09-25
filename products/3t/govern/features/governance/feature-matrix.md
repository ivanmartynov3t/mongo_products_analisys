# Feature Matrix — Govern / Governance & Security

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)
- [3T Lens governance matrix](../../../3t-lens/features/governance/feature-matrix.md) (where these rows lived until 2026-09-25)

## Feature metadata

- Product name: Govern (3T platform track)
- Product group: 3t
- Feature ID: F-GOV (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `governance`
- Analysis date: 2026-09-25
- Version/release context: rows `GOV-002`–`GOV-009` moved here from 3T Lens on 2026-09-25 (owner decision). Internal sources pinned to `3tio/tools` commit `566d6f2` via `prod_info_silo` commit `cde319c742`.

## Source index

Every fact in the matrix carries its own `(S#)`. **Public** sources can be opened by any reader; **internal** sources are private 3T repositories, read through `prod_info_silo`.

Public:

- S1: https://studio3t.com/governed-data-access-platform — the "Govern" track description (silo copy `data/3t/3t-website-2026/governed-data-access-platform.md`, captured 2026-09-15)
- S2: https://studio3t.com/ — homepage product descriptions (silo copy `data/3t/3t-website-2026/index.md`)
- S3: https://studio3t.com/3t-lens/ — **removed: HTTP 404 on 2026-09-25**; last read for this analysis on 2026-07-29. Claims citing only S3 were public then but have no current public source.

Internal (private `3tio/tools` repository, commit `566d6f2`):

- S4: https://github.com/3tio/tools/blob/566d6f25c16450aa449bdf5c614be7ff7d0e8c7c/features/README.md — feature checklist
- S5: https://github.com/3tio/tools/blob/566d6f25c16450aa449bdf5c614be7ff7d0e8c7c/docs/policy-engine-integration.md
- S6: https://github.com/3tio/tools/blob/566d6f25c16450aa449bdf5c614be7ff7d0e8c7c/policy-engine/docs/policy-rules.md
- S7: https://github.com/3tio/tools/blob/566d6f25c16450aa449bdf5c614be7ff7d0e8c7c/docs/violation-observability-operator-guide.md
- S8: https://github.com/3tio/tools/blob/566d6f25c16450aa449bdf5c614be7ff7d0e8c7c/docs/pii-detector-integration.md
- S9: https://github.com/3tio/tools/blob/566d6f25c16450aa449bdf5c614be7ff7d0e8c7c/docs/release-readiness/pii-scanner-beta-readiness.md
- S10: https://github.com/3tio/tools/blob/566d6f25c16450aa449bdf5c614be7ff7d0e8c7c/docs/pii-scanner-brochure/3T-Lens-PII-Scanner-Brochure-v0.8.md
- S11: https://github.com/3tio/tools/blob/566d6f25c16450aa449bdf5c614be7ff7d0e8c7c/docs/mcp-access-control.md
- S12: https://github.com/3tio/tools/blob/566d6f25c16450aa449bdf5c614be7ff7d0e8c7c/mcp-server-rs/README.md

## Status legend

- **confirmed (public)** — a current public source (S1, S2) states it.
- **confirmed 2026-07-29, source removed** — stated on S3 before it was taken down; no current public source.
- **❓ internal only** — stated only in internal repository docs; not confirmed publicly.

## Why "Govern" and not 3T Lens

The public site describes these capabilities as the Govern track, which "checks what the pipeline delivered matches your policy", controls access "humans and AI agents alike", and "continuously monitors and alerts when something drifts" (S1). The homepage now describes 3T Lens only as read-only, governed access for people who "shouldn't change" data (S2), and the page that attributed these features to 3T Lens is gone (S3).

**Alternative attributions** (recorded so the move can be reversed if 3T clarifies):

- **3T Lens:** the removed page listed these features under 3T Lens (S3); the internal PII brochure is titled "3T Lens PII Scanner" (S10); `prod_info_silo` files the same `3tio/tools` docs under both `policy-engine` and `3t-lens`.
- **3T Access:** for `GOV-007` only — the homepage ties MCP governance to 3T Access: "AI agents calling your data through MCP follow the same rules" (S2).
- **Policy Engine / PII Scanner components:** the internal repository documents them as separate services (S5, S8); the #16 decision treats them as components, not products.

## Capability matrix

| Sub-feature ID | Capability | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GOV-002 | Govern — compliance policy templates | Supported | Policies are checked against what is delivered and accessed (S1). Ready-made templates in six categories — ACID, Schema, Index, Security, Naming, Operational (S3; same six in S4). Templates configurable per environment; one-click compliance health check per environment (S3). Custom connection-level policy editor and enable/disable per template (S4). | Which rules are modifiable: unverified (S3 did not say). | Policy checking: confirmed (public) (S1). Six categories, health check: confirmed 2026-07-29, source removed (S3). Editor, enable/disable: ❓ internal only (S4). | S1, S3, S4, S5, S6 | **Template count — three values:** 27 default templates (S4); "Default Policies (26 total)" (S5); "Scope: `global`. 21 policies" (S6) — the 21 is a global-scope subset, not a third total. The 27 vs 26 conflict is open. |
| GOV-003 | Govern — alert channels | Supported | Continuous monitoring with alerts "when something drifts" — schema update, broken pipeline rule, or a new collection with the wrong permissions (S1). Channels: Slack, email, webhooks, with configurable severity per channel (S3). Slack, email (with recipients), webhook, and a delivery test (S4). | Slack and webhook endpoints are configured by an administrator (S3). | Alerting on drift: confirmed (public) (S1). Named channels: confirmed 2026-07-29, source removed (S3); ❓ internal only (S4). | S1, S3, S4 | Severity per channel appears in S3 only; S4 does not mention it. |
| GOV-004 | Govern — PII classification | Supported | Automated PII scanning across collections, sensitivity grouping, timestamped scan records (S3). Four result groups — Critical / PII / Potentially Sensitive / Likely Safe — per-field detail tabs, scan history and delete (S4, S8). CSV/JSON export, a compliance-auditor view across the organisation, an append-only audit trail, role-based masking, and a feed into the Governance Proxy PII cache (S8, S10). | Heuristic; results need human review (S3). Release status: "Conditional GO for a design-partner beta on MongoDB. NOT ready for open/self-serve beta" (S9). | Scanning, grouping, records: confirmed 2026-07-29, source removed (S3). Everything else: ❓ internal only (S4, S8, S9, S10). | S3, S4, S8, S9, S10 | Public masking claims exist but belong to the Pipeline track: "Sensitive data is masked at source" (S1) — see 3TL Bridge `GOV-011`. Not used as evidence here. |
| GOV-005 | Govern — versioned field history and document diffs | Supported | Versioned field history catches breaking schema changes before production; document-level diffs compare two snapshots field by field (S3). | Versioning granularity unverified (S3 did not say). | Confirmed 2026-07-29, source removed (S3). Related public claim: alerts on "a schema update" (S1). | S1, S3 | No internal doc in the silo was checked for this row. |
| GOV-006 | Govern — query performance suggestions | Supported | Index recommendations inside the governance workspace (S3). Named index checks: unused index, redundant index, ESR ordering, COLLSCAN detection (S4, S5). | Algorithm and data source unverified. | Recommendations: confirmed 2026-07-29, source removed (S3). Named checks: ❓ internal only (S4, S5). | S3, S4, S5 | — |
| GOV-007 | Govern — MCP integration and governed tool access | Supported | AI agents are governed "humans and AI agents alike" (S1); "AI agents calling your data through MCP follow the same rules" (S2). Each tool is classified READ / WRITE / ADMIN and blocked above the `MCP_ACCESS_MODE` level, default `read` (S11). | Tool count is contested (see Notes). | Same rules for agents: confirmed (public) (S1, S2). Access modes: ❓ internal only (S11). | S1, S2, S3, S11, S12 | **Tool count — four values:** 59 tools in 10 categories (S3, removed); 60 tools, full build (S11, S12); 40 tools, read-only "lite" build (S12); 41 tools, "power user" build without admin (S12). S11/S12 do not name 3T Lens or Govern, so which build a customer gets is open. |
| GOV-008 | Govern — policy violations and compliance score | Supported | Compliance dashboard with a score and open-violation summary; violations list with an acknowledgement flow (S4). Admin violation observability with actor / client / application / request context; retention rules at platform, tenant and policy level, 1–3650 days, default 90 (S7). | Observability and retention appear in an operator guide (S7), not in the feature checklist (S4): shipped status unclear. | ❓ internal only (S4, S7). Nearest public claim: Govern "turns belief into evidence" and alerts "when reality doesn't match" (S1). | S1, S4, S7 | — |
| GOV-009 | Govern — scheduled policy evaluation | Supported | Scheduled `POLICY_EVALUATE` task type with a creation form and emailed results (S4, S5). | Planned, not shipped: a policy gate that blocks task creation when violations exist — "engine ready, client not yet wired" (S4). | ❓ internal only (S4, S5); policy gate: planned (S4). Nearest public claim: "continuously monitors" (S1). | S1, S4, S5 | — |

## Feature-level conclusion

### Confirmed strengths (public)

- Policy checking of delivered and accessed data, applied to humans and AI agents alike (S1, S2).
- Continuous monitoring with alerts on drift: schema updates, broken pipeline rules, wrongly permissioned collections (S1).

### Confirmed limitations

- PII scanning is heuristic and needs human review (S3); internally cleared only for a design-partner beta (S9).

### Open questions / unknowns

- Is Govern a product, or a track delivered by 3T Lens and 3T Access? The public site does not name the products inside it (S1); the removed page named 3T Lens (S3).
- Where did studio3t.com/3t-lens/ go? It returned 404 on 2026-09-25 and the homepage links to no 3T Lens page (S2, S3).
- MCP tool count a customer gets: 59, 60, 40 or 41 (S3, S11, S12).
- Default policy template count: 27 or 26 (S4, S5).
