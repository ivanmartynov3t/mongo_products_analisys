# Feature Report — 3T Lens / Governance & Security

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [High-level comparison](../../../../../reports/comparisons/high-level-product-comparison.md)

## Scope

This report covers 3T Lens, the browser-based governed data workspace in the "Governed Access" track (alongside [3T Access](../../../3t-access/product-report.md)). It is a separate deployable product that extends the Studio 3T platform into enterprise governance use cases.

## Behavioral walkthrough

3T Lens is a browser-based governed data workspace. Its primary function is centralizing MongoDB connection management: connections are defined once and shared to all users without distributing passwords. Access scoping happens before login — a user who does not have View permission for a production database cannot see that connection at all. Compliance features are built around configurable policy templates (ACID, Schema, Index, Security, Naming, Operational) with one-click environment-level health checks. Alert channels (Slack, email, webhook) make compliance failures visible in the team's existing notification infrastructure.

3T Lens also provides PII classification (automated scanning with sensitivity grouping and timestamped scan records), versioned field history (schema drift detection before production), and document-level diffs (exact field-by-field comparison between snapshots). Query performance suggestions surface index recommendations within the governance context. Notably, 3T Lens extends its access control to AI agents: the 59 MCP tools available to AI agents are governed by the same 3T Access role policies as human users — an AI agent cannot exceed the permissions of the access policy it operates under.

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| GOV-platform-lens | Centralized connection management with no shared passwords and pre-login access scoping eliminates the most common credential hygiene failure mode in team MongoDB environments. | Directly reduces production incident risk from credential sharing. | studio3t.com/3t-lens/ |
| GOV-005 | Versioned field history and document-level diffs provide schema change detection before production — proactive rather than reactive schema governance. | Enables schema contract enforcement across teams working on the same MongoDB deployment. | studio3t.com/3t-lens/ |
| GOV-007 | AI agent MCP tools governed by the same 3T Access policies as human users is a forward-looking design — agent permissions are not orthogonal to human permissions. | Prevents the emerging pattern of AI agents bypassing human-level access controls. | studio3t.com/3t-lens/ |

## Constraints and risks

- 3T Lens is a separate deployable product — not a feature of the Desktop IDE. It requires infrastructure provisioning; pricing is unknown/unverified.
- Integration between 3T Lens centralized connections and the Desktop IDE connection manager is not explicitly documented — it is unverified whether Desktop IDE users can consume 3T Lens-managed connections seamlessly.
- Automated PII classification uses heuristics; results require human review and cannot be treated as an authoritative compliance determination.
- 10 categories and full tool list for the 59 MCP tools are unknown/unverified beyond the total count.

## Interactions and dependencies

- Shares 3T Access as the identity/permission plane — see [3T Access product report](../../../3t-access/product-report.md).
- Complements [3TL Bridge](../../../3tl-bridge/product-report.md) (CDC pipeline engine) as part of the broader governance tier.

## Conclusions

### Strengths

- Centralized, pre-login access scoping eliminates a common credential-sharing failure mode.
- Proactive schema governance via versioned field history and document diffs.
- AI agent access uses the same policy plane as human access.

### Limitations

- Separate deployment; infrastructure and pricing overhead versus IDE-native features.

### Unknowns

- Full breakdown of the 59 MCP tools across their 10 categories.
- Integration depth with the Desktop IDE connection manager.
