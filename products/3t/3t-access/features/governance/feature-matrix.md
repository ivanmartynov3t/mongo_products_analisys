# Feature Matrix — 3T Access / Governance & Security

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Source index

- S1: https://studio3t.com/3t-lens/ (3T Access has no independently confirmed dedicated product page; it is described within the 3T Lens product page)

## Capability matrix

| Capability ID | Capability | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GOV-platform-access | 3T Access — identity and governance plane | Supported | Deployed on customer infrastructure. Centralized user, role, and permission management across all 3T products (Desktop IDE, 3T Explore, 3T Lens, 3TL Bridge). Full audit trail: every connection recorded with who, what, and when — for both human and AI agent access. Pre-login access scoping applied before any connection is opened. | Customer-deployed; requires infrastructure provisioning. Integration details with individual 3T products are partially unverified. | confirmed | S1 | Referenced by [3T Lens](../../../3t-lens/features/governance/feature-matrix.md) (GOV-platform-lens) and [3T Explore](../../../3t-explore/features/governance/feature-matrix.md) (GOV-platform-explore) as the shared identity plane. |

## Feature-level conclusion

### Confirmed strengths

- Centralized identity/permission management across all 3T products, rather than per-product silos.
- Full audit trail covering both human and AI agent access.
- Pre-login access scoping.

### Confirmed limitations

- Customer-deployed; requires infrastructure provisioning.
- Integration details with individual 3T products are partially unverified.

### Open questions / unknowns

- Whether 3T Access has a dedicated product page/documentation distinct from 3T Lens's.
