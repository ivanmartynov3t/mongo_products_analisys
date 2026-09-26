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
2. Matrix rows: the first-column IDs of every capability table (a table with a `Current support` or `Status` column) in the product's feature matrices.
3. A row **covers** a silo tag when its ID is the tag, or when [`reports/taxonomy-reconciliation.tsv`](../../reports/taxonomy-reconciliation.tsv) maps it to that tag (directly or through the ID it is a `child-of` / synonym of).
4. A silo tag is a **candidate** for the product when at least `min_docs` of the product's catalog entries carry it with probability ≥ `min_probability`, and no row covers it.
5. The report also lists matrix IDs the silo never tags for that product.

## Columns

| Column | Meaning |
|---|---|
| Web | public web pages carrying the tag; the top `top_docs` are listed by URL with their probability |
| Repo / Source | repository documents and indexed source files carrying the tag; **counted, never named** |
| Shared | entries whose file is indexed under more than one silo product (e.g. one repository copied into several products); a mostly shared candidate may belong to another product |

## Guarantees

- **Read-only.** The silo is read from git objects at the pinned `silo_ref`; the only file the tool can write is the configured output in `reports/` (`review.guarded_write`).
- **Deterministic** for the same silo commit and repository content (tested).
- **No private content.** This repository is public: repository documents and source files are counted, never named or quoted; a page whose `source_url` is on GitHub counts as a repository file.
- **Leads, not facts.** A candidate never becomes a ✅ or ❌; a claim needs a human-checked source.
