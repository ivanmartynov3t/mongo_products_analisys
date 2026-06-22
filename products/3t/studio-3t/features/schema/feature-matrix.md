# Feature Matrix — Studio 3T / Schema

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Source index

- S1: https://studio3t.com/knowledge-base/articles/schema/
- S2: https://studio3t.com/knowledge-base/articles/create-mongodb-view/

## Capability matrix

| Capability ID | Capability | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SCHEMA-sampling | Sample configuration | Supported | Sample mode: Random, First, Last, All. Configurable sample document count. "Omit individual array elements" checkbox (default: on — avoids inflating element-level statistics). Query criteria filter on sample (analyze a subset matching a query). | "All" mode on large collections is resource-intensive and may time out. | confirmed | S1 | All editions. |
| SCHEMA-field-prob | Schema tree — field probability | Supported | All discovered fields displayed with probability as a percentage of sampled documents containing that field. Surfaces sparse and inconsistently-present fields at a glance. | Probability is relative to sample size, not the full collection, unless mode = All. | confirmed | S1 | All editions. |
| SCHEMA-type-prob | Schema tree — per-field type probabilities | Supported | Each field shows all discovered BSON types with individual type probabilities (e.g., String 80%, Null 15%, Int32 5%). Reveals polymorphic fields that may cause application type errors. | Type probabilities are relative to documents in the sample containing that field. | confirmed | S1 | All editions. |
| SCHEMA-explore-docs | Right-click explore on schema fields | Supported | Right-click any field in the schema tree: "Explore documents containing selected field" or "Explore documents not containing selected field" — opens Collection Tab with the corresponding query pre-built ({field: {$exists: true/false}}). | Requires an open Collection Tab connection. | confirmed | S1 | All editions. |
| SCHEMA-histogram | Value Histogram (numeric fields) | Supported | Frequency histogram of most common numeric values in the sample. Surfaces value distribution and outlier spikes. | Histogram represents sample; rare values in the full collection may not appear. | confirmed | S1 | All editions. |
| SCHEMA-top-values | Top Values chart (string and mixed fields) | Supported | Frequency chart of top string values in the sample. Surfaces high-cardinality vs low-cardinality fields; reveals anomalies like unexpected null strings or typos. | Limited to top N values — long tail not visible in chart. | confirmed | S1 | All editions. |
| SCHEMA-date-dist | Date distribution visualizations | Supported | Date fields show four distribution breakdowns: hourly, daily, monthly, weekly, and all-time. Useful for time-series density analysis and detecting ingestion gaps. | Only available for fields with confirmed Date BSON type. | confirmed | S1 | All editions. |
| SCHEMA-stats-notes | Statistics and Comments tabs | Supported | Statistics tab shows numeric statistics per field. Comments tab allows annotating fields with notes (stored locally in Studio 3T). | Comments are not stored in MongoDB; they are local to the Studio 3T installation. | confirmed | S1 | All editions. |
| SCHEMA-doc-export | Documentation export | Supported | "Generate documentation" button exports schema documentation to Word (.docx) or CSV. Includes field names, types, probabilities, and statistics. | Requires write access to the target file system location. | confirmed | S1 | All editions. |
| SCHEMA-rename-discover | Rename-on-discover workflow | Supported | Right-click outlier field variant in schema tree → "Explore documents containing selected field" → right-click a value in result → "Rename Field" → "All documents in collection". Enables bulk field rename triggered directly from schema analysis. | Rename Field is a write operation; requires write access to the collection. | confirmed | S1 | All editions. |
| SCHEMA-view-editor | View Editor — db.createView() | Supported | Visual pipeline builder (same UI as Aggregation Editor stages) wrapped in a db.createView() call. $match stage pre-added. Any further aggregation stages can be added. | Requires MongoDB ≥ 3.4. Requires write access to the database. | confirmed | S2 | All editions. |
| SCHEMA-view-from-sql | View creation from SQL Query or Aggregation Editor | Supported | Create view from SQL Query via Query Code tab → paste pipeline. Create from Aggregation Editor via Save → "Create view from aggregate query". Both paths share the same View Editor. | SQL Query creation path requires Pro/Base+ edition. | confirmed | S2 | View Editor: all editions. SQL path: Pro/Base+. |
| SCHEMA-views-tree | Views in Connection Tree | Supported | Created views appear under the source database in the Connection Tree in a dedicated "Views" folder. Views are first-class queryable objects in Studio 3T (Collection Tab, Export, etc.). | Views reflect the pipeline definition; query performance depends on the underlying collection's indexes. | confirmed | S2 | All editions. |
