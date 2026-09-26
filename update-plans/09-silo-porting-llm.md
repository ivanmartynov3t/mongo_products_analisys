# Plan 09 — LLM-assisted data porting from prod_info_silo

This is part 2 of the silo porting. [Plan 08](08-silo-porting-mechanical.md) built the scripts that surface signals. This plan adds the judgement: whether a signal is a real capability, which ID it maps to, what status it gets, and which source backs it.

Measured 2026-09-26 at silo `55dbb2cb`. **Status: approved (2026-09-26); step 1 in review.** Issues #52–#57.

## Flow

1. **Mechanical stage.** `tools/silo-sync/run.sh` refreshes the reports and the local evidence batches. It is deterministic.
2. **Claude stage.** `/silo-port` runs in Claude Code, not through the API. It loops over [`09-product-loop.md`](09-product-loop.md), one product at a time. For each product it:
   - creates a branch from an up-to-date `main`;
   - updates the product's files from the reports;
   - runs the validator;
   - opens one PR;
   - ticks the product.

   The loop ends with the cross-product reports, then the `README.md` dashboard.

For each product, the Claude stage handles:

| Report | Action |
|---|---|
| `silo-candidates.md` | triage the **web-backed** candidates (outcomes below) |
| `review-queue.md` | re-check rows and reports whose cited page changed |
| `silo-pins` re-pin plan | apply unchanged pins; re-check rows behind changed ones |
| `evidence-gaps.md` | add a public URL source to matrices that cite none, where the silo holds one |
| downstream | the product's feature and product reports (prompt 03) |

Repository-wide items run once:
- **First:** scope triggers.
- **Then:** the cross-product reports (low-level comparison, gap analysis) via prompt 03.
- **Last:** `README.md`, rebuilt with the existing [`update-readme-dashboard.prompt.md`](../.github/prompts/update-readme-dashboard.prompt.md).

**Out of scope:**
- the 104 candidates backed only by repository or source documents (decision 2);
- silo seed URLs (prod_info_silo#47);
- changes to the silo classifier.

## Rules

- **The LLM drafts; a human approves.** The LLM may draft a matrix edit, including a status. A human approves it in the PR, and nothing reaches `main` without that review. This is the only change from Plan 08's rule.
- **Silo tags are not evidence.**
  - A silo tag or its probability is never evidence for a status. Evidence is a source's text, cited by URL.
  - "Matrix IDs the silo never tags" never leads to a ❌ or a row removal.
- **Statuses follow weekly prompt 01. No new labels.**
  - ✅ needs an exact URL and an access date.
  - ❌ needs an explicit exclusion in the source.
  - ❓ needs a "Checked [URL] on [DATE]" note.
- **Bad captures.** A page captured as navigation or a cookie banner is marked `needs-human`, never ❌.
- **Citations.**
  - Cite the live URL, plus a P6 pin: `` silo: `data/…/x.md@<sha>` ``.
  - Quote the source word for word.
  - Prefer an existing dictionary ID.
- **This is a public repository.** No private repository name, path or content may appear in any file, commit, issue or PR.
- **Scope of each run.**
  - The silo is read only at a pinned ref.
  - A product run edits only that product's files, plus the ledger, `decisions.tsv` and the checklist.
  - `README.md` changes only in its own item, through its prompt.

## Candidate outcomes

| Outcome | Lands in |
|---|---|
| `add-row` | a new matrix row |
| `existing-row` | `tools/taxonomy-reconcile/decisions.tsv` (a mapping, not an ad hoc edit) |
| `other-product` | the ledger; the evidence belongs to another product (Shared column) |
| `noise` | the ledger only |
| `needs-human` | the ledger, with a reason |

## Steps

Each step has one issue and one PR.

| # | Step | Issue | What |
|---|---|---|---|
| 1 | L1 Triage ledger | [#52](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/52) | Add `tools/silo-candidates/triage.tsv`: product, tag, outcome, date, silo commit, PR or reason. `candidates.py` hides decided candidates and re-opens one if its web-document count grows. |
| 2 | L4 Validator | [#53](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/53) | Add `tools/silo-candidates/validate.py`. It checks that each ID exists, each status is legal and carries its required fields, and pins resolve. It also checks that quotes appear word for word in the pinned page, that no private host or repository is named, that every batch candidate has one ledger row, and that the diff stays in scope. Exit codes: 0 clean, 1 needs a human, 2 error. |
| 3 | L2 Evidence batches | [#54](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/54) | Add `tools/silo-candidates/batch.py`, run by `run.sh`. It writes every public silo page per open candidate to a gitignored `.local/silo-batches/` folder. Private documents are left out. |
| 4 | L3 `/silo-port` | [#55](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/55) | Add `.claude/commands/silo-port.md`. It implements the loop above and reuses weekly prompts 01 and 03 and the README prompt. Re-running it resumes at the first unticked item. |
| 5 | L5 Pilot | [#56](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/56) | Run the loop for scope triggers and DataGrip (33 web-backed candidates, none shared). Record the outcomes, the share of candidates that became rows, and the review corrections. The owner then decides: go, retune the thresholds, or stop. |
| 6 | L6 Rollout | [#57](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/57) | The loop runs the remaining products, the cross-product reports and the README. The LLM stays out of `run.sh`. |

- **Steps 1–4 (tools)** follow Plan 08's loop:
  - a code review before each merge;
  - every finding fixed or accepted by the owner;
  - checkboxes ticked on the branch.
- **Steps 5–6 (product runs)** also review content: every new or changed row is checked against its cited source.

## Input (from `reports/silo-candidates.md`)

- **239 candidates:**
  - **135** web-backed, in scope;
  - **104** backed only by repository or source documents, 100 of them on 3T products.
- **Web-backed candidates by product:**
  - DBeaver 34, DataGrip 33;
  - Compass 14, NoSQLBooster 14;
  - Studio 3T 10;
  - TablePlus 8, VisuaLeaf 8;
  - Navicat 7;
  - other 3T products 7.

## Owner decisions

1. **Runtime.** Decided: a Claude Code session running `/silo-port`, no API.
2. **The 104 private-source candidates.** Recommendation: a separate plan. That plan needs a rule for how private-source findings may be worded publicly, and no such rule exists yet.
3. **Access date for ✅.** Recommendation: accept the silo's retrieval date within a window the owner sets (for example 30 days); otherwise re-fetch the page live.
4. **Merging in the loop.** Recommendation: during the pilot, the loop waits for the owner to merge each PR. After the gate, the owner may grant standing approval once a review passes.

## Execution log

- 2026-09-26 — Draft written; approved and merged (#51); issues #52–#57 created.
- 2026-09-26 — Owner decisions:
  - two stages (`run.sh`, then a Claude Code command);
  - no API;
  - one product at a time;
  - a checklist file that the command loops over;
  - the loop ends with the README dashboard prompt.
- 2026-09-26 — Owner: "start step 1, non-stop till the end". Recorded as standing merge approval after each passing review for steps 1–4. The pilot (step 5) still stops at its go/no-go gate.
- 2026-09-26 — Step 1 (#52): `triage.tsv` ledger added and read by `candidates.py`.
  - Decided candidates are hidden; one re-opens when its Web count grows.
  - `needs-human` decisions stay listed.
  - A malformed ledger exits 2 before the silo is read.
  - The ledger starts empty, so the report's counts are unchanged.
