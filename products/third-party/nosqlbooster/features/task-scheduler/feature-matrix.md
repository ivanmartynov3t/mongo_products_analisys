# Feature Matrix — NoSQLBooster / Task Scheduler

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: NoSQLBooster
- Product group: third-party
- Feature ID: F-SCHED (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `task-scheduler`
- Analysis date: 2026-09-04
- Version/release context: v11.0–v11.1 line

## Source index

- S1: NoSQLBooster Competitive Analysis, `research/google_research/nosqlbooster-competitive-analysis/NoSQLBooster Competitive Analysis.md`
- S2: NoSQLBooster Competitive Intelligence Analysis, `research/google_research/nosqlbooster-competitive-intelligence-analysis/NoSQLBooster Competitive Intelligence Analysis.md`
- P1: nosqlbooster.com/features (primary; fetched directly by this review 2026-09-04 — "Tasks and Task Scheduler" and "NoSQLBooster Command Line Interface (nbcli)" sections)
- P2: nosqlbooster.com/compareEditions (primary; fetched directly by this review 2026-09-04)

## Capability matrix (low-level)

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SCHED-cli-headless | Headless CLI automation | Confirmed | P1: "The nbcli is a simple command-line interface for NoSQLBooster. It allows you to run javascript or SQL query statement, javascript file, and NoSQLBooster tasks in terminal or integrate NoSQLBooster into your continuous development." S1: "Command-line execution is handled by nbcli." S2: "Operational tasks can also be triggered headlessly through a Command Line Interface (nbcli)." | Excluded from Free and Personal tiers per S1's pricing table and P2's edition-comparison table (`Run Tasks` under Command Line Interface unlocked at Commercial). P1 notes nbcli "is not a REPL (Read Evaluate Print Loop) tool." | N/A | S1, S2, P1, P2 | Direct, near-exact-definition evidentiary match for the `SCHED-cli-headless` dictionary ID — this is the capability the ID was minted to describe during this same five-product effort. |
| SCHED-task-types | Task types | Confirmed | P1 itemizes exactly: "Run MongoDB Script File," "Import from JSON and BSON files," "Import Tables from MySQL, PostgreSQL, and MSSQL," "Restore MongoDB Databases (mongorestore)," "Export Collection/Query to JSON, BSON, CSV\|TSV and SQL," "Export Database to JSON, BSON, CSV\|TSV, and SQL," "Backup MongoDB Databases (mongodump)." S1/S2 corroborate generally (backup, restore, import, export, script execution). | — | N/A | S1, S2, P1 | Script-file tasks are explicitly extensible via NoSQLBooster's own NPM `require()` support, per P1: "the functionality of this script is extensible and flexible." |
| SCHED-types-time | Time-based schedules | Confirmed | P1: "Task Scheduler lets you define tasks that execute on a one-time basis or a recurring schedule that you specify. It supports tasks that perform daily, weekly, or monthly, and you can choose the day(s) of the week or month when you want each task to execute." | — | N/A | P1 | Neither S1 nor S2 itemizes the specific recurrence granularity (daily/weekly/monthly with day-of-week/month selection) — confirmed via primary source. |
| SCHED-cron | Cron expression | Unverified | P1 states the underlying OS mechanism (see below) but does not describe user-facing cron-expression syntax as an authoring option — scheduling is presented as named recurrence patterns (one-time/daily/weekly/monthly), not raw cron strings. | — | N/A | — | Not marked Confirmed: the presence of OS-level cron as an execution mechanism does not by itself confirm a user-facing cron-expression authoring field. |
| SCHED-history | Execution history | Confirmed (existence only) | P1: "The task view allows you to view all scheduled tasks at a glance easily," illustrated with a "Tasks - scheduler" screenshot. | — | N/A | P1 | Neither research file nor P1's text itemizes retention limits, per-run status detail, or history depth — existence only. |
| SCHED-notifications | Notifications | Unverified | Not described in S1, S2, or P1's Tasks/Task Scheduler section. | — | N/A | — | The dictionary's supplemental precedent (Studio 3T's own v7.0-era "Task Email Alerts," referenced only in the Navicat/DBeaver comparative material this repository already holds) does not itself evidence NoSQLBooster's own notification behavior — not carried forward without NoSQLBooster-specific evidence. |
| SCHED-plan-limits | Scheduler plan limits | Confirmed | S1's pricing table: Free Edition — "CLI tasks, task scheduling, and enterprise authentication are disabled" after the 30-day trial; Personal License — "Lacks CLI task execution, task scheduling"; Commercial License unlocks "automated task scheduling." P2's edition-comparison table lists `Tasks` and `Task Schedule` rows with `Run Tasks` (CLI) gated to Commercial. | Task creation/definition itself is not explicitly stated as tier-gated separately from *running* tasks via scheduler/CLI — S1's wording ("task scheduling... disabled") is read here as gating the scheduling/execution mechanism, not necessarily one-off manual task use. | N/A | S1, P2 | — |

## Feature-level conclusion

### Confirmed strengths

- A genuine, multi-task-type scheduler (script execution, import, export, backup via `mongodump`, restore via `mongorestore`) driven by native OS schedulers (Windows Task Scheduler on Windows; cron on macOS/Ubuntu, per P1: "NoSQLBooster does not need to run at the scheduled time to run any scheduled tasks... uses the Windows Task Scheduler... while in macOS and Ubuntu, cron is used") rather than requiring NoSQLBooster itself to stay running.
- A headless CLI (`nbcli`) supporting JavaScript, SQL, and saved-task execution — explicitly positioned by the vendor for CI/CD integration ("integrate NoSQLBooster into your continuous development") — the direct evidentiary basis for this effort's `SCHED-cli-headless` dictionary ID.

### Confirmed limitations

- Task scheduling and CLI task execution (`nbcli` "Run Tasks") are both confirmed excluded from the Free and Personal license tiers, unlocking only at Commercial and above — a real automation-adoption barrier for individual/budget-conscious users, the same demographic both research files otherwise say NoSQLBooster's pricing appeals to most.
- No cron-expression authoring surface is described (recurrence is via named patterns — one-time/daily/weekly/monthly with day selection — not raw cron syntax), no notification mechanism (email/in-app) is described in any source reviewed, and no per-run status-state machine (Scheduled/Running/Completed/Failed/Paused) or retention-limit configuration is itemized beyond a bare "view all scheduled tasks at a glance" screenshot.

### Open questions / unknowns

- Whether task execution failures trigger any notification (email or in-app) — not discussed in either research file or the primary source's Tasks/Task Scheduler section.
- Exact execution-history retention limit, retry policy, and concurrent-execution limits — none of these are itemized in the sources reviewed.
- Whether one-off manual task creation/editing (as opposed to automated scheduling or CLI-triggered execution) is available at the Free/Personal tiers, or whether the entire Tasks feature is gated — S1's pricing-table wording ("task scheduling... disabled," "no task scheduling") is ambiguous on this point.
