# Plan 09 — LLM-assisted data porting from prod_info_silo

This is part 2 of the silo porting. [Plan 08](08-silo-porting-mechanical.md) built the scripts that surface signals. This plan adds the judgement: whether a signal is a real capability, which ID it maps to, what status it gets, and which source backs it.

Measured 2026-09-26 at silo `55dbb2cb`. **Status: approved (2026-09-26); step 4 in review.** Issues #52–#57.

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
  - A product run edits only that product's files, plus:
    - the ledger, `decisions.tsv` and the checklist;
    - a new sub-feature ID in `feature-dictionary.md`;
    - the regenerated `reports/silo-candidates.md` and `reports/taxonomy-reconciliation.*`.
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
| 1 | L1 Triage ledger | [#52](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/52) | Add `tools/silo-candidates/triage.tsv`: product, tag, outcome, date, silo commit, `web_docs` (the candidate's Web count when decided), PR or reason. `candidates.py` hides decided candidates and re-opens one when its Web count rises above `web_docs`. |
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

## Progress

**State rule.** A box is ticked only after the item is done and verified. Tick it on the branch, in the same commit as the work. Tick a step's heading box only when all its sub-items are ticked. The merge checklist is Plan 08's, copied into each PR.

- [x] **Step 1 — L1** · [#52](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/52) · branch `feat/52-candidate-triage-ledger`
  - [x] Branch created from the latest `main`
  - [x] Implemented (issue scope only)
  - [x] New tests added; full suite passes locally
  - [x] Tool run against the real silo; summary in the PR
  - [x] Pull request opened: [#58](https://github.com/ivanmartynov3t/mongo_products_analisys/pull/58)
  - [x] Code review done; findings recorded on the PR (round 1: PASSED, 0 must fix · 5 should-fix · 8 nits)
  - [x] Findings fixed or accepted by the owner; re-review has no *must fix* left (round 2: PASSED, 0 must fix · 2 nits, fixed)
  - [x] Docs updated
  - [x] Merge checklist complete
  - [x] Owner approved the merge (standing approval for steps 1–4, see Execution log)
  - [x] Merged to `main` (squash `df06bfc`); branch deleted; issue closed with a result comment
- [x] **Step 2 — L4** · [#53](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/53) · branch `feat/53-porting-validator`
  - [x] Branch created from the latest `main`
  - [x] Implemented (issue scope only)
  - [x] New tests added; full suite passes locally
  - [x] Tool run against the real silo; summary in the PR
  - [x] Pull request opened: [#59](https://github.com/ivanmartynov3t/mongo_products_analisys/pull/59)
  - [x] Code review done; findings recorded on the PR (round 1: NOT PASSED, 5 must fix · 11 should-fix · 7 nits)
  - [x] Findings fixed or accepted by the owner; re-review has no *must fix* left (round 2: NOT PASSED, 1 must fix, fixed; round 3: PASSED)
  - [x] Docs updated
  - [x] Merge checklist complete
  - [x] Owner approved the merge (standing approval for steps 1–4, see Execution log)
  - [x] Merged to `main` (squash `2e10f8e`); branch deleted; issue closed with a result comment
- [x] **Step 3 — L2** · [#54](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/54) · branch `feat/54-evidence-batches`
  - [x] Branch created from the latest `main`
  - [x] Implemented (issue scope only)
  - [x] New tests added; full suite passes locally
  - [x] Tool run against the real silo; summary in the PR
  - [x] Pull request opened: [#60](https://github.com/ivanmartynov3t/mongo_products_analisys/pull/60)
  - [x] Code review done; findings recorded on the PR (round 1: PASSED, 0 must fix · 2 should-fix · 5 nits)
  - [x] Findings fixed or accepted by the owner; re-review has no *must fix* left (round 2: PASSED, 2 nits, fixed)
  - [x] Docs updated
  - [x] Merge checklist complete
  - [x] Owner approved the merge (standing approval for steps 1–4, see Execution log)
  - [x] Merged to `main` (squash `518eb96`); branch deleted; issue closed with a result comment
- [ ] **Step 4 — L3** · [#55](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/55) · branch `feat/55-silo-port-command`
  - [x] Branch created from the latest `main`
  - [x] Implemented (issue scope only)
  - [x] New tests added; full suite passes locally (a prompt has no unit tests; dry run instead)
  - [x] Tool run against the real silo; summary in the PR (dry run of the scope-triggers item)
  - [x] Pull request opened: [#61](https://github.com/ivanmartynov3t/mongo_products_analisys/pull/61)
  - [x] Code review done; findings recorded on the PR (round 1: NOT PASSED, 2 must fix · 4 should-fix · 3 nits)
  - [x] Findings fixed or accepted by the owner; re-review has no *must fix* left (round 2: PASSED, 3 minor points, fixed)
  - [x] Docs updated
  - [x] Merge checklist complete
  - [x] Owner approved the merge (standing approval for steps 1–4, see Execution log)
  - [ ] Merged to `main` (squash); branch deleted; issue closed with a result comment
- [ ] **Step 5 — L5 pilot** · [#56](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/56) · items in [`09-product-loop.md`](09-product-loop.md); stops at the owner's go/no-go gate
- [ ] **Step 6 — L6 rollout** · [#57](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/57) · items in [`09-product-loop.md`](09-product-loop.md)

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
- 2026-09-26 — Step 1 merged (#58, squash `df06bfc`) after two review rounds (both PASSED).
- 2026-09-26 — Step 2 (#53): `validate.py` added.
  - **Status labels.** The vocabulary was tested against all 780 capability rows on `main`. Only one legacy label is unrecognised ("Corrected — …"), and it is judged only if touched.
  - **Quote check.** A dry run treating every row as touched gave 32 quotes not found in their cited repository sources. The ones inspected were paraphrases or quotes of the dictionary; the dictionary is now accepted as a source.
  - **Access date.** Only its presence is checked; the window waits on owner decision 3.
- 2026-09-26 — Step 2 merged (#59, squash `2e10f8e`) after three review rounds (NOT PASSED, NOT PASSED, PASSED). Owner question: 47 of 86 silo repository and source folder names are treated as public because this repository already mentions them.
- 2026-09-26 — Step 3 (#54): `batch.py` added and run by `run.sh`. The real run wrote 13 batches with 135 candidates and 681 public pages (about 10 MB, gitignored).
- 2026-09-26 — Step 3 merged (#60, squash `518eb96`) after two review rounds (both PASSED).
- 2026-09-26 — Step 4 (#55): `.claude/commands/silo-port.md` added.
  - **Dry run** on the scope-triggers item in a throwaway worktree: 0 triggers fired, and the validator exited 0 with no findings. The branch was deleted and nothing was pushed.
  - **Merging.** The command stops after each PR's review unless this log records the owner's standing approval for the loop after the pilot gate.
