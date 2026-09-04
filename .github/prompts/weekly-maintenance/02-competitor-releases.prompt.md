# Step 2: Competitor Changelog Crawl & Scan Prompt

You are tasked with scanning competitor release channels to identify changes across all available release notes (no 30-day limit).

## Target Endpoints & Crawling Rules
Inspect all published release notes and changelog history on each listed endpoint:

1. **MongoDB Compass:**
   - URL: `https://github.com/mongodb/compass/releases`
   - Target Scope: Inspect published releases on the releases feed.
   - Extract: New aggregation operators, authentication methods, index inspection tools, performance profiling, and AI tools.

2. **NoSQLBooster:**
   - URL: `https://nosqlbooster.com/releasenotes`
   - Target Scope: Inspect the full release notes page across all published major and minor versions.
   - Extract: Bundled mongosh version, newly supported drivers, UI changes, debugger features, SQL translation enhancements, and AI Helper updates.

3. **DataGrip:**
   - URL: `https://www.jetbrains.com/datagrip/whatsnew/`
   - Target Scope: Read published feature releases. Filter strictly for mentions of "MongoDB", "NoSQL", or document-database querying. Disregard relational-only engine updates.

4. **Navicat for MongoDB:**
   - URL: `https://www.navicat.com/en/products/navicat-for-mongodb-release-notes`
   - Target Scope: Inspect the full published release notes list.
   - Extract: Schema analyzer changes, synchronization tools, BI/charting updates, and AI query assistance.

5. **DBeaver:**
   - URL: `https://dbeaver.com/category/release-notes/`
   - Target Scope: Inspect release notes feed. Filter strictly for "MongoDB extension" or NoSQL capabilities.

## Action Steps if a New Feature is Detected:
1. **Check Dictionary:** Open `/Users/ivan/Project/3t.tools.intellij/mongo_products_analisys/feature-dictionary.md`.
   - If an existing sub-feature ID covers it, use it.
   - If no sub-feature ID exists, add a new row to `feature-dictionary.md` under the appropriate `F-*` section following `<FEATURE>-<suffix>`.
2. **Update Product Matrix:** Update the product's corresponding `feature-matrix.md` and `feature-report.md` under:
   `/Users/ivan/Project/3t.tools.intellij/mongo_products_analisys/products/third-party/<product>/features/<feature-folder>/`
3. **Add Changelog Note:** Append a dated entry to the Changelog table at the bottom of `/Users/ivan/Project/3t.tools.intellij/mongo_products_analisys/feature-dictionary.md`.
