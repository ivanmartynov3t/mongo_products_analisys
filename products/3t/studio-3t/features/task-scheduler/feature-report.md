# Feature Report — Studio 3T / Task Scheduler

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [High-level comparison](../../../../../reports/comparisons/high-level-product-comparison.md)

## Scope

This report covers Studio 3T's Task Scheduler: supported task types, schedule recurrence patterns, IntelliShell Script Tasks, and Data Compare & Sync — including setup, results visualization, sync operations, and scheduling integration. All capabilities require Pro/Base or Ultimate edition.

## Behavioral walkthrough

Studio 3T's Task Scheduler is a unified scheduling plane that covers seven distinct task types: Import Wizard, Export Wizard, Data Compare & Sync, Reschema, Data Masking, SQL Migration (both directions), and IntelliShell Script Tasks. Rather than each operation type having its own ad-hoc execution model, all of them share the same scheduling infrastructure — six recurrence patterns, on-demand execution, and a unified task management UI.

The six recurrence patterns cover the practical range of data operations scheduling: Once (one-shot future execution), Daily (fixed time), Every (interval in minutes or hours), Weekly (specific weekdays), Monthly (specific days of month), and Custom (a combination mode supporting days of week AND/OR month, with a repeat interval within each day). The Custom pattern is the most flexible — it can express schedules like "every weekday and on the 15th of each month, every 4 hours between 06:00 and 22:00."

IntelliShell Script Tasks are the most developer-oriented task type. A single task contains multiple sequential script units, each specifying a connection/database, an embedded script or loaded .js file, and an output file path. Date/time placeholders in output file paths (e.g., `export_#today.json`) generate unique filenames per run — preventing older output from being overwritten and providing a natural audit trail of execution history. When testing a script task, the output viewer shows raw shell output alongside parsed Table, Tree, and JSON views.

Data Compare & Sync provides a structural comparison between any two MongoDB collections (across different connections, databases, or environments). The match strategy is configurable: default _id matching covers the common case; custom field matching (with multi-field support) covers use cases where _id is not the meaningful document identity. Batch size is configurable to manage memory and network load. The results color scheme (Yellow = differs, Green = source-only, Red = target-only) makes the comparison immediately scannable. The Multiple Matches tab surfaces data quality issues where the match field is not unique — a useful data quality signal in itself.

Sync operations are bidirectional and granular: copy document from source to target, copy document from target to source, copy a specific field from source to target, or copy a field the other way. In-place editing of individual cells in either source or target is also supported. Comparison results can be exported to CSV for external review or documentation. Data Compare & Sync jobs are schedulable, enabling recurring environment drift detection.

## Capability findings

| Capability ID | Finding | Impact |
| --- | --- | --- |
| TSK-001 | Seven task types in a single scheduling plane eliminates the need for separate scheduling mechanisms for each operation type. | Reduces operational complexity for teams running regular MongoDB maintenance workflows. |
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

## Conclusion

The Task Scheduler is a genuine operational differentiator for Studio 3T in the Pro/Base+ and Ultimate tiers. Its combination of seven task types, six recurrence patterns, IntelliShell Script Task multi-unit sequencing, and Data Compare & Sync with field-level sync operations covers most MongoDB operational automation requirements without external tooling. The entire feature area being Pro/Base+-only is the main barrier to adoption at the Free tier.
