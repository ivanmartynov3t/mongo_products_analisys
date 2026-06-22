# Feature Report — MongoDB Compass / Schema Validation

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Scope

This report covers schema discovery, schema export, and validation rule management in Compass.

## Behavioral walkthrough

Schema workflows begin with sampled analysis and visual profiling, then extend into exportable schema artifacts and validation-rule creation/editing with strictness controls.

## Capability findings

| Capability ID | Finding | Impact |
| --- | --- | --- |
| SCH-001 and SCH-002 | Sampling plus rich visual summaries provide quick structural visibility. | Strong exploratory data modeling support. |
| SCH-004 | Multiple export formats improve portability and governance workflows. | Better handoff to documentation/review pipelines. |
| SCH-005 and SCH-006 | Validation model supports both schema-first and query-operator rule styles. | Flexible validation strategy by team maturity. |
| SCH-007 | Add/edit/generate/preview loops reduce rule authoring friction. | Faster validation iteration. |

## Constraints and risks

- Very wide schemas (>1000 fields) hit export/validation limits.
- Sampling can hide rare-field behavior unless explicitly accounted for.

## Conclusion

Schema and validation tooling is strong for practical governance and modeling, with clear constraints documented for large/wide collections.
