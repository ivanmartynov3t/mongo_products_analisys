# Feature Report — 3TL Bridge / Governance & Security

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [High-level comparison](../../../../../reports/comparisons/high-level-product-comparison.md)

## Scope

This report covers 3TL Bridge, the CDC (Change Data Capture) pipeline engine — the sole product in the "Pipeline" track. It is a separate deployable product that extends the Studio 3T platform into data-pipeline use cases.

## Behavioral walkthrough

3TL Bridge's supported topology covers MongoDB, Kafka, Google Pub/Sub, and HTTP as both sources and destinations. The Transform Studio feature allows writing and testing in-flight transformation logic against real data before deployment, with test assertions to catch errors pre-production. Checkpoint recovery enables exact-position resume after restart or failover — a critical reliability feature for production data pipelines. Edit-in-place (modify and redeploy a running pipeline without stopping data flow) reduces pipeline downtime.

PII masking at the pipeline layer (before data reaches the destination) combined with GDPR, HIPAA, and CCPA built-in templates positions 3TL Bridge as a compliance-aware data movement tool. Structured audit logging exportable to SIEM completes the compliance triad.

Security and identity are handled separately from the data-plane concerns above: credentials are encrypted, and authentication supports multi-provider OIDC (Google Workspace, Azure AD, or any standards-compliant OIDC provider), configurable via runtime environment variables without requiring container rebuilds.

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| GOV-platform-cdc | Checkpoint recovery in 3TL Bridge enables exact-position resume after restart/failover — not just best-effort replay. | Critical for production data pipelines where data loss or duplication on restart is unacceptable. | studio3t.com/3tl-bridge/ |
| GOV-011 | Pipeline-layer PII masking (before data reaches destination) means the masking policy is enforced regardless of destination tool or access method. | Stronger masking guarantee than application-layer masking, which can be bypassed by direct DB access. | studio3t.com/3tl-bridge/ |
| GOV-012 | Multi-provider OIDC configurable via runtime environment variables means identity provider changes don't require redeploying the container image. | Lower operational friction for enterprises switching or adding OIDC providers post-deployment. | studio3t.com/3tl-bridge/ |
| GOV-013 | Kubernetes Helm chart deployment with Prometheus/Grafana/Datadog integration and Docker Compose alternative covers both small-team and large-enterprise deployment patterns. | Reduces operational overhead for teams that already use standard Kubernetes observability stacks. | studio3t.com/3tl-bridge/ |

## Constraints and risks

- 3TL Bridge requires MongoDB Change Streams (replica set or sharded cluster) for CDC sourcing — standalone MongoDB deployments are not supported for CDC.
- Transform Studio scripting language is unknown/unverified.
- Template completeness for each compliance standard (GDPR/HIPAA/CCPA) is unverified. SIEM export format is unverified.
- Horizontal scaling scope (which components scale horizontally) is unverified.

## Interactions and dependencies

- Shares 3T Access as the identity/permission plane for platform-wide auth — see [3T Access product report](../../../3t-access/product-report.md).
- Complements [3T Lens](../../../3t-lens/product-report.md) within the broader governance tier (3T Lens covers connection governance and compliance policy; 3TL Bridge covers data movement).

## Conclusions

### Strengths

- Production-grade CDC reliability via checkpoint recovery and edit-in-place pipeline updates.
- Pipeline-layer PII masking with built-in compliance templates (GDPR/HIPAA/CCPA).
- Multi-provider OIDC (Google Workspace, Azure AD, standards-compliant providers) reconfigurable at runtime without container rebuilds.
- Flexible deployment (Kubernetes Helm or Docker Compose) with standard observability integrations.

### Limitations

- Requires MongoDB Change Streams; standalone MongoDB deployments cannot use it for CDC.

### Unknowns

- Transform Studio scripting language, compliance template completeness, SIEM export format, and horizontal scaling scope.
