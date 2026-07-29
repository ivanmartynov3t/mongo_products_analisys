# Feature Matrix — 3T Lens / Governance & Security

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Source index

- S1: https://studio3t.com/3t-lens/

## Capability matrix

| Capability ID | Capability | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GOV-platform-lens | 3T Lens — centralized connection management | Supported | MongoDB connections configured once in 3T Lens and shared automatically to all users. No shared passwords; no hidden connections. Access scoped before login via 3T Access roles. Same connection policies applied to both human users and AI agents. | 3T Lens is a separate product (browser-based); requires deployment distinct from the Desktop IDE. Integration with Desktop IDE connection manager is not explicitly documented. | confirmed | S1 | Access scoping depends on [3T Access](../../../3t-access/features/governance/feature-matrix.md) (GOV-platform-access). |
| GOV-002 | 3T Lens — compliance policy templates | Supported | Ready-made policy templates: ACID, Schema, Index, Security, Naming, Operational. Templates are configurable per environment. One-click compliance health check per environment. | Template customization scope (which rules are modifiable) is unverified. | confirmed | S1 | — |
| GOV-003 | 3T Lens — alert channels | Supported | Alert channels: Slack, email, webhooks. Configurable severity levels per channel. | Slack and webhook endpoints must be configured by the administrator. | confirmed | S1 | — |
| GOV-004 | 3T Lens — PII classification | Supported | Automated PII scanning across collections. Sensitivity grouping of fields. Scan records with timestamps provide an audit trail of when PII was discovered or reclassified. | Automated scanning uses heuristics; results require human review and verification. | confirmed | S1 | — |
| GOV-005 | 3T Lens — versioned field history and document diffs | Supported | Versioned field history catches breaking schema changes before they reach production. Document-level diffs provide exact field-by-field comparison between two dataset snapshots. | Versioning granularity (commit, time, or snapshot-based) is unverified. | confirmed | S1 | — |
| GOV-006 | 3T Lens — query performance suggestions | Supported | Index recommendations surfaced within the governance workspace. | Recommendation engine details (algorithm, data source) are unverified. | confirmed | S1 | — |
| GOV-007 | 3T Lens — MCP integration (59 tools) | Supported | 59 MCP tools across 10 categories available to AI agents within 3T Lens. Tools are governed by the same 3T Access role-based access policies as human users — AI agents cannot exceed the permissions of the access policy assigned to them. | 10 categories and full tool list are unverified beyond the count of 59 total. | confirmed | S1 | — |

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
