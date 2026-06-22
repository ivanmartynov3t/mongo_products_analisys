# Feature Matrix — VisuaLeaf / Task Scheduler

## Navigation

- [← Product Report](../../product-report.md)
- [Feature Report](feature-report.md)
- [← Data Transfer Matrix](../data-transfer/feature-matrix.md)
- [→ Governance Matrix](../governance/feature-matrix.md)

## Source index

- S1: https://visualeaf.com/docs/task-manager

## Capability matrix

| Sub-feature ID | Capability | Status | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| SCHED-task-types | Task types | confirmed | Import tasks (JSON/CSV/BSON) and export tasks (JSON/CSV/BSON/SQL INSERT); configured and saved from the Data Transfer feature. | — | confirmed | S1 |
| SCHED-types-time | Schedule types | confirmed | One-Time: specific date/time execution. Hourly: every hour at configured minute offset. Daily: once per day at configured time. Weekly: specific days of week at configured time. Monthly: specific days of month at configured time. | — | confirmed | S1 |
| SCHED-cron | Cron expression support | confirmed | Full cron expression for advanced scheduling beyond the 5 preset schedule types. | — | confirmed | S1 |
| SCHED-timezone | Timezone-aware scheduling | confirmed | Timezone-aware scheduling with automatic DST handling. | — | confirmed | S1 |
| SCHED-exec-config | Execution configuration | confirmed | Batch Size: default 1,000 documents per batch. Retry Count: default 3 retries on failure. Timeout: default 30 minutes per task. Concurrent Tasks limit: maximum 2 concurrent tasks. Keep History: default 100 execution records retained. | — | confirmed | S1 |
| SCHED-progress | Real-time progress monitoring | confirmed | Live progress bars with document counts during execution. | — | confirmed | S1 |
| SCHED-status-states | Task status states | confirmed | States: Scheduled, Running, Completed, Failed, Paused. | — | confirmed | S1 |
| SCHED-history-retention | Execution history retention | confirmed | History records per task include start/end times, duration, and error logs. Default 100 execution records retained per task (configured via Keep History). | — | confirmed | S1 |
| SCHED-actions | Task lifecycle actions | confirmed | Run Now: immediate ad-hoc execution of any scheduled task. Pause/Resume: suspend and resume scheduled tasks. Edit: modify task configuration after creation. Clone: duplicate an existing task configuration. Delete: permanently remove a task. View History: drill into execution history for a specific task. | — | confirmed | S1 |
| SCHED-notifications | Notifications | confirmed | Email via SendGrid: requires user's own SendGrid account + API key; configured in Settings. In-app notifications. Triggers: On Success, On Failure, On Warning. | Requires own SendGrid account and API key for email | confirmed | S1 |
