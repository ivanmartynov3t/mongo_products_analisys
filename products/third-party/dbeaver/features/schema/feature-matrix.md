# Feature Matrix — DBeaver / Schema

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: DBeaver
- Product group: third-party
- Feature ID: F-SCHEMA (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `schema`
- Analysis date: 2026-09-04
- Version/release context: DBeaver 25.x–26.x line

## Source index

- S1: DBeaver Competitive Intelligence Analysis (secondary research file), `research/google_research/dbeaver-competitive-intelligence-analysis/DBeaver Competitive Intelligence Analysis.md`
- S2: When using MongoDB, the grid view fails to correctly display the millisecond portion of Date values · Issue #40165 - GitHub, https://github.com/dbeaver/dbeaver/issues/40165 (S1 Works Cited #12)
- S3: MongoDB quick filter by Timestamp · Issue #8914 - GitHub, https://github.com/dbeaver/dbeaver/issues/8914 (S1 Works Cited #31)
- S4: Cannot delete or edit and update MongoDB records · Issue #1171 - GitHub, https://github.com/dbeaver/dbeaver/issues/1171 (S1 Works Cited #13)
- S5: Schema compare | DBeaver Documentation, https://dbeaver.com/docs/dbeaver/Schema-compare/ (S1 Works Cited #30)

## Capability matrix (low-level)

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SCHEMA-sampling | Sampling config | Not supported (confirmed absent, per contrast) | S1 describes DBeaver's schema view as "Generic column listing metadata," explicitly contrasted against Studio 3T's sampling-based "Schema Explorer with Field Type Distribution." No sample-mode/sample-count/query-filter controls are described for DBeaver. | — | Not planned | S1 | Confirmed-absent by direct contrast in the source's own comparison table, not merely unmentioned. |
| SCHEMA-field-prob | Field probability | Not supported (confirmed absent, per contrast) | Same comparison row as above; DBeaver's column listing does not include per-field presence-probability statistics. | — | Not planned | S1 | — |
| SCHEMA-type-prob | Type probabilities | Not supported (confirmed absent, per contrast) | Same comparison row; no per-field/per-type breakdown described for DBeaver. | — | Not planned | S1 | — |
| SCHEMA-bson-types | BSON type coverage | Confirmed limitation | S1: "DBeaver's underlying JDBC data rendering pipeline often maps native BSON types into generic Java primitives. This conversion can drop microsecond/millisecond precision on ISODate objects or misinterpret 12-byte BSON ObjectId strings during update or delete operations." Backed by three specific GitHub issues. | Affects date-typed fields (millisecond truncation) and ObjectId-typed fields (misinterpretation causing failed writes). | Not planned (open issues as of source analysis date) | S1, S2, S3, S4 | This is the single most concretely evidenced finding in the entire DBeaver research file — three distinct, primary-sourced GitHub issues. |

Note: DBeaver's schema/structure *compare* capability (relational-DDL-oriented, reported to struggle with nested BSON) is tracked under `GOV-collection-compare` in the [Governance & Security feature matrix](../governance/feature-matrix.md) — the dictionary places collection/schema comparison under F-GOV, not F-SCHEMA, so it is not duplicated here.

## Feature-level conclusion

### Confirmed strengths

- None — the source frames DBeaver's schema tooling as a generic, relational-oriented capability with no MongoDB-specific analytics.

### Confirmed limitations

- No sampling-based schema analysis (field probability, type probability, histograms) — DBeaver's schema view is generic JDBC column-metadata listing, explicitly and directly contrasted against Studio 3T's richer schema explorer in the source's own comparison table.
- Three independently filed, primary-sourced GitHub issues document BSON type-fidelity bugs: millisecond/microsecond date-precision truncation (#40165), quick-filter failures on timestamp fields due to BSON ISODate formatting errors (#8914), and ObjectId misinterpretation causing failed update/delete operations (#1171).
- Schema/structure comparison is relational-DDL-oriented and, per the source's own (unverified-by-us) assessment, struggles with nested BSON arrays/documents.

### Open questions / unknowns

- Whether any of the three cited GitHub issues have since been fixed in a release after the source's analysis date is not stated.
- Whether DBeaver offers any schema validation ($jsonSchema) authoring or deployment workflow for MongoDB — not discussed in the source at all, and therefore omitted from this matrix rather than marked absent.
