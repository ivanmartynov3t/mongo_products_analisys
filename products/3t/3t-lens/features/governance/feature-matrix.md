# Feature Matrix — 3T Lens / Governance & Security

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: 3T Lens
- Product group: 3t
- Feature ID: F-GOV (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `governance`
- Analysis date: 2026-07-29
- Version/release context: —

## Source index

- S1: https://studio3t.com/3t-lens/
- S2: https://github.com/3tio/tools/blob/566d6f25c16450aa449bdf5c614be7ff7d0e8c7c/features/README.md (internal repo, via prod_info_silo `data/3t/policy-engine`)
- S3: https://github.com/3tio/tools/blob/566d6f25c16450aa449bdf5c614be7ff7d0e8c7c/docs/policy-engine-integration.md (internal repo)
- S4: https://github.com/3tio/tools/blob/566d6f25c16450aa449bdf5c614be7ff7d0e8c7c/docs/violation-observability-operator-guide.md (internal repo)
- S5: https://github.com/3tio/tools/blob/566d6f25c16450aa449bdf5c614be7ff7d0e8c7c/docs/pii-detector-integration.md (internal repo)
- S6: https://github.com/3tio/tools/blob/566d6f25c16450aa449bdf5c614be7ff7d0e8c7c/docs/release-readiness/pii-scanner-beta-readiness.md (internal repo)
- S7: https://github.com/3tio/tools/blob/566d6f25c16450aa449bdf5c614be7ff7d0e8c7c/docs/mcp-access-control.md (internal repo)

## Capability matrix

| Capability ID | Capability | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GOV-platform-lens | 3T Lens — centralized connection management | Supported | MongoDB connections configured once in 3T Lens and shared automatically to all users. No shared passwords; no hidden connections. Access scoped before login via 3T Access roles. Same connection policies applied to both human users and AI agents. | 3T Lens is a separate product (browser-based); requires deployment distinct from the Desktop IDE. Integration with Desktop IDE connection manager is not explicitly documented. | confirmed | S1 | Access scoping depends on [3T Access](../../../3t-access/features/governance/feature-matrix.md) (GOV-platform-access). |
| GOV-002 | 3T Lens — compliance policy templates | Supported | Ready-made policy templates: ACID, Schema, Index, Security, Naming, Operational. Templates are configurable per environment. One-click compliance health check per environment. | Template customization scope (which rules are modifiable) is unverified. | confirmed | S1 | Internal docs (S2, S3) add: custom connection-level policy editor, enable/disable per template, and a template count that differs between the two docs (27 in S2, 26 in S3) — ❓ unverified against a public source (internal repo docs only, #31). |
| GOV-003 | 3T Lens — alert channels | Supported | Alert channels: Slack, email, webhooks. Configurable severity levels per channel. | Slack and webhook endpoints must be configured by the administrator. | confirmed | S1 | — |
| GOV-004 | 3T Lens — PII classification | Supported | Automated PII scanning across collections. Sensitivity grouping of fields. Scan records with timestamps provide an audit trail of when PII was discovered or reclassified. | Automated scanning uses heuristics; results require human review and verification. | confirmed | S1 | Internal docs (S2, S5) add: four result buckets (Critical / PII / Potentially Sensitive / Likely Safe), per-field detail tabs, scan history and delete, CSV/JSON export, compliance-auditor view across the organisation, append-only audit trail, role-based masking, and feed into the Governance Proxy PII cache. Status per S6: "Conditional GO for a design-partner beta", not open beta — ❓ unverified against a public source (internal repo docs only, #31). |
| GOV-005 | 3T Lens — versioned field history and document diffs | Supported | Versioned field history catches breaking schema changes before they reach production. Document-level diffs provide exact field-by-field comparison between two dataset snapshots. | Versioning granularity (commit, time, or snapshot-based) is unverified. | confirmed | S1 | — |
| GOV-006 | 3T Lens — query performance suggestions | Supported | Index recommendations surfaced within the governance workspace. | Recommendation engine details (algorithm, data source) are unverified. | confirmed | S1 | Internal docs (S2, S3) name the index evaluators: unused index, redundant index, ESR ordering, COLLSCAN detection — ❓ unverified against a public source (internal repo docs only, #31). |
| GOV-007 | 3T Lens — MCP integration (59 tools) | Supported | 59 MCP tools available to AI agents within 3T Lens, organized (per studio3t.com) into 10 categories. Tools are governed by the same 3T Access role-based access policies as human users — AI agents cannot exceed the permissions of the access policy assigned to them. | Only the total tool count (59) is independently confirmed; the "10 categories" grouping and the full per-category tool list are vendor claims, not independently verified. | confirmed (tool count); unknown/unverified (category breakdown) | S1 | An internal doc (S7) lists 60 MCP tools in 11 groups, each gated READ / WRITE / ADMIN by `MCP_ACCESS_MODE` (default `read`). S7 does not name 3T Lens, so whether it describes the same server as S1's "59 tools" is unconfirmed — ❓ unverified against a public source (internal repo docs only, #31). |
| GOV-008 | 3T Lens — policy violations and compliance score | Supported | Compliance dashboard with a score and open-violation summary; violations list with an acknowledgement flow (S2). Admin violation observability with actor / client / application / request context and retention rules at platform, tenant and policy level (1–3650 days, default 90) (S4). | Observability and retention: status unclear — described in an operator guide (S4), not in the feature checklist (S2). | ❓ unverified against a public source (internal repo docs only, #31) | S2, S4 | — |
| GOV-009 | 3T Lens — scheduled policy evaluation | Supported | Scheduled `POLICY_EVALUATE` task type with a creation form and email delivery of results (S2, S3). | Planned, not shipped: a policy gate that blocks task creation when violations exist ("engine ready, client not yet wired", S2). | ❓ unverified against a public source (internal repo docs only, #31); policy gate: planned | S2, S3 | — |

## Feature-level conclusion

### Confirmed strengths

- Centralized connection management eliminates shared-password credential hygiene failures.
- PII classification, versioned field history, and document diffs give proactive schema/compliance governance.
- AI agent MCP tools governed by the same access policies as human users.

### Confirmed limitations

- Separate deployable product — requires infrastructure provisioning.
- Automated PII classification uses heuristics and requires human review.

### Open questions / unknowns

- 10 categories and full tool list for the 59 MCP tools.
- Whether 3T Lens replaces or supplements the Desktop IDE connection manager in practice.
