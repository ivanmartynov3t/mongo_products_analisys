# Feature Report — MongoDB Compass / Querying

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Scope

This report covers document-query authoring and execution controls from the query bar and related reuse/export tooling.

## Behavioral walkthrough

Query workflows are centered on filter + options controls (project, sort, skip, limit, collation, maxTimeMS), with history/favorites support for reuse and driver-language export for implementation handoff.

## Capability findings

| Capability ID | Finding | Impact |
| --- | --- | --- |
| QRY-001 | Filter workflows are direct and expressive. | Fast query iteration in GUI. |
| QRY-002 to QRY-006 | Option controls cover common execution and shaping needs. | Good parity with everyday shell-level query controls. |
| QRY-007 and QRY-008 | History/favorites reduce repeated manual authoring. | Improves analyst productivity and repeatability. |
| QRY-009 | Driver-language export shortens implementation handoff. | Reduces translation friction from GUI to code. |

## Constraints and risks

- Query correctness and performance still depend on user-selected operators and indexes.
- Timeouts may require manual tuning for heavy datasets.

## Conclusion

Querying support is mature and practical, with strong authoring, reuse, and export workflows for developer teams.
