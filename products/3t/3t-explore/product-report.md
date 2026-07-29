# Product Report — 3T Explore

## Navigation

- [Repository README](../../../README.md)
- [Feature dictionary](../../../feature-dictionary.md)
- [3T products index](../README.md)
- [High-level comparison](../../../reports/comparisons/high-level-product-comparison.md)
- [Low-level comparison](../../../reports/comparisons/low-level-feature-comparison.md)

## Product metadata

- Product name: 3T Explore
- Product group: 3t
- Website: https://studio3t.com/3t-explore/
- Maker: 3T Software Labs
- Category: Browser-based MongoDB IDE
- Analysis date: 2026-07-28
- Version/release context: Browser IDE product in the "Build" track (alongside the Studio 3T Desktop IDE and 3T MCP). Split out of the Studio 3T product report into its own product folder 2026-07-29 (was previously documented as a sub-section of Studio 3T's AI Features and Governance & Security). This repository's earlier drafts mislabeled this product "3T Build" — corrected 2026-07-28; "Build" is the track name, not the product name.

## Product summary

3T Explore is the browser-based IDE product in Studio 3T's "Build" track (tagline per studio3t.com: "The browser IDE for MongoDB and other document databases"). It bundles Explore (view/query/edit collection data in browser), Visual Query Builder, IntelliShell, Aggregation Editor, an AI Helper (context-aware query assistance), a Workspace Switcher (manage multiple workspaces with role-based data visibility), and Access Control integration with 3T Access Manager for granular database/collection permissions (see [3T Access](../3t-access/product-report.md)).

3T Explore is a separate product/deployment from the Studio 3T Desktop IDE. Its edition/plan requirements, and whether it requires a separate license from the Desktop IDE, are unknown/unverified — studio3t.com describes the product's capabilities but not its pricing or licensing model.

## Feature inventory

Feature IDs and folder names from [feature-dictionary.md](../../../feature-dictionary.md).

| Feature ID | Feature | Matrix | Report | Status |
| --- | --- | --- | --- | --- |
| F-AI | AI Features | [feature-matrix.md](features/ai/feature-matrix.md) | [feature-report.md](features/ai/feature-report.md) | Completed |
| F-GOV | Governance & Security | [feature-matrix.md](features/governance/feature-matrix.md) | [feature-report.md](features/governance/feature-report.md) | Completed |

## Product-level conclusions

### Strategic strengths

- Extends governed, role-based MongoDB access to non-developer users without provisioning Desktop IDE licenses per user (per studio3t.com: "the governance that makes it safe to hand out").
- Bundles the same core productivity surface as the Desktop IDE (Explore, VQB, IntelliShell, Aggregation Editor, AI Helper) in a zero-install browser context.
- Workspace Switcher and 3T Access Manager integration extend pre-login, role-based access scoping to a browser surface.

### Strategic risks / gaps

- Edition/plan requirements are unknown/unverified, including whether it requires a separate license from the Desktop IDE.
- As a separate deployment, integration maturity with the Desktop IDE connection manager is not fully verified.

### Open questions

- What edition/plan is required for 3T Explore access?
- Does 3T Explore require a separate license from the Desktop IDE?
