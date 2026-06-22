# Mongo Products Analysis

This repository is for **hierarchical, deep feature analysis** of products that communicate with MongoDB.

## Quick navigation

- [**Unified Feature Dictionary**](feature-dictionary.md) ← start here for feature IDs
- [Products index](products/README.md)
- [Third-party products](products/third-party/README.md)
- [3t products](products/3t/README.md)
- [Cumulative report index](reports/cumulative-report.md)
- [High-level comparison](reports/comparisons/high-level-product-comparison.md)
- [Low-level comparison](reports/comparisons/low-level-feature-comparison.md)
- [Copilot instructions](.github/copilot-instructions.md)

## Core approach

Analysis is organized in levels:

1. **Feature dictionary** (`feature-dictionary.md`): canonical registry of all 11 Feature IDs and all sub-feature IDs. Every matrix, report, and comparison must use these IDs.
2. **Product level**: one high-level product report composed of feature summaries using Feature IDs.
3. **Feature level**: each feature has:
   - a detailed **feature matrix** (sub-feature IDs from the dictionary)
   - a detailed **feature report**
4. **Comparison level**:
   - high-level product comparison (Feature ID rows)
   - low-level feature-by-feature comparison (sub-feature ID rows)

## Feature IDs

| Feature ID | Folder | Display name |
|---|---|---|
| F-CONN | `connectivity` | Connectivity |
| F-QUERY | `querying` | Querying |
| F-AGG | `aggregation` | Aggregation |
| F-SCHEMA | `schema` | Schema |
| F-IDX | `indexing-performance` | Indexing & Performance |
| F-TRANSFER | `data-transfer` | Data Transfer |
| F-SHELL | `shell` | Shell |
| F-AI | `ai` | AI Features |
| F-SQL | `sql-tools` | SQL Tools |
| F-GOV | `governance` | Governance & Security |
| F-SCHED | `task-scheduler` | Task Scheduler |

See [feature-dictionary.md](feature-dictionary.md) for all sub-feature IDs.

## Product groups

We maintain the same structure for two product groups:

- `products/third-party/` for external products
- `products/3t/` for 3t products

## Repository structure

```text
.
├── feature-dictionary.md       ← unified feature + sub-feature ID registry
├── .github/
│   ├── copilot-instructions.md
│   └── prompts/
├── products/
│   ├── 3t/
│   │   └── studio-3t/
│   │       ├── product-report.md
│   │       └── features/
│   │           ├── connectivity/
│   │           ├── querying/
│   │           ├── aggregation/
│   │           ├── schema/
│   │           ├── indexing-performance/
│   │           ├── data-transfer/
│   │           ├── shell/
│   │           ├── ai/
│   │           ├── sql-tools/
│   │           ├── governance/
│   │           └── task-scheduler/
│   └── third-party/
│       ├── mongodb-compass/
│       │   └── features/
│       │       ├── connectivity/
│       │       ├── querying/
│       │       ├── aggregation/
│       │       ├── schema/
│       │       ├── indexing-performance/
│       │       └── governance/
│       └── visual-eaf/
│           └── features/
│               ├── connectivity/
│               ├── querying/
│               ├── aggregation/
│               ├── schema/
│               ├── indexing-performance/
│               ├── data-transfer/
│               ├── shell/
│               ├── ai/
│               ├── governance/
│               └── task-scheduler/
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

1. Read `feature-dictionary.md` to understand all Feature IDs and sub-feature IDs.
2. Choose product group (`third-party` or `3t`) and product.
3. Create product-level report using Feature IDs from the dictionary.
4. For each applicable feature, create:
   - `features/<feature-folder>/feature-matrix.md` using sub-feature IDs from the dictionary
   - `features/<feature-folder>/feature-report.md`
5. If a needed sub-feature ID does not exist in the dictionary, add it there first.
6. Update high-level and low-level comparison reports.

## Quality bar

- Feature analysis must be **implementation-aware** and low-level, not generic.
- Every major claim must be **source-backed**.
- All IDs must come from `feature-dictionary.md`.
- Clearly separate **confirmed behavior**, **roadmap/planned behavior**, and **unknown/unverified behavior**.