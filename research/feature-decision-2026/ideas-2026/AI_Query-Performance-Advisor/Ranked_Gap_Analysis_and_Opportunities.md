# AI Query/Index Performance Advisor — Ranked Gap Analysis & Opportunities

**Date:** 2026-08-11 | **Research by:** Ivan Martynov
**Sources:** 50+ Jira tickets across KONG, SHL, PM, MARIO, AIAG projects; customer feedback; competitive evidence

---

## Evidence Base Summary

| Source Type | Key Evidence |
|-------------|-------------|
| **Annual Survey** | "Query profiler" and "Indexing strategy optimizer" = consistently #1 and #2 most-requested features (KONG-7603, KONG-8267) |
| **Customer Loss** | "Many customers note moving to Compass for indexing and other performance needs" (KONG-7603, KONG-7801) |
| **Named Customers** | Anthem Insurance requested index utilization stats (KONG-3284); 4 customers asked for DB profiling (KONG-454); user ticket for busiest-queries view (KONG-1872) |
| **Internal Vision** | Performance Workbench spec defined 4-step workflow: Monitor → See → Diagnose → Fix (KONG-7603) |
| **Competitive** | Compass ships visual explain + performance advisor; VisuaLeaf ships index advisor; PMM/dbHelm do automated index suggestions (from competitive intel docs) |
| **3 Abandoned Attempts** | KONG-7572 (2022), KONG-10474 (2025), KONG-10884/11000 (2026) — all Won't Do |
| **Monitoring Product** | SHL-352 (In Progress): long-running query alerts with explain plan in Mongor |

---

## RANKED GAPS — By Implementation Value

---

### 🥇 RANK 1: AI-Powered Index Recommendation Engine
**Value Score: 10/10** | **Feasibility: High** | **Effort: Medium (2-3 sprints)**

#### What's Missing
No logic (rule-based OR LLM-driven) that proposes `createIndex({field:1, ...})` based on observed query patterns and explain plan results.

#### Evidence of Demand
- **Annual survey:** #1 most-requested alongside query profiler (KONG-7603)
- **Anthem Insurance** specifically asked for "which indexes are being utilised the most (and which are not)" (KONG-3284)
- **KONG-7572** (Highest priority, 2022): Detailed 8-step implementation plan designed, customer call recordings captured, Google Doc spec written — then abandoned
- **KONG-10884** (2026): Epic reopened, immediately Won't Do'd again (KONG-11000)
- **Competitive:** Compass Performance Advisor, VisuaLeaf, PMM, dbHelm all ship this
- **Customer churn trigger:** "Many customers note moving to Compass for indexing" (KONG-7801)

#### Building Blocks Ready
- `explain_query` tool → knows what scans are happening
- `list_indexes` tool → knows current indexes
- `analyze_schema` tool → knows field distributions
- `get_collection_statistics` → knows collection size
- LangChain4j agent framework → can chain tools

#### What To Build
1. **$indexStats integration** in `list_indexes` (adds access counts, last-used timestamps)
2. **Composite "diagnose_query" workflow**: explain → schema → indexes → LLM reasoning
3. **Structured prompt** for ESR rule, compound index awareness, prefix coverage
4. **UI card** in AI Helper showing recommendation + "Apply" button

#### Why It's #1
- Broadest reach (every persona that writes queries)
- Direct purchasing criterion for DBAs
- 3 attempts prove persistent demand; failure was prioritization, not technical
- Building blocks are 100% deployed — this is a prompt engineering + UX exercise

---

### 🥈 RANK 2: Profiler → AI Helper Integration ("Diagnose This Slow Query")
**Value Score: 9/10** | **Feasibility: Very High** | **Effort: Low (1 sprint)**

#### What's Missing
Query Profiler (UI) and AI Helper (sidebar) are completely disconnected. Users can't right-click a slow query in Profiler and say "why is this slow?"

#### Evidence of Demand
- **SHL-352** (In Progress): Mongor/Shield building exactly this — slow query alert → profiler tab → explain plan details. Proves the workflow is validated.
- **SHL-324**: "Update Long running query alert Details to include explain plan" — user-tested mockup showed demand for explain-in-context
- **KONG-7603 customer workflow:** "a way to see what is causing the performance issue → a way to diagnose why the problem happened"
- **Tab Context Registry** (KONG-10894) already knows which tab is active — just needs to pipe Profiler selection into AI context

