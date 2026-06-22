# VisuaLeaf — Data Import/Export Feature Matrix

| ID | Capability | Status | Detail | Source |
|---|---|---|---|---|
| IMP-001 | Export format: JSON | **confirmed** | Pretty-print optional; standard MongoDB Extended JSON | https://visualeaf.com/docs/task-manager |
| IMP-002 | Export format: CSV | **confirmed** | Configurable delimiters and headers | https://visualeaf.com/docs/task-manager |
| IMP-003 | Export format: BSON | **confirmed** | Native MongoDB BSON format; suitable for backup/restore | https://visualeaf.com/docs/task-manager |
| IMP-004 | Export format: SQL INSERT | **confirmed** | SQL INSERT statements; for relational database migration | https://visualeaf.com/docs/task-manager |
| IMP-005 | Import format: JSON | **confirmed** | Import from JSON file | https://visualeaf.com/docs/task-manager |
| IMP-006 | Import format: CSV | **confirmed** | Import from CSV file | https://visualeaf.com/docs/task-manager |
| IMP-007 | Import format: BSON | **confirmed** | Import from BSON file | https://visualeaf.com/docs/task-manager |
| IMP-008 | Import: Field mapping | **confirmed** | Map source field names to destination field names | https://visualeaf.com/docs/task-manager |
| IMP-009 | Import: Data transformations | **confirmed** | Type conversion, filtering, custom JS functions applied during import | https://visualeaf.com/docs/task-manager |
| IMP-010 | Import: Upsert mode | **confirmed** | Update existing documents or insert new ones based on match key | https://visualeaf.com/docs/task-manager |
| IMP-011 | Scheduling: One-Time | **confirmed** | Specific date/time execution | https://visualeaf.com/docs/task-manager |
| IMP-012 | Scheduling: Hourly | **confirmed** | Every hour at configured minute offset | https://visualeaf.com/docs/task-manager |
| IMP-013 | Scheduling: Daily | **confirmed** | Once per day at configured time | https://visualeaf.com/docs/task-manager |
| IMP-014 | Scheduling: Weekly | **confirmed** | Specific days of week at configured time | https://visualeaf.com/docs/task-manager |
| IMP-015 | Scheduling: Monthly | **confirmed** | Specific days of month at configured time | https://visualeaf.com/docs/task-manager |
| IMP-016 | Scheduling: Cron expression | **confirmed** | Full cron expression for advanced scheduling | https://visualeaf.com/docs/task-manager |
| IMP-017 | Scheduling: Timezone support | **confirmed** | Timezone-aware scheduling with automatic DST handling | https://visualeaf.com/docs/task-manager |
| IMP-018 | Task execution: Batch Size | **confirmed** | Default 1,000 documents per batch | https://visualeaf.com/docs/task-manager |
| IMP-019 | Task execution: Retry Count | **confirmed** | Default 3 retries on failure | https://visualeaf.com/docs/task-manager |
| IMP-020 | Task execution: Timeout | **confirmed** | Default 30 minutes per task | https://visualeaf.com/docs/task-manager |
| IMP-021 | Task execution: Concurrent Tasks limit | **confirmed** | Maximum 2 concurrent tasks | https://visualeaf.com/docs/task-manager |
| IMP-022 | Task execution: Keep History | **confirmed** | Default 100 execution records retained | https://visualeaf.com/docs/task-manager |
| IMP-023 | Monitoring: Real-time progress bars | **confirmed** | Live progress bars with document counts during execution | https://visualeaf.com/docs/task-manager |
| IMP-024 | Monitoring: Task status states | **confirmed** | States: Scheduled, Running, Completed, Failed, Paused | https://visualeaf.com/docs/task-manager |
| IMP-025 | Monitoring: Execution history | **confirmed** | History records with start/end times, duration, error logs | https://visualeaf.com/docs/task-manager |
| IMP-026 | Task action: Run Now | **confirmed** | Immediate ad-hoc execution of any scheduled task | https://visualeaf.com/docs/task-manager |
| IMP-027 | Task action: Pause / Resume | **confirmed** | Pause and resume scheduled tasks | https://visualeaf.com/docs/task-manager |
| IMP-028 | Task action: Edit | **confirmed** | Modify task configuration after creation | https://visualeaf.com/docs/task-manager |
| IMP-029 | Task action: Clone | **confirmed** | Duplicate an existing task configuration | https://visualeaf.com/docs/task-manager |
| IMP-030 | Task action: Delete | **confirmed** | Permanently remove a task | https://visualeaf.com/docs/task-manager |
| IMP-031 | Task action: View History | **confirmed** | Drill into execution history for a specific task | https://visualeaf.com/docs/task-manager |
| IMP-032 | Notifications: Email via SendGrid | **confirmed** | Requires user's own SendGrid account + API key; configured in Settings | https://visualeaf.com/docs/task-manager |
| IMP-033 | Notifications: In-App | **confirmed** | In-app notification on task lifecycle events | https://visualeaf.com/docs/task-manager |
| IMP-034 | Notification trigger: On Success | **confirmed** | Send notification when task completes successfully | https://visualeaf.com/docs/task-manager |
| IMP-035 | Notification trigger: On Failure | **confirmed** | Send notification when task fails | https://visualeaf.com/docs/task-manager |
| IMP-036 | Notification trigger: On Warning | **confirmed** | Send notification on task warning condition | https://visualeaf.com/docs/task-manager |
| IMP-037 | Transformation: Field Mapping | **confirmed** | Rename fields and restructure document shape on import | https://visualeaf.com/docs/task-manager |
| IMP-038 | Transformation: Data Type Conversion | **confirmed** | E.g., string → date conversion during import | https://visualeaf.com/docs/task-manager |
| IMP-039 | Transformation: Filtering | **confirmed** | Include/exclude documents by condition before import | https://visualeaf.com/docs/task-manager |
| IMP-040 | Transformation: Custom JavaScript functions | **confirmed** | User-defined JS transform functions applied per document | https://visualeaf.com/docs/task-manager |
| IMP-041 | Transformation: Aggregation Pipeline pre-export | **confirmed** | Apply $pipeline stages as server-side pre-export transform | https://visualeaf.com/docs/task-manager |
| IMP-042 | Plan: Community — 0 tasks | **confirmed** | Community (free) plan allows no import/export tasks | https://visualeaf.com/docs/task-manager |
| IMP-043 | Plan: Basic — up to 2 tasks | **confirmed** | Basic plan allows a maximum of 2 tasks | https://visualeaf.com/docs/task-manager |
| IMP-044 | Plan: Professional — unlimited tasks | **confirmed** | Professional plan has no task count limit | https://visualeaf.com/docs/task-manager |

## Navigation

- [← Product Report](../../product-report.md)
- [Feature Report](feature-report.md)
- [← Indexing & Performance Matrix](../indexing-performance/feature-matrix.md)
- [→ Visual Schema Matrix](../visual-schema/feature-matrix.md)
- [→ Shell Matrix](../shell/feature-matrix.md)
- [→ AI Assistant Matrix](../ai-assistant/feature-matrix.md)
- [→ Security & Governance Matrix](../security-governance/feature-matrix.md)
