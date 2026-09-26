# Plan 09 — LLM-assisted data porting from prod_info_silo

Part 2 of the silo porting. [Plan 08](08-silo-porting-mechanical.md) built the mechanical part: scripts that surface signals. This plan covers the part that needs judgement. It decides whether a signal is a real capability, which sub-feature it maps to, what status it gets, and how to word it with a source.

**The flow (owner decision, 2026-09-26):**

1. **Mechanical stage.** Run `tools/silo-sync/run.sh`. It is deterministic and refreshes the reports and the local evidence batches.
2. **Claude stage.** Run `/silo-port` in Claude Code, not through the API. It loops over the products in [`09-product-loop.md`](09-product-loop.md), **one product at a time**. For each product it polishes the files from the reports, runs the validator, opens one PR, and ticks that product's checkbox.

Measured 2026-09-26 at silo commit `55dbb2cb` and `reports/silo-candidates.md`.

**Status: draft, awaiting owner review.** No issues are created yet.

## Issues

| # | Proposal | Issue | Depends on |
|---|---|---|---|
| L1 | Triage ledger: decided candidates leave the queue | TBD | — |
| L2 | Evidence batches: all silo documents per candidate, local only | TBD | — |
| L3 | `/silo-port` command: the product loop | TBD | L1, L2, L4 |
| L4 | Row validator, run before every PR | TBD | — |
| L5 | Pilot on one product, with a go/no-go gate | TBD | L1–L4 |
| L6 | Rollout: the loop runs over the remaining products | TBD | L5 |

**Scope.** The input is everything `run.sh` produces, per product:

| Report | What the Claude stage does for the product |
|---|---|
| `silo-candidates.md` (P4) | triage the **web-backed** candidates (§2) |
| `review-queue.md` (P7) | re-check rows and reports whose cited page changed since review |
| `silo-pins` re-pin plan (P6) | apply unchanged pins; re-check the rows behind changed ones |
| `evidence-gaps.md` (P5) | add a public URL source to a matrix that cites none, where the silo holds one |
| downstream | cascade the product's feature and product reports (prompt 03) |

Two items are repository-wide, not per product, so the loop handles each once:
- **First item: scope triggers.** A fired trigger may add or drop a product.
- **Second-to-last item: the cross-product reports.** These are the low-level comparison and gap analysis (prompt 03). They are cascaded once, after every product is merged.
- **Last item: the top-level `README.md` dashboard.** It is rebuilt with the existing prompt [`.github/prompts/update-readme-dashboard.prompt.md`](../.github/prompts/update-readme-dashboard.prompt.md), unchanged. That prompt reads this repository only, so it runs after every other item has merged and reflects the final state.

Out of scope:
- **Private-source candidates.** The 104 candidates backed only by repository or source documents are an owner decision (§6).
- **Silo seed URLs.** They stay with prod_info_silo#47.

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

- **Command.** `tools/silo-candidates/batch.py`, run by `run.sh` for every product. It is deterministic, so it belongs in the mechanical stage.
- **What it collects.** For each open candidate of the product:
  - every public silo document carrying the tag (not only the top 3 the report lists);
  - its URL, probability, retrieval date and `path@sha` pin;
  - the product's current matrix rows and the dictionary definition of the tag.
- **Where it writes.** Only a gitignored directory, `.local/silo-batches/`. Batches can be large and are working files, not reports.
- **Private documents.** Batches contain public pages only. Repository and source documents are left out, not just unnamed, so a batch is safe to paste into a session.

### L3 — `/silo-port` command (the product loop)

- **Files.**
  - `.claude/commands/silo-port.md`, a Claude Code slash command;
  - the checklist [`09-product-loop.md`](09-product-loop.md).

  The command reuses the existing prompts rather than copying them:
  - `weekly-maintenance/01` (verify);
  - `weekly-maintenance/03` (cascade);
  - `update-readme-dashboard.prompt.md` (the README, last item).
- **Loop.**
  1. Stop with a message if `run.sh` did not finish cleanly, or its reports are older than the silo ref.
  2. Take the first unticked product in the checklist.
  3. Create `port/<product>-<date>` from an up-to-date `main`.
  4. Work through the product's items in the checklist (the scope table above). Use only that product's batch and report sections.
  5. Run the validator (L4). Fix its findings or record them as `needs-human`.
  6. Tick the product's sub-items on the branch, only for items done and verified.
  7. Commit, push, and open one PR for the product.
  8. Review and merge, per owner decision 5.
  9. Tick the product and move on to the next one.

  The loop ends when every item is ticked, the README dashboard last. A product with nothing to do is ticked with "no changes" and gets no PR.
- **Why products run one after another.** Every product branch starts from a `main` that already holds the previous product's merge. That avoids conflicts in the checklist, the dictionary and the shared reports.
- **Outputs.**
  - **Matrix edits.** Rows added for `add-row`; rows re-checked from the review queue.
  - **Mapping decisions.** `decisions.tsv` entries for `existing-row`.
  - **Ledger.** One ledger row for every triaged candidate.
  - **Downstream cascade.** The product's feature and product reports.