#### What To Build
1. "Ask AI" button in Query Profiler on selected slow query row
2. Auto-populate AI Helper with: the query, the collection, exec stats
3. AI runs `explain_query` → interprets → suggests fix
4. Optional: "Open in IntelliShell" with suggested rewrite

#### Why It's #2
- Lowest effort gap to close (context injection + 1 button)
- Immediately visible value ("it explains my slow query in English")
- The SHL product is building the same workflow for Mongor — Desktop should have parity

---

### 🥉 RANK 3: Plain-Language Explain Plan Interpreter
**Value Score: 8/10** | **Feasibility: Very High** | **Effort: Low (1 sprint)**

#### What's Missing
The `explain_query` tool returns raw JSON. No structured prompt ensures the LLM consistently produces: "This query scanned 145,000 docs to return 12. A compound index on {region, status} would reduce scans to ~12."

#### Evidence of Demand
- **KONG-1639** (Won't Do): "Provide high-level, readily understandable / actionable description of explain data" — requested 2018
- **KONG-2241** (2018): "present information in useful, readily understandable ways"
- **SHL-324 comment:** "this is a massive feature" — the monitoring team considers explain interpretation significant
- **Competitive:** Compass AI Explain Plan Assistant is on their roadmap (mongodb-evolution-and-roadmap, L143)

#### What To Build
1. **Structured system prompt** for explain plan interpretation with few-shot examples
2. **Guardrails:** Always report docsExamined vs nReturned ratio, stage type (COLLSCAN/IXSCAN), execution time
3. **Template response format:** Problem → Impact → Recommended Fix → createIndex command
4. **Unit tests:** Feed known explain outputs, verify quality of interpretation

#### Why It's #3
- Near-zero implementation cost (prompt engineering only)
- Transforms existing `explain_query` tool from "data retrieval" to "actionable insight"
- Validated demand since 2018

---

### RANK 4: Unused / Redundant Index Detection
**Value Score: 8/10** | **Feasibility: High** | **Effort: Low-Medium (1-2 sprints)**

#### What's Missing
`list_indexes` returns definitions but NOT `$indexStats` (access counts). Can't detect:
- Indexes with zero accesses (waste storage, slow writes)
- Overlapping prefix indexes (e.g., `{a:1}` when `{a:1, b:1}` exists)
- Indexes that haven't been used since a certain date

#### Evidence of Demand
- **Anthem Insurance** (KONG-3284): "which indexes are being utilised the most (and which are not)"
- **KONG-7801 rationale:** "Index stats, so that they can see exactly how effective their indexes are"
- **KONG-10474 research (Ivan, Oct 2025):** Found IDX1 with 0 accesses → recommended removal. Proves the analysis works when done manually.
- **Index Manager** already shows index stats in the UI (KONG-7801, deployed) — but they're not piped to AI

#### What To Build
1. New tool: `get_index_stats` wrapping `db.collection.aggregate([{$indexStats:{}}])`
2. LLM prompt: detect zero-access indexes, prefix overlaps, duplicate patterns
3. UI recommendation: "Drop IDX1 (0 uses in 30 days) — saves 20KB, speeds writes"

#### Why It's #4
- Anthem Insurance = real revenue-attached customer request
- Index Manager already shows this data — just not AI-interpreted
- Directly actionable ("drop this index") with measurable impact

---

### RANK 5: Proactive COLLSCAN / Slow-Query Alerting (Desktop)
**Value Score: 7/10** | **Feasibility: Medium** | **Effort: Medium (2-3 sprints)**

#### What's Missing
Everything is pull-only. No background detection like: "3 queries in the last hour did COLLSCAN on `orders` — want me to suggest indexes?"

#### Evidence of Demand
- **KONG-7603 customer workflow step 1:** "a way to monitor when something goes wrong" — explicitly OUT OF SCOPE in PW#1, deferred to monitoring product
- **SHL-352** (In Progress): Mongor IS building this ("alert for when a query runs slower than X ms")
- **KONG-1872** (customer ticket): "View top 5 or 10 busiest queries per day/week/month"
- **KONG-3284 discussion:** "gathering statistics for 10 or 30 minutes would be enough to provide valuable information"

#### What To Build
1. Background task: sample `system.profile` every N minutes while Profiler tab is open
2. Pattern detection: group by query shape, flag COLLSCANs, compute docsExamined/nReturned ratio
3. Notification badge: "3 new performance issues detected"
4. Click → AI Helper with pre-loaded context

#### Why It's #5
- Differentiator vs Compass (which doesn't proactively alert in the GUI)
- But: requires background processing architecture that's new for Desktop
- SHL/Mongor building it separately — could share logic or be Desktop-only

---

### RANK 6: One-Click Index Creation from AI Recommendations
**Value Score: 7/10** | **Feasibility: High** | **Effort: Low (1 sprint)**

#### What's Missing
AI suggests `db.collection.createIndex({...})` in chat. User must copy-paste to IntelliShell. No "Apply" button.

#### Evidence of Demand
- **KONG-2241 comment (2018):** "ideally actually perform the suggested optimizations (create index, rewrite query)"
- **KONG-7801:** "Easy index addition, so that they can add an index quickly if their query needs it"
- Competitive: Compass "one-click index recommendations" on roadmap

#### What To Build
1. New agent tool: `create_index` (with confirmation dialog / human-in-the-loop)
2. AI recommendation card with "Create Index" button
3. Confirmation modal: "This will create index {zipCode:1, status:1} on `orders`. Proceed?"
4. Background creation with progress indicator

#### Why It's #6
- Reduces friction between "know what to do" → "do it"
- Technically simple (Index Manager already has createIndex logic)
- Must have confirmation guard (production safety)

---

### RANK 7: Aggregation Pipeline Performance Analysis
**Value Score: 7/10** | **Feasibility: Medium** | **Effort: Medium (2 sprints)**

#### What's Missing
`explain_query` works for find queries but aggregation explain is different (per-stage breakdown). No AI analysis of which aggregation stage is the bottleneck.

#### Evidence of Demand
- **KONG-5881** (Deployed, UserVoice): Users requested `hint` in aggregation — they're actively tuning pipelines
- **KONG-9258:** "Explain plan doesn't match actual for aggregation queries" — users expect aggregation explain support
- **Competitive intel:** "Users frequently request an automated indexing and query tuning engine that… provides actionable recommendations to optimize slow-running aggregation pipelines" (studio-3t-review-mining, L55)
- **PM-41** (Logged): "Execute aggregation query in any environment" — pipeline is a core workflow

#### What To Build
1. Extend `explain_query` tool to support `aggregate` explain (already partially supported in MongoDB driver)
2. Per-stage analysis prompt: identify stage doing COLLSCAN, blocking sorts, $lookup without indexes
3. Recommend: indexes for $match stages, $project before $group to reduce document size
4. Integration with Aggregation Editor AI Helper (KONG-8664, already deployed)

#### Why It's #7
- Aggregation is the core advanced workflow
- Users already have AI Helper in Aggregation Editor — just lacks performance awareness
- Slightly higher complexity than find-query analysis

---

### RANK 8: Vector / Search / Atlas Search Index Management
**Value Score: 6/10** | **Feasibility: Medium** | **Effort: Medium-High (3 sprints)**

#### What's Missing
No support for creating/managing Atlas Search indexes, vector search indexes, or text indexes from the AI advisor context.

#### Evidence of Demand
- **PM-91** (Logged): "Indexing settings for configuring vector, search"
- MongoDB 8.0+ pushing vector search as primary differentiator
- Atlas Search indexes have different creation syntax not supported by traditional Index Manager

#### What To Build
1. Extend Index Manager to support Atlas Search index definitions
2. AI tool for `createSearchIndex` recommendations
3. Schema-aware: detect text fields → suggest text indexes; detect embedding fields → suggest vector indexes

#### Why It's #8
- Growing importance but niche today (not all users on Atlas)
- Requires Atlas-specific API calls
- Less proven customer demand (only 1 PM idea, no customer tickets)

---

### RANK 9: Historical Query Performance Trending
**Value Score: 5/10** | **Feasibility: Low-Medium** | **Effort: High (3-4 sprints)**

#### What's Missing
No historical view of query performance over time. Can't answer: "Is this query getting slower as the collection grows?"

#### Evidence of Demand
- **KONG-1872:** "View top 5 or 10 busiest queries per day, week, month, year"
- **KONG-3284 discussion:** "keeping statistics somewhere and updating them continuously" — acknowledged as hard for desktop app
- **SHL-352:** Mongor building 30-minute window trending

#### What To Build
1. Local SQLite/H2 store for profiler snapshots
2. Trend charts: avg execution time per query shape over time
3. Alert thresholds: "query X is 40% slower than last week"
4. AI analysis: "growth in collection size correlates with degradation"

#### Why It's #9
- **Hard architectural problem** for a desktop app (requires persistent background data collection)
- Acknowledged limitation since 2019 (KONG-3284 comment: "a desktop application is not quite the ideal tool")
- Better suited for Mongor/SHL product
- Still valuable if user keeps Studio 3T open

---

### RANK 10: Query Rewrite Suggestions
**Value Score: 5/10** | **Feasibility: Medium** | **Effort: Medium (2 sprints)**

#### What's Missing
AI can explain WHY a query is slow but doesn't suggest alternative query structures (e.g., "use $lookup with pipeline instead of client-side joins", "add $project before $group to reduce pipeline document size").

#### Evidence of Demand
- **KONG-2241 comment (2018):** "1. wtf is this query so slow? 2. what can be done about it? this can range from index suggestion to re-writing an aggregate pipeline differently"
- **AIAG-119:** "Convert find query to aggregation code" — code transformation already exists
- AI Helper in Aggregation Editor (KONG-8664) already generates queries — just not performance-optimized versions

#### What To Build
1. "Optimize this query" prompt workflow
2. Compare explain before/after rewrite
3. Show both versions with performance delta
4. "Apply rewritten query" button

#### Why It's #10
- Higher complexity (query equivalence verification is hard)
- Risk of LLM generating semantically different queries
- Valuable but needs strong guardrails

---

## PRIORITIZATION MATRIX

| Rank | Gap | Value | Effort | Building Blocks Ready? | Customer Evidence |
|------|-----|-------|--------|----------------------|-------------------|
| 1 | **Index Recommendation Engine** | 10 | Medium | ✅ All deployed | Annual survey #1, Anthem, 3 attempts, competitive |
| 2 | **Profiler → AI Integration** | 9 | Low | ✅ Tab Registry + tools | SHL-352 validates workflow, customer workflow spec |
| 3 | **Plain-Language Explain** | 8 | Low | ✅ explain_query tool | KONG-1639, KONG-2241, Compass roadmap |
| 4 | **Unused Index Detection** | 8 | Low-Med | ⚠️ Needs $indexStats | Anthem Insurance, KONG-7801, research spike |
| 5 | **Proactive COLLSCAN Alerting** | 7 | Medium | ⚠️ Needs background job | KONG-7603 step 1, SHL-352, KONG-1872 |
| 6 | **One-Click Index Creation** | 7 | Low | ✅ Index Manager logic | KONG-2241, KONG-7801, Compass parity |
| 7 | **Aggregation Pipeline Analysis** | 7 | Medium | ⚠️ Needs agg explain | KONG-5881, review mining, PM-41 |
| 8 | **Vector/Search Index Support** | 6 | Med-High | ❌ New infrastructure | PM-91, MongoDB direction |
| 9 | **Historical Trending** | 5 | High | ❌ New storage layer | KONG-1872, KONG-3284, desktop limitation |
| 10 | **Query Rewrite Suggestions** | 5 | Medium | ⚠️ Needs equivalence check | KONG-2241, AIAG-119 |

---

## RECOMMENDED IMPLEMENTATION PHASES

### Phase 1: "Quick Wins" (2-3 weeks) — Ranks 2, 3, 6
- Wire Profiler → AI Helper (1 button + context injection)
- Add structured explain-interpretation prompt + few-shot examples
- Add `create_index` tool with confirmation dialog

**Impact:** Transforms existing tools from "data retrieval" into "actionable advisor"
**Effort:** ~1 developer, 2-3 weeks
**No new infrastructure needed**

### Phase 2: "Core Advisor" (4-6 weeks) — Ranks 1, 4
- Add `$indexStats` to index tool
- Build composite "diagnose slow query" multi-tool workflow
- Implement unused/redundant index detection
- UI: recommendation cards with "Apply" button in AI Helper

**Impact:** The actual "advisor" feature — competitive parity with Compass
**Effort:** ~2 developers, 4-6 weeks

### Phase 3: "Differentiation" (6-8 weeks) — Ranks 5, 7
- Background profiler sampling + COLLSCAN detection
- Notification system for performance issues
- Aggregation pipeline per-stage analysis

**Impact:** Goes BEYOND Compass (proactive detection)
**Effort:** ~2 developers, 6-8 weeks, new background processing architecture

---

## KEY RISK REPEATED

> Compass and VisuaLeaf already ship versions of Rank 1. Studio 3T's differentiator must be **recommendation quality** (multi-query pattern analysis, compound index awareness, ESR rule, redundancy detection) — not just "an advisor exists."

The AI approach gives us an inherent advantage: LLM reasoning can consider more context simultaneously than rule-based systems. The risk is inconsistency — prompts must be engineered with few-shot examples and structured output to match or exceed deterministic rule-based advisors.
