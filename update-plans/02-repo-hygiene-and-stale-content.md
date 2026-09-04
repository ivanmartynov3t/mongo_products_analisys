# Plan 2 — Repo Hygiene and Stale Content

## Objective

Fix five small, independent, low-risk problems that make the repository harder to navigate and trust, none of which require new research. Run this after Plan 1 lands (Plan 1 edits some of the same report files touched here).

## Task 1 — Fix the broken `next-feature-recommendation.md` link

`feature-dictionary.md`, `README.md`, and multiple files inside `research/feature-decision-2026/` (`01-research-plan.md`, `06-verification-notes.md`, `00-dialog-and-inputs.md`) all link to `reports/next-feature-recommendation.md`. That file does not exist in `reports/`. This is not a simple typo: `01-research-plan.md`'s own file map documents `reports/next-feature-recommendation.md` as the intended **Stage 5 final memo** — a finished deliverable that belongs in `reports/` (finished output) rather than `research/` (drafts/working notes), matching this repo's own reports-vs-research separation. The actual content was drafted directly under `research/feature-decision-2026/` instead, as `next-feature-recommendationv.1.0.md` and `next-feature-recommendationv.1.1.md`, and never copied/moved to its intended location.

Resolve it as a move, not a redirect:
1. Confirm `next-feature-recommendationv.1.1.md` is the current version (check its own header and `01-research-plan.md`'s file-status table for confirmation it's the latest revision, not v1.0).
2. Copy `research/feature-decision-2026/next-feature-recommendationv.1.1.md` to `reports/next-feature-recommendation.md` (this is the "finished memo" the rest of the repo already expects at that path — do not just link to the draft in place).
3. Add a one-line pointer at the top of `next-feature-recommendationv.1.1.md` noting it has been published as `reports/next-feature-recommendation.md` and that file is now the canonical version to link to; keep `v.1.0.md` and `v.1.1.md` in place under `research/` as the versioned drafts/history, per this repo's convention of not deleting superseded-but-cited research artifacts (see the `PROP-` retirement rule in `feature-dictionary.md`).
4. Leave every existing link exactly as `reports/next-feature-recommendation.md` — they were already pointing at the correct intended path; the bug was that nothing had been published there yet, not that the links were wrong.
5. Before finishing, check `01-research-plan.md` lines ~177–180 ("not yet synced to Stage 8" / "should be re-synced in a follow-up pass") against the actual content of v1.1 — if v1.1 already reflects the Stage 8 correction (e.g. `PROP-webhook-notify` already shown at 4.67, not 7.00), that stale warning note in `01-research-plan.md` should be updated to say the sync happened, rather than left implying the memo is still out of date.

After fixing, grep the full repo for the string `next-feature-recommendation.md` (without a version suffix) to confirm every reference now resolves to the real, newly-created `reports/next-feature-recommendation.md`.

## Task 2 — Remove committed `.DS_Store` files

Files: `products/.DS_Store`, `research/.DS_Store`, `.git/.DS_Store` (the last one is inside git's own internals — do not touch it directly; it is not a tracked repo file, ignore it).

- Delete `products/.DS_Store` and `research/.DS_Store` from the working tree and from git tracking (`git rm --cached` if they're tracked, then delete the file).
- Add `.DS_Store` to a repository `.gitignore` file at the repo root. If `.gitignore` does not exist, create it with at minimum `.DS_Store` as an entry.
- Do not add any other pattern to `.gitignore` beyond what this task needs unless a later plan specifically asks for it.

## Task 3 — Decide and act on `write_high_level.py`

`README.md` already documents that this script is stale, its embedded content has diverged from the hand-maintained `high-level-product-comparison.md`, and it must not be run to "sync." That leaves it as dead weight with no resolution. Apply this rule:

- Open the script and check whether it contains any content (feature descriptions, data points) that is **more accurate or more complete** than what's currently in `reports/comparisons/high-level-product-comparison.md`. If it does not (the expected case, given the README's own warning), delete the file.
- If it does contain something not yet captured elsewhere, extract only that specific content into the relevant hand-maintained `.md` file (with a source citation noting it came from the old generator script), then delete the script.
- Either way, remove the "STALE generator script" bullet from `README.md`'s repo map once the file is gone, and add one line to the Changelog table at the bottom of `feature-dictionary.md` if the deletion changes anything that table tracks (it likely doesn't — check before adding).

## Task 4 — Resolve the `visual-eaf` / "VisuaLeaf" naming mismatch

The product is branded "VisuaLeaf" everywhere in prose (README, product-report.md, feature-dictionary.md) but its directory and all its file paths use `visual-eaf`. This is not necessarily wrong — `products/README.md` documents that folder names are a path convention, not a branding decision — but it is undocumented as a deliberate choice, which makes it look like an error to anyone new to the repo.

- Do not rename the `products/third-party/visual-eaf/` directory or any file inside it. Renaming would break every existing relative link across `reports/`, `feature-dictionary.md`, and the product's own files, for a purely cosmetic gain.
- Instead, add one explicit sentence to `products/third-party/README.md` (next to the existing path-convention note) stating that `visual-eaf` is the folder slug for the product branded "VisuaLeaf," so a future agent doesn't "fix" the mismatch by renaming things.

## Task 5 — Fix stale product/matrix counts in `README.md`

`README.md`'s repository map and Products section were written before the 2026-07-29 product split and the resulting growth in feature-matrix files, and its own header note about the "28 vs 35" discrepancy still describes it as something to reconcile rather than something already reconciled.

- Count the actual current `feature-matrix.md` files under `products/` (expected: 35 as of this writing — 7 for MongoDB Compass, 11 for VisuaLeaf, 11 for Studio 3T, 2 for 3T Explore, 1 each for 3T MCP / 3TL Bridge / 3T Lens / 3T Access).
- Update every place in `README.md` that states a feature-matrix count to the real, freshly-counted number — do not copy the number from this plan without recounting, since Plan 4 (competitor expansion) or Plan 1 may have changed it by the time this runs.
- Update `reports/cumulative-report.md`'s "Current scope" table the same way, and remove its "stale" annotation once the number is corrected in place (don't leave a note saying a number is stale next to the now-correct number).

## Verification before marking this plan done

- `grep -r "next-feature-recommendation.md" .` (excluding `.git/`) returns only paths that actually exist, and `reports/next-feature-recommendation.md` itself exists with v1.1's content.
- `.DS_Store` no longer appears in `git ls-files`.
- `write_high_level.py` no longer exists at the repo root, and `README.md` no longer references it.
- `products/third-party/README.md` explicitly documents the `visual-eaf` / "VisuaLeaf" naming.
- `README.md` and `reports/cumulative-report.md` state the same, freshly-counted feature-matrix total.

## Execution log

(One line per session: date, what was fixed, what the recount found.)
