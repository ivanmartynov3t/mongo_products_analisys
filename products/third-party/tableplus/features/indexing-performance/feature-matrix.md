# Feature Matrix — TablePlus / Indexing & Performance

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: TablePlus
- Product group: third-party
- Feature ID: F-IDX (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `indexing-performance`
- Analysis date: 2026-09-04
- Version/release context: 2026 release line

## Source index

- S1: TablePlus Competitive Intelligence Analysis (secondary research file, no inline per-claim citation markers), `research/google_research/tableplus-competitive-intelligence-analysis/TablePlus Competitive Intelligence Analysis.md`

## Judgment call: thin matrix vs. prose-only

The source explicitly discusses index capability (unlike DBeaver's or DataGrip's sources, where MongoDB indexing was never mentioned at all and the area was omitted entirely). TablePlus's own comparison table names a specific, real capability — "Basic index listing & creation" — and separately confirms the absence of Explain plans and an index-performance analyzer. Because the area is discussed with enough specificity to support both a real (thin) positive row and clearly confirmed-absent rows, this matrix is built rather than folded into prose only.

## Capability matrix (low-level)

| Sub-feature ID | Sub-feature name | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| IDX-inventory | Index inventory | Unverified — per secondary source, no primary citation | S1 (Section 5, comparison table): "Index Tuning & Explain Plans | Basic index listing & creation." | — | Unverified | S1 | Existence of a listing surface is stated; depth (name/type/size/usage-count columns) is not itemized. |
| IDX-type-single | Single-field index | Unverified — per secondary source, no primary citation | S1 (Section 5 narrative): "Developers can... add basic indexes." | "Basic" qualifier used by the source itself; compound/specialty index-type support not itemized. | Unverified | S1 | — |
| IDX-type-compound | Compound index | Unverified — no evidence either way | Not itemized in the source beyond "basic indexes." | — | Unverified / no evidence | S1 | Not claimed present or absent — simply not itemized at this depth. |
| IDX-explain-brief | Explain — plan mode | Confirmed absent | S1 (Section 5, comparison table): "Index Tuning & Explain Plans | Basic index listing & creation | ... Visual Explain plans & index performance analyzer [Studio 3T] | Moderate: TablePlus offers limited index optimization tools." The row structure directly contrasts TablePlus's basic listing against Studio 3T's Explain plans, without listing Explain plans as part of TablePlus's own offering. | — | Confirmed absent | S1 | Treated as confirmed-absent because the comparison table's own TablePlus-column entry omits Explain plans entirely while explicitly naming them for Studio 3T in the adjacent column — the standard pattern this repository uses elsewhere (e.g., DataGrip's F-SCHEMA) for a comparison-table-driven confirmed absence. |
| IDX-explain-full | Explain — full stats | Confirmed absent | Same evidence as `IDX-explain-brief` — no execution-stats explain mode of any kind is named for TablePlus. | — | Confirmed absent | S1 | — |
| IDX-perf-insights | Performance insights | Confirmed absent | Same comparison-table row: "Moderate: TablePlus offers limited index optimization tools" — stated as a direct limitation, not merely unmentioned. | — | Confirmed absent | S1 | — |
| IDX-profiler-config | Profiler configuration | Confirmed absent (no evidence, consistent with the broader "limited index optimization tools" statement) | Not discussed anywhere in the source beyond the general limitation statement above. | — | Unverified / no evidence | S1 | Not itemized separately; grouped under the same general limitation. |

## Feature-level conclusion

### Confirmed strengths

- None — the one positive capability (basic index listing/creation) does not trace to a primary-source citation and is explicitly qualified as "basic" by the secondary source itself.

### Confirmed limitations

- No Explain plan of any kind (plan-only or full execution-stats) and no index-performance analyzer — the source's own comparison table directly and explicitly contrasts this against Studio 3T's visual Explain plans and analyzer, labeling TablePlus's index tooling "limited."

### Open questions / unknowns

- Exact index types supported for creation (single-field, compound, text, geospatial, TTL, wildcard, hashed) — the source only states "basic indexes" without itemizing types.
- Whether index properties (unique, sparse, partial, hidden, collation) are configurable through any UI, or require hand-written commands.
- Whether any real-time performance monitoring (mongostat/mongotop/currentOp equivalent) exists — not discussed in the source at all.
