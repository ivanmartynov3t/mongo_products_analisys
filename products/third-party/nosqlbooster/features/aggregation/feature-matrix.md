# Feature Matrix — NoSQLBooster / Aggregation

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: NoSQLBooster
- Product group: third-party
- Feature ID: F-AGG (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `aggregation`
- Analysis date: 2026-09-04
- Version/release context: v11.0–v11.1 line

## Source index

- S1: NoSQLBooster Competitive Analysis
- S2: NoSQLBooster Competitive Intelligence Analysis
- P1: nosqlbooster.com/features (primary; fetched directly by this review)

## Capability matrix (low-level)

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AGG-editor-layout | Editor layout | Confirmed absent (no visual builder) | S1, under "Missing functionality": "NoSQLBooster lacks a dedicated stage-by-stage visual aggregation pipeline editor. Pipeline creation relies on manual scripting, code snippets, or fluent method chaining." | — | N/A | S1 | Not a placeholder gap — a direct, specific statement of absence, mirroring DBeaver's/DataGrip's own confirmed-absent visual pipeline builders. |
| AGG-stage-preview | Stage preview | Confirmed absent | S1: "The client does not offer an interface to inspect input and output documents at each stage of a pipeline side-by-side." | — | N/A | S1 | — |
| AGG-code-gen | Code generation | Confirmed | S2: the Query Code Generator "converts MongoDB queries (find, aggregate, or SQL) into syntactically correct target code across multiple programming languages." P1's "Query Code Generator" section confirms `aggregate` as one of the three accepted query types, across the same 8 confirmed target languages as `QUERY-export-lang`. | — | N/A | S2, P1 | Same underlying deterministic Query Code Generator as `QUERY-export-lang` in F-QUERY — this row exists because the dictionary's `AGG-code-gen` and `QUERY-export-lang` are tracked as separate sub-feature IDs even though NoSQLBooster implements them via one shared tool. |

## Feature-level conclusion

### Confirmed strengths

- Aggregation pipelines can be translated to 8 target driver languages via the same deterministic Query Code Generator used for `find()` queries — a real, if narrow, aggregation-specific capability confirmed via primary source.

### Confirmed limitations

- No visual, stage-by-stage pipeline builder and no per-stage input/output preview — both confirmed absent by direct statement in S1, not merely unmentioned. Pipeline authoring happens exclusively through code: manual JSON, the fluent chaining API's `$` operator helper, or code snippets (e.g., the "aggregate" snippet mentioned in P1's Snippets section).

### Open questions / unknowns

- Neither source file itemizes a specific supported pipeline-stage catalog, `allowDiskUse`/collation/`maxTimeMS` pipeline-level options, stage enable/disable toggles, or a MapReduce-style alternate editor (this repository's newly-added `AGG-mapreduce-editor` ID, minted for Navicat, has no matching evidence anywhere in either NoSQLBooster source file and is deliberately not used here).
- Whether pipelines authored via the fluent API or raw JSON can be saved/loaded as named, reusable pipeline definitions distinct from general script save/load (tracked under F-SHELL) is not confirmed.
