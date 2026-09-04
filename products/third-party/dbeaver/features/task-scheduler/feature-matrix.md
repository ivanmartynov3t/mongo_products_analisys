# Feature Matrix — DBeaver / Task Scheduler

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: DBeaver
- Product group: third-party
- Feature ID: F-SCHED (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `task-scheduler`
- Analysis date: 2026-09-04
- Version/release context: DBeaver 25.x–26.x line

## Source index

- S1: DBeaver Competitive Intelligence Analysis (secondary research file), `research/google_research/dbeaver-competitive-intelligence-analysis/DBeaver Competitive Intelligence Analysis.md`
- S2: License types - DBeaver PRO, https://dbeaver.com/license-types/ (S1 Works Cited #16); Differences between license types · GitHub wiki (S1 Works Cited #18, #19)

## Capability matrix (low-level)

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SCHED-task-types | Task types | Confirmed | S1: "Task Management and Automation Scheduler: Background process manager capable of scheduling recurring database tasks, automated schema backups, database-to-database data transfers, and composite execution workflows without external orchestrators like cron or Airflow (Enterprise/Ultimate tiers)." | Enterprise/Ultimate tiers only, per S1's explicit parenthetical. | Unverified (exact task-type list) | S1 | Dictionary's coverage-matrix note already flags this as the reason DBeaver's F-SCHED cell is "partial." |
| SCHED-plan-limits | Scheduler plan limits | Confirmed | Same S1 sentence plus the pricing/edition table, which places "Task Types" among the capabilities DBeaver gates to convert free Community users to paid tiers. | Enterprise/Ultimate only — not available in Community or Lite. | Unverified | S1, S2 | — |
| SCHED-cli-headless | Headless CLI automation | Unverified — per secondary source, no primary citation | S1: "Headless Operations via Command Line (dbvr): Terminal-first utility allowing developers to run database operations, data export tasks, and schema migrations in headless CI/CD environments." | Exact operation scope and tier requirement not specified. | Unverified | S1 | This DBeaver capability (`dbvr`) is the direct evidentiary basis for the new dictionary ID `SCHED-cli-headless` added in this same effort (2026-09-04); its existence in the dictionary does not itself make the claim Confirmed. |

## Feature-level conclusion

### Confirmed strengths

- A background task scheduler exists (Enterprise/Ultimate tiers), supporting recurring tasks, automated schema backups, and database-to-database transfers without external orchestration tools.
- A dedicated headless CLI (`dbvr`) targets CI/CD automation use cases — conceptually similar to the `PROP-cli-automation` gap-close candidate already tracked in this repository's [Proposed Feature Registry](../../../../../feature-dictionary.md#proposed-feature-registry-research-pipeline) as a DBeaver-motivated competitive comparison point.

### Confirmed limitations

- Task Scheduler is gated to Enterprise/Ultimate tiers — not available in Community or Lite, where MongoDB support itself already requires Lite or above.
- No cron-expression support, timezone/DST handling, execution-config detail (batch size, retry, concurrency), notification channels, or task-status state machine is described in the source for DBeaver's scheduler — these are silent gaps, not confirmed absences, and are therefore omitted from this matrix.

### Open questions / unknowns

- Exact list of task types beyond "schema backups" and "database-to-database data transfers."
- Whether `dbvr` can trigger the same scheduled tasks the GUI scheduler manages, or is a fully separate automation surface.
- Cron/timezone/notification support — not discussed in the source in either direction.
