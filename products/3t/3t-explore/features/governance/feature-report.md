# Feature Report — 3T Explore / Governance & Security

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [High-level comparison](../../../../../reports/comparisons/high-level-product-comparison.md)

## Scope

This report covers the governance-relevant aspects of 3T Explore: its Workspace Switcher and 3T Access Manager integration.

## Behavioral walkthrough

3T Explore's Workspace Switcher lets users manage multiple workspaces with role-based data visibility, and its Access Control integrates with 3T Access Manager (see [3T Access product report](../../../3t-access/product-report.md)) for granular database/collection permissions. Together these extend pre-login, role-based access scoping — the same governance model used by [3T Lens](../../../3t-lens/product-report.md) — to a browser-based surface aimed at non-developer users.

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| GOV-platform-explore | Workspace Switcher and 3T Access Manager integration extend pre-login, role-based access scoping to a browser-based surface aimed at non-developer users. | Lets teams hand out governed MongoDB access broadly (per studio3t.com: "the governance that makes it safe to hand out") without provisioning Desktop IDE licenses per user. | studio3t.com/3t-explore/ |

## Constraints and risks

- 3T Explore's edition/plan requirements are unknown/unverified.

## Interactions and dependencies

- Depends on 3T Access for identity/permission management — see [3T Access product report](../../../3t-access/product-report.md).
- AI Helper aspect documented separately — see [ai/feature-report.md](../ai/feature-report.md).

## Conclusions

### Strengths

- Extends governed access to non-developer/browser-only users.

### Limitations

- Edition/plan requirements unverified.

### Unknowns

- Integration maturity with the Desktop IDE connection manager.
