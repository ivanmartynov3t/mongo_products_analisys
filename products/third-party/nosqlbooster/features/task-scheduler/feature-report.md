# Feature Report — NoSQLBooster / Task Scheduler

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Scope

- Feature name: Task Scheduler
- Feature ID: F-SCHED (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Product: NoSQLBooster
- Product group: third-party
- Analysis date: 2026-09-04

## Behavioral walkthrough

NoSQLBooster's Task Scheduler lets users define, save, and run tasks — script files, JSON/BSON imports, relational-table imports (MySQL/PostgreSQL/MSSQL), `mongorestore`-based database restores, collection/query/database exports (JSON/BSON/CSV/TSV/SQL), and `mongodump`-based backups — on a one-time or recurring (daily/weekly/monthly, with day-of-week/month selection) basis. Rather than requiring NoSQLBooster itself to be running at the scheduled time, the scheduler delegates to the host OS's own scheduling mechanism: Windows Task Scheduler on Windows, and `cron` on macOS and Ubuntu. A task view lists all scheduled tasks for at-a-glance review.

Separately, `nbcli` is a standalone command-line executable that runs JavaScript statements/files, SQL query statements, and saved NoSQLBooster tasks from a terminal — explicitly positioned by the vendor as an integration point for "continuous development" (CI/CD) pipelines, and supporting the same shell extensions, fluent query API, and third-party library/Node module environment as the GUI editor. The vendor is explicit that `nbcli` is not an interactive REPL.

Both task scheduling and `nbcli`'s task-execution capability are commercially gated: the Free Edition disables CLI tasks and task scheduling after a 30-day trial, and the Personal License permanently excludes both — only the Commercial License and above unlock automated task scheduling and CLI task execution. This is a materially different constraint from Studio 3T's own scheduler, which (per this repository's other product reports) is not tier-gated in the same all-or-nothing way at the Studio 3T Team/Ultimate level.

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| SCHED-cli-headless | `nbcli` runs scripts, SQL, and saved tasks outside the GUI, explicitly marketed for CI/CD integration. | The direct evidentiary basis for this effort's `SCHED-cli-headless` dictionary ID; per S1's own comparison framing, this is a genuine automation-story advantage NoSQLBooster has that Studio 3T's desktop client did not have as of this repository's most recent Studio 3T Desktop source-code review. | S1, S2, P1, P2 |
| SCHED-plan-limits | Task scheduling and CLI task execution are both excluded below the Commercial tier. | A real automation-adoption barrier for the individual-developer and budget-conscious-team audience both research files otherwise say NoSQLBooster's perpetual pricing appeals to most — the scheduler/CLI combination that differentiates NoSQLBooster from a "just a GUI shell" client is precisely the part gated behind the higher-priced tier. | S1 (pricing table), P2 (edition-comparison table) |
| SCHED-types-time | Recurrence is authored via named patterns (one-time/daily/weekly/monthly with day selection), not a raw cron-expression field, per the primary source. | Users get a simpler, guided scheduling UI at the cost of the flexibility a cron-expression field would offer for less common recurrence patterns. | P1 |

## Constraints and risks

- The entire scheduler/CLI automation surface is unavailable below the Commercial license tier — teams evaluating NoSQLBooster on a Free or Personal license cannot assess this feature area hands-on without upgrading.
- Neither research file nor the primary source's Tasks/Task Scheduler section describes a notification mechanism (email or in-app) on task success/failure/warning, a formal task-status state machine (Scheduled/Running/Completed/Failed/Paused), retry policy, or execution-history retention limits — these are open gaps in the source material, not confirmed absences.

## Interactions and dependencies

- Task types draw directly on capabilities documented elsewhere: script-file tasks depend on F-SHELL's mongosh engine and NPM/utility-library environment (a scheduled script can `require()` the same third-party packages an interactive script can); import/export task types share their format coverage with F-TRANSFER's import/export matrix (`TRANSFER-task-save` in that matrix is the same underlying "save as task" mechanism cross-referenced here); backup/restore tasks wrap the native `mongodump`/`mongorestore` binaries.
- `nbcli`'s SQL-statement execution depends on the same SQL engine documented in [F-SQL](../sql-tools/feature-report.md).

## Conclusions

### Strengths

- A genuine multi-task-type scheduler (script, import, export, backup, restore) built on native OS schedulers rather than requiring the application to stay running, plus a CI/CD-oriented headless CLI (`nbcli`) — together the direct evidentiary basis for this effort's `SCHED-cli-headless` dictionary ID.

### Limitations

- Task scheduling and CLI task execution are both confirmed excluded from the Free and Personal tiers, unlocking only at Commercial and above.
- No cron-expression authoring, notification mechanism, formal task-status state machine, or retry/history-retention configuration is described in any source reviewed.

### Unknowns

- Whether task failures trigger any notification.
- Execution-history retention limits, retry policy, and concurrent-execution limits.
- Whether one-off manual task creation (versus automated scheduling or CLI-triggered execution specifically) is available below the Commercial tier.
