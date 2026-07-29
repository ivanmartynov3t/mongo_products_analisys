# Feature Matrix — Studio 3T / Governance & Security

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Scope note

This file previously documented the Studio 3T platform's governance-tier products (3T Lens, 3T Access, 3TL Bridge) and 3T Explore's governance-relevant aspects as sub-sections of Studio 3T. As of 2026-07-29, each of those products has been split into its own product folder under `products/3t/` with its own `product-report.md` and `features/governance/{feature-matrix.md,feature-report.md}`. See the pointer table below.

The Desktop IDE's own native governance capabilities (RBAC user/role management, audit logging, data masking, collection compare/sync, read-only/protect mode) are tracked by dictionary IDs (`GOV-readonly-mode`, `GOV-rbac-users`, `GOV-rbac-roles`, `GOV-audit-log`, `GOV-collection-compare`, `GOV-collection-sync`, `GOV-data-masking`, `GOV-cred-protection`) that the [comparison reports](../../../../../reports/comparisons/low-level-feature-comparison.md) already reference against this file, but a dedicated capability matrix for them has not yet been authored here — this is an existing gap, not something introduced by the 2026-07-29 split.

## Pointer table — platform-tier products now documented separately

| Sub-feature ID | Product | Matrix | Report |
| --- | --- | --- | --- |
| GOV-platform-lens, GOV-002, GOV-003, GOV-004, GOV-005, GOV-006, GOV-007 | 3T Lens | [feature-matrix.md](../../../3t-lens/features/governance/feature-matrix.md) | [feature-report.md](../../../3t-lens/features/governance/feature-report.md) |
| GOV-platform-access | 3T Access | [feature-matrix.md](../../../3t-access/features/governance/feature-matrix.md) | [feature-report.md](../../../3t-access/features/governance/feature-report.md) |
| GOV-platform-cdc, GOV-010, GOV-011, GOV-012, GOV-013 | 3TL Bridge | [feature-matrix.md](../../../3tl-bridge/features/governance/feature-matrix.md) | [feature-report.md](../../../3tl-bridge/features/governance/feature-report.md) |
| GOV-platform-explore | 3T Explore | [feature-matrix.md](../../../3t-explore/features/governance/feature-matrix.md) | [feature-report.md](../../../3t-explore/features/governance/feature-report.md) |

## Feature-level conclusion

### Confirmed strengths

- N/A here — see the linked per-product matrices above for confirmed platform-tier governance capabilities.

### Confirmed limitations

- Desktop IDE-native governance capabilities (RBAC, audit log, data masking, collection compare/sync) do not yet have a dedicated capability matrix in this file.

### Open questions / unknowns

- Author a Desktop IDE-native governance capability matrix covering `GOV-readonly-mode`, `GOV-rbac-users`, `GOV-rbac-roles`, `GOV-audit-log`, `GOV-collection-compare`, `GOV-collection-sync`, `GOV-data-masking`, and `GOV-cred-protection`.
