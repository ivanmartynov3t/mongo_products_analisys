# Weekly Maintenance Orchestrator Prompt

You are an automated agent performing weekly maintenance on the `mongo_products_analisys` repository.
You must execute the weekly maintenance checklist in strict sequential order. Do not skip steps. Do not modify source code outside this repository.

## Absolute Paths in Repository
- Root: `/Users/ivan/Project/3t.tools.intellij/mongo_products_analisys`
- Unified Feature Dictionary: `/Users/ivan/Project/3t.tools.intellij/mongo_products_analisys/feature-dictionary.md`
- Master Comparison Table: `/Users/ivan/Project/3t.tools.intellij/mongo_products_analisys/reports/comparisons/low-level-feature-comparison.md`
- High-level Comparison: `/Users/ivan/Project/3t.tools.intellij/mongo_products_analisys/reports/comparisons/high-level-product-comparison.md`
- Portfolio Gap Analysis: `/Users/ivan/Project/3t.tools.intellij/mongo_products_analisys/reports/gap-analysis-not-on-3t-products.md`
- Desktop Gap Analysis: `/Users/ivan/Project/3t.tools.intellij/mongo_products_analisys/reports/gap-analysis-not-on-3t-desktop.md`
- Cumulative Report: `/Users/ivan/Project/3t.tools.intellij/mongo_products_analisys/reports/cumulative-report.md`
- Plan 3 Execution Log: `/Users/ivan/Project/3t.tools.intellij/mongo_products_analisys/update-plans/03-resolve-unverified-subfeatures.md`

## Weekly Execution Sequence
1. Run Step 1: `/Users/ivan/Project/3t.tools.intellij/mongo_products_analisys/.github/prompts/weekly-maintenance/01-verify-subfeatures.prompt.md`
   - Target scope: resolve a batch of exactly 5 to 10 sub-feature IDs marked unverified.
2. Run Step 2: `/Users/ivan/Project/3t.tools.intellij/mongo_products_analisys/.github/prompts/weekly-maintenance/02-competitor-releases.prompt.md`
   - Target scope: scan competitor release notes across all available releases (no 30-day limit).
3. Run Step 3: `/Users/ivan/Project/3t.tools.intellij/mongo_products_analisys/.github/prompts/weekly-maintenance/03-sync-downstream-reports.prompt.md`
   - Target scope: cascading matrix -> comparison -> gap analysis sync.
4. Run Verification:
   - Run `git diff --stat` to verify only intended files were modified.
   - Append date and summary entry to `## Execution log` in `/Users/ivan/Project/3t.tools.intellij/mongo_products_analisys/update-plans/03-resolve-unverified-subfeatures.md`.
