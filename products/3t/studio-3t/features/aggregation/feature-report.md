# Feature Report — Studio 3T / Aggregation

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [High-level comparison](../../../../../reports/comparisons/high-level-product-comparison.md)

## Scope

This report covers Studio 3T's Aggregation Editor: pipeline layout and navigation, stage lifecycle management, execution options, code generation, integration with export/views/VQB, and cross-session pipeline reuse.

## Behavioral walkthrough

The Studio 3T Aggregation Editor is a dedicated five-panel workspace for building and iterating on MongoDB aggregation pipelines. The left panel lists all pipeline stages with enable/disable checkboxes; the right panel is the code editor for the selected stage. The bottom row shows stage input and output side by side, with a Run button per panel — enabling the user to observe what each stage transforms in isolation before running the full pipeline.

Stage lifecycle management is fully interactive: stages can be added before or after the selected stage, duplicated, reordered with keyboard shortcuts (Shift+F8 / F8), enabled/disabled without deletion, and deleted. This non-destructive enable/disable model allows experimentation with optional stages (e.g., a $limit for development speed that is disabled for production runs) without editing the pipeline JSON.

Three pipeline-level options are exposed: `allowDiskUse` (for pipelines that exceed memory limits), custom collation (for locale-aware string comparisons), and index hint (to test specific index strategies). These map directly to the MongoDB aggregation options document, giving Studio 3T users low-level control without requiring manual `aggregate()` option construction in a shell.

Code generation is a high-value feature: the Query Code tab produces idiomatic driver code in eight target languages (JavaScript/Node.js, Java for three driver API generations, C#, Python, PHP, Ruby, and MongoDB Shell). The Java sub-tabs for 2.x, 3.x, and 4.x driver APIs reflect genuine version-specific API differences and save non-trivial developer time.

The Aggregation Editor integrates tightly with other Studio 3T tools: the Export Wizard can be launched from any Stage I/O panel to export intermediate pipeline results; a "Create view from aggregate query" action wraps the pipeline in db.createView(); and bidirectional sync with the Visual Query Builder keeps the $match and $project stages in the VQB UI synchronized with their equivalent stages in the Aggregation Editor.

## Capability findings

| Capability ID | Finding | Impact |
| --- | --- | --- |
| AGG-001 | Five-panel layout with per-stage input/output preview is the most structured pipeline development environment of any MongoDB GUI tool reviewed. | Significantly reduces pipeline debugging iteration cycles. |
| AGG-003 | Per-stage enable/disable without deletion supports iterative development — stages can be toggled for testing without modifying the pipeline definition. | Reduces accidental data loss from deleted stages during iterative development. |
| AGG-004 | allowDiskUse, collation, and index hint are exposed as first-class UI options — no manual option document construction required. | Saves time versus IntelliShell option assembly; avoids syntax errors. |
| AGG-005 | Eight-language code generation including Java for three driver API versions is unique among MongoDB GUIs. | High value for polyglot teams and teams on older Java driver versions. |
| AGG-009 | Bidirectional VQB ↔ Aggregation Editor sync means filter conditions built in VQB instantly appear as $match stages — and vice versa. | Bridges visual and code-based workflows without context switching. |
| AGG-011 | Date Tags in $match stages reduce ISODate boilerplate throughout pipeline development, not just in Collection Tab queries. | Consistent date-range semantics across all Studio 3T entry points. |

## Constraints and risks

- Code generation reflects the current pipeline at generation time; it does not automatically update when the pipeline changes after code is copied.
- `allowDiskUse` requires sufficient disk space on the MongoDB server's `dbPath`; Studio 3T does not validate available space before enabling.
- Creating a view from a pipeline requires MongoDB ≥ 3.4 and database write access; there is no in-app validation of the MongoDB version before the createView attempt.
- Date Tags in pipelines expand at execution time within Studio 3T; .js exports use the literal expanded date values, not the tag tokens.

## Conclusion

The Aggregation Editor is a mature and feature-rich pipeline authoring environment. Its per-stage I/O preview, non-destructive enable/disable, pipeline-level options, and multi-language code generation put it ahead of comparable tools. Tight integration with VQB, Export Wizard, and view creation makes it a central hub for MongoDB data transformation work in Studio 3T.
