# Feature Report — NoSQLBooster / Aggregation

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Scope

- Feature name: Aggregation
- Feature ID: F-AGG (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Product: NoSQLBooster
- Product group: third-party
- Analysis date: 2026-09-04

## Behavioral walkthrough

NoSQLBooster's aggregation story is genuinely thin relative to its rich querying and shell surfaces, and — unusually for this product — the thinness is confirmed by direct statement rather than being an unresearched gap: S1's own "Missing functionality" section states plainly that NoSQLBooster "lacks a dedicated stage-by-stage visual aggregation pipeline editor," with pipeline creation instead relying on "manual scripting, code snippets, or fluent method chaining," and that there is no interface to inspect a pipeline's per-stage input/output documents side by side. This puts NoSQLBooster's F-AGG surface in a similar position to DBeaver's (text/code-only, no visual builder) rather than Navicat's or Studio 3T's (full visual, drag-and-drop, stage-by-stage builders with per-stage preview).

What does exist is code-level: the fluent chaining API's `$` operator helper supports building aggregation pipelines through method chaining (`db.companies.aggregate($.where('founded_year').gte(2000).lte(2010)).group(...).sort(...).limit(...)`), and the deterministic Query Code Generator explicitly accepts `aggregate` queries as one of its three input types (alongside `find` and SQL), translating them into the same 8 confirmed target languages used for find queries.

## Sub-feature notes

| Sub-feature ID | Finding | Impact | Evidence |
| --- | --- | --- | --- |
| AGG-editor-layout / AGG-stage-preview | Both confirmed absent by direct statement, not silence. | A genuine, source-confirmed competitive gap versus Navicat, Studio 3T, Compass, and VisuaLeaf, all of which have real visual pipeline builders per this repository's other product reports. | S1 |
| AGG-code-gen | Aggregation-specific code generation is real, sharing the same 8-language roster confirmed for F-QUERY. | A narrow but genuine strength distinguishing NoSQLBooster from Navicat, whose aggregation builder is confirmed to lack multi-language driver code generation entirely. | S2, P1 |

## Constraints and risks

- Because pipeline authoring is code-only, users without JavaScript/mongosh fluency have no code-free path to building an aggregation pipeline in NoSQLBooster, unlike the Visual Query Builder's code-free path for simple `find()` queries.
- No MapReduce-style dedicated editor is described anywhere in either source file — this repository's `AGG-mapreduce-editor` dictionary ID (minted for Navicat) does not apply to NoSQLBooster.

## Interactions and dependencies

- Aggregation authoring depends entirely on the shell/script editor (F-SHELL) and its debugger, autocomplete, and NPM-utility integration — there is no separate aggregation-specific editor surface the way there is for querying (Visual Query Builder) or SQL (SQL Query Engine).
- The SQL-to-MongoDB translation engine (F-SQL) internally generates aggregation pipelines from SQL `GROUP BY`/`JOIN` queries, per S1's table row ("Transpiles SQL syntax into MongoDB aggregation pipelines and db.collection.find() queries") — but this is an F-SQL-facing capability, not a user-facing F-AGG authoring surface, and is tracked under F-SQL instead.

## Conclusions

### Strengths

- Aggregation-specific multi-language code generation, confirmed via primary source.

### Limitations

- No visual, stage-by-stage pipeline builder; no per-stage input/output preview — both confirmed absent by direct statement.

### Unknowns

- Supported pipeline-stage catalog breadth, pipeline-level execution options (`allowDiskUse`, collation, `maxTimeMS`), and whether pipelines can be saved/loaded as named, reusable definitions distinct from general script save/load.
