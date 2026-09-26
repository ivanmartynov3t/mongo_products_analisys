# silo-candidates

Answers one question: **which capabilities does the silo see for a product that no matrix row covers?** (issue #36, Plan 08 P4). The output is the input queue for the LLM-assisted step (Plan 08 part 2).

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
- **Deliberate omission.** Candidates backed only by repository documents or source files show "—" under top public pages: naming them would expose private repositories. Part 2 (LLM step) needs a local-only view for those.
- **Leads, not facts.** A candidate never becomes a ✅ or ❌; a claim needs a human-checked source.
