# Product Report — 3TL Bridge

## Navigation

- [Repository README](../../../README.md)
- [Feature dictionary](../../../feature-dictionary.md)
- [3T products index](../README.md)
- [High-level comparison](../../../reports/comparisons/high-level-product-comparison.md)
- [Low-level comparison](../../../reports/comparisons/low-level-feature-comparison.md)

## Product metadata

- Product name: 3TL Bridge
- Product group: 3t
- Website: https://studio3t.com/3tl-bridge/
- Maker: 3T Software Labs
- Category: Change Data Capture (CDC) pipeline engine
- Analysis date: 2026-06-22
- Version/release context: The sole product in the "Pipeline" track. Split out of the Studio 3T product report into its own product folder 2026-07-29 (was previously documented as a sub-section of Studio 3T's Governance & Security).

## Product summary

3TL Bridge is a real-time Change Data Capture (CDC) pipeline engine. Its supported topology covers MongoDB, Kafka, Google Pub/Sub, and HTTP as both sources and destinations. The Transform Studio feature allows writing and testing in-flight transformation logic against real data before deployment, with test assertions to catch errors pre-production. Checkpoint recovery enables exact-position resume after restart or failover — a critical reliability feature for production data pipelines. Edit-in-place (modify and redeploy a running pipeline without stopping data flow) reduces pipeline downtime.

PII masking at the pipeline layer (before data reaches the destination) combined with GDPR, HIPAA, and CCPA built-in templates positions 3TL Bridge as a compliance-aware data movement tool. Structured audit logging exportable to SIEM completes the compliance triad. Deployment is via Kubernetes (single Helm chart covering ingress, secrets, monitoring, HA, and multi-customer namespaces) or Docker Compose, with Prometheus-compatible metrics and Grafana/Datadog integration.

3TL Bridge is a separate deployable product — not a feature of the Studio 3T Desktop IDE. It requires MongoDB Change Streams (replica set or sharded cluster) for CDC sourcing; standalone MongoDB deployments are not supported.

## Feature inventory

Feature IDs and folder names from [feature-dictionary.md](../../../feature-dictionary.md).

| Feature ID | Feature | Matrix | Report | Status |
| --- | --- | --- | --- | --- |
| F-GOV | Governance & Security | [feature-matrix.md](features/governance/feature-matrix.md) | [feature-report.md](features/governance/feature-report.md) | Completed |

## Product-level conclusions

### Strategic strengths

- Checkpoint recovery enables exact-position resume after restart/failover — not just best-effort replay.
- Pipeline-layer PII masking (before data reaches destination) is enforced regardless of destination tool or access method — a stronger guarantee than application-layer masking.
- Kubernetes Helm chart deployment with Prometheus/Grafana/Datadog integration and a Docker Compose alternative covers both small-team and large-enterprise deployment patterns.

### Strategic risks / gaps

- Separate deployable product — requires infrastructure provisioning; pricing is unknown/unverified.
- Requires MongoDB Change Streams (replica set or sharded cluster) for CDC sourcing — standalone MongoDB deployments are not supported.
- Transform Studio scripting language is unknown/unverified.
- Template completeness for each compliance standard (GDPR/HIPAA/CCPA) is unverified.
- SIEM export format is unverified.

### Open questions

- Which scripting language does Transform Studio use?
- Which components scale horizontally in the Kubernetes deployment?
