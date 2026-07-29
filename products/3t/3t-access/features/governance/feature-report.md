# Feature Report — 3T Access / Governance & Security

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [High-level comparison](../../../../../reports/comparisons/high-level-product-comparison.md)

## Scope

This report covers 3T Access, the identity and governance plane in the "Governed Access" track (alongside [3T Lens](../../../3t-lens/product-report.md)). It is a separate deployable product that provides the shared identity/permission plane for the rest of the Studio 3T platform.

## Behavioral walkthrough

3T Access is deployed on customer infrastructure. It provides centralized user, role, and permission management across all 3T products and maintains a full audit trail of every connection (who connected, to what, when) for both human and AI agent access. Pre-login access scoping ensures that access policy is applied before any connection attempt, not after — the same mechanism [3T Lens](../../../3t-lens/product-report.md) relies on to hide connections a user isn't permitted to see, and that [3T Explore](../../../3t-explore/product-report.md) relies on for its Access Control / Workspace Switcher integration.

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| GOV-platform-access | Centralized identity/permission management across all 3T products, with a full audit trail for both human and AI agent access, and pre-login access scoping. | Establishes a single shared policy plane rather than per-product identity silos — human and AI agent access are governed identically. | studio3t.com/3t-lens/ |

## Constraints and risks

- Customer-deployed; requires infrastructure provisioning (unknown/unverified pricing).
- Integration details with individual 3T products are partially unverified.
- No dedicated 3T Access product page has been independently fetched — all capability detail here is sourced from the 3T Lens product page's description of the platform.

## Interactions and dependencies

- Shared identity plane for [3T Lens](../../../3t-lens/product-report.md), [3T Explore](../../../3t-explore/product-report.md), [3TL Bridge](../../../3tl-bridge/product-report.md), and the Studio 3T Desktop IDE.

## Conclusions

### Strengths

- Single shared identity/permission plane across the whole 3T platform, rather than per-product silos.
- Human and AI agent access governed by the same policies.

### Limitations

- Requires customer-side infrastructure provisioning.

### Unknowns

- Whether 3T Access is independently documented/priced apart from 3T Lens.
- Exact integration mechanism with the Desktop IDE's own connection manager.
