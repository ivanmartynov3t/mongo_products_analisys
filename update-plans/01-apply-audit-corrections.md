# Plan 1 — Apply Outstanding Audit Corrections

## Objective

`research/studio-3t-desktop-review-2026/12-consolidated-corrections.md` is a completed, cited, ready-to-apply correction set from a full source-code re-audit of Studio 3T Desktop. Its own closing section, "What downstream reports need," lists exactly which of four report files still need edits and what those edits are. None of that propagation work has been done yet. This plan is pure transcription against an already-approved source — do not re-derive findings, do not re-open the underlying research.

## Source of truth

Read `research/studio-3t-desktop-review-2026/12-consolidated-corrections.md` in full before starting. Its sections §1–§11 are the fact base; its closing "What downstream reports need" section (numbered 1–4) is the task list this plan turns into concrete edits. Cite this file (not the per-feature findings files) in every edit you make as a result of this plan, unless you need a specific number/quote, in which case cite the specific `0X-*-findings.md` file that number came from.

## Task 1 — `reports/gap-analysis-not-on-3t-products.md`

- Confirm the "Confirmed absent" count and table already read 9 (they do, as of this writing — verify before editing; if someone already applied this, skip to Task 2).
- If not already applied: change the "13 confirmed absent" language to 9, remove `SCHEMA-validation-model`, `SCHEMA-validation-strictness`, `SCHEMA-validation-ui`, `SCHEMA-deploy-validator`, `SCHEMA-validation-limits` from the confirmed-absent table (§2 of the corrections file), and add a one-line note in the "Takeaway" paragraph that validator authoring/deployment is confirmed present, not absent.
- Cross-check the "77 unverified" count: subtract the 5 IDs moved out of confirmed-absent only if they were previously double-counted as unverified elsewhere (they should not be — verify they don't appear twice in the file before changing the unverified count).

## Task 2 — `reports/gap-analysis-not-on-3t-desktop.md`

- Apply the same 13→9 F-SCHEMA correction as Task 1, scoped to this file's own tables/counts.
- Re-check the "17 present elsewhere in 3T family" bucket against §3 (F-SCHED items newly moved to confirmed-absent) and §4 (F-IDX items newly confirmed) of the corrections file — any ID that changed status in §3/§4 must be moved to the correct bucket in this file if it currently sits in the wrong one.
- Re-check the "78 unverified" figure against the same two sections for the same reason.

## Task 3 — `reports/comparisons/high-level-product-comparison.md`

Correct the Studio 3T row for each of the following feature areas, citing `12-consolidated-corrections.md` by section:

- F-AGG / F-QUERY: Visual Query Builder sync described as "bidirectional" → correct to "one-way handoff" (§6).
- F-SQL: any description implying a visual/drag-drop JOIN mapping editor → correct to plain-SQL-text single-equality joins only (§7).
- F-TRANSFER: masking op-type count "8" → 19; SQL migration dialect count "4" → 6, noting Sybase and IBM DB2 are both Enterprise-gated and asymmetric (§5).
- F-GOV: audit-logging description → narrow to Connection-Manager-actions-only, off-by-default, Windows-Group-Policy-enabled (§8). Remove any claim that the matrix "has not yet been authored" — it now has full 20-ID content.
- F-IDX: index copy-paste availability "all editions" → "Professional tier and above" (§4).
- F-AI: any claim that AI Helper is on-by-default or lower-friction than competitors on that basis → correct to opt-in as of release 2026.12.0 (§10).

## Task 4 — `reports/comparisons/low-level-feature-comparison.md`

This is the largest edit surface — row-level changes for every corrected or new sub-feature ID in §§1–11 of the corrections file.

1. Add one row for each of the 17 new sub-feature IDs listed in §1, with Studio 3T's status set per the corrections file and every other product's cell set to ❓ (unverified) unless that product's own `feature-matrix.md` already documents it independently — do not assume absence.
2. For every ID named in §§2–11 as corrected (not new), find its existing row and update the Studio 3T cell and any accompanying note to match the corrected finding. Use the exact section list in §§2–11 as your checklist — each one names the specific sub-feature ID(s) it affects.
3. Do not change any other product's column as part of this plan — those are out of scope for a Studio-3T-Desktop source-code audit.

## Verification before marking this plan done

- Every sub-feature ID named anywhere in `12-consolidated-corrections.md` §§1–11 appears, correctly, in `reports/comparisons/low-level-feature-comparison.md`.
- `reports/gap-analysis-not-on-3t-products.md` and `reports/gap-analysis-not-on-3t-desktop.md` both say 9, not 13, for the F-SCHEMA confirmed-absent count.
- `reports/comparisons/high-level-product-comparison.md`'s Studio 3T row contains no reference to "8 masking op types," "4 SQL dialects," "bidirectional VQB sync," "not yet authored" governance matrix, or unqualified "all editions" index copy-paste.
- Grep the whole `reports/` directory for the literal strings "8 op types", "four dialects" / "4 dialects", and "bidirectional" to catch any instance this task list missed.

## Execution log

- 2026-09-04 — Audited all four target files against `12-consolidated-corrections.md` §§1-11 before editing. Found Tasks 1-4 were **already applied** in a prior session (all four reports carry "Last reviewed: 2026-07-31" and the corrected figures/wording: 9 confirmed-absent F-SCHEMA IDs, 19 masking ops, 6 SQL dialects, one-way VQB handoff, narrowed audit-log scope, Professional-tier index copy-paste, all 17 new sub-feature IDs present in `low-level-feature-comparison.md`). Only gap found: `high-level-product-comparison.md`'s F-AI assessment lacked the AI-Helper-opt-in-by-default note that `low-level-feature-comparison.md` already carries — added it for consistency, citing §10.
- **Open issue found, not fixed by this plan (out of scope — would require new derivation, not transcription):** `reports/gap-analysis-not-on-3t-products.md`'s unverified count is internally consistent at **77** (verified by counting every row in its own tables), but `reports/gap-analysis-not-on-3t-desktop.md` still refers to "the companion report's 78" in two places (its §4 methodology note and its "Coverage accounting" section's 78−14−1−9=54 derivation) and its own accounting section's portfolio-wide "239 implemented" figure does not reconcile against the companion report's 328−9−77−17=225. Recommend a dedicated pass that re-derives both counts from the same row-level baseline rather than guessing at which side is stale — flagged here rather than silently resolved.
