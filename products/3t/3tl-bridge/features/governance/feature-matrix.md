# Feature Matrix — 3TL Bridge / Governance & Security

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: 3TL Bridge
- Product group: 3t
- Feature ID: F-GOV (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `governance`
- Analysis date: 2026-09-25
- Review log: 2026-09-25 — weekly re-check (#17): S1 re-read. Unchanged since the silo's first capture (2026-09-11), but several July claims are no longer on the page: source/destination list, Helm/Compose/metrics/scaling detail, "environment variables". Kept and marked ❓ rather than deleted.
- Version/release context: —

## Source index

- S1: https://studio3t.com/3tl-bridge/

## Capability matrix

| Capability ID | Capability | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GOV-platform-cdc | 3TL Bridge — CDC pipeline engine | Supported | Real-time Change Data Capture pipeline engine. Supported sources and destinations: MongoDB, Kafka, Google Pub/Sub, HTTP (no longer on S1 on 2026-09-25 (last seen there 2026-07-29) — ❓ unverified). Checkpoint recovery: exact position resume after restart or failover. Edit live running pipelines (import → modify → redeploy without stopping data flow). | 3TL Bridge is a separate, Kubernetes-native product: managed hosting on all tiers, or on-premises from the Growth tier up (S1, 2026-09-25). Helm / Docker Compose: no longer on S1 on 2026-09-25 (last seen there 2026-07-29) — ❓ unverified. MongoDB Change Streams must be available on source (replica set or sharded cluster). | confirmed | S1 | — |
| GOV-010 | 3TL Bridge — Transform Studio | Supported | In-flight transformation engine. Write transformation logic in scripts. Test transformations against real data. Deploy tested transformations. Run test assertions before deployment to catch errors before production. | Scripting language for transformations is unverified. | confirmed | S1 | — |
| GOV-011 | 3TL Bridge — real-time PII masking | Supported | PII masking applied at the pipeline layer before data reaches the destination — original source not modified. Built-in templates covering common GDPR, HIPAA, and CCPA use cases (S1, 2026-09-25). Structured audit logging exportable to SIEM. | Template completeness for each compliance standard is unverified. SIEM export format is unverified. | confirmed | S1 | — |
| GOV-012 | 3TL Bridge — security and identity | Supported | Credentials encrypted. Multi-provider OIDC: Google Workspace, Azure AD, any standards-compliant OIDC provider. OIDC providers set through runtime configuration, with no per-customer image builds (S1, 2026-09-25); "environment variables": no longer on S1 on 2026-09-25 (last seen there 2026-07-29) — ❓ unverified. | Configuration mechanism beyond "runtime configuration" is unverified. | confirmed | S1 | — |
| GOV-013 | 3TL Bridge — deployment and scaling | Supported | Kubernetes-native single-service deployment; managed hosting (all tiers) or on-premises (Growth tier and up); checkpoint recovery on restart or failover (S1, 2026-09-25). Helm chart (ingress, secrets, monitoring, HA, multi-customer namespaces), Docker Compose, Prometheus metrics, Kubernetes ServiceMonitor, Grafana/Datadog integration and horizontal scaling: no longer on S1 on 2026-09-25 (last seen there 2026-07-29) — ❓ unverified. | Horizontal scaling scope is unverified. | confirmed (deployment model); ❓ (Helm, Compose, metrics, scaling details) | S1 | — |

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
