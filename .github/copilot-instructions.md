# Copilot Instructions — Hierarchical Analysis

## Mission

Build a source-backed, hierarchical intelligence base for MongoDB-related products.

## Mandatory structure

Use this hierarchy for every product:

1. Product group:
   - `products/third-party/`
   - `products/3t/`
2. Product folder:
   - `products/<group>/<product-name>/product-report.md`
3. Feature folders:
   - `products/<group>/<product-name>/features/<feature-name>/feature-matrix.md`
   - `products/<group>/<product-name>/features/<feature-name>/feature-report.md`

## Mandatory reporting layers

- Product-level comparison report:
  - `reports/comparisons/high-level-product-comparison.md`
- Feature-level comparison report:
  - `reports/comparisons/low-level-feature-comparison.md`
- Top-level report index:
  - `reports/cumulative-report.md`

## Authoring rules

- Each feature must have both a matrix and a report.
- Feature matrices must be low-level and implementation-aware.
- Product report must summarize features, constraints, and positioning.
- Every major statement must be traceable to a source.
- Keep feature naming normalized across all products and both groups.
- Add a `Navigation` section in every new report/template file with relative links to related artifacts.
- Explicitly label items as:
  - confirmed
  - roadmap/planned
  - unknown/unverified
