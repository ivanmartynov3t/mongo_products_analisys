# Feature Report — Studio 3T / Task Scheduler

**Last reviewed:** 2026-07-31 — see [research findings](../../../../../research/studio-3t-desktop-review-2026/11-task-scheduler-findings.md)

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [High-level comparison](../../../../../reports/comparisons/high-level-product-comparison.md)

## Scope

This report covers Studio 3T's Task Scheduler: supported task types, schedule recurrence patterns, IntelliShell Script Tasks, and Data Compare & Sync — including setup, results visualization, sync operations, and scheduling integration. All capabilities require Pro/Base or Ultimate edition.

**Scope correction (2026-07-31):** `t3/taskmanager/RemoteAggregationTask.java` and `t3/taskmanager/LensApiClient.java` are **not** part of the desktop Task Scheduler covered by this report, despite living in a package named `t3.taskmanager` and despite the class name containing "Task." They implement a separate, one-shot "Save Aggregation to Remote 3T Lens Server" handoff action available from the Aggregation Editor's save menu (`AggregationComposite.addSaveToRemoteServerMenuItem()`), which POSTs a pipeline definition to a 3T Lens server's own task API and does not create, schedule, list, or monitor anything through `t3.tasks.TaskScheduleManager`/`Task.fromMap()`. Aggregation is not a `TaskType`. This capability is already documented under `AGG-save-load` in [Aggregation's feature-matrix.md](../aggregation/feature-matrix.md) — it is cross-referenced here only to prevent a future pass from miscategorizing it as Task Scheduler functionality.

## Behavioral walkthrough

Studio 3T's Task Scheduler is a unified scheduling plane that covers 13 concrete, independently schedulable task types (`t3/tasks/gui/TaskType.java`): Collection Import, CSV Import, JSON Import, SQL Import, BSON-folder Import, BSON-archive Import, Export, SQL Migration (SQL→MongoDB), SQL Migration (MongoDB→SQL), Reschema, Data Masking, Data Compare & Sync, and IntelliShell Script Task. Import is not a single task type — it splits into 6 separately schedulable concrete task classes (Collection/CSV/JSON/SQL/BSON-folder/BSON-archive), each independently configurable and schedulable. Rather than each operation type having its own ad-hoc execution model, all of them share the same scheduling infrastructure — six recurrence patterns, on-demand execution, and a unified task management UI.

The six recurrence patterns cover the practical range of data operations scheduling: Once (one-shot future execution), Daily (fixed time), Every (interval in minutes or hours), Weekly (specific weekdays), Monthly (specific days of month), and Custom (a combination mode supporting days of week AND/OR month, with a repeat interval within each day). The Custom pattern is the most flexible, but it is important not to overstate it: it is built from structured day-of-week/day-of-month/hour/minute pickers (`TaskScheduleEditor`, `DayButtonFactory`, `MonthDaysPad`, `WeekDaysPad`), not a free-form cron-expression text field. Internally, `CronLikePattern.java` implements a genuine cron-style range/list/step matcher that powers those structured fields — so the matching engine is cron-like, but there is no UI surface where a user can type a raw cron string (e.g. `0 */4 * * *`). Within that constraint, Custom can still express schedules like "every weekday and on the 15th of each month, every 4 hours between 06:00 and 22:00."

## Execution model — async, uncapped, no operational controls

Tasks are fired by `TaskScheduleManager`, a `Daemon3TThread` that polls once per minute and launches every matching task via `display.asyncExec(() -> task.execute(true))`. This is worth stating plainly rather than leaving implicit: **there is no concurrency cap, throttling, retry, or timeout mechanism at the scheduler level.** The code contains its own acknowledgment of this design: a comment directly on the firing path reads, verbatim, **"tasks are launched asynchronously, avalanche is possible."** This is a known, acknowledged design characteristic of the scheduler — not an oversight discovered by this audit. If several tasks share a trigger time (e.g., multiple daily tasks all set to 02:00), all of them fire concurrently with nothing in the scheduler holding any of them back.

Two further consequences follow directly from this design:

- **Missed ticks are skipped, not retried.** If the app is busy past a scheduled minute boundary, `TaskScheduleManager.executeTasks()` records a "Skipped execution" background operation for the missed tick rather than re-attempting the task afterward.
- **No scheduler-level execution configuration exists at all** — no batch-size, retry-count, timeout, or concurrent-task-limit fields were found anywhere in `t3/tasks/*.java` or `t3/taskmanager/*.java`. A per-task-type "stop on first error" flag exists for some import task types (e.g. `BSONFolderImportTask.isStopOnError()`), but that is an import-job-level option inherited from the manual import/export worker layer, not a scheduler-provided retry policy. Data Compare & Sync's own batch-size setting (default 1,000 docs, documented under `SCHED-compare-setup`) is likewise a DCS-specific option, not a general scheduler capability.

Execution status is also not persisted. There is no `TaskStatus`-style enum (`RUNNING`/`COMPLETED`/`FAILED`/`PAUSED`/`SCHEDULED`) on the `Task` object; the icon shown in the tasks tree is derived live at render time from static/derived conditions (invalid task file, license gate, broken connection reference, or a generic "ready" icon), not from a stored run-state. Each run does produce a transient `BackgroundOperation` with progress and document counts, visible in the app's background-operations sidebar while it runs — this is real and confirmed (`SCHED-progress`) — but it disappears once dismissed and is not a durable, queryable execution history. `Telemetry.INSTANCE.logTaskExecuted(...)` records an internal analytics event only, not a user-visible history. No email/SMTP or in-app notification code exists anywhere in `t3/tasks`, `t3/tasks/gui`, or `t3/taskmanager` — task completion, failure, or warning states are not communicated to the user outside of manually reopening the tasks tree. Nor is there a Pause/Resume action on a scheduled task (the only way to stop one firing is to remove its schedule or lose the licensing feature) or a "View History" action.

None of this should be read as the scheduler being unreliable — the core fire/poll/recurrence engine is stable and unchanged in the last 24 months of git history. The gap is specifically in *operational* controls (concurrency, retry, history, notifications, status tracking) layered on top of that engine, which do not exist for any task type today.

IntelliShell Script Tasks are the most developer-oriented task type. A single task contains multiple sequential script units, each specifying a connection/database, an embedded script or loaded .js file, and an output file path. Date/time placeholders in output file paths (e.g., `export_#today.json`) generate unique filenames per run — preventing older output from being overwritten and providing a natural audit trail of execution history. When testing a script task, the output viewer shows raw shell output alongside parsed Table, Tree, and JSON views.

Data Compare & Sync provides a structural comparison between any two MongoDB collections (across different connections, databases, or environments). The match strategy is configurable: default _id matching covers the common case; custom field matching (with multi-field support) covers use cases where _id is not the meaningful document identity. Batch size is configurable to manage memory and network load. The results color scheme (Yellow = differs, Green = source-only, Red = target-only) makes the comparison immediately scannable. The Multiple Matches tab surfaces data quality issues where the match field is not unique — a useful data quality signal in itself.

Sync operations are bidirectional and granular: copy document from source to target, copy document from target to source, copy a specific field from source to target, or copy a field the other way. In-place editing of individual cells in either source or target is also supported. Comparison results can be exported to CSV for external review or documentation. Data Compare & Sync jobs are schedulable, enabling recurring environment drift detection.

## Capability findings

| Capability ID | Finding | Impact |
| --- | --- | --- |
| TSK-001 | 13 concrete task types (import splitting into 6 separate types) in a single scheduling plane eliminates the need for separate scheduling mechanisms for each operation type. | Reduces operational complexity for teams running regular MongoDB maintenance workflows. |
| TSK-012 | The scheduler fires tasks asynchronously with no concurrency cap, retry policy, timeout, or execution-config surface — an intentional design choice ("avalanche is possible") rather than an oversight, but one with no configurability for users who need throttling. | Teams scheduling many tasks at overlapping trigger times should expect them to run fully in parallel; there is no built-in way to serialize or limit them. |
| TSK-013 | No persistent execution history, no status-state tracking, and no notifications (email or in-app) exist for scheduled runs — only a transient, dismissible progress indicator per run. | Operational visibility into whether a scheduled task succeeded, failed, or ran at all depends entirely on the user proactively reopening the tasks tree during or shortly after execution; there is no passive way to find out later. |
| TSK-007 | Custom recurrence (days of week AND/OR month + intra-day interval) covers complex enterprise scheduling patterns that other tools handle only via cron or external schedulers. | Eliminates the need to build or maintain external scheduling infrastructure for Studio 3T tasks. |
| TSK-008 | IntelliShell Script Tasks with sequential units and date/time placeholder filenames create a natural audit trail of script execution output without additional tooling. | Enables script-driven MongoDB maintenance with built-in output history. |
| TSK-009 | Data Compare & Sync's batch size configuration and field inclusion/exclusion prevent memory and network overload on large collection comparisons. | Makes cross-environment comparison practical for multi-million-document collections. |
| TSK-010 | Color-coded comparison results (Yellow/Green/Red) with a dedicated Multiple Matches tab surfaces both data drift and data quality issues (non-unique match fields) in a single view. | Dual-purpose: environment sync verification AND data quality diagnosis. |
| TSK-011 | Field-level (not just document-level) bidirectional sync operations allow surgical remediation of individual field differences without overwriting entire documents. | Reduces data loss risk compared to document-level overwrite sync strategies. |

## Constraints and risks

- All Task Scheduler capabilities require Pro/Base+ edition — the entire feature is unavailable to Free edition users.
- Automated sync execution on a schedule (as opposed to automated compare + manual sync) is **unknown/unverified** — scheduled compare jobs may require human review before sync.
- Data Compare & Sync using a non-unique match field will produce Multiple Matches results without preventing the comparison from running — users must be aware that match field uniqueness is their responsibility to verify.
- IntelliShell Script Tasks with embedded scripts run with the permissions of the configured connection; destructive operations in a script will execute without additional confirmation when run on schedule.
- Reschema and Data Masking scheduled tasks are in-place write operations — scheduling them incorrectly can cause irreversible data changes without the usual manual confirmation step.
- Minimum interval for the "Every N minutes" recurrence is **unknown/unverified** — very short intervals could cause performance issues on the MongoDB server.
- No concurrency cap exists between scheduled tasks — multiple tasks sharing a trigger time all fire in parallel ("avalanche is possible," per the code's own comment), with no scheduler-level batch size, retry, or timeout control to mitigate load spikes.
- No persistent execution history, status-state tracking, or notifications (email or in-app) exist — a failed or skipped scheduled run produces no durable record and no alert; discovering it requires the user to notice a missing or stale output on their own.
- There is no Pause/Resume action for a scheduled task; temporarily suspending one requires removing its schedule entirely (losing the recurrence configuration) rather than toggling it off and back on.

## Conclusion

The Task Scheduler is a genuine operational differentiator for Studio 3T in the Pro/Base+ and Ultimate tiers. Its combination of 13 concrete task types (import split across 6 types), six recurrence patterns, IntelliShell Script Task multi-unit sequencing, and Data Compare & Sync with field-level sync operations covers most MongoDB operational automation requirements without external tooling. The entire feature area being Pro/Base+-only is one barrier to adoption at the Free tier; the other, distinct from edition gating, is operational maturity — the scheduler has no concurrency control, retry policy, execution history, status tracking, or notifications, so it is best suited to lower-stakes or closely-watched automation rather than unattended, mission-critical scheduling today.
