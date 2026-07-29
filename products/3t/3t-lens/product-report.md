# Product Report — 3T Lens

## Navigation

- [Repository README](../../../README.md)
- [Feature dictionary](../../../feature-dictionary.md)
- [3T products index](../README.md)
- [High-level comparison](../../../reports/comparisons/high-level-product-comparison.md)
- [Low-level comparison](../../../reports/comparisons/low-level-feature-comparison.md)

## Product metadata

- Product name: 3T Lens
- Product group: 3t
- Website: https://studio3t.com/3t-lens/
- Maker: 3T Software Labs
- Category: Browser-based governed data workspace (connection management, compliance, PII classification)
- Analysis date: 2026-06-22
- Version/release context: Part of the "Governed Access" track (alongside 3T Access). Split out of the Studio 3T product report into its own product folder 2026-07-29 (was previously documented as a sub-section of Studio 3T's Governance & Security).

## Product summary

3T Lens is a browser-based governed data workspace. Its primary function is centralizing MongoDB connection management: connections are defined once and shared to all users without distributing passwords. Access scoping happens before login — a user who does not have View permission for a production database cannot see that connection at all, per access scoping enforced through [3T Access](../3t-access/product-report.md).

Compliance features are built around configurable policy templates (ACID, Schema, Index, Security, Naming, Operational) with one-click environment-level health checks. Alert channels (Slack, email, webhook) make compliance failures visible in the team's existing notification infrastructure. 3T Lens also provides PII classification (automated scanning with sensitivity grouping and timestamped scan records), versioned field history (schema drift detection before production), and document-level diffs (exact field-by-field comparison between snapshots). Query performance suggestions surface index recommendations within the governance context.

Notably, 3T Lens extends its access control to AI agents: the 59 MCP tools available to AI agents are governed by the same 3T Access role policies as human users — an AI agent cannot exceed the permissions of the access policy it operates under.

3T Lens is a separate deployable product — not a feature of the Studio 3T Desktop IDE. It requires infrastructure provisioning and is likely separately priced (unknown/unverified pricing). Integration between 3T Lens centralized connections and the Desktop IDE connection manager is not explicitly documented.

## Feature inventory

Feature IDs and folder names from [feature-dictionary.md](../../../feature-dictionary.md).

| Feature ID | Feature | Matrix | Report | Status |
| --- | --- | --- | --- | --- |
| F-GOV | Governance & Security | [feature-matrix.md](features/governance/feature-matrix.md) | [feature-report.md](features/governance/feature-report.md) | Completed |

## Product-level conclusions

### Strategic strengths

- Centralized connection management with no shared passwords and pre-login access scoping eliminates a common credential hygiene failure mode in team MongoDB environments.
- Versioned field history and document-level diffs provide schema change detection before production — proactive rather than reactive schema governance.
- AI agent MCP tools governed by the same 3T Access policies as human users — agent permissions are not orthogonal to human permissions.

### Strategic risks / gaps

- Separate deployable product — requires infrastructure provisioning; pricing is unknown/unverified.
- Integration between 3T Lens centralized connections and the Desktop IDE connection manager is not explicitly documented.
- Automated PII classification uses heuristics; results require human review and cannot be treated as an authoritative compliance determination.
- 10 categories and full tool list for the 59 MCP tools are unknown/unverified beyond the total count.

### Open questions

- Does 3T Lens replace or supplement the Desktop IDE connection manager in practice?
- What is the full breakdown of the 59 MCP tools across their 10 categories?
