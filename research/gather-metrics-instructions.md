> **Status: rewritten 2026-09-04 (disposition: rewrite as compliant).** The original version of this document instructed scraping G2, Capterra, TrustRadius, and Reddit — all of which restrict automated collection in their Terms of Service — alongside legitimately compliant sources (Studio 3T's own public forum, public competitor changelogs). This rewrite removes the non-compliant sources and keeps the rest of the framework (extraction method, metric translation, output schema, deduplication) unchanged, since none of that is source-specific. [`reports/voice-of-customer-metrics.md`](../reports/voice-of-customer-metrics.md) already executed exactly this compliant subset as a 7-record pilot — treat that report as the worked example of this framework, not just a "what was dropped" note. See `update-plans/06-retire-or-rewrite-methodology-docs.md` for the disposition rule applied here.

Here is the human-readable guide for **Part 1: Metrics Gathering**, designed to show exactly where and how **Claude** (acting as an autonomous AI agent) collects, analyzes, and quantifies product feedback from the public internet without requiring internal logins or credentials — using only sources that permit automated, unauthenticated collection.

---

## Autonomous Public Metrics Gathering Framework

To build a defensible product roadmap without internal database access, Claude operates as an unauthenticated web research agent. It continuously monitors public developer channels, extracts unstructured user feedback, translates human sentiment into quantifiable metrics, and benchmarks Studio 3T against its primary market competitors.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      CLAUDE AI AGENT HARVESTING FLOW                    │
└─────────────────────────────────────────────────────────────────────────┘
                                     │
                  ┌──────────────────┴──────────────────┐
                  ▼                                      ▼
┌─────────────────────────┐                    ┌─────────────────────────┐
│  PUBLIC DISCOURSE       │                    │  COMPETITOR CHANGELOGS  │
│  - Studio 3T Forum      │                    │  - MongoDB Compass      │
│  (Stack Overflow: check,│                    │  - DBeaver (GitHub)     │
│   low yield confirmed)  │                    │  - Navicat              │
└────────────┬────────────┘                    └────────────┬────────────┘
             │                                              │
             └──────────────────────┬───────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     CLAUDE SEMANTIC PROCESSING ENGINE                   │
│   • HTML Extraction & Text Cleaning                                     │
│   • Entity Mapping to Feature Dictionary                                │
│   • Sentiment & Pain Severity Scoring (1–5)                             │
│   • Enterprise Keyword Detection & Workaround Tagging                   │
└─────────────────────────────────────────────────────────────────────────┘
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     STRUCTURED METRIC METRICS STORE                     │
└─────────────────────────────────────────────────────────────────────────┘

```

**Removed from the original version, and why:** Reddit (automated collection restricted by Reddit's Terms of Service outside its official API), and G2/Capterra/TrustRadius (all three explicitly prohibit automated scraping of review content in their Terms of Service). Do not add these back without first confirming a ToS-compliant access path (e.g., an official, authenticated API with a data-use license that permits this purpose) — "it's publicly visible in a browser" is not the same as "permitted to be scraped."

---

## 1. Public Internet Data Sources

Claude targets two compliant public internet categories to gather user sentiment and feature demand (Stack Overflow may optionally be checked as a third, but see the note below):

### A. Studio 3T Community Forum (`community.studio3t.com` — migrated from `forum.studio3t.com`)

* **Why It Matters**: The highest-density source of direct user feedback, feature requests, and bug reports from active Studio 3T users, published by 3T Software Labs itself.
* **What Claude Looks For**: Community discussions around missing tools, visual editor bugs, performance bottlenecks, and database connection issues.

### B. (Optional) Stack Overflow

* **Status**: Checked during the 2026-07-29 pilot ([`reports/voice-of-customer-metrics.md`](../reports/voice-of-customer-metrics.md)) via Stack Overflow's own search — no ToS issue with searching public Q&A this way. Confirmed low/no signal for Studio-3T-specific content at that time; re-check periodically rather than treating it as a dead source permanently, but don't force inclusion if a check comes up empty.

### D. Competitor Release Logs & Documentation

* **Target Endpoints**:
* **MongoDB Compass**: Public release notes (`[mongodb.com/docs/compass/current/release-notes](https://mongodb.com/docs/compass/current/release-notes)`)
* **DBeaver**: GitHub public release logs (`[github.com/dbeaver/dbeaver/releases](https://github.com/dbeaver/dbeaver/releases)`)
* **Navicat for MongoDB**: Official release notes (`navicat.com`)


* **Why It Matters**: Provides real-time visibility into feature additions by competitors.
* **What Claude Looks For**: New capabilities shipped by competitors that Studio 3T currently lacks (identifying competitive gaps).

---

## 2. Web Retrieval & Extraction Methods

Claude uses targeted web queries and text-parsing methods to discover and ingest data across these channels.

### Search Engine Query Strategy

Claude executes precise web search strings via public search endpoints (such as DuckDuckGo HTML or Bing Search) to find relevant discussions without logging in:

* **Finding User Friction & Workarounds**:
`site:community.studio3t.com ("slow" OR "crash" OR "error" OR "workaround" OR "freeze")`
* **Finding Missing Feature Requests**:
`site:community.studio3t.com ("feature request" OR "would be great" OR "missing")`
* **Uncovering Switcher & Comparison Signals (compliant form)**:
`site:community.studio3t.com ("Compass" OR "DBeaver" OR "alternative")` — scoped to Studio 3T's own forum, not a third-party site whose ToS restricts automated search/collection.

Removed: the original version of this section also included example `site:` queries against `reddit.com` and `g2.com`. Do not run automated queries scoped to those domains — see the removal note above.

### HTML Processing & Text Cleansing

When Claude fetches a public web page, it automatically cleans the content before analysis:

1. **Removes Web Noise**: Strips out navigation bars, headers, footers, advertisements, and JavaScript code.
2. **Isolates Thread Content**: Extracts only the main post title, body text, user comments, upvote counts, and publication dates using target HTML container tags.
3. **Converts to Plain Text**: Standardizes raw HTML into clean Markdown text for semantic analysis.

---

## 3. How Claude Translates Text into Quantifiable Metrics

Once plain text is harvested, Claude reads and evaluates the content, converting qualitative human prose into five standardized metrics:

```
Raw Text Input:
"Studio 3T crashed when opening our sharded cluster. We had to write a custom Python script to run this aggregation!"

                                 │
                                 ▼
                     CLAUDE EXTRACTION PROCESS
                                 │
  ├── 1. Feature Identified  ►  CONN-sharded-cluster-timeout
  ├── 2. Pain Severity       ►  5 / 5 (Application Crash)
  ├── 3. Enterprise Signal   ►  Detected ("sharded cluster")
  └── 4. Workaround Present  ►  True ("custom Python script")

```

### Metric 1: Feature Mapping (`feature_id`)

Claude maps every user comment or review to a specific feature in Studio 3T’s Unified Feature Dictionary (e.g., `AGG-visual-builder`, `CONN-readonly-lock`, `SQL-query-translator`). If a requested capability is entirely new, Claude creates a standardized short identifier for it.

### Metric 2: Pain Severity Score (1 to 5 Scale)

Claude evaluates the user's emotional intensity and operational frustration to assign a numerical severity rating:

* **1 (Mild Request)**: Cosmetic suggestions, minor UI adjustments, or nice-to-have visual themes.
* **2 (Minor Inconvenience)**: Clunky navigation or extra clicks required, but the task is easily achievable.
* **3 (Workflow Drag)**: Noticeably slow performance or confusing interfaces that delay daily work.
* **4 (Major Impairment)**: Missing critical capabilities that force the user to open a secondary tool.
* **5 (Blocking Issue / Crash)**: Application crashes, data corruption risks, or inability to connect to production databases.

### Metric 3: Enterprise Signal Multiplier

To estimate commercial value without access to internal CRM data, Claude scans text for **Enterprise Indicators**—keywords that signify the feedback comes from a high-value enterprise user:

* *Enterprise Indicators*: `"SOC2"`, `"sharded cluster"`, `"AWS DocumentDB"`, `"production cluster"`, `"Single Sign-On (SSO)"`, `"SAML"`, `"team license"`, or `"audit logs"`.

If these indicators are present, Claude flags the record as **Enterprise-Linked**, giving it higher weight in the prioritization model.

### Metric 4: Workaround Friction Flag

Claude analyzes whether the user had to invent a workaround because Studio 3T lacked a feature or failed to execute a task.

* *Workaround Signals*: Phrasing like *"I had to export to CSV and write a Python script"*, *"We use DBeaver alongside Studio 3T just for this"*, or *"I ended up using the terminal command line instead"*.

### Metric 5: Competitor Parity Gap Flag

By cross-referencing competitor release notes, Claude checks if a capability requested by Studio 3T users is already fully supported in competitor tools (MongoDB Compass, DBeaver, or Navicat).

* *Status*: Marked as **High Urgency Gap** if two or more competitors already offer the feature.

---

## 4. Structured Output Data Schema

After evaluating a thread or review, Claude outputs a standardized, structured record. These records form the raw input data for **Part 2 (Cumulative Report Calculation)**.

| Metric Field | Type | Description | Example Value |
| --- | --- | --- | --- |
| **Source URL** | Text | Direct public URL of the harvested page | `[https://forum.studio3t.com/t/topic-slug/123](https://forum.studio3t.com/t/topic-slug/123)` |
| **Target Product** | Categorical | Primary software referenced | `Studio 3T` |
| **Feature ID** | Identifier | Feature Dictionary Code | `CONN-readonly-lock` |
| **Feedback Type** | Categorical | Nature of the post | `usability_friction` |
| **Pain Severity** | Numeric (1–5) | Claude-evaluated frustration score | `5` |
| **Manual Workaround?** | Boolean | Did the user need a workaround? | `True` |
| **Enterprise Signals** | List | Extracted enterprise context keywords | `["production", "sharded_cluster"]` |
| **Competitor Gap** | Boolean | Do competitors already have this? | `True (Supported in Compass & DBeaver)` |
| **User Quote** | Text | Key verbatim statement extracted by Claude | *"We almost wiped our production database because there is no read-only lock toggle!"* |

---

## 5. Deduplication & Data Integrity

To ensure metrics are accurate and not skewed by duplicate records, Claude applies two automatic validation rules:

1. **Content Hashing**: Claude generates a unique digital signature for every webpage it reads. If the same forum post or review is scraped twice, it is automatically discarded.
2. **Bot & Spam Filtering**: Claude screens out automated marketing posts, generic SEO spam, and duplicate cross-posts, keeping only authentic human developer feedback in the metric pipeline.