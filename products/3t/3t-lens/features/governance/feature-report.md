# Feature Report — 3T Lens / Governance & Security

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [High-level comparison](../../../../../reports/comparisons/high-level-product-comparison.md)
- [Govern feature report](../../../govern/features/governance/feature-report.md)

## Scope

This report covers 3T Lens's own capability, `GOV-platform-lens`. Policy, alerting, PII, schema-history, performance and MCP-governance rows (`GOV-002`–`GOV-009`) moved to [Govern](../../../govern/features/governance/feature-report.md) on 2026-09-25. Source numbers refer to the [feature matrix](feature-matrix.md#source-index).

## Behavioral walkthrough

The homepage presents 3T Lens as a governed, read-only workspace: analysts and business users explore live data with "no way to change, delete, or damage" it, and query results inherit the organization's access policies (S2). The removed product page (S1, last read 2026-07-29) added centralized connection management: connections are defined once and shared without distributing passwords, and access is scoped before login through 3T Access roles.

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| GOV-platform-lens | Read-only, policy-inheriting access for non-developers is the current public positioning (S2); centralized connections and pre-login scoping come from the removed page (S1). | Reduces credential sharing and accidental writes. | S1, S2 |

## Constraints and risks

- The dedicated product page returned 404 on 2026-09-25 (S1); only homepage text is public now (S2).
- Separate deployable product (S1); pricing unknown.
- Integration with the Desktop IDE connection manager is not documented (S1, S2).

## Interactions and dependencies

- [3T Access](../../../3t-access/product-report.md) — identity and permission plane (S1, S2).
- [Govern](../../../govern/product-report.md) — governance track; alternative home of the moved rows.

## Conclusions

### Strengths

- Safe, read-only data access with inherited policies (S2).

### Limitations

- Little current public detail (S1 removed).

### Unknowns

- Whether 3T Lens delivers the Govern capabilities; new address of its product page.
