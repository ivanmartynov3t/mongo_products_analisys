# Feature Report — Studio 3T / Shell

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Querying feature](../querying/feature-matrix.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Scope

- Feature name: Shell
- Product: Studio 3T
- Product group: 3t
- Analysis date: 2026-06-22

## Behavioral walkthrough

Studio 3T's IntelliShell is a full-featured MongoDB shell environment embedded inside the IDE, built around the bundled mongosh runtime. The editor surface is Monaco-based with Studio 3T–specific extensions: auto-completion of field names and collection names pulled from the live connection, live syntax validation, and Date Tag macro expansion.

The defining architectural choice is the **dual-mode execution model**. In **Shell mode** the shell functions as a pure script runner: all output lands in a single Raw tab, identical to a terminal session. In **Query Assist mode** (the default for `find()`/aggregation workloads), every standalone query that returns a cursor opens its own labeled, editable result tab — wiring the shell output directly into Studio 3T's full result-view stack (Tree, Table, JSON, Visual Explain, code-generation tabs). This means a developer can author queries in shell syntax and immediately benefit from point-and-click editing, explain plans, and code generation without switching tools.

Scripts are executed with three distinct run granularities (F5 / F6 / F9), enabling step-through debugging workflows without external tooling. The IntelliShell is deeply integrated across Studio 3T: it is the target for "Open in IntelliShell" actions from the Collection Tab, Aggregation Editor, and Query Profiler, and it is the runtime used by Pro/Base+ Task Scheduler script tasks.

## Capability-by-capability notes

| Capability ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| SHELL-engine | mongosh binary is bundled; override path configurable per connection or globally. Date Tags usable inside scripts. Format/indent keyboard shortcuts available. | No external mongosh installation required for most users; advanced users can pin a specific version. | confirmed — S1 |
| SHELL-autocomplete | Ctrl+Space triggers completion for JS keywords, shell methods, operators, collection names, field names. Contextual: collection and field suggestions require an active connection. | Significantly reduces syntax errors and speeds up query authoring compared to a bare terminal shell. | confirmed — S1 |
| SHELL-validation | Live red gutter crosses and right-ruler markers surface syntax errors before execution. | Reduces wasted round-trips from script typos and malformed expressions. | confirmed — S1 |
| SHELL-run-all | F5 runs full script. In Query Assist mode each cursor-returning call opens its own result tab. | Enables full-script execution with per-query result isolation; avoids having to manually split scripts. | confirmed — S1 |
| SHELL-run-cursor | F6 executes from script start to cursor position. | Supports incremental development and debugging without copy-pasting sub-sections. | confirmed — S1 |
| SHELL-run-select | F9 runs the selected text block. | Enables ad-hoc one-off execution of any fragment without altering the overall script. | confirmed — S1 |
| SHELL-modes | Shell mode vs Query Assist mode is per-tab toggleable. Query Assist mode is default for find()/aggregation. | Query Assist mode is the key differentiator from a bare terminal; destructive-op warnings add a safety layer. | confirmed — S1 |
| SHELL-result-tabs | Per-query result tabs in Query Assist mode, labeled with source line number. Pinnable across re-runs. | Allows side-by-side comparison of multiple query results within one script run; pinning preserves prior results for diffing. | confirmed — S1 |
| SHELL-result-views | Full result-view stack available in shell result tabs: Tree, Table, JSON, Query Code, Visual Explain. | Eliminates the need to copy-paste queries from shell to Collection Tab just to get explain plans or code generation. | confirmed — S1 |
| SHELL-save-load | Save to Query Manager (with full connection context) or as .js file. Load from either source. | Query Manager saves enable sharing and reuse across sessions; .js saves enable version control or external editor workflows. | confirmed — S1, S2 |
| SHELL-integrations | Bi-directional integrations with Collection Tab, Aggregation Editor, Query Profiler, and Task Scheduler. | IntelliShell is the hub that connects all Studio 3T tools; "Open in IntelliShell" is available from every major tool. | confirmed — S1, S2 |

## Constraints and risks

- **Query Assist mode scope**: Result tabs only open for standalone `find()` and aggregation pipeline calls. Administrative commands, bulk writes, and other shell operations still output to the Raw tab only.
- **mongosh binary dependency**: The bundled mongosh must match the MongoDB server's wire protocol version. Very old or very new server versions may require overriding to a matching mongosh build.
- **Visual Explain in Shell mode**: Visual Explain is unavailable in Shell mode; users must switch to Query Assist mode to access explain plans from IntelliShell.
- **Task Scheduler integration requires Pro/Base+**: IntelliShell Script Tasks (scheduling .js scripts) are gated behind the Pro/Base+ tier; free-tier users cannot schedule shell scripts.

## Interactions and dependencies

- **Querying**: "Open in IntelliShell" from the Collection Tab sends the current query filter as a `db.collection.find(...)` call; the shell and Collection Tab are complementary, not redundant.
- **Aggregation**: The Aggregation Editor's Query Code tab (MongoDB Shell target) feeds directly into IntelliShell via the "Open in IntelliShell" button; pipelines authored visually can be refined in the shell.
- **Indexing & Performance**: Visual Explain is shared between IntelliShell result tabs and Collection Tab result tabs; Query Profiler "Open in IntelliShell" surfaces profiled queries for re-execution and optimization.
- **Task Scheduler**: IntelliShell Script Tasks are the shell's scheduled-execution surface; script units can produce output files with date-stamped names using Date Tag placeholders.
- **Data Transfer**: Date Tags (shared with the Query Bar and Aggregation Editor) enable time-windowed `find()` calls in shell scripts used as export sources.

## Conclusions

### Strengths

- **Query Assist mode** is a major differentiator: shell-authored queries gain the full result-view stack (explain, code-gen, inline edit) without leaving the shell.
- **Tri-granularity execution** (F5/F6/F9) supports professional scripting and debugging workflows.
- **Deep bi-directional integration** across all Studio 3T tools makes IntelliShell the central scripting hub of the IDE.
- **mongosh bundled + configurable**: zero setup for standard use; precise version control for edge cases.

### Limitations

- Query Assist mode result-tab support is limited to `find()` and aggregation; administrative/write operations produce raw-only output.
- Visual Explain is unavailable in Shell mode; mode switching is required for explain workflows initiated from a shell script.
- Task Scheduler script tasks are a Pro/Base+ feature; free-tier users cannot automate shell script execution.

### Unknowns

- Maximum script file size or line count limits are unverified.
- Whether multiple IntelliShell tabs can run concurrently (parallel execution) is unverified.
- Auto-save / crash-recovery behavior for unsaved scripts is unverified.
