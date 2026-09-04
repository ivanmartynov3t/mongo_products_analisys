# Step 3: Cascading Downstream Reports Sync Prompt

You are tasked with cascading all product-level matrix changes made in Steps 1 and 2 into downstream roll-ups.
Never edit downstream comparison reports without first verifying the change exists in the product's own `feature-matrix.md`.

## File Update Sequence (Strict Order)

### 1. Master Low-Level Comparison
- Path: `/Users/ivan/Project/3t.tools.intellij/mongo_products_analisys/reports/comparisons/low-level-feature-comparison.md`
- Action:
  - Find the sub-feature ID row.
  - Update the product's cell using the canonical symbols: `✅`, `🧪`, `🗺️`, `❓`, `❌`, `💼`, `🏢`.
  - Update the citation column with the primary URL and access date.

### 2. High-Level Comparison (If Feature Area Overview Changed)
- Path: `/Users/ivan/Project/3t.tools.intellij/mongo_products_analisys/reports/comparisons/high-level-product-comparison.md`
- Action:
  - If a feature area moved from absent (`—`) to present (`✓`) or partial (`🧪`), update the "Product-level comparison" table.
  - If a major capability changed, update the product's summary paragraph in that feature section.

### 3. Gap Analysis Reports
- Portfolio Gap: `/Users/ivan/Project/3t.tools.intellij/mongo_products_analisys/reports/gap-analysis-not-on-3t-products.md`
- Desktop Gap: `/Users/ivan/Project/3t.tools.intellij/mongo_products_analisys/reports/gap-analysis-not-on-3t-desktop.md`
- Action:
  - If a 3T sub-feature was resolved:
    - If confirmed present: Remove ID from the "Unverified" table. Decrement the unverified count by the exact count removed.
    - If confirmed absent: Move ID from "Unverified" to "Confirmed absent". Increment absent count, decrement unverified count.
  - Re-verify counts: Count rows directly in the file. Do NOT guess or hand-decrement without counting.

### 4. Cumulative Report Scope Update
- Path: `/Users/ivan/Project/3t.tools.intellij/mongo_products_analisys/reports/cumulative-report.md`
- Action:
  - Update table in `## Current scope` if dictionary sub-feature totals or unverified counts changed.
  - Update `## Unverified items requiring follow-up` table if any of the tracked items were resolved.

### 5. Execution Logging
- Path: `/Users/ivan/Project/3t.tools.intellij/mongo_products_analisys/update-plans/03-resolve-unverified-subfeatures.md`
- Action: Append 1 line to `## Execution log`:
  `- YYYY-MM-DD — Resolved N IDs ([ID-1], [ID-2], ...) via [Vendor URL]. Unverified count updated to X.`
