# Plan 5 — Advance the Feature-Decision Pipeline

## Objective

`feature-dictionary.md`'s Proposed Feature Registry tracks 20 `PROP-` candidates for "what should Studio 3T Desktop build next." Several sit in `Shortlisted` with no forward motion documented, and a queued follow-up research plan (`research/feature-decision-2026/07-v1.1-research-plan.md`) has not been executed. This plan closes that gap.

## Before starting

Read, in order: `feature-dictionary.md`'s full Proposed Feature Registry section (including the classification legend), `research/feature-decision-2026/01-research-plan.md` (the scoring rubric — Priority Score = (Evidence Strength + Reach + Severity + Competitive Urgency) / Build Effort), `research/feature-decision-2026/07-v1.1-research-plan.md`, and both recommendation memos (`next-feature-recommendationv.1.0.md`, `next-feature-recommendationv.1.1.md`).

## Task 1 — Execute the v1.1 research plan

`07-v1.1-research-plan.md` defines a specific next research step (read it for the exact scope — this plan does not restate its contents, since restating a plan invites drift from what it actually says). Execute exactly what it specifies, no more:

- Do not re-score candidates that plan doesn't ask you to re-score.
- Do not add new `PROP-` candidates unless the v1.1 plan explicitly calls for candidate discovery, not just re-verification of existing ones.
- Record findings in a new dated file under `research/feature-decision-2026/` following the existing numbering convention (the next unused number after `07-v1.1-research-plan.md`).

## Task 2 — Move Shortlisted candidates forward

For each `PROP-` candidate currently in `Shortlisted` status in `feature-dictionary.md`'s registry table (`PROP-webhook-notify`, `PROP-idx-perf-advisor`, `PROP-qe-key-vault-ui` as of this writing — recheck the live table, it may have changed):

1. Check whether Task 1's v1.1 research plan execution produced new evidence for that specific candidate. If yes, use it.
2. If a candidate has had no new evidence in more than one research pass (check the dictionary's Changelog table and the candidate's own citation trail in `04-scored-longlist.md` for dates) and none is available from Task 1 either, do not leave it silently Shortlisted — apply this rule: move it to `Deferred` with a one-sentence reason ("no new evidence surfaced in the v1.1 pass; revisit in the next full feature-decision cycle"), rather than letting it accumulate in Shortlisted indefinitely with no audit trail of why.
3. If new evidence changes a candidate's Priority Score, recompute it using the exact rubric formula from `01-research-plan.md` — do not eyeball a new score.

## Task 3 — Reconcile `PROP-webhook-notify`'s known-stale note

The registry table's `PROP-webhook-notify` row already documents a corrected score with a strikethrough (`~~7.00~~ → 4.67`) and cites `04-scored-longlist.md`. Check whether that candidate's `Shortlisted` status itself should also be reconsidered given the corrected (lower) score, using the same rubric-driven comparison against other Shortlisted/Cut candidates' scores — a status correction should follow from the score correction, it should not have been silently skipped when the score was fixed.

## Task 4 — Update the registry and changelog

- Update `feature-dictionary.md`'s Proposed Feature Registry table with every status/score change from Tasks 1–3.
- Add one row to `feature-dictionary.md`'s Changelog table (bottom of file) summarizing what changed and why, in the same style as the existing 2026-07-31/2026-07-30/2026-07-29 entries — cite the specific research file(s) that justified each change, exactly as those existing entries do.
- If any candidate reaches `Recommended` status as a result of this plan, that is a signal for a separate, human-owned decision (whether to actually build it) — do not take any action beyond updating its status and citing the evidence. Building the feature is out of scope for this repository entirely (it's an analysis repo, not the product codebase).

## What NOT to do

- Do not change the Priority Score formula itself — that's a methodology change requiring its own explicit decision, not something to slip in while updating scores.
- Do not retroactively edit `04-scored-longlist.md`'s historical entries — add corrections as new dated notes, following the pattern already used for the `PROP-webhook-notify` correction, so the original scoring reasoning stays visible.
- Do not mark a `Cut` candidate as anything else without new evidence — `Cut` is not meant to be revisited casually.

## Verification before marking this plan done

- No `PROP-` row is `Shortlisted` without either a same-session evidence update or an explicit, dated `Deferred` reason.
- Every changed Priority Score is traceable to the rubric formula applied to specific, cited evidence.
- `feature-dictionary.md`'s Changelog table has a new entry matching what this plan actually changed.

## Execution log

(One line per session: date, which candidates moved status, what the v1.1 research plan execution found.)