- **Rules the command states.**
  - **Outcomes.** Use only the outcomes in §2.
  - **Statuses.** Use only the status rules above.
  - **IDs.** Prefer an existing dictionary ID; new IDs follow the dictionary's naming rules.
  - **Citations.** Cite the live URL in the Source index, plus the P6 pin: `` silo: `data/…/x.md@<sha>` ``.
  - **Quotes.** Quote the source verbatim in "Detailed behavior", as current matrices do.
  - **Bad captures.** A page captured as navigation or a cookie banner is `needs-human`, never ❌.
- **What the command may not do.**
  - Edit another product's files.
  - Change an existing row's status without a changed or new cited source.
  - Edit a generated file in `reports/` that a tool owns.
  - Patch `README.md` by hand; it is only rebuilt by its prompt, in the last item.
- **Resuming.** Re-running `/silo-port` continues from the first unticked product. A new cycle starts when the owner resets the checklist, for example after a weekly `run.sh` shows new work.

### L4 — Row validator

- **Command.** `tools/silo-candidates/validate.py`, run on the branch before a PR.
- **Checks.** For every added or changed matrix row and ledger entry:
  1. The ID exists in `feature-dictionary.md`, or is added by the same diff.
  2. The status is a legal label, and ✅/❌/❓ carry the fields the rule requires.
  3. Every `silo:` pin resolves at the pinned commit (reuses `tools/silo-pins`).
  4. Every quoted passage appears verbatim, whitespace-normalised, in the pinned document body. This catches invented quotes and badly captured pages.
  5. The diff names no host in `non_public_hosts` and no repository that is not public.
  6. Every candidate in the batch has exactly one ledger row.
  7. The diff touches only the current product's files, plus the ledger, `decisions.tsv` and the checklist. `README.md` may change only in the README item.
- **Exit codes.** Same contract as Plan 08: 0 clean, 1 needs a human, 2 error.
- **Tests.** Offline tests with throwaway git repositories.

### L5 — Pilot

- **Product.** DataGrip: 33 web-backed candidates, none shared, 16 matrix IDs today. The alternative is DBeaver (34, none shared).
- **Process.** Run the loop for two items only: the scope-trigger item, then DataGrip. Each gets its own PR, with human review.
- **What to record in the execution log:**
  - outcomes per type;
  - the share of candidates that became rows;
  - validator findings;
  - review corrections;
  - the time taken.
- **Gate.** The owner decides from the pilot whether to continue, retune `min_probability` or `min_docs`, or stop. No threshold is set in advance.

### L6 — Rollout

- **What runs.** `/silo-port` continues the loop over the remaining products in checklist order.
- **Weekly command.** The Claude stage stays **out of `tools/silo-sync/run.sh`**, because it is not deterministic. `run.sh` only refreshes the reports and batches, including the ledger-aware `candidates.py`.

## 4. Order

| Step | Issue | Branch | Why here |
|---|---|---|---|
| 1 | L1 | `feat/<n>-candidate-triage-ledger` | The queue must be able to shrink before anyone works it |
| 2 | L4 | `feat/<n>-porting-validator` | The guardrail exists before the first LLM edit |
| 3 | L2 | `feat/<n>-evidence-batches` | Input for the Claude stage; added to `run.sh` |
| 4 | L3 | `feat/<n>-silo-port-command` | Needs L1, L2 and L4 to test against |
| 5 | L5 | `port/<item>-<date>` | Go/no-go: scope triggers and DataGrip |
| 6+ | L6 | `port/<product>-<date>` | One per product, created by the loop |

The per-issue loop for L1–L4 is Plan 08's:
- one branch and one PR per issue;
- code review before every merge, with every finding fixed or explicitly accepted by the owner;
- re-review until nothing must be fixed;
- plan checkboxes ticked on the branch as work is done and verified.

For L5 and L6 the review also covers the **content**: every new or changed row is checked against its cited source.

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

1. **Runtime.** Decided (2026-09-26): a Claude Code session running `/silo-port`, no API.
2. **Access date for ✅.**
   - **The question:** does the silo's retrieval date count as the access date, or must the page be re-fetched live before a ✅?
   - **Recommendation:** accept the silo date when the page was retrieved within a window the owner sets (for example 30 days), and re-fetch otherwise. This decides whether the LLM can work from silo copies alone.
3. **The 104 repository/source-only candidates.**
   - **Recommendation:** defer them to a separate plan. Porting them needs a local-only view of private documents and a rule for how private-source findings may be worded in this public repository.
   - **Do not invent that rule here.** No such rule exists yet.
4. **Feedback to the silo classifier.** `noise` decisions could improve the silo's classifier. Plan 08 put silo improvements out of scope, so this plan only records them in the ledger.
   - **Recommendation:** keep feeding them back out of scope. Offer the ledger to the silo as a separate issue if wanted.
5. **Who merges a product PR inside the loop.**
   - **Recommendation:** during the pilot, the loop stops after opening each PR and waits for the owner to merge it.
   - **After the gate:** the owner may give standing approval to merge after the review passes, as in Plan 08.

## 7. Execution log

- 2026-09-26 — Draft written from `reports/silo-candidates.md` at silo `55dbb2cb`.
- 2026-09-26 — Owner decisions:
  - **Flow.** Two stages: `run.sh`, then a Claude Code command.
  - **Runtime.** No API.
  - **Pace.** One product at a time.
  - **Checklist.** A checkbox file lists the products, and the command loops over all of them.
  - **README.** The Claude stage ends by rebuilding the top-level `README.md` with the existing dashboard prompt.
