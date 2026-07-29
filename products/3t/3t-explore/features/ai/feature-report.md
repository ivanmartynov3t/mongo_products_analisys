# Feature Report — 3T Explore / AI Features

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [High-level comparison](../../../../../reports/comparisons/high-level-product-comparison.md)

## Scope

This report covers the AI Helper available within 3T Explore, the browser-based MongoDB IDE product in Studio 3T's "Build" track.

## Behavioral walkthrough

3T Explore bundles an AI Helper offering context-aware query assistance ("based on what you're actually working with," per studio3t.com) alongside its core Explore, Visual Query Builder, IntelliShell, and Aggregation Editor surfaces. This mirrors the Desktop IDE's AI Helper concept (see [Studio 3T's AI feature report](../../../studio-3t/features/ai/feature-report.md)) but runs in the browser IDE context.

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| AI-012 | AI Helper available in the browser IDE extends AI-assisted querying to users without a Desktop IDE install. | Broadens AI-assisted MongoDB access to browser-only or non-developer users. | studio3t.com/3t-explore/ |

## Constraints and risks

- 3T Explore's AI Helper availability and edition/plan requirements are unknown/unverified.

## Interactions and dependencies

- Governance-relevant aspects of 3T Explore (Workspace Switcher, Access Control) are documented separately — see [governance/feature-report.md](../governance/feature-report.md).

## Conclusions

### Strengths

- Brings AI-assisted query generation to a zero-install browser surface.

### Limitations

- Edition/plan requirements unverified.

### Unknowns

- Whether 3T Explore requires a separate license from the Desktop IDE.
