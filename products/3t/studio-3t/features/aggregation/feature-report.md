# Feature Report — Studio 3T / Aggregation

**Last reviewed:** 2026-07-31 — see [research findings](../../../../../research/studio-3t-desktop-review-2026/03-aggregation-findings.md)

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [High-level comparison](../../../../../reports/comparisons/high-level-product-comparison.md)

## Scope

This report covers Studio 3T's Aggregation Editor: pipeline layout and navigation, stage lifecycle management, execution options, code generation, integration with export/views/VQB, cross-session pipeline reuse, and the legacy Map-Reduce editor.

## Behavioral walkthrough

The Studio 3T Aggregation Editor is a multi-panel workspace for building and iterating on MongoDB aggregation pipelines: a pipeline panel listing all stages with enable/disable checkboxes, a per-stage raw-JSON editor, per-stage input/output preview panels with a Run button, a full pipeline output tab, and Query Code / Explain tabs. A 2026 release-notes entry documents a redesign that replaced per-stage tabs with a list view — the precise current panel arrangement has not been visually re-verified against a current build in this pass, so the historical "five-region" framing is carried forward as unconfirmed rather than re-asserted (see feature-matrix.md, AGG-editor-layout).

Stage lifecycle management is mostly keyboard-driven but has a gap: stages can be added before or after the selected stage (Shift+Ctrl+N), reordered (Shift+F8 / F8), and enabled/disabled without deletion via checkbox or right-click. **Duplicate and Delete, however, have no registered keyboard shortcut** — `ShortcutAction.java` registers run/add/move/show-input-output actions only; `duplicateStage()` and `deleteStage()` are reachable exclusively through the right-click context menu (`AggregationStageEditor.java:849-855`). The non-destructive enable/disable model still allows experimentation with optional stages (e.g., a $limit for development speed that is disabled for production runs) without editing the pipeline JSON.

Each stage has a single raw-JSON editor (`AggregationStageEditor.stageEditor`); there is no separate form/visual mode and no wizard mode. Selecting an operator from the stage's operator-picker combo inserts a pre-built JSON template into that same raw editor — a convenience over typing the stage from scratch, not a distinct editing mode.

Pipeline-level options expose `allowDiskUse` (for pipelines that exceed memory limits), custom collation (for locale-aware string comparisons, server ≥3.4), and index hint (to test specific index strategies, server ≥3.6). These map directly to the MongoDB aggregation options document. `maxTimeMS` is supported only when it is already present in an imported or pasted pipeline options document (e.g. a pasted mongosh script) — there is no dedicated Options-dialog control to set it, and the live-execution option-building path does not write it.

