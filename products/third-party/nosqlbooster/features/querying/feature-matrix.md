# Feature Matrix — NoSQLBooster / Querying

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: NoSQLBooster
- Product group: third-party
- Feature ID: F-QUERY (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `querying`
- Analysis date: 2026-09-04
- Version/release context: v11.0–v11.1 line

## Source index

- S1: NoSQLBooster Competitive Analysis
- S2: NoSQLBooster Competitive Intelligence Analysis
- P1: nosqlbooster.com/features (primary; fetched directly by this review 2026-09-04 to adjudicate the Visual Query Builder and code-gen-language-count conflicts between S1 and S2)
- P2: nosqlbooster.com/compareEditions (primary; fetched directly by this review 2026-09-04)

## Capability matrix (low-level)

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| QUERY-fluent-api | Fluent chaining query API | Confirmed | S1: "a Mongoose-like fluent chaining API along with an operator helper ($) that translates chained methods into standard BSON query objects." S2: "a Mongoose-like chainable fluent query API, enabling developers to build complex database queries and aggregation pipelines using method chaining rather than manually composing nested JSON objects." P1 confirms with a worked code example (`db.user.where('age').gte(18).lte(65)...`). | — | N/A | S1, S2, P1 | This is the direct evidentiary basis this repository used to add the `QUERY-fluent-api` dictionary ID during this same effort. |
| QUERY-vqb-core | Visual Query Builder core | Confirmed (resolves S1/S2 conflict) | P1's Feature Tour page: "NoSQLBooster for MongoDB comes with a visual query builder. The *two-way* query builder could help you construct and display complex MongoDB find statements even without the knowledge of the MongoDB shell commands syntax." P2 lists "Visual Query Builder" as a feature row present across Free/Personal/Commercial tiers. | — | N/A | P1, P2; contradicts S1 | **Reconciliation:** S1's "Missing functionality" section states NoSQLBooster "lacks a visual drag-and-drop query builder" (cited to [3, 23] — a DbSchema roundup blog and a Reddit thread, neither a NoSQLBooster primary source). S2 asserts a Visual Query Builder exists but with no inline citation. This review fetched P1 (a source both files themselves cite) directly and found it confirms the builder's existence — S1's specific absence claim is not carried into the coverage matrix as a confirmed absence. See `product-report.md`'s "Two-file reconciliation" section, point 1. |
| QUERY-vqb-bidirectional | VQB bidirectional sync | Confirmed | S2: "maintains real-time synchronization between visual drag-and-drop rule builders and underlying editor scripts." P1 independently describes it as "two-way." | — | N/A | S2, P1 | — |
| QUERY-export-lang | Export to language | Confirmed, 8 targets (resolves S1/S2 conflict) | P1's "Query Code Generator" section: "translate MongoDB queries (find, aggregate, or SQL query) to various target languages: MongoDB Shell, JavaScript (Node.js), Java, C#, Python, PHP, Ruby, and Golang." | — | N/A | P1, S2 (count matches); contradicts S1 | **Reconciliation:** S2's Technical Capability Comparison Matrix states "8 Targets," matching P1 exactly. S1's narrative claims "Node.js, Python, Java, C#, Go, Rust, Kotlin, PHP, Ruby, and C++" (10, no MongoDB Shell target) but attributes this to the *AI Helper's* "cross-language code translation," not the separate deterministic Query Code Generator P1 describes — see `product-report.md`'s "Two-file reconciliation" point 2 and `features/ai/feature-matrix.md` for the distinct, Unverified AI-Helper-specific translation claim. |
| QUERY-view-tree | Tree view | Confirmed | S1: "Data grid rendering is powered by AG-Grid, offering tabular and tree views." P2 lists "Tree/Table/JSON Viewer" as one row. | — | N/A | S1, P2 | — |
| QUERY-view-table | Table view | Confirmed | Same S1/P2 citation as QUERY-view-tree. | — | N/A | S1, P2 | — |
| QUERY-view-json | JSON/BSON view | Confirmed | P2's "Tree/Table/JSON Viewer" row explicitly includes JSON; not separately itemized in S1/S2 body text. | — | N/A | P2 | Weaker evidentiary basis than QUERY-view-tree/table since neither research file's body text calls out a JSON view mode by name — confirmed via primary source only. |
| QUERY-inline-edit | Inline editing | Confirmed | S1: AG-Grid data viewer provides "nested field column grouping, field type conversions, and in-place document editing." | — | N/A | S1 | — |
| QUERY-view-gridfs | GridFS viewer | Confirmed | S1: "binary storage is managed through a graphical GridFS viewer." P1 adds detail: "read and write to GridFS collections. Files can be added quickly with drag and drop." | — | N/A | S1, P1 | Upload/download/CRUD depth is tracked separately under `TRANSFER-gridfs-crud` in `features/data-transfer/feature-matrix.md`, per the dictionary's own read/browse vs. CRUD distinction. |
| QUERY-ai-builder | AI query builder | Confirmed | S1/S2 both describe the AI Helper's natural-language-to-query generation in the querying context; cross-referenced with `AI-nl-query` in `features/ai/feature-matrix.md`. | Gated behind active Software Assurance even on a perpetual license — see F-AI matrix. | N/A | S1, S2, P1 | — |

## Feature-level conclusion

### Confirmed strengths

- A genuine two-way Visual Query Builder (confirmed via primary source after resolving a direct S1/S2 conflict) alongside a distinctive Mongoose-like fluent chaining API — two different code-free-to-code-heavy authoring surfaces for the same underlying find() queries.
- A deterministic, 8-target Query Code Generator, precisely confirmed via primary source.
- AG-Grid-based result viewing (tree/table/JSON) with inline editing and a dedicated GridFS viewer.

### Confirmed limitations

- Neither research file itemizes projection/sort/collation/skip-limit controls, saved-query management, or copy-options behavior in the querying UI specifically — these remain unconfirmed rather than assumed absent or present.

### Open questions / unknowns

- Whether the Visual Query Builder's scope extends beyond `find()` statements to projection and sort controls (`QUERY-vqb-proj-sort`) — P1's own description scopes it to "construct and display complex MongoDB find statements," which does not explicitly confirm projection/sort sections.
- The AI Helper's own cross-language *script* translation language roster, as distinct from the confirmed 8-target Query Code Generator — see `product-report.md`'s reconciliation point 2.
