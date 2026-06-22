# Cumulative Report (Hierarchy Index)

This file is the top-level index for all comparison layers.

## Navigation

- [Repository README](../README.md)
- [Feature dictionary](../feature-dictionary.md)
- [Products index](../products/README.md)
- [High-level comparison](comparisons/high-level-product-comparison.md)
- [Low-level comparison](comparisons/low-level-feature-comparison.md)

## Comparison layers

1. High-level product comparison:
   - `reports/comparisons/high-level-product-comparison.md`
2. Low-level feature comparison:
   - `reports/comparisons/low-level-feature-comparison.md`

## Current scope status

- Third-party products analyzed:
  - MongoDB Compass (6 features: F-CONN, F-QUERY, F-AGG, F-SCHEMA, F-IDX, F-GOV)
  - VisuaLeaf (10 features: F-CONN, F-QUERY, F-AGG, F-SCHEMA, F-IDX, F-TRANSFER, F-SHELL, F-AI, F-GOV, F-SCHED)
- 3t products analyzed:
  - Studio 3T (11 features: all F-CONN through F-SCHED)

## Feature coverage by product

See [feature-dictionary.md](../feature-dictionary.md) for feature ID definitions.

| Feature ID | Feature | Studio 3T | MongoDB Compass | VisuaLeaf |
|---|---|---|---|---|
| F-CONN | Connectivity | ✓ | ✓ | ✓ |
| F-QUERY | Querying | ✓ | ✓ | ✓ |
| F-AGG | Aggregation | ✓ | ✓ | ✓ |
| F-SCHEMA | Schema | ✓ | ✓ | ✓ |
| F-IDX | Indexing & Performance | ✓ | ✓ | ✓ |
| F-TRANSFER | Data Transfer | ✓ | — | ✓ |
| F-SHELL | Shell | ✓ | — | ✓ |
| F-AI | AI Features | ✓ | — | ✓ |
| F-SQL | SQL Tools | ✓ | — | — |
| F-GOV | Governance & Security | ✓ | ✓ | ✓ |
| F-SCHED | Task Scheduler | ✓ | — | ✓ |

## Executive summary

- Repository is organized with unified feature IDs and sub-feature IDs across all products.
- The [feature dictionary](../feature-dictionary.md) is the authoritative source for all IDs.
- All future analysis must use Feature IDs from the dictionary for folder names and sub-feature IDs for matrix rows.
- Feature folder names are normalized: `schema`, `ai`, `governance`, `data-transfer`, `shell`, `task-scheduler`.
- Comparison updates must keep high-level and low-level reports synchronized with the dictionary.
