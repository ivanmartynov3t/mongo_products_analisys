# Feature Matrix — MongoDB Compass / Aggregation

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
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
| AGG-editor-layout | Pipeline editor layout | Supported | Stage View, Stage Wizard, Focus Mode, and Text View are available authoring modes for the pipeline builder. | Stage Wizard targets simpler use cases. | Unknown | S1 | Text view supports raw syntax and linting. |
| AGG-stage-modes | Stage edit modes | Supported | Each stage can be authored in Stage View (visual), Stage Wizard (simplified form), Focus Mode (full-screen), or Text View (raw JSON). | Mode availability depends on stage type. | Unknown | S1 | Per-stage mode selection. |
| AGG-stage-toggle | Stage enable/disable | Supported | Toggle stage inclusion without deletion to iterate on partial pipelines. | User must validate stage semantics manually. | Unknown | S1 | Useful for iterative debugging. |
| AGG-stage-mgmt | Stage management | Supported | Reorder stages via drag-drop, add, duplicate, and delete stages with keyboard shortcuts. | User must validate stage semantics manually. | Unknown | S1 | Keyboard shortcuts documented. |
| AGG-stage-preview | Pipeline preview controls | Supported | Sampled preview documents per stage with configurable builder settings. Preview settings do not affect final pipeline run. | Sample size affects preview fidelity. | Unknown | S1, S2 | Separate controls for preview behavior. |
| AGG-save-load | Save/open pipeline workflows | Supported | Pipelines can be saved and reopened from saved query views. | Saved artifacts require explicit user save action. | Unknown | S3, S4 | Supports iterative team workflows. |
| AGG-code-gen | Pipeline export to languages | Supported | Exports pipeline to major driver languages with optional import statements and driver syntax. | Export fidelity depends on valid pipeline/options. | Unknown | S5 | Strong code handoff capability. |
| AGG-export-results | Export pipeline results | Supported | Results export supports JSON/CSV and extended JSON variants. | CSV can lose type fidelity. | Unknown | S6 | Docs explicitly warn for backup use. |
| IDX-explain-brief | Explain plan — plan mode | Supported | Plan-only explain of the pipeline without full execution; visual tree view. | Explain is analysis-only workflow. | Unknown | S7 | Stage-level drill-down supported. |
| IDX-explain-full | Explain plan — full stats | Supported | Full execution-stats explain with per-stage timing and document counts; raw JSON explain also available. | Interpretation quality depends on query/index understanding. | Unknown | S7 | Stage-level drill-down supported. |
| AGG-create-view | Create views from pipeline | Supported | Pipeline output can be materialized into read-only MongoDB views. | Creating a view does not automatically save the pipeline. | Unknown | S8 | View becomes separate artifact. |
| AGG-pipeline-opts | Pipeline options | Supported | Supports custom collation and pipeline-level maxTimeMS configuration. | Collation requires valid locale; timeouts may need tuning. | Unknown | S9, S10 | Operational safety control. |
| AGG-pagination | Result pagination | Supported | Count-results control exposes output count for current pipeline execution state. | Manual refresh required after data changes. | Unknown | S11 | Helpful for quick validation. |
