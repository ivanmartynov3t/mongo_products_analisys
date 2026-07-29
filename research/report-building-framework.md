Here is the comprehensive, human-readable instruction manual for **Part 2: Cumulative Report Calculation**.

Once **Claude** finishes gathering and structuring metrics from the public internet (Part 1), it executes this workflow to synthesize thousands of individual data points into an executive-level, mathematically defensible product roadmap report.

---

# Part 2: Cumulative Report Generation Framework

The goal of this phase is to convert the raw `.jsonl` metric database into an **Executive Product Roadmap Report**. Claude acts as a principal product manager and data scientist—aggregating data, normalizing scores, calculating the **Public Feature Prioritization Index (FPI)**, and drafting actionable feature specifications.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                 PART 2: CUMULATIVE REPORT ENGINE (CLAUDE)               │
└─────────────────────────────────────────────────────────────────────────┘
                                     │
 1. DATA ROLLUP           ► Aggregate raw records per Feature ID
                                     │
 2. SCORE NORMALIZATION   ► Convert raw metrics to standardized 0–100 scale
                                     │
 3. FPI CALCULATION       ► Run Public Feature Prioritization Index formula
                                     │
 4. EFFORT ESTIMATION     ► Apply architectural complexity heuristics
                                     │
 5. REPORT COMPOSITION    ► Generate Executive Matrix, Roadmap & Draft PRD

```

---

## Step 1: Metric Rollup & Aggregation

Claude scans all harvested JSON records and groups them by `feature_id`. For every unique feature identified in the public dataset, Claude calculates five core aggregated metrics:

```
                  ┌─────────────────────────────────────┐
                  │    RAW METRIC ROLLUP PER FEATURE    │
                  └──────────────────┬──────────────────┘
                                     │
   ┌─────────────────┬───────────────┴───────────────┬─────────────────┐
   ▼                 ▼                               ▼                 ▼
Total Mentions    Demand Intensity            Enterprise Density   Friction Index
 (Count $N_f$)   ($D_f = \sum \text{Severity}$)  ($\text{EPI}_f = \frac{\text{Ent}}{\text{Total}}$)  ($\text{Friction}_f$)

```

### Aggregation Formulas Executed by Claude

1. **Total Public Volume ($N_f$)**: The total count of unique, deduplicated public posts, reviews, and threads mentioning feature $f$.
2. **Raw Demand Intensity ($D_f$)**: The sum of all user-reported pain severity scores for feature $f$.

$$D_f = \sum_{i=1}^{N_f} \text{PainSeverity}_i$$


3. **Enterprise Proxy Indicator ($\text{EPI}_f$)**: The percentage of user mentions that contain high-value enterprise keywords (e.g., `production`, `sharded cluster`, `SOC2`, `AWS DocumentDB`).

$$\text{EPI}_f = \frac{\text{Mentions containing Enterprise Signals}}{N_f}$$


4. **Friction Index ($\text{Friction}_f$)**: A weighted sum measuring how severely the lack of feature $f$ breaks user workflows.

$$\text{Friction}_f = \sum_{i=1}^{N_f} \Big(1.0 + (1.5 \times \text{HasWorkaround}_i) + (2.0 \times \text{IsCrashOrDataLoss}_i)\Big)$$


5. **Competitor Parity Weight ($\text{Gap}_f$)**: A multiplier assigned based on competitor coverage (from MongoDB Compass, DBeaver, or Navicat changelogs):
* **1.5 (High Threat)**: Supported by 2 or more primary competitors.
* **1.2 (Moderate Threat)**: Supported by 1 competitor.
* **1.0 (Unique/Differentiating)**: Not offered by any direct competitors.



---

## Step 2: R&D Effort Estimation Heuristic

To calculate return-on-investment (ROI), Claude evaluates the architectural scope of each feature request and assigns an estimated development effort ($\text{EstEffort}_f$) using a standard Fibonacci story point scale ($1, 2, 3, 5, 8, 13, 21$).

Claude applies these rules to estimate complexity without internal codebase access:

| Complexity Category | Architectural Scope | Example Features | Point Estimate ($\text{EstEffort}_f$) |
| --- | --- | --- | --- |
| **Minor UI / Polish** | Front-end changes, theme fixes, text copy updates | Dark mode canvas tweaks, export button repositioning | **1 – 2 Points** |
| **Localized Tool Enhancement** | Modifying an existing UI view or adding minor parameters | Adding CSV delimiter options, connection timeout flags | **3 – 5 Points** |
| **Core Workflow Update** | Modifying multi-step UI workflows or query parser rules | Visual aggregation builder drag-and-drop enhancements | **8 Points** |
| **System-Wide Feature** | New security layers, auth protocols, or driver integrations | SSO / SAML integration, read-only production safety locks | **13 Points** |
| **Major Engine Redesign** | New query engine, real-time sync systems, or offline caching | Real-time multi-user workspace sharing, custom query optimizer | **21 Points** |

---

## Step 3: Compute the Public Feature Prioritization Index (FPI)

Before running the final FPI calculation, Claude normalizes all raw variables on a $0$ to $100$ scale across the entire backlog using Min-Max scaling:

$$\text{Norm}(X_f) = \left( \frac{X_f - X_{\min}}{X_{\max} - X_{\min}} \right) \times 100$$

### The Public FPI Formula

Claude computes the final priority score for every feature candidate:

$$\text{Public FPI}_f = \frac{0.30 \cdot \text{Norm}(D_f) + 0.30 \cdot \text{Norm}(\text{EPI}_f) + 0.25 \cdot \text{Norm}(\text{Friction}_f) + 0.15 \cdot \text{Norm}(\text{Gap}_f)}{\Big(\text{Norm}(\text{EstEffort}_f) + 10\Big)^{1.1}}$$

* **Why the $+10$ padding?**: Prevents division-by-zero for 1-point micro-tasks.
* **Why the $1.1$ exponent?**: Slightly penalizes overly large enterprise initiatives ($13–21$ points) to favor high-impact, medium-effort releases.

---

## Step 4: Generating the Final Cumulative Report Output

Claude formats the calculated metrics into a four-part markdown report designed for product leaders and executive teams.

### Section A: Executive Priority Matrix & Roadmap Table

A sorted, high-level summary ranking candidate features from highest ROI to lowest.

| Rank | Feature ID | Feature Name | Public FPI | Total Mentions ($N_f$) | Enterprise Ratio ($\text{EPI}$) | Friction Index | Estimated Points | Strategic Recommendation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **1** | `CONN-readonly-lock` | Production Read-Only Safety Locks | **2.45** | 142 | 88% | 185.0 | 13 | **Top Priority (Q3 Release)** |
| **2** | `AGG-visual-nested-ui` | Nested Field Support in Aggregation Builder | **1.92** | 210 | 42% | 140.0 | 8 | **High ROI Major Feature** |
| **3** | `GEO-map-renderer` | GeoJSON Interactive Map View | **1.35** | 64 | 25% | 45.0 | 5 | **Competitor Parity Patch** |
| **4** | `SCHEMA-export-plantuml` | Export Schema to PlantUML / ERD | **0.52** | 18 | 10% | 12.0 | 3 | **Low Priority Backlog** |

---

### Section B: Deep-Dive Feature Evidence Analysis

For the top 3 ranked features, Claude generates a detailed breakdown showcasing the real-world public evidence:

```markdown
### Feature Deep-Dive #1: Production Read-Only Safety Locks (`CONN-readonly-lock`)

