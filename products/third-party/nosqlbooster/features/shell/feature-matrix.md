# Feature Matrix — NoSQLBooster / Shell

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: NoSQLBooster
- Product group: third-party
- Feature ID: F-SHELL (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `shell`
- Analysis date: 2026-09-04
- Version/release context: v11.0–v11.1 line

## Source index

- S1: NoSQLBooster Competitive Analysis
- S2: NoSQLBooster Competitive Intelligence Analysis
- P1: nosqlbooster.com/features (primary; fetched directly by this review)

## Capability matrix (low-level)

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SHELL-engine | Shell engine | Confirmed | S1: "embeds the official mongosh shell... version 2.8 in recent releases... support modern JavaScript (ES2022+) and top-level await syntax." Electron + Node.js runtime. | — | N/A | S1, S2, P1 | — |
| SHELL-autocomplete | Auto-complete | Confirmed | S1: "true IntelliSense that auto-completes collection names, field paths, BSON types, operators, and method signatures as the user types." | — | N/A | S1, P1 | — |
| SHELL-debugger | Interactive script debugger | Confirmed — richest evidence of any sub-feature in this product | S1: "an interactive MongoDB script debugger that supports setting line breakpoints (F9), stepping through execution (F5), inspecting call stacks, and editing variable values at runtime." S2 adds: "conditional breakpoints... step over, step into, step out... evaluate statements within a dedicated Debug Console REPL." P1 corroborates with the same F9/F5 shortcuts and describes it as a "unique feature." | — | N/A | S1, S2, P1 | S1 calls this "its most praised feature" — corroborated by both files' user-sentiment sections independently quoting developers praising it, and by the direct evidentiary basis for this effort's `SHELL-debugger` dictionary ID. |
| SHELL-npm-utils | Bundled utility libraries | Confirmed | S1: "pre-loads common utility libraries—including Lodash (_), Moment.js (moment), ShellJS, Mathjs, and Faker.js." S2: "Developers can execute standard `npm install` commands within the NoSQLBooster user data directory, enabling scripts to `require` third-party packages." | — | N/A | S1, S2, P1 | Direct evidentiary basis for this effort's `SHELL-npm-utils` dictionary ID; independently and consistently the single most-praised capability across both files' user-sentiment sections. |
| SHELL-run-all | Run all | Confirmed | P1: "Press `F5` to start debugging, `CTRL+↵|CTRL+F5` to run without debugging." | — | N/A | P1 | Neither S1 nor S2 itemizes run-control keyboard shortcuts specifically; confirmed via primary source. |
| SHELL-save-load | Save & load scripts | Confirmed | S1 (Task Scheduler section): "Run MongoDB Script File" as a task type implies persistent, loadable script files. S2: "recurring workflows for... script executions." | — | N/A | S1, S2 | Moderate evidentiary strength — inferred from task-automation context rather than a direct "save/load script" statement. |

## Feature-level conclusion

### Confirmed strengths

- An interactive, breakpoint-based JavaScript debugger (line breakpoints, step over/into/out, call stack inspection, live variable watch/edit, dedicated Debug Console REPL) — the single most consistently and specifically evidenced capability in this entire product review, appearing in both research files' feature inventories, both files' user-sentiment sections (independently quoting developers), and the primary source, with matching F9/F5 keyboard-shortcut detail across all three.
- Deep pre-loaded utility-library integration (Lodash, Moment.js, ShellJS, Math.js, Faker.js) plus arbitrary NPM package installation and `require()` — the second most consistently praised capability across both files.
- A full mongosh v2.8 engine with ES2022+ and top-level-`await` support.

### Confirmed limitations

- Neither research file discusses shell session management (multiple concurrent sessions, persistent session variables, background execution, auto-reconnect) or a formal "shell mode vs. query-assist mode" distinction the way Studio 3T's and VisuaLeaf's shells are documented elsewhere in this repository — these are simply not itemized, not confirmed absent.

### Open questions / unknowns

- Whether NoSQLBooster's script/query history is a distinct, searchable, curated feature (`SHELL-history`) beyond the general "My Queries" saved-script tab the primary source describes — neither research file discusses shell history specifically.
- The multi-node replica-set command-broadcast capability (S1: "Multi-node cluster management allows users to broadcast shell commands across multiple replica set members simultaneously, aggregating the execution results into a single JSON response") does not cleanly fit any existing `SHELL-*` sub-feature ID's definition and is described narratively in `feature-report.md` rather than forced into a matrix row.
