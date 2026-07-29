# Feature Matrix — 3TL Bridge / Governance & Security

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Source index

- S1: https://studio3t.com/3tl-bridge/

## Capability matrix

| Capability ID | Capability | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GOV-platform-cdc | 3TL Bridge — CDC pipeline engine | Supported | Real-time Change Data Capture pipeline engine. Supported sources and destinations: MongoDB, Kafka, Google Pub/Sub, HTTP. Checkpoint recovery: exact position resume after restart or failover. Edit live running pipelines (import → modify → redeploy without stopping data flow). | 3TL Bridge is a separate product deployed on Kubernetes (Helm) or Docker Compose. MongoDB Change Streams must be available on source (replica set or sharded cluster). | confirmed | S1 | — |
| GOV-010 | 3TL Bridge — Transform Studio | Supported | In-flight transformation engine. Write transformation logic in scripts. Test transformations against real data. Deploy tested transformations. Run test assertions before deployment to catch errors before production. | Scripting language for transformations is unverified. | confirmed | S1 | — |
| GOV-011 | 3TL Bridge — real-time PII masking | Supported | PII masking applied at the pipeline layer before data reaches the destination — original source not modified. Built-in compliance templates: GDPR, HIPAA, CCPA. Structured audit logging exportable to SIEM. | Template completeness for each compliance standard is unverified. SIEM export format is unverified. | confirmed | S1 | — |
| GOV-012 | 3TL Bridge — security and identity | Supported | Credentials encrypted. Multi-provider OIDC: Google Workspace, Azure AD, any standards-compliant OIDC provider. OIDC providers configurable via runtime environment variables (no container rebuilds required). | OIDC configuration requires environment variable access to the deployment. | confirmed | S1 | — |
| GOV-013 | 3TL Bridge — deployment and scaling | Supported | Kubernetes deployment via single Helm chart (ingress, secrets, monitoring, HA, multi-customer namespaces). Docker Compose single-command deployment. Prometheus-compatible metrics. Kubernetes ServiceMonitor. Grafana and Datadog integration. Horizontal scaling at app tier. Pipeline checkpoint recovery for HA. | Horizontal scaling scope (which components scale horizontally) is unverified. | confirmed | S1 | — |

## Feature-level conclusion

### Confirmed strengths

- Checkpoint recovery gives exact-position resume after restart/failover.
- Pipeline-layer PII masking with built-in GDPR/HIPAA/CCPA templates.
- Kubernetes Helm chart plus Docker Compose deployment options with standard observability integrations.

### Confirmed limitations

- Requires MongoDB Change Streams (replica set or sharded cluster); standalone deployments unsupported for CDC sourcing.

### Open questions / unknowns

- Transform Studio scripting language.
- Compliance template completeness per standard.
- SIEM export format.
- Horizontal scaling scope.
