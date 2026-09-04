# Step 1: Sub-Feature Primary-Source Verification Prompt

You are tasked with resolving 5 to 10 unverified sub-feature IDs during this session.

## Input Files to Read First
1. `/Users/ivan/Project/3t.tools.intellij/mongo_products_analisys/reports/gap-analysis-not-on-3t-products.md` (Check the "Unverified" sections).
2. `/Users/ivan/Project/3t.tools.intellij/mongo_products_analisys/feature-dictionary.md` (Lookup the official name and definition of the selected IDs).

## Selection Rule
Select exactly 5 to 10 sub-feature IDs marked `❓` in priority order:
- Priority 1: IDs cited in `feature-dictionary.md`'s `Proposed Feature Registry` under `🔗 Dictionary link`.
- Priority 2: IDs unverified across multiple competitors in `/Users/ivan/Project/3t.tools.intellij/mongo_products_analisys/reports/comparisons/low-level-feature-comparison.md`.
- Priority 3: First 5 sequential unverified IDs in `reports/gap-analysis-not-on-3t-products.md`.

## Crawling & Verification Boundaries (Strict Single-Domain Requests)
You are permitted to fetch ONLY the official vendor primary documentation URLs listed below. Do not click off-site links. Do not crawl forums, Reddit, or review aggregators.

### Vendor Documentation Whitelist:
1. **MongoDB Compass:**
   - Base URL: `https://www.mongodb.com/docs/compass/current/`
   - Navigation: Fetch ONLY the specific feature page (e.g., `/query/filter/`, `/indexes/`, `/security/`). Limit to 1 URL per sub-feature.
2. **VisuaLeaf:**
   - Features URL: `https://visualeaf.com/features`
   - Pricing/Tiers URL: `https://visualeaf.com/pricing`
   - Specific subpages: `https://visualeaf.com/features/sql-mode/`, `https://visualeaf.com/features/mongosync/`
3. **NoSQLBooster:**
   - Features URL: `https://nosqlbooster.com/features`
   - Edition Comparison: `https://nosqlbooster.com/compareEditions`
   - Release Notes: `https://nosqlbooster.com/releasenotes`
4. **DBeaver (MongoDB Extension):**
   - Documentation URL: `https://dbeaver.com/docs/dbeaver/Enterprise-Edition/`
5. **DataGrip (MongoDB Engine):**
   - JetBrains MongoDB Docs: `https://www.jetbrains.com/help/datagrip/mongodb.html`
6. **Navicat for MongoDB:**
   - Feature Matrix: `https://www.navicat.com/en/products/navicat-for-mongodb-feature-matrix`

## Allowed Status Values (Do Not Invent New Labels)
- `✅ confirmed` (Requires exact URL citation and access date).
- `❌ not supported` (Requires citation to explicit exclusion or omission in feature list).
- `❓ unverified` (If vendor page is inconclusive; MUST add a 1-line note: "Checked [URL] on [DATE]; no documentation of capability found.").

## Mandatory Output Edits
When an ID is resolved:
1. Open the specific product's `feature-matrix.md` under:
   `/Users/ivan/Project/3t.tools.intellij/mongo_products_analisys/products/<group>/<product-name>/features/<feature-folder>/feature-matrix.md`
   Update the row's Status, Behavior, and Source columns.
2. Proceed to `/Users/ivan/Project/3t.tools.intellij/mongo_products_analisys/.github/prompts/weekly-maintenance/03-sync-downstream-reports.prompt.md` to cascade.
