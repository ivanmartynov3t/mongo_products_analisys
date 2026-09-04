# Update Plans — Overview & Master Sequencing

## Who this is for

An agent that executes literal, explicit instructions well but should not be trusted to infer intent, resolve ambiguity, or invent conventions. Every plan file in this folder is written so that agent can pick it up cold and finish it without asking "what did you mean." Where a step requires judgment, the plan states the exact rule to apply instead of asking the agent to use discretion.

## Ground rules for every plan (read once, apply to all six)

1. Before touching anything, read, in order: `.github/copilot-instructions.md`, `feature-dictionary.md`, `README.md`. These define the non-negotiable structure (Feature IDs, folder names, confirmed/roadmap/unverified labeling, mandatory Navigation sections). Nothing in these plans overrides them; if a plan step and `copilot-instructions.md` conflict, `copilot-instructions.md` wins and the conflict must be reported, not silently resolved.
2. Never invent a Feature ID or sub-feature ID. If a step needs one that does not exist in `feature-dictionary.md`, add it to the dictionary first (Sub-feature registry, correct feature section, next free ID following the existing `<FEATURE>-<suffix>` pattern), then use it.
3. Every factual claim added or changed must cite a source: either an existing repo file (path + section) or an external primary source (vendor doc/pricing page URL + access context). "Unverified" is an acceptable and expected status — do not upgrade something to confirmed without a citation.
4. Use the existing icon/label vocabulary exactly as defined in `reports/comparisons/low-level-feature-comparison.md`'s legend (✅ confirmed · 🧪 partial/limited · 🗺️ roadmap · ❓ unverified · ❌ not supported · 💼 paid-tier · 🏢 enterprise-tier) and the confirmed/roadmap/unverified/absent vocabulary elsewhere. Do not introduce new status words.
5. Every new or rewritten file must include a `Navigation` section with relative links to: the relevant product report, the relevant feature matrix/report, `feature-dictionary.md`, and the relevant comparison report(s) — copy the pattern from an existing file of the same type rather than composing one from scratch.
6. Do not run `write_high_level.py` under any circumstances (see Plan 02) and do not treat any content inside it as authoritative.
7. Do not touch anything under `product-suite/` or any path outside this repository.
8. After finishing a plan, append one line to that plan file's own "Execution log" section (add one if it doesn't exist) with the date and a one-sentence summary of what was actually done — this repo's convention (see the Changelog table at the bottom of `feature-dictionary.md`) is to log changes at the point of change, not to silently overwrite history.
9. One plan, one commit (or one PR). Do not mix work from two plan files in the same commit — it makes the per-plan execution log meaningless and makes a bad edit harder to isolate and revert.

## The six plans

| # | File | What it does | Depends on |
|---|---|---|---|
| 1 | `01-apply-audit-corrections.md` | Propagate the already-written, already-cited corrections in `research/studio-3t-desktop-review-2026/12-consolidated-corrections.md` into the four downstream reports that don't have them yet. Pure transcription against an existing source — no new research. | none |
| 2 | `02-repo-hygiene-and-stale-content.md` | Fix the broken `next-feature-recommendation.md` link, remove committed `.DS_Store` files, decide and act on `write_high_level.py`'s fate, resolve the `visual-eaf`/"VisuaLeaf" naming mismatch, fix the stale product/matrix counts in `README.md`. | Should run after Plan 1 (Plan 1 changes some of the same report files; doing hygiene first would create merge noise) |
| 3 | `03-resolve-unverified-subfeatures.md` | Systematically drive down the 77 unverified 3T-portfolio sub-feature IDs (and the comparable unverified set for Compass/VisuaLeaf) via primary-source research, with a defined stopping rule. | Should run after Plan 1 (Plan 1 changes several rows this plan would otherwise research redundantly) |
| 4 | `04-extend-competitor-coverage.md` | Build structured `products/third-party/` entries (product-report + feature matrices/reports) for DBeaver, DataGrip, Navicat, NoSQLBooster, and TablePlus from the existing raw research in `research/google_research/`, and fold them into the dictionary coverage matrix and comparison reports. | Independent of 1–3; can run in parallel once Plan 1 has landed (shares comparison-report files with Plan 1, so sequence after it to avoid conflicts) |
| 5 | `05-advance-feature-decision-pipeline.md` | Execute `research/feature-decision-2026/07-v1.1-research-plan.md` and move the Shortlisted `PROP-` candidates in `feature-dictionary.md`'s Proposed Feature Registry to their next pipeline state. | Independent |
| 6 | `06-retire-or-rewrite-methodology-docs.md` | Make and execute an explicit decision on the three non-compliant `research/` methodology documents (rewrite compliant, mark permanently archival, or delete) instead of leaving them in permanent limbo. | Independent |

## Recommended execution order

1. **Plan 1** first, always — it is pure transcription of already-approved corrections, touches the core comparison/gap reports, and every other plan that reads those reports (3, 4) benefits from starting off a corrected baseline instead of a stale one.
2. **Plan 2** next — cheap, low-risk, removes noise (dead link, `.DS_Store`, naming) before more content lands on top of it.
3. **Plan 4** and **Plan 5** can run in parallel with each other and with Plan 3 (different files, different subject matter) once Plans 1–2 are merged.
4. **Plan 3** last among the content plans, since it is open-ended (bounded by its own stopping rule, not by a fixed task list) and benefits most from a stable, corrected, hygienic baseline.
5. **Plan 6** can run whenever — it has no file overlap with the others — but do it before anyone tries to actually execute the metrics-gathering framework described in those documents, since right now doing so would violate the ToS constraints already documented in `README.md`.

## Definition of done for the whole batch

- All four files named in `12-consolidated-corrections.md`'s "What downstream reports need" section reflect its §§1–11.
- `README.md`'s repo map and scope figures match the real file counts.
- No link in `README.md` or `feature-dictionary.md` points to a nonexistent file.
- No `.DS_Store` file is tracked by git; a `.gitignore` entry prevents recurrence.
- `write_high_level.py` is either deleted with its content's still-useful pieces (if any) merged into the hand-maintained file, or explicitly archived with a header explaining why it's kept.
- `products/third-party/` has an entry for every one of the seven direct-competitor reports in `research/google_research/` that has enough source material to support one (DBeaver, DataGrip, MongoDB Compass [already done], Navicat, NoSQLBooster, TablePlus — 5 new), each following the same product-report + feature-matrix/feature-report structure as the existing two.
- `feature-dictionary.md`'s Proposed Feature Registry has no candidate stuck in "Shortlisted" without a dated note on why it hasn't moved.
- The three methodology documents in `research/` each carry an explicit, dated disposition decision at the top of the file (not just the existing "unconfirmed origin" flag).

## Execution log

(Add one line per completed plan, e.g. `2026-08-12 — Plan 1 completed: all four reports updated per 12-consolidated-corrections.md §§1-11.`)
