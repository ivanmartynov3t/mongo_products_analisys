# Product Report — 3T Lens

## Navigation

- [Repository README](../../../README.md)
- [Feature dictionary](../../../feature-dictionary.md)
- [3T products index](../README.md)
- [High-level comparison](../../../reports/comparisons/high-level-product-comparison.md)
- [Low-level comparison](../../../reports/comparisons/low-level-feature-comparison.md)

## Product metadata

- Product name: 3T Lens
- Product group: 3t
- Website: https://studio3t.com/ (homepage section). The former page https://studio3t.com/3t-lens/ returned **404 on 2026-09-25**.
- Maker: 3T Software Labs
- Category: Browser-based governed, read-only data workspace
- Analysis date: 2026-09-25
- Version/release context: split out of Studio 3T on 2026-07-29. On 2026-09-25 the governance rows `GOV-002`–`GOV-009` moved to [Govern](../govern/product-report.md) (owner decision), leaving `GOV-platform-lens` here.

## Product summary

The homepage describes 3T Lens as a "Governed Data Workspace": "Safe, governed access to your MongoDB data for everyone who needs to see it but shouldn't change it. Query results automatically inherit your organization's access policies" (studio3t.com homepage, silo copy `data/3t/3t-website-2026/index.md` at silo commit `cde319c7`; at `b142fcc4` that path holds license.studio3t.com by mistake).

The removed product page (studio3t.com/3t-lens/, last read 2026-07-29) also described centralized connection management — connections defined once and shared without passwords, access scoped before login through [3T Access](../3t-access/product-report.md) — and the policy, alert, PII, schema-history and MCP features now documented under [Govern](../govern/product-report.md), where 3T Lens is recorded as an alternative attribution.

## Feature inventory

| Feature ID | Feature | Matrix | Report | Status |
| --- | --- | --- | --- | --- |
| F-GOV | Governance & Security | [feature-matrix.md](features/governance/feature-matrix.md) | [feature-report.md](features/governance/feature-report.md) | Completed (`GOV-platform-lens` only) |

## Product-level conclusions

### Strategic strengths

- Read-only, policy-inheriting access for analysts and business users (homepage).
- Centralized connections without shared passwords (removed page, 2026-07-29).

### Strategic risks / gaps

- No current dedicated public page.
- Separate deployment; pricing unknown.

### Open questions

- Was the product page removed on purpose, and where is its replacement?
- Does 3T Lens deliver the Govern capabilities?
- Does 3T Lens replace or supplement the Desktop IDE connection manager?
