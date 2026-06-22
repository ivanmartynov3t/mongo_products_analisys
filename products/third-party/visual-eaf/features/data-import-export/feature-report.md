# VisuaLeaf — Data Import/Export Feature Report

## Summary

VisuaLeaf's Task Manager provides a full data pipeline scheduling system for import and export operations. Supported export formats are JSON (pretty-print optional), CSV (configurable delimiters), BSON, and SQL INSERT statements. Import accepts JSON, CSV, and BSON. Tasks can be scheduled with cron-level granularity (One-Time, Hourly, Daily, Weekly, Monthly, raw cron expression), with DST-aware timezone support. Custom JavaScript transformations, field mapping, type conversion, aggregation pipeline pre-processing, and upsert mode are confirmed. Email notifications via SendGrid (user-supplied API key) and in-app notifications complete the monitoring stack. Community plan: 0 tasks; Basic: up to 2 tasks; Professional: unlimited.

---

## Strengths

- **SQL INSERT export:** Enables relational migration workflows without requiring separate ETL tooling.
- **Full cron scheduling:** One-Time, Hourly, Daily, Weekly, Monthly, and raw cron expression — matches the scheduling flexibility of dedicated ETL tools.
- **DST-aware timezone handling:** Critical for scheduled tasks that cross daylight saving time boundaries; prevents clock-shift data gaps.
- **Custom JavaScript transforms:** User-defined per-document JS functions allow arbitrary field transformation during import.
- **Aggregation pipeline as pre-export transform:** Server-side transformation before export — efficient for large collections.
- **Upsert mode:** Import can update existing or insert new — supports incremental sync patterns without duplicating data.
- **Comprehensive task lifecycle:** Run Now, Pause, Resume, Edit, Clone, Delete, View History — full task management without a separate scheduler.
- **User-controlled SendGrid integration:** Users bring their own SendGrid API key — no external SozoCode dependency for email delivery; privacy-preserving.

---

## Limitations / Gaps

- **Community plan: zero tasks:** Import/export workflows completely unavailable on the free tier.
- **Basic plan: 2-task cap:** Severely limits automated pipeline workflows for Basic subscribers.
- **Max 2 concurrent tasks (all plans):** Hard concurrency ceiling; no parallelism for bulk or time-sensitive operations.
- **SendGrid only for email:** No SMTP, AWS SES, or other email provider; users without SendGrid accounts lose email notifications.
- **No import from URL or API endpoint:** Import is file-based only; no HTTP source, S3, or database-to-database pull documented.
- **No export to cloud storage:** No S3, GCS, or Azure Blob export destination documented.
- **SQL INSERT dialect unspecified:** Whether SQL output targets MySQL, PostgreSQL, or generic SQL is **unknown/unverified**.

---

## Comparison Notes (vs MongoDB Compass baseline)

| Aspect | VisuaLeaf | MongoDB Compass |
|---|---|---|
| Export formats | JSON, CSV, BSON, SQL INSERT | JSON, CSV, BSON |
| Import formats | JSON, CSV, BSON | JSON, CSV, BSON |
| Scheduled tasks | **confirmed** (cron-level) | not available |
| Custom JS transforms | **confirmed** | not available |
| Upsert mode | **confirmed** | not available |
| Field mapping on import | **confirmed** | not available |
| Email notifications | **confirmed** (SendGrid) | not available |
| Pre-export aggregation pipeline | **confirmed** | not available |
| Community plan support | 0 tasks | full import/export (ad-hoc) |
| Concurrent task limit | 2 | N/A (ad-hoc only) |
| Task history / audit log | **confirmed** (100 records) | not available |

---

## Navigation

- [← Product Report](../../product-report.md)
- [Feature Matrix](feature-matrix.md)
- [← Indexing & Performance](../indexing-performance/feature-report.md)
- [→ Visual Schema Designer](../visual-schema/feature-report.md)
- [→ MongoDB Shell](../shell/feature-report.md)
- [→ AI Assistant](../ai-assistant/feature-report.md)
- [→ Security & Governance](../security-governance/feature-report.md)
