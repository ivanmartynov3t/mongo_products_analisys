# Product Report — 3T Access

## Navigation

- [Repository README](../../../README.md)
- [Feature dictionary](../../../feature-dictionary.md)
- [3T products index](../README.md)
- [High-level comparison](../../../reports/comparisons/high-level-product-comparison.md)
- [Low-level comparison](../../../reports/comparisons/low-level-feature-comparison.md)

## Product metadata

- Product name: 3T Access
- Product group: 3t
- Website: unknown/unverified — no dedicated product page has been independently fetched; 3T Access is described within the [3T Lens product page](https://studio3t.com/3t-lens/) (see the [feature matrix's Source index](features/governance/feature-matrix.md)).
- Maker: 3T Software Labs
- Category: Identity and access-governance plane (RBAC, audit trail)
- Analysis date: 2026-06-22
- Version/release context: Part of the "Governed Access" track (alongside 3T Lens). Split out of the Studio 3T product report into its own product folder 2026-07-29 (was previously documented as a sub-section of Studio 3T's Governance & Security).

## Product summary

3T Access is the identity and governance plane, deployed on customer infrastructure. It provides centralized user/role/permission management across all 3T products (Desktop IDE, [3T Explore](../3t-explore/product-report.md), [3T Lens](../3t-lens/product-report.md), [3TL Bridge](../3tl-bridge/product-report.md)) and maintains a full audit trail of every connection (who connected, to what, when) for both human and AI agent access. Pre-login access scoping ensures that access policy is applied before any connection attempt, not after. Note: this "all 3T products" enumeration is quoted from studio3t.com/3t-lens/ and does not name [3T MCP](../3t-mcp/product-report.md); whether 3T MCP is governed by 3T Access or relies solely on its own 3T-account/OAuth login is unverified.

3T Access is customer-deployed and requires infrastructure provisioning; integration details with individual 3T products are partially unverified. All currently available capability detail was sourced from the 3T Lens product page (studio3t.com/3t-lens/), which describes 3T Access as the shared identity plane behind 3T Lens's access scoping — no dedicated 3T Access marketing page has been independently confirmed.

## Feature inventory

Feature IDs and folder names from [feature-dictionary.md](../../../feature-dictionary.md).

| Feature ID | Feature | Matrix | Report | Status |
| --- | --- | --- | --- | --- |
| F-GOV | Governance & Security | [feature-matrix.md](features/governance/feature-matrix.md) | [feature-report.md](features/governance/feature-report.md) | Completed |

## Product-level conclusions

### Strategic strengths

- Centralized user/role/permission management across all 3T products, rather than per-product identity silos.
- Full audit trail (who, what, when) for both human and AI agent access.
- Pre-login access scoping applies policy before any connection attempt, not after.

### Strategic risks / gaps

- Customer-deployed; requires infrastructure provisioning (unknown/unverified pricing).
- Integration details with individual 3T products (Desktop IDE, 3T Explore, 3T Lens, 3TL Bridge) are partially unverified.
- No dedicated 3T Access product page has been independently fetched; all detail is sourced via 3T Lens's description of the platform.

### Open questions

- Does 3T Access have its own dedicated product page/documentation distinct from 3T Lens's?
- What is the exact integration mechanism between 3T Access and the Desktop IDE's own connection manager?
- Is 3T MCP (the standalone `stt-cli` binary) governed by 3T Access at all, or does its separate 3T-account/OAuth login model sit outside 3T Access's scope entirely?
