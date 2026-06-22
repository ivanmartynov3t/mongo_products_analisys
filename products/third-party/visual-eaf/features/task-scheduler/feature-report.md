# Feature Report — VisuaLeaf / Task Scheduler

## Navigation

- [← Product Report](../../product-report.md)
- [Feature Matrix](feature-matrix.md)
- [← Data Transfer Matrix](../data-transfer/feature-matrix.md)
- [→ Governance Matrix](../governance/feature-matrix.md)

## Summary

VisuaLeaf's Task Scheduler provides full automation for import/export tasks with 6 schedule types (One-Time, Hourly, Daily, Weekly, Monthly, Cron expression), timezone-aware scheduling with automatic DST handling, and configurable execution parameters (batch size, retry count, timeout, concurrency limit, execution history retention). It offers real-time progress monitoring via live progress bars, complete task lifecycle management (run/pause/resume/edit/clone/delete), and email/in-app notifications via SendGrid integration. Task types cover all supported import (JSON/CSV/BSON) and export (JSON/CSV/BSON/SQL INSERT) formats from the Data Transfer feature.

## Strengths

- **6 schedule types** including full cron expression support for advanced use cases
- **Timezone-aware with DST handling**: no manual offset adjustments needed
- **Configurable execution params**: batch size, retry count, timeout, concurrency, history retention all adjustable
- **Email + in-app notifications**: on Success, Failure, and Warning events
- **Task clone**: quickly duplicate existing configs for similar jobs
- **Per-task execution history**: start/end times, duration, and error logs retained (default 100 records)
- **Live progress monitoring**: document counts shown in real time during execution
- **Run Now**: ad-hoc immediate execution of any scheduled task

## Limitations

- **Community plan**: 0 tasks — no scheduling or automation available
- **Basic plan**: maximum 2 tasks
- **Max 2 concurrent tasks**: no horizontal scale-out beyond 2 parallel executions
- **Email requires own SendGrid account**: users must supply and manage their own SendGrid API key
- **Task types limited to import/export**: no shell script scheduling or arbitrary command execution documented
- **No cross-connection dependency chains** between tasks documented

## Plan requirements

| Plan | Task limit |
| --- | --- |
| Community (free) | 0 tasks |
| Basic | Up to 2 tasks |
| Professional | Unlimited |

## Source index

- S1: https://visualeaf.com/docs/task-manager
