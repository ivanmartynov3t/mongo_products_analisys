# Product Report — Govern

## Navigation

- [Repository README](../../../README.md)
- [Feature dictionary](../../../feature-dictionary.md)
- [3T products index](../README.md)
- [High-level comparison](../../../reports/comparisons/high-level-product-comparison.md)
- [Low-level comparison](../../../reports/comparisons/low-level-feature-comparison.md)

## Product metadata

- Product name: Govern
- Product group: 3t
- Website: https://studio3t.com/governed-data-access-platform
- Maker: 3T Software Labs
- Category: Platform track — policy checks, drift alerts, PII classification, governed AI-agent access
- Analysis date: 2026-09-25
- Version/release context: **A platform track, not a separately sold product.** The public site presents three tracks with "Govern at the center" and does not name the products that deliver it (source: studio3t.com/governed-data-access-platform, silo copy captured 2026-09-15). Rows `GOV-002`–`GOV-009` moved here from [3T Lens](../3t-lens/product-report.md) on 2026-09-25 by owner decision, because the 3T Lens page that attributed them (studio3t.com/3t-lens/) returned 404 that day.

## Product summary

Publicly, Govern "checks what the pipeline delivered matches your policy", controls access for "humans and AI agents alike", and "continuously monitors and alerts when something drifts" (studio3t.com/governed-data-access-platform). AI agents calling data through MCP "follow the same rules" (studio3t.com homepage, 3T Access section).

Detailed capabilities — policy templates, alert channels, PII classification, field history, index suggestions, compliance score, violations, scheduled evaluation, MCP tool gating — come from the removed 3T Lens page (last read 2026-07-29) or from private 3T repositories. Each fact is attributed to its source in the [feature matrix](features/governance/feature-matrix.md), which also records the alternative attributions (3T Lens, 3T Access).

## Feature inventory

| Feature ID | Feature | Matrix | Report | Status |
| --- | --- | --- | --- | --- |
| F-GOV | Governance & Security | [feature-matrix.md](features/governance/feature-matrix.md) | [feature-report.md](features/governance/feature-report.md) | Completed — most detail ❓ internal only or from a removed page |

## Product-level conclusions

### Strategic strengths

- One policy plane for people and AI agents, with drift alerts (public).

### Strategic risks / gaps

- Public documentation of the detailed features is thin; the dedicated 3T Lens page is gone.
- PII features are internally cleared only for a design-partner beta.

### Open questions

- Which product delivers Govern: 3T Lens, 3T Access, or both?
- New address of the 3T Lens page, if any.
- MCP tool count (59 / 60 / 40 / 41) and default policy template count (27 / 26).
