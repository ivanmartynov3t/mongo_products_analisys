# Feature Matrix — 3T Explore / Governance & Security

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Source index

- S1: https://studio3t.com/3t-explore/

## Capability matrix

| Capability ID | Capability | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GOV-platform-explore | 3T Explore — browser IDE workspace and access control | Supported | Browser-based IDE extending the Desktop IDE experience (Explore data view/query/edit, Visual Query Builder, IntelliShell, Aggregation Editor, AI Helper) with two governance-relevant additions: Workspace Switcher (manage multiple workspaces with role-based data visibility) and Access Control (integration with 3T Access Manager for granular database/collection permissions). | 3T Explore is a separate product (browser-based); edition/plan requirements are unverified. | confirmed | S1 | AI Helper aspect cross-referenced at [ai/feature-matrix.md](../ai/feature-matrix.md) (AI-012). Access Control depends on [3T Access](../../../3t-access/product-report.md). |

## Feature-level conclusion

### Confirmed strengths

- Workspace Switcher + 3T Access Manager integration extend pre-login, role-based access scoping to a browser-based surface aimed at non-developer users.

### Confirmed limitations

- Edition/plan requirements unverified.

### Open questions / unknowns

- Whether 3T Explore requires a separate license from the Desktop IDE.
