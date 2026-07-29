# Feature Report — Studio 3T / Governance Platform

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [High-level comparison](../../../../../reports/comparisons/high-level-product-comparison.md)

## Scope

As of 2026-07-29, this report no longer covers the governance-tier products directly — they have each been split into their own product folder under `products/3t/` with an independent product report and feature report:

- [3T Lens](../../../3t-lens/features/governance/feature-report.md) — governed data workspace (centralized connection management, compliance policy templates, PII classification, versioned field history, MCP integration)
- [3T Access](../../../3t-access/features/governance/feature-report.md) — identity and governance plane (RBAC, audit trail, pre-login access scoping)
- [3TL Bridge](../../../3tl-bridge/features/governance/feature-report.md) — CDC pipeline engine (Transform Studio, PII masking, security/identity, deployment/scaling)
- [3T Explore](../../../3t-explore/features/governance/feature-report.md) — the governance-relevant aspects (Workspace Switcher, Access Control) of the browser IDE product

Previously, this report treated all four as a single "governance platform tier" of Studio 3T. Per studio3t.com, 3T Explore, the Desktop IDE, and 3T MCP make up the "Build" track; 3TL Bridge is the "Pipeline" track; 3T Lens and 3T Access are the "Governed Access" track — three separate tracks, five separate products (excluding the Desktop IDE itself), now documented independently.

This report's remaining scope is the Studio 3T Desktop IDE's own native governance capabilities. That capability matrix has not yet been authored (see the [feature matrix](feature-matrix.md)'s Scope note) — it is a pre-existing gap, not something introduced by the 2026-07-29 split. Comparison reports already reference `GOV-readonly-mode`, `GOV-rbac-users`, `GOV-rbac-roles`, `GOV-audit-log`, `GOV-collection-compare`, `GOV-collection-sync`, `GOV-data-masking`, and `GOV-cred-protection` against this product; those references are unaffected by this split.

## Behavioral walkthrough

See the linked per-product reports above for full behavioral detail on 3T Lens, 3T Access, 3TL Bridge, and 3T Explore's governance surface. In summary: 3T Access is the shared identity/permission plane; 3T Lens is the browser-based governed workspace built on top of it (connection governance, compliance, PII classification); 3TL Bridge is the CDC pipeline engine with pipeline-layer PII masking; and 3T Explore extends the same access-scoping model to a browser IDE surface via its Workspace Switcher and 3T Access Manager integration.

## Constraints and risks

- 3T Lens, 3T Access, and 3TL Bridge are separate deployable products — not features of the Desktop IDE. They require infrastructure provisioning and are likely separately priced (**unknown/unverified** pricing).
- Integration between 3T Lens centralized connections and the Desktop IDE connection manager is not explicitly documented — it is unverified whether Desktop IDE users can consume 3T Lens-managed connections seamlessly.
- The Desktop IDE's own governance capabilities (RBAC, audit log, data masking, collection compare/sync, protect mode) do not yet have a dedicated feature report in this product folder.

## Conclusion

The Studio 3T governance platform is architecturally ambitious: a three-product tier (3T Lens + 3T Access + 3TL Bridge) covering connection governance, identity management, audit trails, schema versioning, PII classification, CDC pipelines, and compliance-aware data movement, plus 3T Explore extending the same access model to a browser IDE. The design principle of applying the same access policies to AI agents and human users is noteworthy and positions the platform for enterprise AI governance use cases. As of 2026-07-29 each of these products is documented in its own folder — see the links in Scope above for full detail. The main caveat remains that these are separate deployments, not Desktop IDE features — their adoption implies infrastructure investment beyond the Desktop IDE.
