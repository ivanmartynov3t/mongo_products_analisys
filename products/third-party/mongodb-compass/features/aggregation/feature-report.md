# Feature Report — MongoDB Compass / Aggregation

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [High-level comparison](../../../../../reports/comparisons/high-level-product-comparison.md)

## Scope

This report covers aggregation pipeline authoring, execution analysis, result export, and view creation workflows.

## Behavioral walkthrough

Compass supports visual and text-based aggregation authoring with stage-level controls, preview tuning, explain analysis, and export operations. It supports saving pipelines for reuse and creating read-only views from pipeline output.

## Capability findings

| Capability ID | Finding | Impact |
| --- | --- | --- |
| AGG-001 | Multi-mode editing includes visual and raw text workflows. | Covers both beginner and advanced users. |
| AGG-004 | Saved pipeline workflows support repeatable analysis. | Better reuse and team transfer. |
| AGG-005 and AGG-006 | Export supports both implementation handoff and data extraction. | Bridges analytics-to-development workflows. |
| AGG-007 | Explain tools provide execution-level transparency. | Strong support for performance troubleshooting. |
| AGG-008 | View creation makes pipeline output reusable as read-only artifacts. | Useful for controlled data consumption. |

## Constraints and risks

- Powerful stages can be destructive if not reviewed carefully.
- CSV export is not type-safe for backup-grade use.

## Conclusion

Aggregation is one of Compass’s strongest areas, with deep authoring controls and practical operational outputs.
