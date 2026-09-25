# Plan 08 — Mechanical data porting from prod_info_silo

Research record and improvement plan for the **mechanical** (scripted) part of moving data from `prod_info_silo` into this repository. The LLM-assisted part (interpretation, mapping, clarification) is a separate, later plan.

Measured 2026-09-25 at silo commit `f1e28e8d` and `reports/review-queue.md`.

## Issues

| # | Proposal | Issue | Depends on |
|---|---|---|---|
| P1 | Make GitHub-repo citations checkable | [#33](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/33) | — |
| P2 | Silo snapshot report | [#34](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/34) | — |
| P3 | Automatic scope-trigger check | [#35](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/35) | P2 |
| P4 | Candidate-signal queue | [#36](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/36) | — |
| P5 | Evidence-gap report (seed proposals moved to a silo issue) | [#37](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/37) | — |
| P6 | Machine-readable silo pins | [#38](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/38) | — |
| P7 | Staleness queue for reports and research | [#39](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/39) | — |
| P8 | One weekly command | [#40](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/40) | P2, P3, P4 |
| P9 | Silo clean-up (prerequisite, not porting) | [prod_info_silo#45](https://github.com/ivanmartynov3t/prod_info_silo/issues/45) | — |
| — | Silo seed URLs for cited, compliant domains (split from P5; outside this plan) | [prod_info_silo#47](https://github.com/ivanmartynov3t/prod_info_silo/issues/47) | P5 |

**Scope (owner decision, 2026-09-26).** This plan covers only the **mechanical porting of data from the silo into this repository**. Changes that improve the silo itself are out of scope: P9 is finished only because it was nearly done and gives the porting a clean source; the silo seed-URL proposals that used to be part of P5 are a separate silo issue. The LLM part follows after this plan.

Order: P9 (finish, prerequisite) → porting core P2, P1, P6, P7, P3, P4 → P8 (one command) → P5 (gap report only).

## Rule for every proposal

No mechanical tool writes a capability status (✅/🧪/🗺️/❓/❌) into a matrix. Tools produce reports and queues; a human or the LLM step decides. Tools read the silo from git objects at a pinned ref, write only their configured output, and are deterministic and tested — the guarantees `tools/silo-review` already has.

## 1. Summary

- Only two scripts move silo data today, `silo-review` and `taxonomy-reconcile`. Both produce **checks and reports**; neither ports content.
- Everything else from the silo arrives **by hand**: prose citations in matrices and numbers copied into decision records.
- The weekly-maintenance prompts (`.github/prompts/weekly-maintenance/`) do not read the silo at all; they go to vendor websites directly.
- Result: the silo holds a large, classified corpus, but this repository uses little of it, and 72% of its citations cannot be checked against the silo.

## 2. What flows today

| Channel | Silo input | Tool | Output here | Automation |
|---|---|---|---|---|
| Staleness check | `.md` frontmatter (`source_url`, `checksum_sha256`, `http_last_modified`) + git history | `tools/silo-review/review.py` | `reports/review-queue.md` | Scripted, read-only, deterministic |
| Taxonomy match | `config/taxonomy.yaml`, `data/catalog_index.json` | `tools/taxonomy-reconcile/reconcile.py` | `reports/taxonomy-reconciliation.{md,tsv}` | Scripted; decisions entered by hand in `decisions.tsv` |
| Definition probes | silo corpus text | `tools/taxonomy-reconcile/probes.py` | evidence for decisions | Manual trigger |
| Citations in matrices | individual silo files | none | "silo copy … at commit …" in prose | Manual |
| Scope decisions | `products.yaml` status, doc counts | none | `docs/coverage-scope.md` | Manual; already stale (Policy Engine recorded 492 docs, now 529) |
| Weekly maintenance prompts | — | LLM prompts | matrices, reports | Do not use the silo |
| `source-extract` | private repository source | — | — | Reverted (`ac83447`); only an untracked `__pycache__` remains |

## 3. Silo data not used here

| Silo artefact | What it holds | Possible use |
|---|---|---|
| `catalog_index.json` → `by_product` sub-feature tags | classifier output per document | candidate matrix rows (P4) |
| `by_proposed_feature` | 10 `PROP-*` proposed features | the dictionary's Proposed Feature Registry |
| `by_dimension` | personas, deployment and licensing models, compliance standards | product reports, personas research |
| `config/products.yaml` | release status, track, seed URLs | scope decisions, dashboard, revisit triggers (P2, P3) |
| Per-product `README.md` / `DIFF.md` | silo dashboards and change lists | weekly "what changed" signal |
| `baseline_metrics.json` | per-product counts | dashboard (P2) |
| `repo_symbols_and_strings.json` (17 files) | code symbols and strings | source-code evidence for 3T products |

## 4. Effectiveness

**Citation coverage.** 677 distinct URLs are cited across 103 files; **486 (72%) are not checkable**.

| Domain | Not checkable | Why |
|---|---|---|
| mongodb.com | 65 | outside the silo's crawl scope |
| github.com | 55 | repo docs have no checksum in frontmatter, and URLs are SHA-pinned so they never match (P1) |
| reddit.com | 41 | not crawled; excluded by policy (ToS) |
| 3tsoftwarelabs.atlassian.net | 41 | internal Jira/Confluence, not crawled |
| forums, reviews, blogs | rest | not crawled |

**Matrices invisible to the staleness check.** 22 of 73 matrices cite no URL (mostly NoSQLBooster, TablePlus, Navicat); their sources are research files.

**Changes that reach no queue.** 19 cited URLs changed since review, yet the queue shows 0 stale matrices: the changes are cited only by reports and research, which are not queued (P7).

**Silo signals with no matrix row.** For the 13 analysed products that map to a silo slug, the silo tags **456** product × sub-feature signals (≥ 2 docs) that have no matrix row. Govern has no silo slug and is not counted. The classifier is noisy, so these are leads, not facts.

| Product | Silo docs | Silo-only signals | Matrix IDs |
|---|---|---|---|
| 3TL Bridge | 1,709 | 107 | 5 |
| 3T Lens | 533 | 63 | 1 |
| DBeaver | 814 | 61 | 37 |
| DataGrip | 1,033 | 46 | 16 |
| MongoDB Compass | 583 | 35 | 77 |
| Navicat | 15 | 10 | 93 |

3TL Bridge may be inflated by source documents it shares with Studio 3T EE (not verified). Navicat is the reverse case: the analysis goes far beyond what the silo holds.

## 5. Problems found

1. `data/3t/studio-3t/index.md` has held the License Manager page since `c7fd312a` (2026-09-14) — residue of prod_info_silo#44 not repaired by its fix (P9).
2. The silo's master `DIFF.md` reported "No Changes Detected" after the run that removed 4,979 files; cause not found (P9).
3. Repo-only products show `Last Retrieved: N/A` in the silo (P9).
4. Silo pins in matrices are prose, not machine-readable; re-pinning after #44 was manual (P6).
5. Scope triggers in `docs/coverage-scope.md` are checkable by script but are checked by hand (P3).

## 6. Proposals

| # | Proposal | Effect | Effort |
|---|---|---|---|
| P1 | Silo adds checksums to repo docs; `review.py` matches GitHub URLs by repo + path, ignoring the SHA | ~55 URLs become checkable, including Govern's internal sources | S + S |
| P2 | Generated `reports/silo-snapshot.{md,json}`: silo commit, per-product status, doc counts, last retrieved, seed URLs | one source for the README dashboard and scope decisions | S |
| P3 | Scope-trigger check on the snapshot | replaces a manual #18 step | S |
| P4 | Generated `reports/silo-candidates.md`: silo tags per product with no matrix row, filtered by doc count and probability | input queue for the LLM part | M |
| P5 | Evidence-gap report: no-URL matrices, thin products, cited domains the silo does not crawl (seed changes to the silo are a separate silo issue) | shows where the 72% comes from | S |
| P6 | `silo: <path>@<commit>` pins in Source index, plus a bulk re-pin tool | re-pinning becomes one command | M |
| P7 | Staleness queue also covers reports and research | surfaces the 19 hidden changes | S |
| P8 | `tools/silo-sync/run.sh` chaining the steps above | the Monday procedure becomes one local command | S |
| P9 | Silo clean-up (items 1–3 above, plus a filename ↔ `source_url` audit test). Prerequisite, not porting | a trustworthy source | S |

## 7. Hand-off to the LLM part

Scripts can surface signals (P4, P5, P7). Deciding whether a signal is a real capability, which sub-feature it maps to, what status it gets and how to word it with a source needs judgement. That is part 2, which should start from the P4 candidate queue.

## 8. Implementation plan

Each issue is fixed on its own branch and lands through its own pull request. **Nothing merges to `main` until its code review is done and every finding is either fixed or explicitly accepted by the owner.** This is a required condition, not a best effort.

### Order

Each step starts from an up-to-date `main` that already contains the previous merge.

| Step | Issue | Repo(s) | Branch | Why here |
|---|---|---|---|---|
| 1 | P9 | silo | `fix/45-silo-cleanup` | Prerequisite: clean source; nearly done |
| 2 | P2 | analysis | `feat/34-silo-snapshot` | Porting core: imports silo state; base for P3 and P8 |
| 3 | P1 | silo, then analysis | `feat/33-repo-doc-checksums` (silo), `feat/33-github-citations` (analysis) | Porting core: ~55 more citations checkable; silo side merges first |
| 4 | P6 | analysis | `feat/38-silo-pins` | Porting core: machine-readable pins that P7 and P4 can read |
| 5 | P7 | analysis | `feat/39-queue-reports-research` | Porting core: staleness for reports and research; `review.py` after P1 |
| 6 | P3 | analysis | `feat/35-scope-triggers` | Porting core: needs P2 |
| 7 | P4 | analysis | `feat/36-silo-candidates` | Porting core: input queue for the LLM part |
| 8 | P8 | analysis | `feat/40-silo-sync` | Chains P2, P3, P4, P7 into one command |
| 9 | P5 | analysis | `feat/37-evidence-gaps` | Gap report only; silo seed changes are out of scope |

### Per-issue loop

For every step:

1. **Branch** from the latest `main`.
2. **Implement** only what the issue asks. Follow the existing tool conventions: pinned git-object reads, guarded writes, deterministic output, a `plan` or `--check` mode that writes nothing.
3. **Test locally**: new tests for the change, and the full suite of the touched tool(s) and of the silo (`pytest`) must pass. CI is unavailable (no credits), so the PR description records the exact commands run and their results.
4. **Run the tool** against the real silo and attach a summary of its output (counts before and after) to the PR.
5. **Open the pull request** with: linked issue (`Closes #N`), what changed and why, test evidence, output evidence, and anything deliberately left out.
6. **Code review** (required):
   - review the full diff for correctness, edge cases, security (no tokens, credentials or private-repo text in output), OWASP-relevant input handling, and consistency with the repository's conventions and documentation;
   - check the documentation the change affects (tool README, `.github/copilot-instructions.md`, templates, this plan);
   - record the findings on the PR as a list, each marked *must fix* or *suggestion*.
7. **Fix the findings** on the same branch, one commit per finding or group; re-run tests and the tool; mark each finding fixed, or record the owner's decision to accept it.
8. **Re-review** the changed parts. Repeat 6–7 until no *must fix* finding remains.
9. **Owner approval**: the owner confirms the merge.
10. **Merge** to `main` (squash), delete the branch, close the issue with a short result comment.
11. **Update the state**: tick each finished sub-item in *Progress* below as it is done (not at the end in bulk).

### Merge checklist (every PR)

Copy into each PR description and tick there; the plan's *Merge checklist complete* item is ticked only when all of these are ticked.

- [ ] Only files in the issue's scope changed (`git diff --stat main...`)
- [ ] New and existing tests pass locally; commands and results are in the PR
- [ ] Tool run against the real silo; output summary in the PR
- [ ] Code review done; every *must fix* finding fixed; suggestions fixed or accepted by the owner
- [ ] Docs updated (tool README, conventions, this plan)
- [ ] No secrets, tokens, personal data or private-repository text in code, output or PR text
- [ ] Owner approved the merge

### Progress

**State rule (required).** A checkbox is ticked `[x]` only after that item is actually done and verified. Everything not yet done stays `[ ]`. Update this section in the same commit as the work it records, so the plan always shows the real state. Tick a step's heading box only when all its sub-items are ticked.

- [ ] **Step 1 — P9** · [prod_info_silo#45](https://github.com/ivanmartynov3t/prod_info_silo/issues/45) · branch silo `fix/45-silo-cleanup`
  - [x] Branch created from the latest `main`
  - [x] Implemented (issue scope only)
  - [x] New tests added; full suite passes locally (commands and results in the PR)
  - [x] Tool run against the real silo; before/after summary in the PR
  - [x] Pull request opened: PR link: [prod_info_silo#46](https://github.com/ivanmartynov3t/prod_info_silo/pull/46)
  - [x] Code review done; findings recorded on the PR (round 1: 4 must fix · 11 suggestions · 4 docs; round 2: 0 must fix · 8 suggestions, all applied; round 3: PASSED, 0 must fix · 10 suggestions, 7 fixed in `c950c1a4`, 3 await owner decision)
  - [x] All *must fix* findings fixed; tests re-run
  - [ ] Re-review: no *must fix* left; suggestions fixed or accepted by the owner
  - [x] Docs updated (tool README, conventions, this plan)
  - [ ] Merge checklist complete
  - [ ] Owner approved the merge
  - [ ] Merged to `main`; branch deleted; issue closed with a result comment

- [ ] **Step 2 — P2** · [#34](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/34) · branch `feat/34-silo-snapshot`
  - [x] Branch created from the latest `main`
  - [x] Implemented (issue scope only)
  - [x] New tests added; full suite passes locally (commands and results in the PR)
  - [x] Tool run against the real silo; before/after summary in the PR
  - [x] Pull request opened: PR link: [#41](https://github.com/ivanmartynov3t/mongo_products_analisys/pull/41)
  - [ ] Code review done; findings recorded on the PR (must fix: — · suggestions: —)
  - [ ] All *must fix* findings fixed; tests re-run
  - [ ] Re-review: no *must fix* left; suggestions fixed or accepted by the owner
  - [x] Docs updated (tool README, conventions, this plan)
  - [ ] Merge checklist complete
  - [ ] Owner approved the merge
  - [ ] Merged to `main`; branch deleted; issue closed with a result comment

- [ ] **Step 3 — P1** · [#33](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/33) · branch silo `feat/33-repo-doc-checksums`, then analysis `feat/33-github-citations`
  - [ ] Branch created from the latest `main`
  - [ ] Implemented (issue scope only)
  - [ ] New tests added; full suite passes locally (commands and results in the PR)
  - [ ] Tool run against the real silo; before/after summary in the PR
  - [ ] Pull request opened (silo): PR link: —
  - [ ] Silo PR merged before the analysis PR
  - [ ] Pull request opened (analysis): PR link: —
  - [ ] Code review done; findings recorded on the PR (must fix: — · suggestions: —)
  - [ ] All *must fix* findings fixed; tests re-run
  - [ ] Re-review: no *must fix* left; suggestions fixed or accepted by the owner
  - [ ] Docs updated (tool README, conventions, this plan)
  - [ ] Merge checklist complete
  - [ ] Owner approved the merge
  - [ ] Merged to `main`; branch deleted; issue closed with a result comment

- [ ] **Step 4 — P6** · [#38](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/38) · branch `feat/38-silo-pins`
  - [ ] Branch created from the latest `main`
  - [ ] Implemented (issue scope only)
  - [ ] New tests added; full suite passes locally (commands and results in the PR)
  - [ ] Tool run against the real silo; before/after summary in the PR
  - [ ] Pull request opened: PR link: —
  - [ ] Code review done; findings recorded on the PR (must fix: — · suggestions: —)
  - [ ] All *must fix* findings fixed; tests re-run
  - [ ] Re-review: no *must fix* left; suggestions fixed or accepted by the owner
  - [ ] Docs updated (tool README, conventions, this plan)
  - [ ] Merge checklist complete
  - [ ] Owner approved the merge
  - [ ] Merged to `main`; branch deleted; issue closed with a result comment

- [ ] **Step 5 — P7** · [#39](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/39) · branch `feat/39-queue-reports-research`
  - [ ] Branch created from the latest `main`
  - [ ] Implemented (issue scope only)
  - [ ] New tests added; full suite passes locally (commands and results in the PR)
  - [ ] Tool run against the real silo; before/after summary in the PR
  - [ ] Pull request opened: PR link: —
  - [ ] Code review done; findings recorded on the PR (must fix: — · suggestions: —)
  - [ ] All *must fix* findings fixed; tests re-run
  - [ ] Re-review: no *must fix* left; suggestions fixed or accepted by the owner
  - [ ] Docs updated (tool README, conventions, this plan)
  - [ ] Merge checklist complete
  - [ ] Owner approved the merge
  - [ ] Merged to `main`; branch deleted; issue closed with a result comment

- [ ] **Step 6 — P3** · [#35](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/35) · branch `feat/35-scope-triggers`
  - [ ] Branch created from the latest `main`
  - [ ] Implemented (issue scope only)
  - [ ] New tests added; full suite passes locally (commands and results in the PR)
  - [ ] Tool run against the real silo; before/after summary in the PR
  - [ ] Pull request opened: PR link: —
  - [ ] Code review done; findings recorded on the PR (must fix: — · suggestions: —)
  - [ ] All *must fix* findings fixed; tests re-run
  - [ ] Re-review: no *must fix* left; suggestions fixed or accepted by the owner
  - [ ] Docs updated (tool README, conventions, this plan)
  - [ ] Merge checklist complete
  - [ ] Owner approved the merge
  - [ ] Merged to `main`; branch deleted; issue closed with a result comment

- [ ] **Step 7 — P4** · [#36](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/36) · branch `feat/36-silo-candidates`
  - [ ] Branch created from the latest `main`
  - [ ] Implemented (issue scope only)
  - [ ] New tests added; full suite passes locally (commands and results in the PR)
  - [ ] Tool run against the real silo; before/after summary in the PR
  - [ ] Pull request opened: PR link: —
  - [ ] Code review done; findings recorded on the PR (must fix: — · suggestions: —)
  - [ ] All *must fix* findings fixed; tests re-run
  - [ ] Re-review: no *must fix* left; suggestions fixed or accepted by the owner
  - [ ] Docs updated (tool README, conventions, this plan)
  - [ ] Merge checklist complete
  - [ ] Owner approved the merge
  - [ ] Merged to `main`; branch deleted; issue closed with a result comment

- [ ] **Step 8 — P8** · [#40](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/40) · branch `feat/40-silo-sync`
  - [ ] Branch created from the latest `main`
  - [ ] Implemented (issue scope only)
  - [ ] New tests added; full suite passes locally (commands and results in the PR)
  - [ ] Tool run against the real silo; before/after summary in the PR
  - [ ] Pull request opened: PR link: —
  - [ ] Code review done; findings recorded on the PR (must fix: — · suggestions: —)
  - [ ] All *must fix* findings fixed; tests re-run
  - [ ] Re-review: no *must fix* left; suggestions fixed or accepted by the owner
  - [ ] Docs updated (tool README, conventions, this plan)
  - [ ] Merge checklist complete
  - [ ] Owner approved the merge
  - [ ] Merged to `main`; branch deleted; issue closed with a result comment

- [ ] **Step 9 — P5** · [#37](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/37) · branch `feat/37-evidence-gaps`
  - [ ] Branch created from the latest `main`
  - [ ] Implemented (issue scope only)
  - [ ] New tests added; full suite passes locally (commands and results in the PR)
  - [ ] Tool run against the real silo; before/after summary in the PR
  - [ ] Pull request opened: PR link: —
  - [ ] Code review done; findings recorded on the PR (must fix: — · suggestions: —)
  - [ ] All *must fix* findings fixed; tests re-run
  - [ ] Re-review: no *must fix* left; suggestions fixed or accepted by the owner
  - [ ] Docs updated (tool README, conventions, this plan)
  - [ ] Merge checklist complete
  - [ ] Owner approved the merge
  - [ ] Merged to `main`; branch deleted; issue closed with a result comment

### Risks

- **No CI.** Local test runs are the only gate; the PR must show them. Once billing is fixed, re-run CI on `main`.
- **Two repositories.** P1 lands in two PRs; the analysis-side PR must not merge before the silo-side one.
- **Shared files.** P1, P7 and P4 all touch `tools/silo-review/review.py`; the strict order above (P1 → P7 → P4) avoids conflicts.
- **P6 changes many matrices.** Its review must check that every migrated pin points at the same content as the prose it replaces. It now runs before P7 and P4, so those tools can read the pins from the start.

## Execution log

- 2026-09-25 — research done; plan written; issues #33–#40 and prod_info_silo#45 opened.
- 2026-09-25 — implementation plan (section 8) added with per-step checkboxes.
- 2026-09-26 — Step 1 (P9): PR prod_info_silo#46; review round 1 NOT PASSED (4 must fix), round 2 PASSED; suggestions applied. Owner request: silo pre-commit hook removed (classify + catalog stay in every workflow script).
- 2026-09-26 — Owner decision: plan scoped to mechanical porting silo → this repository. Steps reordered (P9 → P2 → P1 → P6 → P7 → P3 → P4 → P8 → P5). P5 reduced to the gap report; silo seed URLs moved to [prod_info_silo#47](https://github.com/ivanmartynov3t/prod_info_silo/issues/47). P9 kept as a prerequisite.
- 2026-09-26 — Step 2 (P2) started before step 1 merged (owner: continue). Snapshot at silo `f1e28e8d` still counts the stale License Manager page under Studio 3T; regenerate after prod_info_silo#46 merges.
- 2026-09-26 — Step 1 (P9): review round 3 PASSED (0 must fix). Docs/test suggestions fixed in `c950c1a4`; S1 code part, S3, S8 (pre-existing pipeline behaviour) await owner decision.
