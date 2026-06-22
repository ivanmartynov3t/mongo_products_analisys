# Feature Matrix — Studio 3T / Governance & Security

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Source index

- S1: https://studio3t.com/3t-lens/
- S2: https://studio3t.com/3tl-bridge/

## Capability matrix

| Capability ID | Capability | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GOV-platform-lens | 3T Lens — centralized connection management | Supported | MongoDB connections configured once in 3T Lens and shared automatically to all users. No shared passwords; no hidden connections. Access scoped before login via 3T Access roles. Same connection policies applied to both human users and AI agents. | 3T Lens is a separate product (browser-based); requires deployment distinct from the Desktop IDE. Integration with Desktop IDE connection manager is not explicitly documented. | confirmed | S1 | 3T Lens product; separate deployment. |
| GOV-002 | 3T Lens — compliance policy templates | Supported | Ready-made policy templates: ACID, Schema, Index, Security, Naming, Operational. Templates are configurable per environment. One-click compliance health check per environment. | Template customization scope (which rules are modifiable) is unverified. | confirmed | S1 | 3T Lens product. |
| GOV-003 | 3T Lens — alert channels | Supported | Alert channels: Slack, email, webhooks. Configurable severity levels per channel. | Slack and webhook endpoints must be configured by the administrator. | confirmed | S1 | 3T Lens product. |
| GOV-004 | 3T Lens — PII classification | Supported | Automated PII scanning across collections. Sensitivity grouping of fields. Scan records with timestamps provide an audit trail of when PII was discovered or reclassified. | Automated scanning uses heuristics; results require human review and verification. | confirmed | S1 | 3T Lens product. |
| GOV-005 | 3T Lens — versioned field history and document diffs | Supported | Versioned field history catches breaking schema changes before they reach production. Document-level diffs provide exact field-by-field comparison between two dataset snapshots. | Versioning granularity (commit, time, or snapshot-based) is unverified. | confirmed | S1 | 3T Lens product. |
| GOV-006 | 3T Lens — query performance suggestions | Supported | Index recommendations surfaced within the governance workspace. | Recommendation engine details (algorithm, data source) are unverified. | confirmed | S1 | 3T Lens product. |
| GOV-007 | 3T Lens — MCP integration (59 tools) | Supported | 59 MCP tools across 10 categories available to AI agents within 3T Lens. Tools are governed by the same 3T Access role-based access policies as human users — AI agents cannot exceed the permissions of the access policy assigned to them. | 10 categories and full tool list are unverified beyond the count of 59 total. | confirmed | S1 | 3T Lens product. |
| GOV-platform-access | 3T Access — identity and governance plane | Supported | Deployed on customer infrastructure. Centralized user, role, and permission management across all 3T products (Desktop IDE, 3T Build, 3T Lens, 3TL Bridge). Full audit trail: every connection recorded with who, what, and when — for both human and AI agent access. Pre-login access scoping applied before any connection is opened. | Customer-deployed; requires infrastructure provisioning. Integration details with individual 3T products are partially unverified. | confirmed | S1 | 3T Access product; customer-deployed. |
| GOV-platform-cdc | 3TL Bridge — CDC pipeline engine | Supported | Real-time Change Data Capture pipeline engine. Supported sources and destinations: MongoDB, Kafka, Google Pub/Sub, HTTP. Checkpoint recovery: exact position resume after restart or failover. Edit live running pipelines (import → modify → redeploy without stopping data flow). | 3TL Bridge is a separate product deployed on Kubernetes (Helm) or Docker Compose. MongoDB Change Streams must be available on source (replica set or sharded cluster). | confirmed | S2 | 3TL Bridge product; separate deployment. |
| GOV-010 | 3TL Bridge — Transform Studio | Supported | In-flight transformation engine. Write transformation logic in scripts. Test transformations against real data. Deploy tested transformations. Run test assertions before deployment to catch errors before production. | Scripting language for transformations is unverified. | confirmed | S2 | 3TL Bridge product. |
| GOV-011 | 3TL Bridge — real-time PII masking | Supported | PII masking applied at the pipeline layer before data reaches the destination — original source not modified. Built-in compliance templates: GDPR, HIPAA, CCPA. Structured audit logging exportable to SIEM. | Template completeness for each compliance standard is unverified. SIEM export format is unverified. | confirmed | S2 | 3TL Bridge product. |
| GOV-012 | 3TL Bridge — security and identity | Supported | Credentials encrypted. Multi-provider OIDC: Google Workspace, Azure AD, any standards-compliant OIDC provider. OIDC providers configurable via runtime environment variables (no container rebuilds required). | OIDC configuration requires environment variable access to the deployment. | confirmed | S2 | 3TL Bridge product. |
| GOV-013 | 3TL Bridge — deployment and scaling | Supported | Kubernetes deployment via single Helm chart (ingress, secrets, monitoring, HA, multi-customer namespaces). Docker Compose single-command deployment. Prometheus-compatible metrics. Kubernetes ServiceMonitor. Grafana and Datadog integration. Horizontal scaling at app tier. Pipeline checkpoint recovery for HA. | Horizontal scaling scope (which components scale horizontally) is unverified. | confirmed | S2 | 3TL Bridge product. |
