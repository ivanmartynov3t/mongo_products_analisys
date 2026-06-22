# Feature Matrix — MongoDB Compass / Aggregation

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Source index

- S1: https://www.mongodb.com/docs/compass/create-agg-pipeline/
- S2: https://www.mongodb.com/docs/compass/agg-pipeline-builder/aggregation-pipeline-builder-settings/
- S3: https://www.mongodb.com/docs/compass/agg-pipeline-builder/save-agg-pipeline/
- S4: https://www.mongodb.com/docs/compass/agg-pipeline-builder/open-saved-pipeline/
- S5: https://www.mongodb.com/docs/compass/agg-pipeline-builder/export-pipeline-to-language/
- S6: https://www.mongodb.com/docs/compass/agg-pipeline-builder/export-pipeline-results/
- S7: https://www.mongodb.com/docs/compass/agg-pipeline-builder/view-pipeline-explain-plan/
- S8: https://www.mongodb.com/docs/compass/agg-pipeline-builder/create-a-view/
- S9: https://www.mongodb.com/docs/compass/agg-pipeline-builder/pipeline-custom-collation/
- S10: https://www.mongodb.com/docs/compass/agg-pipeline-builder/maxtime-ms-pipeline/
- S11: https://www.mongodb.com/docs/compass/agg-pipeline-builder/count-pipeline-results/

## Capability matrix

| Capability ID | Capability | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AGG-001 | Multi-mode pipeline authoring | Supported | Stage View, Stage Wizard, Focus Mode, and Text View are available. | Stage Wizard targets simpler use cases. | Unknown | S1 | Text view supports raw syntax and linting. |
| AGG-002 | Stage-level editing controls | Supported | Toggle stage inclusion, reorder via drag-drop, and keyboard shortcuts. | User must validate stage semantics manually. | Unknown | S1 | Useful for iterative debugging. |
| AGG-003 | Pipeline preview controls | Supported | Sampled preview documents and configurable builder settings. | Preview settings do not affect final pipeline run. | Unknown | S1, S2 | Separate controls for preview behavior. |
| AGG-004 | Save/open pipeline workflows | Supported | Pipelines can be saved and reopened from saved query views. | Saved artifacts require explicit user save action. | Unknown | S3, S4 | Supports iterative team workflows. |
| AGG-005 | Pipeline export to languages | Supported | Exports to major driver languages with optional import statements/driver syntax. | Export fidelity depends on valid pipeline/options. | Unknown | S5 | Strong code handoff capability. |
| AGG-006 | Export pipeline results | Supported | Results export supports JSON/CSV and extended JSON variants. | CSV can lose type fidelity. | Unknown | S6 | Docs explicitly warn for backup use. |
| AGG-007 | Explain plan for pipelines | Supported | Visual tree and raw JSON explain with execution metrics. | Explain is analysis-only workflow. | Unknown | S7 | Stage-level drill-down supported. |
| AGG-008 | Create views from pipeline output | Supported | Pipeline output can be materialized into read-only views. | Creating a view does not automatically save pipeline. | Unknown | S8 | View becomes separate artifact. |
| AGG-009 | Pipeline collation and time controls | Supported | Supports custom collation and pipeline-level maxTimeMS configuration. | Collation requires valid locale; timeouts may need tuning. | Unknown | S9, S10 | Operational safety control. |
| AGG-010 | Result counting | Supported | Count-results control exposes output count for current pipeline execution state. | Manual refresh required after data changes. | Unknown | S11 | Helpful for quick validation. |
