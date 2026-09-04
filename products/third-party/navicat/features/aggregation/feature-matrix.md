# Feature Matrix — Navicat / Aggregation

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: Navicat
- Product group: third-party
- Feature ID: F-AGG (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `aggregation`
- Analysis date: 2026-09-04
- Version/release context: Navicat 17 line; initial aggregation pipeline builder introduced during the Navicat 12–15 release cycle per the source's release history

## Source index

- S1: Navicat Competitive Intelligence Analysis (secondary research file), `research/google_research/navicat-competitive-intelligence-analysis/Navicat Competitive Intelligence Analysis.md`
- S2: Navicat Online Manual, https://www.navicat.com/manual/online_manual/en/navicat_17/win_manual/ (S1 Works Cited #5)

## Capability matrix (low-level)

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AGG-editor-layout | Editor layout | Confirmed | S1: "Navicat provides a visual stage-by-stage aggregation pipeline builder. Developers drag and drop operators (such as $match, $group, $project, $lookup, and $unwind) into a sequential pipeline interface." | — | Unverified | S1 | Introduced during the Navicat 12–15 release cycle per S1's Release History section ("introducing the initial visual Aggregation Pipeline builder for MongoDB"). |
| AGG-stage-mgmt | Stage management | Confirmed (existence); Unverified (depth) | Implied by the drag-and-drop sequential pipeline interface described above; add/reorder of stages is the mechanism's basic function. | Keyboard shortcuts, duplicate/move operations not itemized. | Unverified | S1 | — |
| AGG-stage-modes | Stage edit modes | Confirmed | S1: "Developers drag and drop operators... into a sequential pipeline interface" — a visual/form-based editing mode is the described mechanism (as opposed to DBeaver's raw-JSON-only console). | Whether a raw-JSON per-stage or whole-pipeline edit mode also exists alongside the visual mode is not stated. | Unverified | S1 | — |
| AGG-stage-preview | Stage preview | Confirmed, limited depth | S1: "The editor renders preview results at each stage, enabling users to verify output documents as transformation rules are applied." | The comparison table (Direct Comparison section) contrasts this explicitly against Studio 3T: "Aggregation Pipeline Builder | Visual stage builder with output preview. | [vs.] Deep visual stage debugger with IO inspection & code gen." | Not planned | S1 | Per-stage *output* preview is Confirmed; combined input+output ("IO") inspection is explicitly the comparison table's stated gap — see `Basic Aggregation Debugging Tools` in Confirmed limitations below. |
| AGG-code-gen | Code generation | Not supported (confirmed absent) | S1 (user feedback section): "it lacks... instant driver code generation across multiple programming languages (e.g., C#, Java, Python, JavaScript, PHP, Ruby)—key productivity features found in Studio 3T's Aggregation Editor." Repeated in the head-to-head table: "Aggregation Pipeline Builder | Visual stage builder with output preview. | [vs.] Deep visual stage debugger with IO inspection & code gen." | — | Not planned (per S1's own framing as a Studio 3T competitive advantage) | S1 | Confirmed-absent by direct, repeated statement — not merely unmentioned. |
| AGG-mapreduce-editor | MapReduce editor | Confirmed | S1: "The MapReduce editor provides forms to author, test, and debug scripts using sampled document sets before executing full cluster jobs." Also listed in the Feature Inventory: "Graphical designers for Collections, Views, Functions, Indexes, Aggregation Pipelines, GridFS file buckets, and MapReduce jobs." | Testing/debugging is against sampled document sets, not necessarily the full collection, before a full-cluster run. | Unverified | S1 | This Navicat capability is the direct evidentiary basis for the new dictionary ID `AGG-mapreduce-editor` added in this same effort (2026-09-04) — a distinct, dedicated author/test/debug workflow for map/reduce, separate from the aggregation pipeline builder. |
| AGG-create-view | Create view | Unverified | Not discussed for MongoDB specifically. S1 mentions "Views" among the objects Navicat has "Graphical designers" for, but does not describe creating a view *from* a pipeline. | — | Unverified | S1 | — |
| AGG-pipeline-opts | Pipeline options | Unverified | Not discussed (allowDiskUse, collation, index hint, maxTimeMS not mentioned for the pipeline builder). | — | Unverified | S1 | — |
| AGG-export-results | Export results | Unverified | Not discussed specifically for aggregation pipeline output, though general Export Wizard capability exists (see [F-TRANSFER](../data-transfer/feature-matrix.md)) for collection/view/query-result export — pipeline-result export specifically is not itemized. | — | Unverified | S1 | — |

## Feature-level conclusion

### Confirmed strengths

- A genuine visual, drag-and-drop, stage-by-stage pipeline builder with named operator support ($match, $group, $project, $lookup, $unwind) and per-stage output preview — categorically ahead of DBeaver's raw-JSON-array console and DataGrip's complete absence of any pipeline surface.
- A dedicated MapReduce author/test/debug editor working against sampled document sets before full-cluster execution — a distinct capability from the aggregation pipeline builder, evidenced specifically enough to justify the new `AGG-mapreduce-editor` dictionary ID.

### Confirmed limitations

- No multi-language driver code generation from a pipeline (confirmed absent, by direct and repeated statement in the source, contrasted explicitly against Studio 3T's Aggregation Editor).
- No deep stage-by-stage input/output document inspection ("IO inspection") — the source's own head-to-head comparison table draws this exact line: Navicat has "output preview" only, while Studio 3T has a "deep visual stage debugger with IO inspection."

### Open questions / unknowns

- Whether stage enable/disable toggling, pipeline execution options (allowDiskUse, collation, maxTimeMS), keyboard shortcuts, or JSON pipeline import/export exist at all — not discussed in the source in either direction.
- Whether a MongoDB view can be created directly from a saved aggregation pipeline.
- Total number of pipeline stage types supported by the visual builder (stage catalog breadth) is not itemized.
