# Feature Matrix — 3T Explore / Governance & Security

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: 3T Explore
- Product group: 3t
- Feature ID: F-GOV (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `governance`
- Analysis date: 2026-09-25
- Review log: 2026-09-25 — weekly re-check (#17): S1 re-read; GOV-platform-explore holds, wording aligned with the current page.
- Version/release context: —

## Source index

- S1: https://studio3t.com/3t-explore/

## Capability matrix

| Capability ID | Capability | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GOV-platform-explore | 3T Explore — browser IDE workspace and access control | Supported | Browser-based IDE extending the Desktop IDE experience (Explore data view/query/edit, Visual Query Builder, IntelliShell, Aggregation Editor, AI Helper) with two governance-relevant additions: Workspace Switcher (hold multiple workspaces and switch between them in one session; each shows only the connections and data an administrator configured for it (S1, 2026-09-25)) and Access Control (integration with 3T Access Manager for which environments, databases, and collections each user can reach (S1, 2026-09-25)). | 3T Explore is a separate product (browser-based); edition/plan requirements are unverified. | confirmed | S1 | AI Helper aspect cross-referenced at [ai/feature-matrix.md](../ai/feature-matrix.md) (AI-012). Access Control depends on [3T Access](../../../3t-access/product-report.md). |

## Feature-level conclusion

### Confirmed strengths

- Workspace Switcher + 3T Access Manager integration extend pre-login, role-based access scoping to a browser-based surface aimed at non-developer users.

### Confirmed limitations

- Edition/plan requirements unverified.

### Open questions / unknowns

- Whether 3T Explore requires a separate license from the Desktop IDE.
