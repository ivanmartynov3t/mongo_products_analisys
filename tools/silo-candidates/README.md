# silo-candidates

Answers one question: **which capabilities does the silo see for a product that no matrix row covers?** (issue #36, Plan 08 P4). The output is the input queue for the LLM-assisted step ([Plan 09](../../update-plans/09-silo-porting-llm.md)).

```bash
uv run tools/silo-candidates/candidates.py plan      # print the report, write nothing
uv run tools/silo-candidates/candidates.py apply     # write reports/silo-candidates.md
uv run tools/silo-candidates/test_candidates.py      # offline tests
```

Needs a clone of `prod_info_silo` next to this repository; `git -C ../prod_info_silo fetch` before a run. Configuration: [`silo-candidates.toml`](silo-candidates.toml).

## How a candidate is found

1. Products: every `products/<category>/<slug>/` folder whose name is a silo product in `data/catalog_index.json`.
2. Matrix rows: the first-column IDs of every capability table (a table with a `Current support` or `Status` column) in the product's feature matrices. A cell may hold several IDs (`A / B`, `A, B`); annotations in parentheses, such as **(PENDING DICTIONARY ADDITION)**, are ignored. The parser is `review.matrix_table_ids`, for reuse by other tools.
3. A row **covers** a silo tag when its ID is the tag, or when [`reports/taxonomy-reconciliation.tsv`](../../reports/taxonomy-reconciliation.tsv) maps it to that tag (directly or through the ID it is a `child-of` / synonym of).
4. A silo tag is a **candidate** for the product when at least `min_docs` of the product's catalog entries carry it with probability ≥ `min_probability`, and no row covers it.
5. IDs in a **pointer table** (an ID table without a status column, e.g. "Moved to") are documented in another product's matrix. Their tags are not candidates; the report lists them per product instead.
6. The report also lists matrix IDs the silo never tags for that product, at any probability.
7. Candidates decided in the triage ledger leave the tables (below).

## Triage ledger

[`triage.tsv`](triage.tsv) records decided candidates (issue #52, Plan 09 L1). It is edited by hand (and, from Plan 09 step 4, by the `/silo-port` command); this tool only reads it. One tab-separated row per candidate:

| Column | Meaning |
|---|---|
| `product` | the product folder name, e.g. `datagrip` |
| `tag` | the silo tag, e.g. `QUERY-projection` |
| `outcome` | `add-row`, `existing-row`, `other-product`, `noise` or `needs-human` |
| `date` | decision date, `YYYY-MM-DD` |
| `silo_commit` | silo commit the decision was made at (7–40 hex), for traceability |
| `web_docs` | the candidate's **Web** count when it was decided; the re-open check compares against it |
| `ref` | the PR, or a one-line reason. This repository is public: never name a private repository or document |

- **Decided candidates.** They leave the tables. The summary's **Triaged** column counts ledger rows per outcome.
- **Re-opening.** A decided candidate comes back, marked *re-opened*, when its **Web** count is now above `web_docs`. To close it again, edit the same row: update `date`, `silo_commit` and `web_docs`, since duplicate rows are rejected.
- **`needs-human` decisions.** They stay listed per product while the tag is still a lead. To resolve one, change its outcome.
- **Malformed ledgers.** A malformed row stops the run with exit 2 before the silo is read. So does a row for a product without a silo product, which is detected once the catalog is read. Examples: an unknown product, a duplicate row, a bad outcome, date, tag or count.
  - A well-formed but wrong value, such as a too-high `web_docs`, is not detected. The PR review is the check for that.

## Columns

| Column | Meaning |
|---|---|
| Web | public web pages carrying the tag; the top `top_docs` are listed by URL with their probability |
| Repo / Source | repository documents and indexed source files carrying the tag; **counted, never named** |
| Shared | entries also indexed under another silo product with the same content: the same normalised URL for a top-level page, the same body (frontmatter removed) for other stored files, the same path for source files the silo does not store. Unrelated vendors' stored `index.md` never count; for source files the silo does not store, only the path can be compared, so two unrelated products with the same unstored path would count as shared. A mostly shared candidate may belong to another product |

## Guarantees

- **Read-only.** The silo is read from git objects at the pinned `silo_ref`; the only file the tool can write is `reports/silo-candidates*.md` (`review.guarded_write`).
- **Deterministic** for the same silo commit and repository content (tested).
- **No private content.** This repository is public: repository documents and source files are counted, never named or quoted; a page on a host in `non_public_hosts` (GitHub, GitLab, Bitbucket, Atlassian), or whose file the silo does not store, is counted in **Source**. The same page captured under two URL forms is counted once.
- **Deliberate omission.** Candidates backed only by repository documents or source files show "—" under top public pages: naming them would expose private repositories. The LLM-assisted step ([Plan 09](../../update-plans/09-silo-porting-llm.md)) needs a local-only view for those.
- **Leads, not facts.** A candidate never becomes a ✅ or ❌; a claim needs a human-checked source.
