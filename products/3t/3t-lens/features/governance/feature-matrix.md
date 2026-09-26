# Feature Matrix — 3T Lens / Governance & Security

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)
- [Govern governance matrix](../../../govern/features/governance/feature-matrix.md)

## Feature metadata

- Product name: 3T Lens
- Product group: 3t
- Feature ID: F-GOV (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `governance`
- Analysis date: 2026-09-25
- Version/release context: rows `GOV-002`–`GOV-009` moved to [Govern](../../../govern/features/governance/feature-matrix.md) on 2026-09-25 (owner decision). The original analysis was done on 2026-07-29 against S1.

## Source index

- S1: https://studio3t.com/3t-lens/ — **removed: HTTP 404 on 2026-09-25**; last read for this analysis on 2026-07-29. Public source at that time; no replacement page found.
- S2: https://studio3t.com/ — homepage 3T Lens descriptions (silo: `data/3t/3t-website-2026/index.md@f1e28e8d`), current public source.

## Pointer table — rows now documented under Govern

| Sub-feature ID | Moved to | Why |
| --- | --- | --- |
| GOV-002, GOV-003, GOV-004, GOV-005, GOV-006, GOV-007, GOV-008, GOV-009 | [Govern matrix](../../../govern/features/governance/feature-matrix.md) | The public site describes policy checks, drift alerts and governed agent access as the Govern track, not as 3T Lens; the page that attributed them to 3T Lens (S1) is gone. The Govern matrix records 3T Lens as an alternative attribution. |

## Capability matrix

| Sub-feature ID | Capability | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GOV-platform-lens | 3T Lens — governed read-only workspace and centralized connection management | Supported | Read-only access so analysts and business users can explore live data with "no way to change, delete, or damage" it (S2). Query results "automatically inherit your organization's access policies" (S2). Connections configured once and shared to all users; no shared passwords, no hidden connections; access scoped before login via 3T Access roles; same connection policies for human users and AI agents (S1). | Separate browser-based product, deployed apart from the Desktop IDE (S1). Integration with the Desktop IDE connection manager is not documented (S1, S2). | Read-only workspace, inherited policies: confirmed (public) (S2). Connection management: confirmed 2026-07-29, source removed (S1). | S1, S2 | Access scoping depends on [3T Access](../../../3t-access/features/governance/feature-matrix.md) (`GOV-platform-access`). |

## Feature-level conclusion

### Confirmed strengths

- Read-only, policy-inheriting data access for non-developers (S2).

### Confirmed limitations

- Separate deployable product (S1).

### Open questions / unknowns

- Was studio3t.com/3t-lens/ removed on purpose, and does it have a new address? The homepage links to no 3T Lens page (S2).
- Does 3T Lens deliver the Govern capabilities, or does another product? See the [Govern matrix](../../../govern/features/governance/feature-matrix.md#why-govern-and-not-3t-lens).
- Whether 3T Lens replaces or supplements the Desktop IDE connection manager (S1, S2 are silent).
