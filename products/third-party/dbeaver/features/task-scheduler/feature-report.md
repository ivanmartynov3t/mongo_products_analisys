# Feature Report — DBeaver / Task Scheduler

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Scope

- Feature name: Task Scheduler (partial)
- Feature ID: F-SCHED (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Product: DBeaver
- Product group: third-party
- Analysis date: 2026-09-04

## Behavioral walkthrough

DBeaver's Task Management and Automation Scheduler is a background process manager, available only in Enterprise and Ultimate tiers, that can run recurring database tasks — the research file names automated schema backups and database-to-database data transfers as examples, framed as replacing external orchestration tools like cron or Airflow. Separately, DBeaver ships a terminal-first headless CLI (`dbvr`) that lets developers run database operations, data-export tasks, and schema migrations from CI/CD pipelines without the GUI.

Neither capability is described with the granularity this repository's dictionary tracks for other products (cron expressions, timezone/DST handling, retry/batch execution config, notification channels, task-status state machines) — the source simply asserts the scheduler and the CLI exist and names a few example use cases, so this feature area's matrix is intentionally short.

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| SCHED-task-types, SCHED-plan-limits | Task scheduler exists but is gated to Enterprise/Ultimate tiers. | Compounds DBeaver's tiered-MongoDB-access model: MongoDB itself needs Lite+, and task automation needs a further step up to Enterprise/Ultimate. | Research file narrative + licensing pages |
| SCHED-cli-headless | Standalone `dbvr` CLI for CI/CD-driven database operations, exports, and migrations. | Positions DBeaver in the same headless-automation competitive space this repository already tracks via `PROP-cli-automation` (Gap-Close vs. DBeaver Pro/Ultimate) in the Proposed Feature Registry. | Research file narrative only — no primary source cited |

## Constraints and risks

- Every claim in this feature area rests solely on the secondary research file's narrative; none is tied to a specific DBeaver documentation page in its own Works Cited list, so all rows are marked Unverified rather than Confirmed.
- Do not infer cron-expression support, timezone awareness, or notification channels — none of these is discussed in either direction for DBeaver.

## Interactions and dependencies

- This repository's [Proposed Feature Registry](../../../../../feature-dictionary.md#proposed-feature-registry-research-pipeline) already references DBeaver Pro/Ultimate as the named competitor for `PROP-cli-automation` (Headless CLI / CI-CD pipeline automation) — this feature report's `SCHED-cli-headless` finding is the underlying evidence for that registry entry.
- Depends on [F-CONN](../connectivity/feature-report.md)'s paid-tier MongoDB connectivity gate.

## Conclusions

### Strengths

- Background task scheduler with recurring-task support, framed as an internal alternative to cron/Airflow.
- Dedicated headless CLI (`dbvr`) for CI/CD automation.

### Limitations

- Both scheduler and (implicitly) its richer automation features are gated to Enterprise/Ultimate tiers.
- No cron, timezone, notification, or execution-config detail is documented.

### Unknowns

- Full task-type catalog beyond the two named examples.
- Whether `dbvr` and the GUI scheduler share the same task definitions or are independent automation paths.
