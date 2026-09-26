# Plan 09 — LLM-assisted data porting from prod_info_silo

Part 2 of the silo porting. [Plan 08](08-silo-porting-mechanical.md) built the mechanical part: scripts that surface signals. This plan covers the part that needs judgement. It decides whether a signal is a real capability, which sub-feature it maps to, what status it gets, and how to word it with a source.

Measured 2026-09-26 at silo commit `55dbb2cb` and `reports/silo-candidates.md`.

**Status: draft, awaiting owner review.** No issues are created yet.

## Issues

| # | Proposal | Issue | Depends on |
|---|---|---|---|
| L1 | Triage ledger: decided candidates leave the queue | TBD | — |
| L2 | Evidence batches: all silo documents per candidate, local only | TBD | — |
| L3 | Porting prompt | TBD | L1, L2 |
| L4 | Row validator, run before every PR | TBD | — |
| L5 | Pilot on one product, with a go/no-go gate | TBD | L1–L4 |
| L6 | Rollout, product by product (web-backed candidates only) | TBD | L5 |

**Scope.** The input is the P4 queue, `reports/silo-candidates.md`, as Plan 08 §7 set it. Only its **135 web-backed candidates** are in scope. The other signals stay where they are:
- P5 evidence gaps go to prod_info_silo#47.
- P7 stale sources go to weekly prompt 01.
- The 104 candidates backed only by repository or source documents are an owner decision (§6).

## Rule for every proposal

Plan 08's rule was that no tool writes a capability status. This plan relaxes it in one way only:

> **The LLM may draft a matrix edit, including a status. A human approves it in the pull request. Nothing reaches `main` without that review.**

Everything else carries over unchanged:

- **Reading the silo.** The silo is read from git objects at a pinned ref, never checked out or written.
- **Outputs.** Every step declares the files it may touch.
- **Evidence.** Silo detection and classifier probability are never evidence for a status; the feature dictionary already states this. Evidence is the text of a source document, cited by its URL.
- **Status labels.** The existing rules apply (weekly prompt 01):
  - ✅ needs an exact URL and an access date;
  - ❌ needs an explicit exclusion in the source;
  - ❓ needs a note "Checked [URL] on [DATE]; no documentation of capability found."

  No new labels.
- **Missing tags are not evidence.** The report's "Matrix IDs the silo never tags" list must never drive a ❌ or a row removal. Matrices already omit rows when a source is silent (for example, DataGrip connectivity).
- **Public repository.** No private repository name, private document path or private content may appear in any file, commit, issue or PR.

## 1. Input

From `reports/silo-candidates.md` at `55dbb2cb`:

| | Candidates |
|---|---|
| Total | 239 |
| Web-backed (at least one public page) | 135 |
| Only repository or source documents | 104 |
| Mostly shared with another silo product | 93 |

The web-backed candidates are concentrated in third-party products:

| Product | Web-backed |
|---|---|
| DBeaver | 34 |
| DataGrip | 33 |
| MongoDB Compass | 14 |
| NoSQLBooster | 14 |
| Studio 3T | 10 (6 mostly shared) |
| TablePlus, VisuaLeaf | 8 each |
| Navicat | 7 |
| 3T products other than Studio 3T | 7 |

The 104 repository/source-only candidates are almost all on 3T products: 3TL Bridge 60, 3T Lens 27, 3T Access 6, 3T Explore 4, MongoDB Compass 4, 3T MCP 3.

## 2. Outcomes

Each candidate gets exactly one outcome, recorded in the ledger (L1):

| Outcome | Meaning | Where it lands |
|---|---|---|
| `add-row` | A source shows the capability, a limitation or an explicit absence | new row in the product's matrix |
| `existing-row` | An existing row already covers it under another ID | a mapping decision in `tools/taxonomy-reconcile/decisions.tsv`, not an ad hoc edit |
| `other-product` | The evidence belongs to another product (see the Shared column) | ledger note; the other product's queue |
| `noise` | The classifier tagged it, but the documents do not describe the capability | ledger only |
| `needs-human` | The evidence is ambiguous, a page was captured badly, or a private source would be needed | ledger, with a reason |

## 3. Steps

### L1 — Triage ledger

- **The ledger file.** Add `tools/silo-candidates/triage.tsv` with one row per decided candidate:
  - product;
  - silo tag;
  - outcome;
  - date;
  - the silo commit the decision was made at;
  - the PR or a one-line reason.
- **Reading the ledger.** `candidates.py` reads it:
  - decided candidates leave the main tables;
  - a count per outcome appears in the summary.
- **Re-opening.** A decided candidate comes back if its web-document count has grown since the decision's silo commit.
- **Why this step comes first.** Without the ledger the queue never shrinks, and `noise` decisions get reviewed again every week.
- **Tests.** Offline tests, as in Plan 08. Deterministic output.

### L2 — Evidence batches

- **Command.** `tools/silo-candidates/batch.py <product>`.
- **What it collects.** For each open candidate of the product:
  - every public silo document carrying the tag (not only the top 3 the report lists);
  - its URL, probability, retrieval date and `path@sha` pin;
  - the product's current matrix rows and the dictionary definition of the tag.
- **Where it writes.** Only a gitignored directory, `.local/silo-batches/`. Batches can be large and are working files, not reports.
- **Private documents.** Batches contain public pages only. Repository and source documents are left out, not just unnamed, so a batch is safe to paste into a session.

### L3 — Porting prompt

- **File.** `.github/prompts/silo-porting/porting.prompt.md`, in the style of the weekly-maintenance prompts.
- **Input.** One batch (L2) per session.
- **Output.**
  - matrix edits for `add-row`;
  - `decisions.tsv` entries for `existing-row`;
  - ledger rows for every candidate in the batch.