Code generation is a high-value feature: the Query Code tab produces idiomatic driver code from 9 registered generator entries covering 7 language targets (JavaScript/Node.js, Java across three driver API generations, C#, Python, PHP, Ruby, and MongoDB Shell). The three Java driver-API variants (2.x/3.x/4.x) are selectable entries in a single language dropdown, not separate sub-tabs — each reflects genuine version-specific API differences and saves non-trivial developer time.

The Aggregation Editor integrates with other Studio 3T tools: the Export Wizard can be launched from any Stage I/O panel to export intermediate pipeline results; a "Create view from aggregate query" action wraps the pipeline in db.createView(); pipelines can be saved to Query Manager, to a `.js` file, or — as of KONG-10915 (2026-05-12) — to a remote 3T Lens server as a new save destination. The Visual Query Builder relationship is a **one-way, on-demand handoff**, not a live sync: an "Open in aggregation editor" action converts the current VQB/find query into a new, independent Aggregation Editor tab. There is no evidence of live bidirectional syncing of edits between an open VQB panel and an open Aggregation Editor tab.

**AI Helper**: the Aggregation Editor toolbar includes an AI Helper entry point (natural-language pipeline generation, sharing a code path with clipboard paste). This capability belongs to F-AI and is documented there — see [AI feature report](../ai/feature-report.md) — rather than duplicated here.

**Map-Reduce**: the legacy Map-Reduce editor (`t3/dataman/gui/mapreduce/`, `t3/utils/mapreduce/`) has seen essentially no feature development in the last 24 months — the only Map-Reduce-specific commit in that window is KONG-11118 (an NPE fix on tab open). This is consistent with upstream MongoDB deprecating (not removing) server-side map-reduce; Studio 3T appears to be maintaining, not extending, this editor.

## Capability findings

| Capability ID | Finding | Impact |
| --- | --- | --- |
| AGG-001 | Multi-panel layout with per-stage input/output preview is a structured pipeline development environment; exact current panel arrangement not re-verified against the 2026 list-view redesign. | Reduces pipeline debugging iteration cycles, pending visual re-verification. |
| AGG-003 | Per-stage enable/disable without deletion supports iterative development — stages can be toggled for testing without modifying the pipeline definition. Duplicate/Delete, however, have no keyboard shortcut and are right-click-menu only. | Reduces accidental data loss from deleted stages during iterative development; the missing shortcuts are a minor workflow friction point for keyboard-first users. |
| AGG-004 | allowDiskUse, collation, and index hint are exposed as first-class UI options — no manual option document construction required. maxTimeMS is honored only when present in an imported pipeline options document; it has no dedicated UI control. | Saves time versus IntelliShell option assembly for the three UI-backed options; maxTimeMS still requires hand-authoring the options document. |
| AGG-005 | Code generation from 9 generator entries across 7 language targets, including Java for three driver API versions selectable from one dropdown, is unique among MongoDB GUIs. | High value for polyglot teams and teams on older Java driver versions. |
| AGG-009 | The VQB relationship is a one-way, on-demand "Open in aggregation editor" handoff — not a live bidirectional sync. Filter conditions built in VQB can be converted into a new, independent aggregation pipeline, but subsequent edits in either tool do not propagate to the other. | Bridges visual and code-based workflows for initial pipeline creation, but does not support round-tripping edits between VQB and the Aggregation Editor. |
| AGG-011 | Date Tags in $match stages reduce ISODate boilerplate throughout pipeline development, not just in Collection Tab queries. | Consistent date-range semantics across all Studio 3T entry points. |

## Constraints and risks

- Code generation reflects the current pipeline at generation time; it does not automatically update when the pipeline changes after code is copied.
- `allowDiskUse` requires sufficient disk space on the MongoDB server's `dbPath`; Studio 3T does not validate available space before enabling.
- Creating a view from a pipeline requires MongoDB ≥ 3.4 and database write access; there is no in-app validation of the MongoDB version before the createView attempt.
- Date Tags in pipelines expand at execution time within Studio 3T; .js exports use the literal expanded date values, not the tag tokens.
- No keyboard shortcut exists for Duplicate or Delete stage; both require the right-click context menu.
- `maxTimeMS` cannot be set from the Options dialog; it only takes effect when already present in an imported/pasted pipeline options document.
- The VQB relationship is one-way and on-demand, not a live sync — teams relying on the previously documented "bidirectional" behavior should adjust their workflow expectations.
- The Map-Reduce editor is in maintenance mode only; no new capability should be expected there.

## Conclusion

The Aggregation Editor is a mature pipeline authoring environment. Its per-stage I/O preview, non-destructive enable/disable, pipeline-level options, and multi-language code generation are strong relative to comparable tools, though this pass corrected two previously overstated claims: the VQB relationship is a one-way handoff rather than a live bidirectional sync, and code generation is dropdown-selectable rather than sub-tabbed. Integration with Export Wizard, view creation, and (as of KONG-10915) a remote 3T Lens save destination make it a central hub for MongoDB data transformation work in Studio 3T. The legacy Map-Reduce editor remains available but has received no feature investment in the last 24 months.
