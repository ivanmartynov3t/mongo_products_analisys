# Feature Matrix — Navicat / Task Scheduler

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: Navicat
- Product group: third-party
- Feature ID: F-SCHED (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `task-scheduler`
- Analysis date: 2026-09-04
- Version/release context: Navicat 17 line

## Source index

- S1: Navicat Competitive Intelligence Analysis (secondary research file), `research/google_research/navicat-competitive-intelligence-analysis/Navicat Competitive Intelligence Analysis.md`

## Capability matrix (low-level)

Navicat's Structure Synchronization and Data Synchronization engines (see [F-GOV](../governance/feature-matrix.md) for their primary detail) are cross-referenced here for their scheduling/automation angle, since the source's Feature Inventory explicitly names "data synchronization" as one of the batch-operation types the integrated task scheduler executes.

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SCHED-task-types | Task types | Confirmed | S1 (Feature Inventory): "Job Automation and Scheduling: Integrated task scheduler executing batch operations for data transfers, data synchronization, backups, map-reduce tasks, and automated report generation." Also (Automation, Backup, and Synchronization section): "Administrators can link sequential operations—such as executing an aggregation pipeline, transferring output data to a target database, exporting results to Excel, and emailing generated reports—into automated workflows triggered by system schedules." | — | Unverified | S1 | The "link sequential operations…into automated workflows" description (composite/chained multi-step jobs) does not have a dedicated dictionary ID of its own; folded into this row's Detailed behavior as the closest fit rather than minting a new ID for one description. |
| SCHED-history-retention | History retention | Confirmed (existence, backups specifically) | S1: "Backup tasks can be encrypted, compressed, and assigned automated retention policies using the scheduler." | Confirmed specifically for backup tasks; retention policy scope for other task types (transfer, sync, map-reduce) not stated. | Unverified | S1 | — |
| SCHED-notifications | Notifications | Confirmed (existence); imperfect fit (report delivery vs. status alerts) | S1: "...emailing generated reports..." as one linked step in an automated workflow. | This is email delivery of a generated report artifact, not a success/failure/warning task-status notification as the dictionary description implies. | Unverified | S1 | Imperfect-fit mapping flagged explicitly: the dictionary's `SCHED-notifications` describes "Email and in-app notifications on success, failure, warning," while Navicat's confirmed capability is emailing a report as a workflow output step. Included as the closest existing ID rather than left unmapped. |
| SCHED-compare-setup | Compare setup | Confirmed | S1 (Structure Synchronization): "Compares DDL and schema definitions across database instances. It identifies structural variances across collections, indexes, views, and validation constraints..." | — | Unverified | S1 | Cross-referenced from `GOV-collection-compare` in [F-GOV](../governance/feature-matrix.md); listed here for the setup-workflow angle. |
| SCHED-compare-results | Compare results | Confirmed | S1: both Structure Synchronization ("producing exact alteration scripts") and Data Synchronization ("generating preview scripts") describe result/diff presentation prior to execution. | — | Unverified | S1 | — |
| SCHED-compare-sync | Compare sync actions | Confirmed | S1 (Data Synchronization): "...generating preview scripts or executing direct synchronization to reconcile data drift." | — | Unverified | S1 | Cross-referenced from `GOV-collection-sync` in [F-GOV](../governance/feature-matrix.md). |
| SCHED-compare-schedule | Compare schedule save | Confirmed (Data Synchronization); Unverified (Structure Synchronization) | S1 (Feature Inventory): "Integrated task scheduler executing batch operations for data transfers, **data synchronization**, backups, map-reduce tasks, and automated report generation." | Structure Synchronization is not explicitly named in this scheduler bullet — only "data synchronization" is. | Unverified (Structure Sync scope) | S1 | Data Synchronization's schedulability is directly confirmed by name; Structure Synchronization's is inferred, not stated, since it is absent from this specific enumeration. |
| SCHED-cron | Cron expression | Unverified | Not discussed — S1 describes "automated workflows triggered by system schedules" without itemizing cron-expression support versus simpler recurrence presets. | — | Unverified | S1 | — |
| SCHED-plan-limits | Scheduler plan limits | Unverified | Not discussed — no tier/edition gating is mentioned for the Automation/Task Scheduler module specifically (contrast with DBeaver, whose scheduler is confirmed Enterprise/Ultimate-only). | — | Unverified | S1 | — |
| SCHED-cli-headless | Headless CLI automation | Unverified | Not discussed anywhere in the source — no standalone command-line/headless automation utility is described for Navicat (contrast with DBeaver's `dbvr`). | — | Unverified | S1 | Included as a row because this dictionary ID was added specifically for this cross-product effort (2026-09-04); Navicat's source gives no evidence either way. |

## Feature-level conclusion

### Confirmed strengths

- An integrated Automation module that chains sequential, heterogeneous operations (aggregation pipeline execution, cross-database data transfer, Excel export, report emailing) into a single scheduled workflow — a materially richer composite-job model than a single-task-type scheduler.
- Backup tasks specifically support encryption, compression, and automated retention policies via the scheduler.
- Both Structure Synchronization and Data Synchronization produce preview/alteration scripts before executing, and Data Synchronization is explicitly named among the task scheduler's batch-operation types.

### Confirmed limitations

- No cron-expression support, timezone/DST handling, execution-config detail (batch size, retry count, concurrent task limit), or task-status state machine (Scheduled/Running/Completed/Failed/Paused) is described in the source for Navicat's scheduler — these are silent gaps, not confirmed absences.
- No tier/edition gating is mentioned for the Automation module, unlike DBeaver's confirmed Enterprise/Ultimate-only scheduler — but this could equally reflect the source simply not discussing pricing-tier boundaries for this specific module rather than confirming universal availability.
- No standalone headless CLI automation utility (a `dbvr`-equivalent) is described anywhere in the source.

### Open questions / unknowns

- Whether Structure Synchronization (as opposed to the explicitly-named Data Synchronization) can itself be saved as a recurring scheduled task, or is triggered only ad hoc.
- Cron/timezone/notification-channel support and exact execution-configuration knobs (batch size, retry, concurrency) — not discussed in the source in either direction.
- Whether the Automation module is gated to any specific Navicat edition or tier.
