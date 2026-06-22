# Feature Report — Studio 3T / Governance Platform

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [High-level comparison](../../../../../reports/comparisons/high-level-product-comparison.md)

## Scope

This report covers Studio 3T's governance platform tier: 3T Lens (governed data workspace), 3T Access (identity and governance plane), and 3TL Bridge (CDC pipeline engine with PII masking and compliance features). These are separate deployable products that extend the Studio 3T platform into enterprise governance and data pipeline use cases.

## Behavioral walkthrough

The Studio 3T governance tier spans three separate products that operate above the Desktop IDE layer. Understanding each is important because they are not features of the Desktop IDE — they are distinct deployments that integrate with the IDE and with each other via 3T Access as the shared identity plane.

**3T Lens** is a browser-based governed data workspace. Its primary function is centralizing MongoDB connection management: connections are defined once and shared to all users without distributing passwords. Access scoping happens before login — a user who does not have View permission for a production database cannot see that connection at all. Compliance features are built around configurable policy templates (ACID, Schema, Index, Security, Naming, Operational) with one-click environment-level health checks. Alert channels (Slack, email, webhook) make compliance failures visible in the team's existing notification infrastructure.

3T Lens also provides PII classification (automated scanning with sensitivity grouping and timestamped scan records), versioned field history (schema drift detection before production), and document-level diffs (exact field-by-field comparison between snapshots). Query performance suggestions surface index recommendations within the governance context. Notably, 3T Lens extends its access control to AI agents: the 59 MCP tools available to AI agents are governed by the same 3T Access role policies as human users — an AI agent cannot exceed the permissions of the access policy it operates under.

**3T Access** is the identity and governance plane, deployed on customer infrastructure. It provides centralized user/role/permission management across all 3T products and maintains a full audit trail of every connection (who connected, to what, when) for both human and AI agent access. Pre-login access scoping ensures that access policy is applied before any connection attempt, not after.

**3TL Bridge** is a CDC (Change Data Capture) pipeline engine. Its supported topology covers MongoDB, Kafka, Google Pub/Sub, and HTTP as both sources and destinations. The Transform Studio feature allows writing and testing in-flight transformation logic against real data before deployment, with test assertions to catch errors pre-production. Checkpoint recovery enables exact-position resume after restart or failover — a critical reliability feature for production data pipelines. Edit-in-place (modify and redeploy a running pipeline without stopping data flow) reduces pipeline downtime.

PII masking at the pipeline layer (before data reaches the destination) combined with GDPR, HIPAA, and CCPA built-in templates positions 3TL Bridge as a compliance-aware data movement tool. Structured audit logging exportable to SIEM completes the compliance triad.

## Capability findings

| Capability ID | Finding | Impact |
| --- | --- | --- |
| GOV-001 | Centralized connection management with no shared passwords and pre-login access scoping eliminates the most common credential hygiene failure mode in team MongoDB environments. | Directly reduces production incident risk from credential sharing. |
| GOV-005 | Versioned field history and document-level diffs provide schema change detection before production — proactive rather than reactive schema governance. | Enables schema contract enforcement across teams working on the same MongoDB deployment. |
| GOV-007 | AI agent MCP tools governed by the same 3T Access policies as human users is a forward-looking design — agent permissions are not orthogonal to human permissions. | Prevents the emerging pattern of AI agents bypassing human-level access controls. |
| GOV-009 | Checkpoint recovery in 3TL Bridge enables exact-position resume after restart/failover — not just best-effort replay. | Critical for production data pipelines where data loss or duplication on restart is unacceptable. |
| GOV-011 | Pipeline-layer PII masking (before data reaches destination) means the masking policy is enforced regardless of destination tool or access method. | Stronger masking guarantee than application-layer masking, which can be bypassed by direct DB access. |
| GOV-013 | Kubernetes Helm chart deployment with Prometheus/Grafana/Datadog integration and Docker Compose alternative covers both small-team and large-enterprise deployment patterns. | Reduces operational overhead for teams that already use standard Kubernetes observability stacks. |

## Constraints and risks

- 3T Lens, 3T Access, and 3TL Bridge are separate deployable products — not features of the Desktop IDE. They require infrastructure provisioning and are likely separately priced (**unknown/unverified** pricing).
- Integration between 3T Lens centralized connections and the Desktop IDE connection manager is not explicitly documented — it is unverified whether Desktop IDE users can consume 3T Lens-managed connections seamlessly.
- 3TL Bridge requires MongoDB Change Streams (replica set or sharded cluster) for CDC sourcing — standalone MongoDB deployments are not supported for CDC.
- Automated PII classification in 3T Lens uses heuristics; results require human review and cannot be treated as an authoritative compliance determination.
- 10 categories and full tool list for the 59 MCP tools in 3T Lens are **unknown/unverified** beyond the total count.
- Transform Studio scripting language is **unknown/unverified**.

## Conclusion

The Studio 3T governance platform is architecturally ambitious: a three-product tier (3T Lens + 3T Access + 3TL Bridge) covering connection governance, identity management, audit trails, schema versioning, PII classification, CDC pipelines, and compliance-aware data movement. The design principle of applying the same access policies to AI agents and human users is noteworthy and positions the platform for enterprise AI governance use cases. The main caveat is that these are separate deployments, not IDE features — their adoption implies infrastructure investment beyond the Desktop IDE.
