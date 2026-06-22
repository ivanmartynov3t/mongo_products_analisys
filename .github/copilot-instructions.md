# Copilot Instructions — Hierarchical Analysis

## Mission

Build a source-backed, hierarchical intelligence base for MongoDB-related products.

## Unified feature dictionary

**All feature analysis must use the [unified feature dictionary](../feature-dictionary.md).**

- Feature IDs: `F-CONN`, `F-QUERY`, `F-AGG`, `F-SCHEMA`, `F-IDX`, `F-TRANSFER`, `F-SHELL`, `F-AI`, `F-SQL`, `F-GOV`, `F-SCHED`
- Feature folder names are defined in the dictionary and must be used exactly.
- Sub-feature IDs (e.g., `CONN-topology`, `QUERY-filter-bar`) are defined in the dictionary and must be used in all matrices.
- **Do not invent sub-feature IDs** — add them to the dictionary first if needed.

## Mandatory structure

Use this hierarchy for every product:

1. Product group:
   - `products/third-party/`
   - `products/3t/`
2. Product folder:
   - `products/<group>/<product-name>/product-report.md`
3. Feature folders — **names must match dictionary folder names exactly**:
   - `products/<group>/<product-name>/features/connectivity/`
   - `products/<group>/<product-name>/features/querying/`
   - `products/<group>/<product-name>/features/aggregation/`
   - `products/<group>/<product-name>/features/schema/`
   - `products/<group>/<product-name>/features/indexing-performance/`
   - `products/<group>/<product-name>/features/data-transfer/`
   - `products/<group>/<product-name>/features/shell/`
   - `products/<group>/<product-name>/features/ai/`
   - `products/<group>/<product-name>/features/sql-tools/`
   - `products/<group>/<product-name>/features/governance/`
   - `products/<group>/<product-name>/features/task-scheduler/`
4. Each feature folder contains:
   - `feature-matrix.md`
   - `feature-report.md`

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
- **Sub-feature IDs** (column: `Sub-feature ID`) must come from the feature dictionary.
- Product report must summarize features using Feature IDs and link to matrix/report.
- Every major statement must be traceable to a source.
- Keep feature naming normalized across all products and both groups.
- Add a `Navigation` section in every new report/template file with relative links to:
  - product report
  - feature matrix or report (as applicable)
  - feature dictionary (`feature-dictionary.md`)
  - relevant comparison reports
- Explicitly label items as:
  - confirmed
  - roadmap/planned
  - unknown/unverified
