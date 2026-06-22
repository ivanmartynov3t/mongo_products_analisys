# Mongo Products Analysis

This repository is for **hierarchical, deep feature analysis** of products that communicate with MongoDB.

## Quick navigation

- [Products index](products/README.md)
- [Third-party products](products/third-party/README.md)
- [3t products](products/3t/README.md)
- [Cumulative report index](reports/cumulative-report.md)
- [High-level comparison](reports/comparisons/high-level-product-comparison.md)
- [Low-level comparison](reports/comparisons/low-level-feature-comparison.md)
- [Copilot instructions](.github/copilot-instructions.md)

## Core approach

Analysis is organized in levels:

1. **Product level**: one high-level product report composed of feature summaries.
2. **Feature level**: each feature has:
   - a detailed **feature matrix**
   - a detailed **feature report**
3. **Comparison level**:
   - high-level product comparison
   - low-level feature-by-feature comparison

## Product groups

We maintain the same structure for two product groups:

- `products/third-party/` for external products
- `products/3t/` for 3t products

## Repository structure

```text
.
├── .github/
│   ├── copilot-instructions.md
│   └── prompts/
├── products/
│   ├── 3t/
│   └── third-party/
├── reports/
│   ├── comparisons/
│   │   ├── high-level-product-comparison.md
│   │   └── low-level-feature-comparison.md
│   └── cumulative-report.md
└── templates/
    ├── product-report-template.md
    ├── feature-matrix-template.md
    ├── feature-report-template.md
    ├── high-level-comparison-template.md
    └── low-level-comparison-template.md
```

## Required workflow

1. Choose product group (`third-party` or `3t`) and product.
2. Create product-level report.
3. Define product feature list.
4. For each feature, create:
   - `feature-matrix.md`
   - `feature-report.md`
5. Update high-level and low-level comparison reports.

## Quality bar

- Feature analysis must be **implementation-aware** and low-level, not generic.
- Every major claim must be **source-backed**.
- Keep naming normalized across products for reliable comparisons.
- Clearly separate **confirmed behavior**, **roadmap/planned behavior**, and **unknown/unverified behavior**.