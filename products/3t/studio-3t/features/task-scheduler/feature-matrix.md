# Feature Matrix — Studio 3T / Task Scheduler

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Source index

- S1: https://studio3t.com/knowledge-base/articles/automate-schedule-mongodb-tasks/
- S2: https://studio3t.com/knowledge-base/articles/intellishell-script-tasks/
- S3: https://studio3t.com/knowledge-base/articles/data-compare-and-sync/

## Capability matrix

| Capability ID | Capability | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SCHED-task-types | Supported task types | Supported (Pro/Base+) | Seven task types schedulable: (1) Import Wizard, (2) Export Wizard, (3) Data Compare & Sync, (4) Reschema, (5) Data Masking, (6) SQL Migration (both SQL→MongoDB and MongoDB→SQL), (7) IntelliShell Script Tasks. Tasks can also be run on-demand outside the schedule. | Requires Pro/Base+ edition. All seven task types require the same Pro/Base+ gate. | confirmed | S1 | Pro/Base+ only. |
| SCHED-recur-once | Schedule recurrence — Once | Supported (Pro/Base+) | Single future execution at a specific date + time. | Requires Pro/Base+ edition. | confirmed | S1 | Pro/Base+ only. |
| SCHED-recur-daily | Schedule recurrence — Daily | Supported (Pro/Base+) | Every day at a specified HH:MM time. Optional end date. | Requires Pro/Base+ edition. | confirmed | S1 | Pro/Base+ only. |
| SCHED-recur-interval | Schedule recurrence — Every (interval) | Supported (Pro/Base+) | Every N minutes or every N hours. Configurable start date+time and optional end date+time. | Requires Pro/Base+ edition. Minimum interval value is unverified. | confirmed | S1 | Pro/Base+ only. |
| SCHED-recur-weekly | Schedule recurrence — Weekly | Supported (Pro/Base+) | Specific days of week (checkbox selection) + time. Configurable start and end date. | Requires Pro/Base+ edition. | confirmed | S1 | Pro/Base+ only. |
| SCHED-recur-monthly | Schedule recurrence — Monthly | Supported (Pro/Base+) | Specific days of month (numeric selection) + time. Configurable start and end date. | Requires Pro/Base+ edition. | confirmed | S1 | Pro/Base+ only. |
| SCHED-cron | Schedule recurrence — Custom | Supported (Pro/Base+) | Combine: days of week AND/OR specific days of month + repeat interval within a day. Configurable start and end date. Most flexible recurrence option for complex schedules (e.g., weekdays + 15th of month, every 4 hours between 06:00–22:00). | Requires Pro/Base+ edition. | confirmed | S1 | Pro/Base+ only. |
| SCHED-script-tasks | IntelliShell Script Tasks | Supported (Pro/Base+) | Multiple sequential script units per task. Each unit: (1) source connection/database, (2) embedded script or loaded .js file from disk, (3) target output file path. Filename placeholders for date/time generate unique output filenames per run (e.g., export_#today.json). Raw shell output + parsed Table/Tree/JSON views available when testing. | Requires Pro/Base+ edition. mongosh binary must be accessible. | confirmed | S2 | Pro/Base+ only. |
| SCHED-compare-setup | Data Compare & Sync — setup | Supported (Pro/Base+) | Source and target: any two MongoDB connections (including same connection, different databases). Drag entire database to compare all its collections, or drag individual collections. Match on: _id (default) or custom field(s) (must be unique; indexed is recommended). Batch size (default 1,000 docs per batch). Number type equality toggle (treat Int32 = Int64 etc.). Field inclusion/exclusion list. Filter criteria (compare a subset of documents). Projection (limit which fields are compared). | Requires Pro/Base+ edition. Custom match field must be unique; non-unique match fields produce results in the Multiple Matches tab. | confirmed | S3 | Pro/Base+ only. |
| SCHED-compare-results | Data Compare & Sync — results view | Supported (Pro/Base+) | Results Overview tab: comparison duration, total documents analyzed, identical count, differing count. Color scheme: Yellow = field or document differs, Green = in source only, Red = in target only, Normal = identical. Multiple Matches tab: documents where match field matched more than one record. | Requires Pro/Base+ edition. | confirmed | S3 | Pro/Base+ only. |
| SCHED-compare-sync | Data Compare & Sync — sync operations | Supported (Pro/Base+) | Bidirectional sync: copy document to target, copy document to source, copy field to target, copy field to source. Double-click any cell for in-place edit in either source or target. Export comparison results to CSV file. | Requires Pro/Base+ edition. Sync operations are write operations; require write access to the target. | confirmed | S3 | Pro/Base+ only. |
| SCHED-compare-schedule | Data Compare & Sync — scheduling | Supported (Pro/Base+) | Data Compare & Sync jobs can be saved as tasks and scheduled via the Task Scheduler using any recurrence pattern. | Requires Pro/Base+ edition. Scheduled compare jobs produce results that must be reviewed; automated sync on schedule is not explicitly confirmed. | confirmed | S3 | Pro/Base+ only. Automated sync on schedule: unverified. |