* **Public FPI Score**: 2.45 (Rank #1)
* **Demand Density**: 142 public discussions across Reddit, Forums, and Stack Overflow.
* **Enterprise Risk Signal**: 88% of requests involve production clusters, SOC2, or AWS DocumentDB.
* **Workflow Friction**: Users report severe anxiety over accidental updates; 30% reported writing custom shell scripts to bypass Studio 3T write capabilities on production.

#### Key Verbatim Evidence Extracted by Claude:
> "We almost wiped our production database because there is no explicit read-only lock toggle on connections!" 
> — *Source: https://forum.studio3t.com/t/...*

> "Compass has a simple read-only mode toggle on connection. Why does Studio 3T still lack this basic safety feature?"
> — *Source: https://reddit.com/r/mongodb/...*

```

---

### Section C: Competitor Parity & Threat Matrix

Claude renders a matrix showing where Studio 3T stands relative to competitors based on public changelog analysis:

| Requested Capability | Studio 3T Status | MongoDB Compass | DBeaver | Navicat | Market Risk Level |
| --- | --- | --- | --- | --- | --- |
| **Production Read-Only Guard** | Missing | Supported | Supported | Supported | **High Migration Risk** |
| **Visual Nested Aggregations** | Partial | Partial | Supported | Not Supported | **Competitive Parity Gap** |
| **SQL-to-MQL Translation** | Full Support | Not Supported | Partial | Not Supported | **Studio 3T Core Moat** |

---

### Section D: Auto-Generated Product Requirement Document (PRD)

For the **#1 ranked feature**, Claude automatically writes a complete draft PRD to fast-track engineering alignment.

```markdown
# Draft PRD: Production Read-Only Safety Connection Locks

## 1. Problem Statement
Public user sentiment indicates that developers and database administrators frequently fear executing unintended write, update, or drop operations on production MongoDB clusters when using Studio 3T. Currently, 88% of enterprise mentions highlight this as a critical operational risk.

## 2. Core User Jobs-To-Be-Done (JTBD)
* **Primary Job**: When connecting to a production cluster, I want to enforce strict read-only execution locks so that I can query and inspect live data without the risk of accidental data modification or cluster downtime.

## 3. Minimum Viable Product (MVP) Scope
1. Add a mandatory **"Read-Only Connection"** toggle switch in the Connection Manager UI.
2. When toggled ON, disable all inline cell editing, collection drop buttons, and write-oriented aggregation stages (`$out`, `$merge`).
3. Display a prominent red **"READ-ONLY PRODUCTION LOCK"** badge in the top navigation bar when connected to locked endpoints.

## 4. Success Metrics
* 50% reduction in forum threads regarding accidental production writes.
* Achieve feature parity with MongoDB Compass and DBeaver within 60 days of release.

```

---

## Step 5: Quality Assurance & Reliability Thresholds

To maintain data integrity and prevent skewed roadmap recommendations, Claude applies two automatic quality controls before publishing the report:

1. **Minimum Sample Size Threshold ($N_f \ge 5$)**: If a feature has fewer than 5 total mentions across the internet, Claude tags it as **"Low Confidence Data"** and excludes it from the top-tier release recommendations.
2. **Outlier Suppression**: If a single user posts 10 identical comments across different forum threads, Claude’s deduplication engine merges them into a single record, preventing individual vocal users from artificially inflating a feature's FPI score.