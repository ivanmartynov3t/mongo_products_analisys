# Feature Report — DBeaver / Schema

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Scope

- Feature name: Schema (partial)
- Feature ID: F-SCHEMA (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Product: DBeaver
- Product group: third-party
- Analysis date: 2026-09-04

## Behavioral walkthrough

DBeaver's schema view for a MongoDB collection is generic JDBC column-metadata listing — the same view it presents for a relational table — rather than a sampling-driven schema analyzer. The research file's own MongoDB capability comparison table contrasts this directly against Studio 3T's "Schema Explorer with Field Type Distribution," describing DBeaver's equivalent as "Generic column listing metadata."

The most concretely evidenced finding for this feature area is not a missing capability but an active data-fidelity bug class: DBeaver's JDBC rendering pipeline maps native BSON types into generic Java primitives, which can (a) drop millisecond/microsecond precision on `ISODate` values, and (b) misinterpret 12-byte BSON `ObjectId` values as other types. Three separate GitHub issues, each cited as a primary source in the research file's own Works Cited list, document concrete symptoms: a grid-view display bug truncating date milliseconds to `.000` (#40165), a quick-filter failure on timestamp fields throwing `DBCException: Unsupported value` (#8914), and `WriteResult{n=0}` failures on document edits because DBeaver misinterprets custom string identifiers as standard ObjectId types (#1171).

DBeaver also has a schema/structure "compare" capability (documented at `dbeaver.com/docs/dbeaver/Schema-compare/`), but it is relational-DDL-oriented; the research file's own assessment (not independently re-verified here) is that it struggles with nested BSON arrays and documents. That capability is tracked as `GOV-collection-compare` in the [Governance & Security feature matrix](../governance/feature-matrix.md), the dictionary's home for cross-collection/schema comparison.

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| SCHEMA-sampling / SCHEMA-field-prob / SCHEMA-type-prob | No sampling-based schema analytics; generic column-metadata listing only. | Confirmed-absent by direct contrast in the source's own MongoDB capability table (not merely unmentioned). | Research file narrative (MongoDB Capability Matrix section) |
| SCHEMA-bson-types | BSON→Java-primitive conversion drops date precision and misinterprets ObjectId, causing display bugs and failed write operations. | Materially affects data integrity for any workflow involving date filtering or document identity (updates/deletes) — the single most concrete, primary-sourced finding in the whole research file. | GitHub #40165, #8914, #1171 (all in S1's Works Cited) |

## Constraints and risks

- The three GitHub issues are dated to whenever they were filed/analyzed; the research file does not state whether they remain open as of the current DBeaver release. Treat "confirmed limitation" as confirmed-as-of-source, not necessarily still-current.
- No JSON-schema-validation authoring/deployment workflow is discussed for DBeaver in the source at all — this is a silent gap in the source, not a confirmed absence, and is therefore omitted from the matrix.

## Interactions and dependencies

- The BSON type-fidelity issues documented here are the direct technical basis for Studio 3T's Pillar 1 competitive-positioning recommendation in the source ("Native BSON & Aggregation Engineering... Type fidelity (ISODate/ObjID)").
- Schema/structure comparison lives under [F-GOV](../governance/feature-report.md) (`GOV-collection-compare`), not this feature.

## Conclusions

### Strengths

- None evidenced for MongoDB schema analysis specifically.

### Limitations

- No sampling-based field-probability/type-probability/histogram analytics for MongoDB collections.
- Confirmed BSON type-fidelity bugs (date precision, ObjectId misinterpretation) backed by three independent GitHub issues.
- Schema/structure compare is relational-DDL-first and reportedly weak on nested BSON (unverified independently).

### Unknowns

- Current (post-analysis-date) status of the three cited GitHub issues.
- Whether any $jsonSchema validation authoring exists for DBeaver's MongoDB connections.
