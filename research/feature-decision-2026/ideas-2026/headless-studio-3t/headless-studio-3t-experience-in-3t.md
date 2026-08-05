Excellent — I found the **key ticket**. Let me get the full details on KONG-2339, which is the original CLI idea ticket.
Now let me get more context on the TTTL project (3TL Bridge) and the recent "Integration with Studio 3T tools" work, which is the closest existing implementation to a headless concept.
Now I have a comprehensive picture from Jira and Confluence. Let me compile the full research findings.

---

## Deep Research Summary: Headless Studio 3T (Ideas)

Here's everything we know internally about the concept of a "headless" or CLI-driven Studio 3T, drawn from Jira history, Confluence documentation, and the broader product evolution.

---

### 1. The Original CLI Idea — KONG-2339 (2018, Closed as "Won't Do")

The explicit request for a CLI was logged in **July 2018**: [KONG-2339](https://3tsoftwarelabs.atlassian.net/browse/KONG-2339)

> *"More and more users call for simple automation capability, something along the lines of:*
> `studio3t.exe --import --importSettings <file> --source importJob.json`
> `studio3t.exe --export --exportSettings <file> -out <outFile>`
> `studio3t.exe --query <query> --out <outFile>`
> *Then users would be able to create simple batch/shell scripts and cronjobs for automation using our product's features."*

**The decision:** A comment from July 2018 says plainly: **"Server 3T is how we'll tackle these."** — meaning the team chose to solve headless execution via a companion server product rather than a CLI wrapper.

Status: **Won't Do** — the idea was architecturally redirected to Server 3T.

---

### 2. Server 3T — The First "Headless" Attempt (2019–2022, Shipped & Later Deprecated)

Server 3T was the product answer to headless execution. Key epics:
- [KONG-3840](https://3tsoftwarelabs.atlassian.net/browse/KONG-3840) — "Server. Just Server." (master epic, 2019)
- [KONG-4939](https://3tsoftwarelabs.atlassian.net/browse/KONG-4939) — Server 3T Phase 2
- [KONG-4076](https://3tsoftwarelabs.atlassian.net/browse/KONG-4076) — Server-side scheduling
- [KONG-5368](https://3tsoftwarelabs.atlassian.net/browse/KONG-5368) — Make task scheduling available in Core/Pro (to support Server exports)
- [KONG-4935](https://3tsoftwarelabs.atlassian.net/browse/KONG-4935) — Confirms Server 3T was installed on **headless Linux servers**

**What it supported:** Remote execution of exports, SQL migrations, and scheduled tasks on a background server process, offloading from the desktop GUI.

**What it did NOT support:** Full CLI invocation from CI/CD, containerized execution, or automated sync. Two customer requests for automating the *synchronization* part of Data Compare & Sync were both closed **Won't Do**:
- [KONG-3285](https://3tsoftwarelabs.atlassian.net/browse/KONG-3285) — Anthem Insurance wanted scheduled sync (2019, Won't Do)
- [KONG-3752](https://3tsoftwarelabs.atlassian.net/browse/KONG-3752) — Another customer wanted automated DCS sync (2019, Won't Do)

---

### 3. The Current Evolution — "Integration with Studio 3T Tools" / studio.3t.io (2026, Done)

The concept has evolved into a **web-based remote task platform** at `studio.3t.io`:

- [KONG-10903](https://3tsoftwarelabs.atlassian.net/browse/KONG-10903) — "Integration with Studio 3T tools" (Epic, Done, April 2026)
    - Supported tasks: **Aggregation, Find Query, Export (to file), Import (from file), Export (to another collection)**
    - Two deliverables: (1) Save as remote tasks, (2) Open browser to the remote tasks list
- [KONG-10915](https://3tsoftwarelabs.atlassian.net/browse/KONG-10915) — Save Task on the remote server (Done)
- [KONG-10919](https://3tsoftwarelabs.atlassian.net/browse/KONG-10919) — Toolbar dropdown for Server Tasks (Done)
- [KONG-10920](https://3tsoftwarelabs.atlassian.net/browse/KONG-10920) — Remote Server(s) settings (Done)
- [KONG-10923](https://3tsoftwarelabs.atlassian.net/browse/KONG-10923) — Opens browser at `https://studio.3t.io/tasks?view=tasks` (Done)

**Assigned to:** Hugo Almeida. **This is the closest thing to "headless" that currently ships** — tasks saved from the desktop client execute on a remote web platform.

---

### 4. 3TL Bridge (TTTL project) — The Strategic Data Pipeline Product (2026, Experimental Release)

The [3t-Bridge Readiness page](https://3tsoftwarelabs.atlassian.net/wiki/spaces/P/pages/1205633045) describes a **fundamentally new product** that addresses many of the same use cases that a headless CLI would:

- **What it is:** A web-based ETL pipeline manager for MongoDB, Kafka, Google Pub/Sub, and HTTP, with Rhai sandboxed transforms, built-in PII masking, and AI assistant.
- **Deployment:** On-prem (Helm chart / Docker Compose) or managed hosting — **fully headless by design**.
- **Stage:** Experimental release, expected $170K ARR by end of 2026.
- **Key connectors:** MongoDB CDC, Kafka, Pub/Sub, HTTP, generator (synthetic data), scanner (bounded scans).
- **HA:** Leader election + checkpointing + consumer-group model.
- **Relevant for headless use case:** Pipelines are defined via config/API, not a GUI — they run on Kubernetes. This is inherently CI/CD-compatible.

However, Bridge is a **separate product** solving data pipeline/ETL, not a CLI wrapper around Studio 3T's existing task types (Import/Export Wizard, Data Compare & Sync, Data Masking, SQL Migration, IntelliShell scripts).

---

### 5. Related Product Ideas in PM Backlog

| Ticket | Summary | Status |
|--------|---------|--------|
| [PM-95](https://3tsoftwarelabs.atlassian.net/browse/PM-95) | Data federation pipelines | Logged |
| [PM-93](https://3tsoftwarelabs.atlassian.net/browse/PM-93) | Stream processing pipelines | Logged |
| [PM-41](https://3tsoftwarelabs.atlassian.net/browse/PM-41) | Execute aggregation query in any environment | Logged |

---

### 6. Key Gaps Confirmed — No CLI Binary Exists Today

Based on exhaustive search:
- ❌ **No headless CLI binary** for Studio 3T exists or is tracked in active development
- ❌ **No GitHub Actions / GitLab CI / Jenkins integration** exists
- ❌ **No containerized pipeline action** for Studio 3T tasks
- ❌ **Data Masking cannot be triggered programmatically** from CI/CD
- ❌ **Data Compare & Sync cannot automate the synchronization step** (only comparison is schedulable)
- ✅ `studio.3t.io` remote tasks exist but are web-triggered, not CLI-triggered
- ✅ 3TL Bridge is headless-native but covers pipeline/ETL, not Studio 3T's existing task library

---

### 7. Summary of the Product Arc

```
2018  KONG-2339: CLI idea logged → redirected to "Server 3T"
2019  Server 3T ships (headless Linux daemon for task execution)
2022  Server 3T reaches maturity (exports, SQL migration, scheduling)
2023  KONG-2339 closed as Won't Do
2026  studio.3t.io remote tasks (web-based remote execution, PoC)
2026  3TL Bridge (new headless pipeline product, experimental)
```

The concept of **headless Studio 3T** has been acknowledged as a need since 2018 but has been architecturally redirected twice — first to Server 3T (a background daemon), now to studio.3t.io + 3TL Bridge. **A proper CLI binary covering all 7 task types for CI/CD invocation remains unbuilt and untracked.**

---

Let me dig deeper into the full history — Server 3T's lifecycle, why it was discontinued, obstacles encountered, and the transitions between approaches.
This is a critical finding — **Server 3T was discontinued in March 2021**, just ~1 year after Phase 1 launched. Let me dig into why and what happened after.
Now let me get the critical ticket about removing Server 3T and understand the discontinuation decision:
Now let me get the full details of the removal ticket and check when Server 3T was actually launched publicly:
Now let me look at what led to the discontinuation — was there a discussion or a specific reason documented? Let me search for tickets around the discontinuation timeframe (March 2021):
Now let me look at the gap period (2021-2026) — was there anything between Server 3T's death and the studio.3t.io approach?
Now let me look at the LM-133 ticket which gives direct insight into the business decision, and search for context around the "relaunch" that was planned for 2021.2 but then cancelled:
Now let me search for context on what happened between 2021 and the new studio.3t.io approach — was there any "Super Mario" (web version) connection:
Now let me look at the early prototype work for Server 3T to understand the architecture challenges:
Now I have enough evidence to compile the complete historical narrative. Let me present the findings:

---

## Complete History: Headless Studio 3T — From Idea to Abandonment to Reinvention

Based on exhaustive search across Jira (60+ tickets) and Confluence, here is the full chronological story of why headless Studio 3T was attempted, what went wrong, and how it ended.

---

### Phase 0: The Original Ask (July 2018)

**[KONG-2339](https://3tsoftwarelabs.atlassian.net/browse/KONG-2339)** — "Introduce CLI (Command Line Interface) for automating tasks"

The ask was simple and direct:
> *"More and more users call for simple automation capability"*
> Example: `studio3t.exe --export --exportSettings <file> -out <outFile>`

**The architectural decision (3 days later, July 5, 2018):**
> "Server 3T is how we'll tackle these."

This single comment set the direction for the next 3 years. Rather than adding CLI flags to the existing desktop binary, the team chose to build a **separate server-side product**.

---

### Phase 1: Server 3T Development (Dec 2019 – Sep 2020)

**[KONG-3840](https://3tsoftwarelabs.atlassian.net/browse/KONG-3840)** — "Server. Just Server." (master epic, Dec 2019)
**[KONG-4071](https://3tsoftwarelabs.atlassian.net/browse/KONG-4071)** — "Server 3T Phase 1" (Feb 2020)

**What was built:**
- A Java-based headless daemon (initially Vert.x, later Spring Boot)
- Ran on headless Linux servers ([KONG-4935](https://3tsoftwarelabs.atlassian.net/browse/KONG-4935) confirms this)
- Supported **SQL migrations** as the first and only task type
- Required its own installation, JRE bundle ([KONG-4574](https://3tsoftwarelabs.atlassian.net/browse/KONG-4574)), licensing, and quota system
- Could run as a system service ([KONG-4483](https://3tsoftwarelabs.atlassian.net/browse/KONG-4483))
- Connected to Studio 3T desktop via proprietary protocol (SSL, custom port 3801)
- ~50 tickets shipped in Phase 1 alone (May–Sep 2020)

**Architectural challenge exposed early ([KONG-2393](https://3tsoftwarelabs.atlassian.net/browse/KONG-2393), the 2018 prototype):**
> *"The key surgery required to be able to make an export job run outwith the context of Studio 3T / in the new context of Server 3T"*
> *"We will need the connection information... the connection info is included in the export task description sent to the server. This also means we'll have to encrypt the job descriptions, as they'll contain sensitive connection info."*

This reveals the fundamental problem: Studio 3T's task execution engine was **deeply coupled to the desktop GUI context**. Making it run headlessly required extracting connection info, credentials, and task definitions into a transferable format — which in turn required encryption, serialization, and a whole client-server protocol.

---

### Phase 2: The "Relaunch" Attempt & Immediate Collapse (Feb–Mar 2021)

**[KONG-4939](https://3tsoftwarelabs.atlassian.net/browse/KONG-4939)** — "Server 3T Phase 2" (Sep 2020)

Phase 2 planned to add:
- Export task support on Server 3T ([KONG-5392](https://3tsoftwarelabs.atlassian.net/browse/KONG-5392))
- Repackaging as Spring Boot ([KONG-5391](https://3tsoftwarelabs.atlassian.net/browse/KONG-5391))
- Making task scheduling available in Core/Pro editions ([KONG-5368](https://3tsoftwarelabs.atlassian.net/browse/KONG-5368))

**Critical signals of trouble:**

1. **Nov 2020 — Version sync problems ([KONG-5151](https://3tsoftwarelabs.atlassian.net/browse/KONG-5151)):** They had to disable the "Server 3T version lower" warning because *"we don't plan to release Server 3T 2020.10"*. The server couldn't keep up with Studio 3T's desktop release cadence.

2. **Mar 2021 — Random execution failures during UX sessions ([KONG-5518](https://3tsoftwarelabs.atlassian.net/browse/KONG-5518)):** During customer demos, exports would randomly fail on Server 3T. The errors were intermittent and unreproducible — "after some random amount of time, the same operations will start working normally." This happened on their own hosted instance (`server3t.ext.cloud.3t.io`).

3. **Stuck task workers ([KONG-4528](https://3tsoftwarelabs.atlassian.net/browse/KONG-4528)):** Tasks would get permanently stuck due to error cascades. Workers entered bad states that could never recover without manual intervention.

---

### The Kill Decision (March 24–30, 2021)

**On March 24, 2021** — just 3 weeks after the UX session failures — the decision was made:

**[KONG-5610](https://3tsoftwarelabs.atlassian.net/browse/KONG-5610):** *"Since as a business we have decided to no longer continue to develop or sell Server 3T"*

**[KONG-4939](https://3tsoftwarelabs.atlassian.net/browse/KONG-4939) comment (Mar 30):** *"Closed as 'Won't Fix', since Server 3T is being discontinued."*

**[LM-133](https://3tsoftwarelabs.atlassian.net/browse/LM-133):** *"Since as a business we have decided to no longer continue to develop or sell Server 3T we need to remove it from License Manager Portal"*

The removal was thorough and immediate:
- Toolbar icon removed
- "Run on Server 3T" buttons removed from Export, SQL Migration, Tasks
- "Run locally" renamed to just "Run"
- License Manager tab removed
- Website pages discontinued
- EULA updated (eventually, by April 2024)
- Code removal ticket filed ([KONG-6562](https://3tsoftwarelabs.atlassian.net/browse/KONG-6562), though ironically closed as "Won't Do" — the dead code still exists in the repo as of 2025)

---

### Why It Failed: Reconstructed Causes

No single ticket states the reason explicitly ("since as a business we have decided" is as close as it gets), but the evidence points to a **convergence of factors**:

| Factor | Evidence |
|--------|----------|
| **Unreliable execution** | Random failures during customer UX sessions (KONG-5518); stuck task workers (KONG-4528); cascading errors |
| **Architectural coupling** | The desktop app's task engine was never designed for headless operation — extracting it required rebuilding the serialization, connection management, and credential handling (KONG-2393) |
| **Maintenance burden** | Couldn't keep pace with Studio 3T releases (KONG-5151 — skipped 2020.10); required separate install, JRE bundle, Spring Boot rewrite |
| **Narrow scope** | After 1+ year of development, only SQL Migration and Exports worked. Imports, Data Masking, DCS, IntelliShell Scripts — the task types customers actually wanted automated — never made it |
| **No commercial traction** | Server 3T required a separate license/quota; no evidence of significant customer adoption. Two customer requests for automated sync (KONG-3285, KONG-3752) were never fulfilled |
| **Team turnover** | All key contributors are now listed as "Former user" — the institutional knowledge left with them |

---

### The 5-Year Gap (2021–2026)

From April 2021 to April 2026, **nothing replaced Server 3T**. The headless use case went completely unaddressed in the product. During this period:
- Studio 3T's Task Scheduler continued to work, but **only locally on the desktop**
- Customers who needed automation fell back to custom scripts, cron jobs, or third-party ETL
- Competitors (DBeaver, NoSQLBooster) shipped their own CLI tools during this window

---

### The Resurrection: studio.3t.io (April 2026)

**[KONG-10903](https://3tsoftwarelabs.atlassian.net/browse/KONG-10903)** — "Integration with Studio 3T tools" (April 2026, Done)

A completely different approach emerged — instead of a headless daemon, tasks are saved to a **web platform** at `studio.3t.io`:
- Supported tasks: Aggregation, Find Query, Export (to file/collection), Import
- Tasks are saved from the desktop client to the remote platform
- Execution happens in the browser/cloud, not via CLI
- Built by Hugo Almeida (who also leads MARIO, the web-based Studio 3T)
- Minimal scope: just "save there as remote tasks" + "open browser in remote tasks list"

This is a **fundamentally different architecture** — web-first rather than daemon-first, and deliberately minimal rather than attempting to replicate the full desktop feature set.

---

### Meanwhile: 3TL Bridge (2026 — Experimental)

The [3t-Bridge](https://3tsoftwarelabs.atlassian.net/wiki/spaces/P/pages/1205633045) product takes the headless concept in yet another direction:
- **Purpose-built** as headless from day one (Kubernetes, Helm chart, Docker Compose)
- Covers data pipeline/ETL, not Studio 3T's existing task library
- Built in Rust (not Java), by a different team (Siamion Makarski)
- Includes PII masking (overlaps with Studio 3T's Data Masking)
- Has no connection to the old Server 3T codebase whatsoever

---

### Summary: Why "Headless Studio 3T" Has Never Shipped

| Attempt | Years | Outcome | Root Cause of Failure |
|---------|-------|---------|----------------------|
| CLI binary (KONG-2339) | 2018 | Redirected to Server 3T | Architectural: task engine too coupled to GUI |
| Server 3T Phase 1 | 2019–2020 | Shipped, limited scope | Only SQL Migration worked |
| Server 3T Phase 2 | 2020–2021 | **Killed after 6 months** | Reliability failures, maintenance burden, no commercial traction |
| 5-year gap | 2021–2026 | Nothing | No investment in the problem |
| studio.3t.io | 2026 | Shipped (minimal) | Web-triggered only, no CLI, limited task types |
| 3TL Bridge | 2026 | Experimental | Different product, different use case |

**The core obstacle that has never been overcome:** Studio 3T's task execution engine was designed as part of a monolithic desktop application. Every attempt to run it outside that context has either required rebuilding fundamental plumbing (Server 3T) or accepting severely reduced scope (studio.3t.io). A true headless CLI covering all 7 task types would require the same extraction surgery that made Server 3T so difficult — but with modern tooling (containers, APIs), the problem is more tractable today than it was in 2018.

---

# Headless Studio 3T — Deep Research Report

## 1. Customer Pain Points (Documented Demand, 2016–2023)

### 1.1 The Original Voices (Pre-Server 3T era, 2016–2018)

Customer demand for automation pre-dates any product response by **two full years**:

| Ticket | Date | Customer / Source | Exact Request |
|--------|------|-------------------|---------------|
| [KONG-966](https://3tsoftwarelabs.atlassian.net/browse/KONG-966) | Apr 2016 | Dave Nicolas, Banker's Healthcare Group | *"Would it be possible to add a set of services that would allow for creation of back end recurring jobs, automated backups and restore"* |
| [KONG-910](https://3tsoftwarelabs.atlassian.net/browse/KONG-910) | Mar 2016 | 6+ named customers (Canal Insurance, Acumen Solutions, Pretty Simple Games, etc.) | Aggregated: schedule sync, schedule backups, schedule CSV exports, **automate export/import from a separate script** — *"I want to generate the call from a separate script, if possible"* |
| [KONG-1648](https://3tsoftwarelabs.atlassian.net/browse/KONG-1648) | May 2017 | Angela Murray, Watermelon Research + 2 others | *"We are looking at alternative options and how we can automate exports/imports as it is currently a daily process for us (twice daily)"* — **urgency signal: considering alternatives** |
| [KONG-2339](https://3tsoftwarelabs.atlassian.net/browse/KONG-2339) | Jul 2018 | Internal (consolidating requests) | The formal CLI proposal: `studio3t.exe --export --exportSettings <file>` |

**Key insight:** By 2017, customers were already signaling they'd leave if automation wasn't addressed ("looking at alternative options"). The pain was:
- **Twice-daily manual export/import cycles** (Watermelon Research)
- **Production → dev sync** that had to be triggered manually
- **Backup scheduling** without any way to script it
- Desire to **invoke from external scripts** (not just GUI schedules)

### 1.2 Enterprise-Grade Requests (2019–2022)

| Ticket | Date | Customer | Pain Point |
|--------|------|----------|------------|
| [KONG-3285](https://3tsoftwarelabs.atlassian.net/browse/KONG-3285) | Jun 2019 | **Anthem Insurance** (from-sales label) | *"Would like to save/schedule the synchronisation portion of Data Compare & Sync. Currently only possible to schedule the comparison."* |
| [KONG-3752](https://3tsoftwarelabs.atlassian.net/browse/KONG-3752) | Nov 2019 | HubSpot customer | Same: automate DCS sync (not just compare). Dev noted: *"This ticket will probably only be relevant if we rework DCS. As it stands, it's non-trivial."* |
| [KONG-4926](https://3tsoftwarelabs.atlassian.net/browse/KONG-4926) | Sep 2020 | 3 HubSpot tickets + 2 UserVoice | Tasks every 5 minutes (not just daily/weekly) — wanting near-real-time ETL behavior from a GUI tool |
| [KONG-6703](https://3tsoftwarelabs.atlassian.net/browse/KONG-6703) | Dec 2021 | Customer running 10 identical tasks per rollout | *"Is it possible to configure tasks to take the target database as a parameter?"* — wanting CLI-style parameterization |
| [KONG-5875](https://3tsoftwarelabs.atlassian.net/browse/KONG-5875) | May 2021 | UserVoice + HubSpot | Email notifications on task completion — customer **requested a pre-release** |

### 1.3 The Fundamental Desktop Limitation

The deepest pain point was articulated perfectly by the team themselves in [KONG-5875](https://3tsoftwarelabs.atlassian.net/browse/KONG-5875) (July 2022):

> **"We think that this is not a feature that would be expected from a Desktop tool. So we will rather not do it anymore. Of course it still would make a lot of sense for a Server 3T solution."**

This reveals the core tension: **customers needed server-grade capabilities (unattended execution, notifications, parameterization, CI/CD triggering) from a desktop application that was architecturally incapable of providing them.**

---

## 2. Architectural Decisions — Why CLI Was Rejected in Favor of Server 3T

### 2.1 The July 2018 Decision

When KONG-2339 proposed adding `--export`/`--import`/`--query` flags to the desktop binary, the response (3 days later) was:

> **"Server 3T is how we'll tackle these."**

**Why this decision was made (reconstructed from code evidence):**

Studio 3T is built on **Eclipse SWT** — a heavyweight desktop GUI toolkit. The entire application architecture is:
- Monolithic Java application (`Studio3TApp.main()` → `AppRunner` → SWT event loop)
- All task execution runs on the **SWT UI thread** (`org.eclipse.swt.widgets.Display.readAndDispatch()`)
- Connection management, credential storage, task serialization — all coupled to the GUI context
- Even the Task Scheduler runs inside `TaskScheduleManager` which dispatches via `RunnableLock.run()` on the SWT thread

**Making this run headlessly would mean:**
1. Stripping out SWT dependencies from the task execution path
2. Extracting connection info, credentials, and task definitions into a standalone serialization format
3. Handling encryption of sensitive data independently of the desktop keystore
4. Managing the lifecycle without a GUI event loop

The team concluded this was **too invasive** for the desktop codebase and chose instead to build a separate server process that could reuse the business logic modules (`data-man-mongodb-ent`) without the GUI layer.

### 2.2 The Architecture of Server 3T

From [KONG-2393](https://3tsoftwarelabs.atlassian.net/browse/KONG-2393) (the original prototype, July 2018):

> *"The key thing we want to achieve is to have Server 3T receive a description of an export job, and be able to execute it."*
> *"The connection info is included in the export task description sent to the server. This also means we'll have to encrypt the job descriptions."*
> *"Don't be afraid of working with the data directly for the descriptions of the export jobs. I'm loath to bind them to a fixed class definition."*

**Stack evolution:**
- **Phase 1 (2020):** Vert.x reactive server + custom protocol + proprietary licensing/quota system
- **Phase 2 attempt (Feb 2021):** Repackaged as Spring Boot ([KONG-5391](https://3tsoftwarelabs.atlassian.net/browse/KONG-5391)) — replacing Vert.x with Spring MVC ([KONG-5394](https://3tsoftwarelabs.atlassian.net/browse/KONG-5394))

This rewrite happened just **6 weeks before discontinuation** — suggesting the team already knew the Vert.x architecture wasn't viable and was desperately trying to salvage the product with a different framework.

---

## 3. Why Server 3T Failed — Root Causes

### 3.1 Technical Reliability Problems

**Intermittent execution failures during live customer demos ([KONG-5518](https://3tsoftwarelabs.atlassian.net/browse/KONG-5518), Mar 2021):**
> *"During the most recent rounds of Server 3T UX sessions we had two cases where our customers would randomly receive errors when trying to execute Exports on Server 3T."*
> *"Then, all of a sudden, after some random amount of time, the same operations will start working normally."*

This happened on 3T's **own hosted instance** (`server3t.ext.cloud.3t.io`) — they couldn't even make it reliable for demos.

**Stuck task workers ([KONG-4528](https://3tsoftwarelabs.atlassian.net/browse/KONG-4528)):**
Workers would enter permanently stuck states, blocking all subsequent tasks. Restarting the server after stuck workers caused **license errors** ([KONG-4529](https://3tsoftwarelabs.atlassian.net/browse/KONG-4529)).

**Cross-platform serialization issues ([KONG-5398](https://3tsoftwarelabs.atlassian.net/browse/KONG-5398)):**
Exporting from Windows Studio 3T to Linux Server 3T produced **empty zip files** — the task format wasn't properly abstracted from the OS.

**Entropy starvation on headless Linux ([KONG-4935](https://3tsoftwarelabs.atlassian.net/browse/KONG-4935)):**
SSH tunnel connections timed out on headless servers because Java's `SecureRandom` blocked on `/dev/random` without a display server providing entropy.

### 3.2 Scope Problem — Couldn't Keep Up

After **16 months** of development (Dec 2019 – Mar 2021), Server 3T supported only:
- ✅ SQL Migrations (Phase 1)
- ✅ Exports (added in Phase 2, the final 6 weeks)
- ❌ Imports — never shipped
- ❌ Data Compare & Sync — never shipped
- ❌ Data Masking — never shipped
- ❌ IntelliShell Scripts — never shipped
- ❌ Collection tasks — never shipped

The task types customers **most** wanted automated (DCS sync, Data Masking) were never even attempted.

### 3.3 Version Coupling — Release Cadence Mismatch

Server 3T couldn't keep pace with Studio 3T's desktop releases:
- [KONG-5151](https://3tsoftwarelabs.atlassian.net/browse/KONG-5151) (Nov 2020): *"We don't plan to release Server 3T 2020.10"* — version check warning had to be disabled
- Server 3T shipped as a **companion binary** requiring manual installation, separate JRE, and tight version alignment with the desktop client
- Every Studio 3T release risked breaking Server 3T's task format compatibility

### 3.4 Commercial Model Challenges

- Required **separate licensing with quota-based billing** ([KONG-4427](https://3tsoftwarelabs.atlassian.net/browse/KONG-4427), [KONG-4433](https://3tsoftwarelabs.atlassian.net/browse/KONG-4433))
- Proof of Concept licenses limited to 1000 documents
- Beta access gated by license flags ([KONG-4498](https://3tsoftwarelabs.atlassian.net/browse/KONG-4498))
- No evidence of any paying customer ever recorded in Jira

### 3.5 Team/Knowledge Concentration

- Every single contributor to Server 3T is now listed as **"Former user"** in Jira
- The Vert.x→Spring rewrite, the task format design, the quota system — all knowledge left the company
- No documentation or retrospective was written (confirmed: no Confluence page exists)

---

## 4. Effort Invested

### 4.1 Ticket Count (Hard Evidence)

| Label/Category | Ticket Count | Period |
|---------------|-------------|--------|
| `product-server-3t` | **78 tickets** | Dec 2019 – Nov 2021 |
| `product-server-3t-backend` | **14 additional tickets** | Sep 2020 – Mar 2021 |
| Related tickets (removal, EULA, LM) | ~8 tickets | Mar–Apr 2021 |
| **Total tracked effort** | **~100 tickets** | **16 months** |

### 4.2 Timeline Reconstruction

| Period | Duration | Work Done |
|--------|----------|-----------|
| Jul 2018 – Dec 2019 | 17 months | Prototype exploration (KONG-2393, ultimately abandoned) |
| Dec 2019 – Sep 2020 | 9 months | Phase 1: Full build — daemon, licensing, quota, UI integration, manual, SQL migration support |
| Sep 2020 – Mar 2021 | 6 months | Phase 2: Spring rewrite, export support, UX sessions with customers |
| Mar 2021 | 2 weeks | Complete removal from product (KONG-5610), license portal, website, EULA |
| Nov 2021 | — | Code cleanup proposed (KONG-6562) but never executed; dead code remains |

### 4.3 Estimated Effort

With ~78 deployed tickets across 15 months, and assuming roughly even distribution:
- **~5 tickets/month** of dedicated work
- Involves minimum **2-3 developers** (backend server dev + desktop integration dev + QA)
- Plus licensing server changes, documentation, UX sessions
- **Conservative estimate: 15–20 person-months of engineering** invested and discarded

---

## 5. The Decision to Kill (March 2021)

The decision was framed identically across 3 tickets:

> *"Since as a business we have decided to no longer continue to develop or sell Server 3T"* — KONG-5610, LM-133

No retrospective document exists. No post-mortem was written. The language ("as a business we have decided") suggests a **top-down strategic call**, not a gradual deprecation.

**Contextual factors at the time of the kill:**
1. UX session failures (Mar 3, 2021 — KONG-5518) happened **3 weeks** before the kill (Mar 24)
2. The Spring Boot rewrite had just been completed (Feb 8, 2021) — suggesting the team had already tried their "last resort" fix
3. Phase 2 was never completed — only exports made it; imports were still being discussed
4. No paying customers are evidenced in any ticket

---

## 6. What Happened After (2021–2026)

### 6.1 The "Server 3T Still Makes Sense" Echo (Jul 2022)

In KONG-5875, when declining email notifications for tasks, the team wrote:
> *"We think that this is not a feature that would be expected from a Desktop tool. Of course it still would make a lot of sense for a **Server 3T solution**."*

14 months after killing Server 3T, they were **still referencing it as the correct solution** for server-grade features — acknowledging the gap remained unfilled.

### 6.2 The studio.3t.io Approach (Apr 2026)

Five years later, [KONG-10903](https://3tsoftwarelabs.atlassian.net/browse/KONG-10903) took a deliberately minimal approach:
- "Proof of concept integration" — explicitly labeled as PoC
- Only 2 deliverables: save remote tasks + open browser to task list
- Web-triggered, not CLI-triggered
- No scheduling, no CI/CD integration, no notifications

### 6.3 3TL Bridge (Jul 2026) — A New Product, Not a Fix

Bridge solves the underlying problem differently:
- Built in **Rust** (not Java) — no SWT/Eclipse baggage
- **Headless-native** from day one (Kubernetes, Helm)
- Purpose-built for data pipelines, not wrapping existing desktop task types
- Covers PII masking (overlaps with Data Masking) and CDC (overlaps with DCS)
- **Does NOT cover:** SQL Migration, Import/Export Wizard, IntelliShell scripts

---

## 7. Lessons (Reconstructed from Evidence)

### Lesson 1: "Extracting Headless from Desktop is Fundamentally Harder Than Building Headless-First"

Server 3T tried to reuse `data-man-mongodb-ent` (the core library) in a server context. But:
- Task serialization was OS-dependent (Windows→Linux = empty zips)
- Credential handling was desktop-keystore-dependent
- Connection testing blocked on OS entropy
- The SWT event loop assumptions were baked into scheduling

**3TL Bridge learned this:** built from scratch in Rust, with no shared codebase.

### Lesson 2: "A Companion Product Creates Two Maintenance Burdens, Not One"

Server 3T required:
- Separate release cadence (couldn't keep up)
- Separate JRE bundle
- Separate licensing/quota system
- Separate installation & configuration
- Version-locked compatibility with the desktop client

**This effectively doubled the surface area** for a small team, while only covering 2 of 7 task types.

### Lesson 3: "Demo-Failing Reliability Kills Products Instantly"

The UX session failures (KONG-5518) — on 3T's own hosted instance — were the proximate trigger. When your product fails **during customer demos**, no amount of technical promise saves it.

### Lesson 4: "No Paying Customer = No Mandate to Fix"

Server 3T never acquired evidenced paying customers. Without revenue:
- Bugs were tolerable to close as "Won't Do"
- Phase 2 scope could be endlessly deferred
- The kill decision had no revenue impact to weigh against

### Lesson 5: "Scope Creep via Feature Parity is Lethal"

The original ask (KONG-2339) was simple: `studio3t.exe --export ...`. The chosen solution was a full server product with its own licensing, quota, multi-user scheduling, and eventually a Spring Boot rewrite. The ambition far exceeded the ask.

### Lesson 6: "Document Nothing = Repeat Everything"

- No retrospective was written
- No architecture decision record exists
- No post-mortem in Confluence
- All contributors left the company
- The dead code remains in the repo (KONG-6562 never executed)
- The same tension resurfaced 5 years later with studio.3t.io

### Lesson 7: "Customers Don't Want a Server — They Want a Command"

Reviewing all customer requests:
- *"Generate the call from a separate script"* (KONG-910)
- *"Take the target database as a parameter"* (KONG-6703)
- *"Automate exports/imports — it's currently a daily process"* (KONG-1648)
- *"Schedule the synchronisation portion"* (KONG-3285)

None of these requested a separate server product. They requested **CLI invocation of existing capabilities**. The product response over-engineered the solution relative to the ask.

---

## 8. Current State Summary (Aug 2026)

| Capability | Status | Product |
|------------|--------|---------|
| CLI binary for Studio 3T tasks | ❌ Never existed | — |
| Headless server daemon | ❌ Killed Mar 2021 (Server 3T) | Dead code in repo |
| Web-based remote tasks | ✅ PoC shipped Apr 2026 | studio.3t.io |
| CI/CD pipeline integration | ❌ Does not exist | — |
| Headless data pipeline execution | ✅ Experimental | 3TL Bridge (different product) |
| Parameterized task invocation | ❌ Never built | — |
| Email/webhook notifications on tasks | ❌ Explicitly declined | — |

**The 2016 customer ask remains substantially unaddressed 10 years later.**
