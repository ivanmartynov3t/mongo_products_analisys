# AI-Driven Query/Index Performance Advisor — Complete Implementation Deep-Dive

**Date:** 2026-08-11 | **Research by:** Ivan Martynov

---

## TL;DR

Studio 3T has **6 deployed AI agent tools** + a **visual Query Profiler** + a **legacy Explain tab** that together form the data-access primitives for a performance advisor. All tools are shipped in **v2026.9.0** (no feature flag), implemented by **Aleksei Beliaev** (tools) and **Ivan Martynov** (AI Helper sidebar + context), owned by the **3T Desktop Team**. The same tools are exposed externally via the **MCP Server** (MARIO-3594). However, **no recommendation engine** connects these primitives — three attempts (2022, 2025, 2026) to build one were all abandoned.

---

## PART 1: Parent Story — KONG-10788 "Implement Agent Tools"

| Field | Value |
|-------|-------|
| **Key** | KONG-10788 |
| **Type** | Story |
| **Status** | ✅ Deployed |
| **Assignee** | Aleksei Beliaev |
| **Reporter** | Hugo Almeida |
| **Created** | 2026-03-16 |
| **Resolved** | 2026-05-07 |
| **Fix Version** | 2026.9.0 |
| **Description** | "Umbrella ticket to migrate existing tools from `3t.tools` MCP branch. Ties with AI Roadmap MVP2." |
| **Source Branch** | `bitbucket.org/3tio/3t.tools/branch/NO-TICKET-MCP-STUDIO3T` |
| **Roadmap Doc** | [AI Roadmap MVP2](https://docs.google.com/document/d/1NYqc1N00ZwndmekbRr9UZOfaw96m6Z5hNnPHmeczUGw/edit) |

**All sub-tasks under this story (all Deployed):**
- KONG-10795 — explain_query
- KONG-10796 — analyze_schema
- KONG-10797 — list_indexes
- KONG-10798 — get_collection_statistics
- KONG-10799 — query
- KONG-10800 — assess_collection_health

---

## PART 2: Each Agent Tool — Detailed Ticket Data

### KONG-10795 — `explain_query` tool

| Field | Value |
|-------|-------|
| **Summary** | Implement explain_query tool |
| **Type** | Sub-task of KONG-10788 |
| **Status** | ✅ Deployed |
| **Assignee** | Aleksei Beliaev |
| **Fix Version** | 2026.9.0 |
| **Created** | 2026-03-16 |
| **Resolved** | 2026-04-09 |
| **Team** | 3T Desktop Team |
| **Category** | Internal |

**What it does:** Runs MongoDB `explain()` on a given query with configurable verbosity levels:
- `queryPlanner` — shows winning plan without execution
- `executionStats` — adds docs examined, keys examined, execution time
- `allPlansExecution` — full stats for all candidate plans

**MCP equivalent:** `ExplainTool.java` (MARIO-3594) — args: `database`, `collection`, `filter`, `verbosity`

---

### KONG-10797 — `list_indexes` tool

| Field | Value |
|-------|-------|
| **Summary** | Implement list_indexes tool |
| **Type** | Sub-task of KONG-10788 |
| **Status** | ✅ Deployed |
| **Assignee** | Aleksei Beliaev |
| **Fix Version** | 2026.9.0 |
| **Created** | 2026-03-16 |
| **Resolved** | 2026-04-09 |
| **Team** | 3T Desktop Team |
| **Category** | Internal |

**What it does:** Returns all index definitions for a collection (name, key pattern, options like unique/sparse/TTL, size).

**Limitation:** Returns definitions only — does NOT include `$indexStats` (access count, last used timestamp). This is the key gap for redundancy/usage analysis.

**MCP equivalent:** `CollectionIndexesTool.java` — args: `database`, `collection`

---

### KONG-10796 — `analyze_schema` tool

| Field | Value |
|-------|-------|
| **Summary** | Implement analyze_schema tool |
| **Type** | Sub-task of KONG-10788 |
| **Status** | ✅ Deployed |
| **Assignee** | Aleksei Beliaev |
| **Fix Version** | 2026.9.0 |
| **Created** | 2026-03-16 |
| **Resolved** | 2026-04-09 |
| **Team** | 3T Desktop Team |
| **Category** | Internal |

**What it does:** Samples N documents (default 100), infers field types, computes:
- Field names and data types
- Frequency (% of documents containing each field)
- Value distributions (min/max/avg for numerics, top values for strings)
- Null counts

**MCP equivalent:** `CollectionSchemaTool.java` — args: `database`, `collection`, `sampleSize`

---

### KONG-10829 — `analyze_schema` in AI Helper (re-implementation)

| Field | Value |
|-------|-------|
| **Summary** | Implement schema analyze tool in AI Helper |
| **Type** | Sub-task |
| **Status** | ✅ Deployed |
| **Assignee** | Eswaranaath MP |
| **Fix Version** | 2026.7.0 |
| **Created** | 2026-03-23 |
| **Resolved** | 2026-04-09 |

**QA Notes (from Hazel Ozmel):**
- Works in IntelliShell, Collection Editor, and Aggregation Editor
- Licensed to Ultimate only (blocked for Pro)
- Tested on Windows 10, 2026.7.0 RC1

---

### KONG-10798 — `get_collection_statistics` tool

| Field | Value |
|-------|-------|
| **Summary** | Implement get_collection_statistics tool |
| **Type** | Sub-task of KONG-10788 |
| **Status** | ✅ Deployed |
| **Assignee** | Aleksei Beliaev |
| **Fix Version** | 2026.9.0 |
| **Created** | 2026-03-16 |
| **Resolved** | 2026-05-07 |
| **Team** | 3T Desktop Team |

**What it does:** Returns `collStats` output:
- Document count
- Average document size
- Total data size / storage size
- Index sizes (per-index breakdown)
- WiredTiger stats (compression ratio, cache usage)
- Capped collection flag

**MCP equivalent:** `CollectionStorageSizeTool.java` + `DbStatsTool.java`

---

### KONG-10799 — `query` tool

| Field | Value |
|-------|-------|
| **Summary** | Implement query tool |
| **Type** | Sub-task of KONG-10788 |
| **Status** | ✅ Deployed |
| **Assignee** | Aleksei Beliaev |
| **Fix Version** | 2026.9.0 |
| **Created** | 2026-03-16 |
| **Resolved** | 2026-04-09 |
| **Team** | 3T Desktop Team |
| **Category** | Internal |

**What it does:** Executes a MongoDB `find()` query and returns results. Allows the LLM to verify hypotheses about data, test filter patterns, or sample results.

---

### KONG-10800 — `assess_collection_health` tool

| Field | Value |
|-------|-------|
| **Summary** | Implement assess_collection_health tool |
| **Type** | Sub-task of KONG-10788 |
| **Status** | ✅ Deployed |
| **Assignee** | Aleksei Beliaev |
| **Fix Version** | 2026.9.0 |
| **Created** | 2026-03-16 |
| **Resolved** | 2026-05-07 |
| **Team** | 3T Desktop Team |

**What it does:** Composite tool that combines schema analysis, index listing, and collection stats into a unified "health" report the LLM can interpret holistically.

---

## PART 3: AI Helper Infrastructure

### KONG-10837 — Global AI Helper Sidebar

| Field | Value |
|-------|-------|
| **Summary** | Create a Global AI Helper as a Side Bar |
| **Type** | Sub-task |
| **Status** | ✅ Deployed |
| **Assignee** | Ivan Martynov |
| **Fix Version** | 2026.9.0 |
| **Created** | 2026-03-27 |
| **Resolved** | 2026-05-07 |
| **Label** | `AI_Helper` |

**What it does:** The persistent sidebar chat interface users interact with. Accessible from any tab in Studio 3T.

---

### KONG-10894 — Tab Context Registry & AI Context-Fetching Tool

| Field | Value |
|-------|-------|
| **Summary** | Implement Tab Context Registry and AI Context-Fetching Tool |
| **Type** | Sub-task |
| **Status** | ✅ Deployed |
| **Assignee** | Ivan Martynov |
| **Fix Version** | 2026.9.0 |
| **Created** | 2026-04-15 |
| **Resolved** | 2026-05-07 |
| **Label** | `AI_Helper` |

**What it does:**
- **Global Tab Registry** — tracks all open tabs (ID, connection info, tab name, tab type)
- **Tab lifecycle hooks** — auto-register on open, deregister on close
- **LangChain4j tool** — AI can query the registry to know which tabs are open and what connections are active
- **System prompt integration** — AI automatically uses this tool when user asks about connections or when context disambiguation is needed
- **Future-proofed** — data model ready for a UI where users manually select tab context

---

### KONG-10789 — AI Helper Use Agent Tools (Integration Ticket)

| Field | Value |
|-------|-------|
| **Summary** | AI Helper use Agent Tools |
| **Type** | Sub-task |
| **Status** | ✅ Deployed |
| **Assignee** | Eswaranaath MP |
| **Resolved** | 2026-04-28 |

**What it does:** Wires the LangChain4j agent framework to call the tools (explain, schema, indexes, stats, query, health) from within the AI Helper sidebar conversations.

---

## PART 4: MCP Server (External Access)

### MARIO-3594 — PR-3: Metadata Tools

| Field | Value |
|-------|-------|
| **Summary** | PR-3: Metadata Tools — collection-schema, collection-indexes, db-stats, collection-storage-size, explain |
| **Type** | Sub-task |
| **Status** | ✅ Deployed |
| **Assignee** | David Contavalli |
| **Created** | 2026-05-20 |
| **Resolved** | 2026-06-08 |

**5 MCP tools implemented (~12 files):**
1. `CollectionSchemaTool.java` — samples N docs, infers field types
2. `CollectionIndexesTool.java` — lists indexes
3. `DbStatsTool.java` — database-level stats
4. `CollectionStorageSizeTool.java` — collection storage metrics
5. `ExplainTool.java` — explain with verbosity forwarded to MongoDB

Each has unit tests. Auto-configured via `MongoMcpAutoConfiguration.java`.

---

## PART 5: UI — Query Profiler (Legacy Feature)

### KONG-8267 — Query Profiler Implementation

| Field | Value |
|-------|-------|
| **Summary** | [PW] Query profiler implementation |
| **Type** | Story |
| **Status** | ✅ Deployed |
| **Reporter** | Eswaranaath MP |
| **Created** | 2023-03-21 |
| **Resolved** | 2024-12-03 |
| **Label** | `performance-wb` |
| **Editions** | Pro, Ultimate |

**What it delivers:**
- Recent slow queries (last X minutes)
- Ordering/sorting to find worst offenders
- Execution count per query shape
- **Similar query detection** — groups repeated slow query patterns
- Open queries directly in IntelliShell or Aggregation Editor for editing

**User background:** "A query profiler is consistently the most requested feature in the annual survey."

**KB Article:** [Google Doc](https://docs.google.com/document/d/1vEjKG1RtId*jm8YlSCDflZW3GgS2xyzz3r5-wBk5eG0/edit)

---

## PART 6: Abandoned Attempts

### KONG-7572 — Index Suggestion for Collection Queries (2022)

| Field | Value |
|-------|-------|
| **Status** | ❌ Won't Do |
| **Priority** | Highest |
| **Reporter** | Eswaranaath MP |
| **Created** | 2022-09-19 |
| **Closed** | 2025-01-24 |
| **Label** | `purge-2025` |

**Planned scope (never built):**
1. From input query, identify field order for index
2. Calculate field value counts (entire collection)
3. Calculate field value counts (sample documents)
4. Calculate Mean, StdDev, Margin of Error
5. Multi-level stats for compound index
6. Define rules for suggestion (cardinality thresholds, user vs auto accuracy)
7. Generate index suggestions from stats + rules
8. Compare new vs existing indexes and advise user

**Supporting docs:** Performance Workbench specifications, customer call recordings (2 parts)

**Why abandoned:** Moved to 2024.2 in Dec 2023, then purged in 2025 cleanup. Never prioritized for actual implementation.

---

### KONG-10474 — Schema Analyzer and AI Recommendations (2025)

| Field | Value |
|-------|-------|
| **Status** | ✅ Done (as research only) |
| **Assignee** | Ivan Martynov |
| **Reporter** | Peter Hägglund |
| **Created** | 2025-10-15 |
| **Closed** | 2026-04-14 |
| **Label** | `backlog` |

**Planned scope:**
- AI-powered schema analysis (anti-patterns, missing/redundant indexes)
- Predictive recommendations based on query patterns
- Automated schema documentation

**What actually happened:** Research spike only. Ivan produced a full AI-generated collection analysis (see comments: 3 detailed reports including field stats, index recommendations, schema refactoring suggestions). Quality was high but no productized feature resulted.

**Closing comment (Ivan, Apr 2026):** "We can close this, it was a research and we didn't move forward with this that time. Now similar task has been implemented by Alexey."

---

### KONG-10884 — Query Profiler Index Suggestions Epic (2026)

| Field | Value |
|-------|-------|
| **Status** | ✅ Done (epic marked done, child Won't Do) |
| **Assignee** | Eswaranaath MP |
| **Reporter** | Hugo Almeida |
| **Created** | 2026-04-14 |
| **Closed** | 2026-08-10 |

**Description:** "The Query Profiler should offer suggestions on what indexes to create. Based on schema and on slow running queries."

**Child ticket KONG-11000** ("Add code changes to generate index suggestions") = **Won't Do**

**Interpretation:** The epic was resolved by marking the feature as out-of-scope/deferred, not by delivering functionality.

---

## PART 7: What's Actually Implemented End-to-End

┌─────────────────────────────────────────────────────────────────────┐
│                    USER INTERACTION LAYER                             │
│                                                                       │
│  ┌────────────────┐  ┌──────────────┐  ┌─────────────────────────┐ │
│  │ Query Profiler │  │ Explain Tab  │  │    AI Helper Sidebar     │ │
│  │ (KONG-8267)    │  │ (legacy)     │  │    (KONG-10837)          │ │
│  │                │  │              │  │                           │ │
│  │ • Slow queries │  │ • Visual     │  │ • Chat interface          │ │
│  │ • Grouping     │  │   explain    │  │ • Context-aware           │ │
│  │ • Exec counts  │  │ • Winning    │  │ • Multi-turn conversation │ │
│  │ • Open in ISH  │  │   plan tree  │  │ • Tab Context Registry    │ │
│  └────────┬───────┘  └──────┬───────┘  └────────────┬──────────────┘ │
│           │                  │                        │                │
│           │          ┌───────▼────────────────────────▼──────────┐    │
│           │          │         LangChain4j Agent Framework         │    │
│           │          │         (KONG-10789)                        │    │
│           │          │                                             │    │
│           │          │  Available Tools:                           │    │
│           │          │  ┌─────────────┐ ┌───────────────┐         │    │
│ NO LINK   │          │  │explain_query│ │ list_indexes  │         │    │
│ EXISTS ◄──┤          │  │ KONG-10795  │ │ KONG-10797    │         │    │
│           │          │  └─────────────┘ └───────────────┘         │    │
│           │          │  ┌──────────────┐ ┌────────────────────┐   │    │
│           │          │  │analyze_schema│ │get_collection_stats│   │    │
│           │          │  │ KONG-10796   │ │ KONG-10798         │   │    │
│           │          │  │ KONG-10829   │ └────────────────────┘   │    │
│           │          │  └──────────────┘                          │    │
│           │          │  ┌─────────────┐ ┌──────────────────────┐  │    │
│           │          │  │    query    │ │assess_collection_    │  │    │
│           │          │  │ KONG-10799  │ │health  KONG-10800    │  │    │
│           │          │  └─────────────┘ └──────────────────────┘  │    │
│           │          │  ┌──────────────────────────────────────┐  │    │
│           │          │  │ get_open_tabs (KONG-10894)            │  │    │
│           │          │  │ → connection, tab type, tab name      │  │    │
│           │          │  └──────────────────────────────────────┘  │    │
│           │          └────────────────────────────────────────────┘    │
│           │                        │                                   │
│           ▼                        ▼                                   │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │              MongoDB Driver / Server Commands                     │  │
│  │  • db.collection.explain()    • db.collection.getIndexes()       │  │
│  │  • db.collection.find()       • db.collection.stats()            │  │
│  │  • db.collection.aggregate()  • db.runCommand({collStats:...})   │  │
│  └─────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘EXTERNAL ACCESS (same tools):
┌─────────────────────────────────────────────────────────────┐
│           MCP Server (MARIO-3594)                             │
│  CollectionSchemaTool | CollectionIndexesTool | ExplainTool   │
│  DbStatsTool | CollectionStorageSizeTool                      │
│  Deployed: 2026-06-08 | Assignee: David Contavalli           │
└─────────────────────────────────────────────────────────────┘
---

## PART 8: Key Facts & Gaps Summary

### What IS shipped (solid foundation)
- **6 agent tools** in Desktop, all v2026.9.0, all GA (Ultimate license)
- **AI Helper sidebar** with tab-context awareness
- **Query Profiler** finding slow queries (Pro + Ultimate)
- **MCP server** exposing same tools externally
- **LangChain4j** multi-step tool orchestration framework

### What is NOT shipped (the advisor gap)
| Gap | Details | Evidence |
|-----|---------|----------|
| **No recommendation logic** | LLM can fetch data but has no structured prompt/workflow to consistently produce index suggestions | KONG-11000 Won't Do |
| **No `$indexStats` exposure** | `list_indexes` returns definitions only, not access counts — can't detect unused indexes | Tool returns `getIndexes()` not `aggregate([{$indexStats:{}}])` |
| **No Profiler → AI pipeline** | Profiler and AI Helper are disconnected UI elements | No ticket exists linking them |
| **No proactive detection** | Everything is user-initiated; no background COLLSCAN alerting | Never proposed |
| **No "Apply" action** | AI can suggest `createIndex` command but user must copy-paste to IntelliShell | No `create_index` tool exists |
| **No compound index intelligence** | LLM lacks guardrails for ESR rule, prefix coverage, or key ordering | No prompt engineering for this |

### Key People
| Person | Role |
|--------|------|
| **Aleksei Beliaev** | Implemented all 6 agent tools |
| **Ivan Martynov** | AI Helper sidebar + Tab Context + research spike (KONG-10474) |
| **Eswaranaath MP** | Schema tool in AI Helper + Query Profiler (original) |
| **Hugo Almeida** | Reporter/stakeholder for agent tools story |
| **David Contavalli** | MCP server metadata tools |
| **Peter Hägglund** | Product lead, reported schema analyzer epic |

### Version Timeline
| Version | What shipped |
|---------|-------------|
| 2024.x | Query Profiler (KONG-8267) |
| 2026.7.0 | Schema analyze tool in AI Helper (KONG-10829) |
| 2026.9.0 | All agent tools + AI Helper sidebar + Tab Context (KONG-10788 family) |
| 2026-06 | MCP Server metadata tools (MARIO-3594) |
