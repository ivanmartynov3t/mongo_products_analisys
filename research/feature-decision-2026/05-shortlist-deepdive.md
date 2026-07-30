# Stage 3 — Shortlist Deep-Dive

## Navigation

- [← Scored long-list](04-scored-longlist.md)
- [Next stage: verification →](06-verification-notes.md)

## Method executed

Per candidate: (a) fresh search on current competitor implementation depth, (b) fresh search for 2026 Studio 3T/3T Software Labs roadmap signal, (c) direct `community.studio3t.com`-targeted search, (d) technical feasibility check against Studio 3T's documented architecture (JVM desktop client; existing Explain Plan/Profiler/Schema-sampling/Task Scheduler infrastructure per the feature reports).

## Candidate 4: Headless CLI / CI-CD pipeline automation — **scores revised**

**(a) Competitor depth found:** DBeaver Enterprise/Ultimate already ships exactly this capability: a `-runTask TASK_ID` command-line flag (via `dbeaver-cli.exe` on Windows) that launches a saved task immediately, with `-var` flags to override task variables at invocation time, plus integration with OS-level schedulers (Windows Task Scheduler, cron). Source: [DBeaver Command Line wiki](https://github.com/dbeaver/dbeaver/wiki/Command-Line), [DBeaver Task Scheduler docs](https://dbeaver.com/docs/dbeaver/Task-Scheduler/).

**(b) Studio 3T roadmap signal:** none found specific to headless/CLI task triggering in the 2026 changelog reviewed in Stage 1e.

**(c) Community corroboration beyond the original VoC record:** found two additional, independent signals — a community forum thread "[How to create a Task with runtime parameters](https://community.studio3t.com/t/how-to-create-a-task-with-runtime-parameteres/784)" and a dedicated customer-feedback item on 3T's own UserVoice board, "[Task Scheduler in UI to run queries and extract results to specific location](https://3t-io.uservoice.com/forums/265122-share-your-ideas-with-us/suggestions/33329998-task-scheduler-in-ui-to-run-queries-and-extract-re)". Both independently reinforce demand for more flexible/parameterized/externally-triggerable task execution, beyond the single VoC pilot quote.

**(d) Feasibility:** DBeaver is architecturally comparable (Eclipse RCP, JVM) and successfully shipped a CLI mode without redesigning its core engine — a directly relevant existence proof that this is buildable on a similar stack without disproportionate effort.

**Score revision:**
- Evidence Strength: 4 → **5** — now corroborated by 3 independent Tier C signals (original VoC record + forum thread + UserVoice item) plus the Tier B recommendation — genuine convergence across research + multiple independent customer touchpoints.
- Competitive Urgency: 3 → **4** — this is no longer "some competitors have partial capability," it's a **confirmed, concretely-documented DBeaver Enterprise feature** with a specific, mature CLI syntax. This changes the framing materially (see note below).
- Reach, Severity, Build Effort: unchanged (4, 3, 2).
- **Revised Priority Score: (5+4+3+4)/2 = 16/2 = 8.00**

**⚠️ Objective-fit note:** this candidate's story has shifted from "possible differentiator" to **explicitly closing a documented DBeaver Enterprise capability gap**. Given the user's stated primary objective is "widen the lead," not "close a gap," this is a real tension worth surfacing plainly in the final memo — even though it is now the single highest-scoring candidate in the entire long-list. The counter-argument: closing this specific gap also *directly and definitively* resolves a real, cited, vendor-confirmed customer complaint (VoC record #2), which is a concrete, low-effort win regardless of how it's framed strategically.

## Candidate 18: Slack/Teams/Jira/PagerDuty webhook notifications — reaffirmed

**(a) Competitor depth:** no specific evidence found (search returned generic webhook/Slack integration content unrelated to any named MongoDB GUI competitor).
**(b) Studio 3T roadmap signal:** none found.
**(c) Community corroboration:** search for `community.studio3t.com` + Slack/webhook/notification returned no on-domain results — no additional Tier C evidence beyond the original Tier B research recommendation and the Tier A in-house precedent (3T Lens's `GOV-003`).
**(d) Feasibility:** confirmed low-risk — this is additive to the existing, already-documented Task Scheduler notification pipeline (`SCHED-notifications`, `SCHED-email`).

**Score revision: none.** No new evidence surfaced in either direction. **Priority Score remains 7.00.**

## Candidate 19: Automated PII classification/discovery — **scores revised**

**(a) Competitor depth found:** the broader PII/DSPM discovery market (BigID, Strac, Varonis, IBM Guardium) is large and active in 2026, but confirmed to be **standalone platforms, not built-in database-GUI-client features** — no evidence any of DBeaver/DataGrip/Navicat/TablePlus has a native PII scanner. This reinforces reading this as a genuine differentiation opportunity, consistent with the "widen the lead" objective.

**(b) Studio 3T roadmap signal / technical detail:** found concrete documentation of the existing in-house implementation (the `scan_pii` capability, evidently the mechanism behind 3T MCP's `AI-011`): it samples the collection, classifies every field by **both name and value pattern**, sorts findings into four tiers (**Critical / PII / Potentially Sensitive / Likely Safe**) with a confidence score and a regulation hint per finding, explicitly flags free-text fields it can't fully classify (`isProse: true`) rather than guessing, and caps/redacts sample values so the scan itself can't leak data. Source: studio3t.com blog and knowledge-base content surfaced via search.

**(c) Community corroboration:** none found specifically requesting this for Desktop.

**(d) Feasibility:** **confirmed strong** — the classification logic, confidence scoring, and safety controls are already fully designed and working in production (in 3T MCP). Porting to Desktop is substantially an integration/UI job, not new invention.

**Score revision:**
- Evidence Strength: 4 → **5** — now backed by concrete confirmation that the existing implementation is sophisticated and production-proven (4-tier classification, confidence scoring, prose-handling, safety controls), not just "exists somewhere."
- Build Effort: 2 → **2** (reaffirmed, if anything more confident it's low — the hard design work is done).
- Reach, Severity, Competitive Urgency: unchanged (4, 3, 2).
- **Revised Priority Score: (5+4+3+2)/2 = 14/2 = 7.00**

## Candidate 1: AI-driven query/index performance advisor — reaffirmed

**(a) Competitor depth:** reaffirms Stage 1e's finding — no named "index advisor"/"query optimizer" feature confirmed at the GUI-client layer for DBeaver, DataGrip, or Navicat as of 2026; MongoDB's own Atlas Performance Advisor remains platform-level, not GUI-client-level.
**(b) Studio 3T roadmap signal:** none found specific to this.
**(c) Community corroboration:** not separately re-searched in Stage 3 (already well-supported by 5 Tier B sources in Stage 1/2).
**(d) Feasibility:** Studio 3T already has `IDX-explain-full` (full execution-stats explain) and `IDX-profiler-analysis` (query grouping, COLLSCAN flags) — a rule-based recommendation layer on top of data these features already surface is a bounded, tractable v1.

**Score revision: none. Priority Score remains 5.00.**

## Candidate 9: Queryable Encryption (QE)/CSFLE key-vault configuration UI — reaffirmed, with one clarification

**(a) Competitor depth:** reaffirmed — Compass's In-Use Encryption UI (view encrypted fields under Advanced Connection options, KMS credential config) remains the only confirmed GUI-client implementation among the products in this analysis.
**(b) Studio 3T status:** a targeted search for Studio 3T's own QE/CSFLE documentation found **no evidence of existing support** — the only encryption-related Studio 3T feature found was **connection password encryption via a cryptographic key store**, which protects Studio 3T's own stored credentials, not MongoDB data via QE/CSFLE. This is a different capability entirely and does not reduce this candidate's gap status.
**(c) Community corroboration:** not separately searched in Stage 3.
**(d) Feasibility:** MongoDB's drivers provide the QE/CSFLE client-side library; Studio 3T's job is the configuration/management UI, not the cryptography itself.

**Score revision: none. Priority Score remains 5.00.** The Stage 3 search strengthens confidence this is a genuine, unaddressed gap for Studio 3T specifically (not just "unverified" — actively searched for and not found).

## Updated shortlist ranking after Stage 3

| Candidate | Stage 2 score | Stage 3 score | Change |
|---|---|---|---|
| 4 — Headless CLI/CI-CD automation | 7.00 | **8.00** | ↑ (evidence + urgency revised) |
| 18 — Webhook notifications | 7.00 | 7.00 | — |
| 19 — PII classification/discovery | 6.50 | **7.00** | ↑ (evidence revised) |
| 1 — AI query/index advisor | 5.00 | 5.00 | — |
| 9 — QE/CSFLE key-vault UI | 5.00 | 5.00 | — |

Candidate 4 remains the top-scored candidate after deeper research, but its case has shifted materially: it is now clearly evidenced as **closing a specific, named DBeaver Enterprise capability**, not a lead-widening move. This is the central tension Stage 4 verification and the Stage 5 memo must address explicitly rather than let the score alone decide.