- **Rules the prompt states.**
  - **Outcomes.** Use only the outcomes in §2.
  - **Statuses.** Use only the status rules above.
  - **IDs.** Prefer an existing dictionary ID; new IDs follow the dictionary's naming rules.
  - **Citations.** Cite the live URL in the Source index, plus the P6 pin: `` silo: `data/…/x.md@<sha>` ``.
  - **Quotes.** Quote the source verbatim in "Detailed behavior", as current matrices do.
  - **Bad captures.** A page captured as navigation or a cookie banner is `needs-human`, never ❌.
  - **Cascade.** Run prompt 03 for the downstream reports afterwards, or state in the PR that the cascade is deferred.
- **What the prompt may not do.** Edit rows outside the batch's candidates, or change the status of an existing row.

### L4 — Row validator

- **Command.** `tools/silo-candidates/validate.py`, run on the branch before a PR.
- **Checks.** For every added or changed matrix row and ledger entry:
  1. The ID exists in `feature-dictionary.md`, or is added by the same diff.
  2. The status is a legal label, and ✅/❌/❓ carry the fields the rule requires.
  3. Every `silo:` pin resolves at the pinned commit (reuses `tools/silo-pins`).
  4. Every quoted passage appears verbatim, whitespace-normalised, in the pinned document body. This catches invented quotes and badly captured pages.
  5. The diff names no host in `non_public_hosts` and no repository that is not public.
  6. Every candidate in the batch has exactly one ledger row.
- **Exit codes.** Same contract as Plan 08: 0 clean, 1 needs a human, 2 error.
- **Tests.** Offline tests with throwaway git repositories.

### L5 — Pilot

- **Product.** DataGrip: 33 web-backed candidates, none shared, 16 matrix IDs today. The alternative is DBeaver (34, none shared).
- **Process.** Run L2 → L3 → L4 end to end. One PR with human review, like every step.
- **What to record in the execution log:**
  - outcomes per type;
  - the share of candidates that became rows;
  - validator findings;
  - review corrections;
  - the time taken.
- **Gate.** The owner decides from the pilot whether to continue, retune `min_probability` or `min_docs`, or stop. No threshold is set in advance.

### L6 — Rollout

- **Pace.** One product per branch and PR, in queue order: DBeaver, MongoDB Compass, NoSQLBooster, Studio 3T, TablePlus, VisuaLeaf, Navicat, then the web-backed 3T candidates.
- **Scope of each PR.** The matrix edits, the ledger rows and the downstream cascade, or an explicit deferral.
- **Weekly command.** The LLM step stays **out of `tools/silo-sync/run.sh`**, because it is not deterministic. The weekly command only runs the ledger-aware `candidates.py`, so new candidates show up and decided ones stay hidden.

## 4. Order

| Step | Issue | Branch | Why here |
|---|---|---|---|
| 1 | L1 | `feat/<n>-candidate-triage-ledger` | The queue must be able to shrink before anyone works it |
| 2 | L4 | `feat/<n>-porting-validator` | The guardrail exists before the first LLM edit |
| 3 | L2 | `feat/<n>-evidence-batches` | Input for the prompt |
| 4 | L3 | `feat/<n>-porting-prompt` | Needs L1, L2 and L4 to test against |
| 5 | L5 | `feat/<n>-pilot-datagrip` | Go/no-go |
| 6+ | L6 | `feat/<n>-port-<product>` | One per product, after the gate |

The per-issue loop is Plan 08's:
- one branch and one PR per issue;
- code review before every merge, with every finding fixed or explicitly accepted by the owner;
- re-review until nothing must be fixed;
- plan checkboxes ticked on the branch as work is done and verified.

For L5 and L6 the review also covers the **content**: every new row is checked against its cited source.

## 5. Risks

| Risk | Mitigation |
|---|---|
| Invented or paraphrased evidence | L4 check 4 (verbatim quote in the pinned document); human review |
| Silo absence read as product absence | Rule above; L3 forbids ❌ without an explicit exclusion |
| Classifier noise inflating matrices | `noise` outcome; L5 gate; thresholds tunable by the owner |
| Private content leaking into the public repository | L2 excludes private documents; L4 check 5; 104 repo-only candidates out of scope |
| Wrong product (content indexed under several silo products) | Shared column; `other-product` outcome |
| Silo copy is stale at review time | Access-date rule (owner decision 2); the P7 staleness queue picks up later changes |

## 6. Owner decisions needed

1. **Runtime.**
   - **Recommendation:** a Claude Code session driven by the L3 prompt, with L2 and L4 as scripted checks before and after.
   - **Why:** it needs no API key and matches how this repository is maintained today.
   - **Alternative:** an API-driven script. It is more reproducible, but brings key handling, cost control and a new dependency.
2. **Access date for ✅.**
   - **The question:** does the silo's retrieval date count as the access date, or must the page be re-fetched live before a ✅?
   - **Recommendation:** accept the silo date when the page was retrieved within the last 30 days, and re-fetch otherwise. This decides whether the LLM can work from silo copies alone.
3. **The 104 repository/source-only candidates.**
   - **Recommendation:** defer them to a separate plan. Porting them needs a local-only view of private documents and a rule for how private-source findings may be worded in this public repository.
   - **Do not invent that rule here.** No such rule exists yet.
4. **Feedback to the silo classifier.** `noise` decisions could improve the silo's classifier. Plan 08 put silo improvements out of scope, so this plan only records them in the ledger.
   - **Recommendation:** keep feeding them back out of scope. Offer the ledger to the silo as a separate issue if wanted.

## 7. Execution log

- 2026-09-26 — Draft written from `reports/silo-candidates.md` at silo `55dbb2cb`.
