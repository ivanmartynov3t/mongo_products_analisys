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

## Porting validator

`validate.py` checks one `/silo-port` checklist item before its PR (issue #53, Plan 09 L4). Configuration: [`validate.toml`](validate.toml).

```bash
uv run tools/silo-candidates/validate.py --item datagrip          # a product folder name
uv run tools/silo-candidates/validate.py --item scope-triggers    # or cross-product, readme
uv run tools/silo-candidates/test_validate.py                     # offline tests
```

It compares the working tree with its merge-base with `main`. Committed, staged, unstaged and untracked changes all count. A rename counts as a deletion plus an addition, so moving another product's file is still out of scope.

**Per touched capability row.** A row counts as touched when its line is new or edited, or when a Source index entry it cites changed or was removed. Untouched rows are never judged.

1. **IDs.** Every ID is in `feature-dictionary.md` and is not retired.
2. **Status.** The status cell holds a legal label from `[status]`. A compound cell gets the requirements of every class it holds:
   - *confirmed* needs a cited source with a URL and a `YYYY-MM-DD` date on its Source index line;
   - *unverified* needs `Checked <URL> on <YYYY-MM-DD>`;
   - *not supported* needs a quoted exclusion found in a cited silo page or repository file; a dictionary quote does not count.
3. **Pins.** Every silo pin on a cited source is *current* or *unchanged* at the silo ref (from `tools/silo-pins`).
4. **Quotes.** Every quoted passage of at least `min_quote_words` words is found in one of:
   - a cited source's pinned silo page;
   - a repository file named in the Source index, read **at the base**, so evidence added in the same change cannot verify itself (paths outside the repository are ignored);
   - the dictionary.

   The comparison is split at ellipses (`...`, `…`, `[…]`), and ignores case, markdown, quote style, dashes and whitespace. A quote whose sources are only live URLs cannot be checked and is a finding.

**Across the diff:**

5. **Private names.** Every changed file is scanned, whatever its suffix; binary files are flagged for a human. Two things are flagged:
   - an added line that links a code host or internal system with a repository the base does not already cite;
   - an added line or new file path that names a silo repository folder the base never mentions, even inside a word such as `name-docs`.

   Every finding is redacted before it is printed, so it can be pasted into a PR. Unexpected errors print only their type; `--debug` shows the traceback.

   **Limit:** a silo repository name that the base already mentions anywhere is treated as public.
6. **Ledger.** For a product item, no open web-backed candidate is left without a ledger row, and added ledger rows belong to that product.
7. **Scope.** Only files in the item's `[scope]` changed. For a product item, `reports/silo-candidates.md` must equal a fresh run, whether or not it changed. Any other tool-owned report in the diff needs a human to confirm it is unchanged tool output.

**Exit codes:** 0 clean, 1 findings for a human, 2 for any error (for example a malformed ledger, an unknown item or base, or no silo). It writes nothing. A malformed-ledger error quotes the offending cell, so check it before pasting it anywhere.

**Not yet checked:**

- **The access-date window for ✅.** Only the date's presence is checked. Whether a silo capture date counts, and how recent it must be, is owner decision 3 in Plan 09.
- **Batch contents.** Check 6 uses the open web-backed candidates, which are exactly the candidates in the product's evidence batch.

## Evidence batches

`batch.py` writes the Claude stage's input (issue #54, Plan 09 L2). `tools/silo-sync/run.sh` runs it after the candidate report.

```bash
uv run tools/silo-candidates/batch.py plan     # summary only, writes nothing
uv run tools/silo-candidates/batch.py apply    # rebuild .local/silo-batches/
uv run tools/silo-candidates/test_batch.py     # offline tests
```

**One folder per product that has a silo product.** Each holds:
- **`README.md`.** For every **open web-backed** candidate (after the triage ledger):
  - its aliases and dictionary definitions;
  - every public page carrying the tag, not only the report's top 3: title, URL, probability, retrieval date (`updated_at`), and the citation to use (`` `URL` (silo: `data/…@<sha8>`) ``, pinned at the silo ref);
  - after the candidates, the product's current matrix rows (ID and status).
- **`pages/`.** Each cited page's body at the silo ref, frontmatter removed.

**Guarantees:**
- **Local only.** `.local/` is gitignored. Every `apply` builds a new folder and swaps it in, so no stale file survives, and a failed run keeps the previous batches. Check the commit in each README header. Nothing is written outside the folder (guarded and tested).
- **Public pages only.** Repository documents, source files and pages on `non_public_hosts` are left out entirely, not just unnamed.
  - Page bodies are copied verbatim, so they may still link code hosts or mention repository names. `validate.py` is the gate before anything is committed.
  - A catalog page the silo does not store at the ref has no URL, so it is never a web page; `candidates.py` counts it as a source file.
- **Deterministic.** The output is the same for the same silo commit, ledger and matrices.
- **Errors.** A malformed ledger, like any other error, exits 2.
