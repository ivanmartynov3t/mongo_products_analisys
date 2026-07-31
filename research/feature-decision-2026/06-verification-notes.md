# Stage 4 — Adversarial Self-Verification (+ Stage 6 full-review addendum)

## Navigation

- [← Shortlist deep-dive](05-shortlist-deepdive.md)
- [Final memo →](../../reports/next-feature-recommendation.md)
- [Stage 6 addendum ↓](#stage-6-full-review-fact-verification-addendum)
- [Stage 8 addendum ↓](#stage-8--2026-07-31-dictionary-gap-analysis-sync-addendum)

## Method executed

Per shortlisted candidate: re-opened every cited source to confirm it says what was attributed to it; searched for disconfirming evidence; re-derived Severity/Urgency from primary text rather than my own earlier paraphrase; labeled every claim confirmed / roadmap-inferred / unverified.

## Finding: a real citation-drift catch on Candidate 4

Stage 3 claimed two community sources "corroborated" demand for external/CLI task triggering, based on their **search-result titles**. Fetching both directly (not just reading the search snippet) shows **neither actually supports that claim**:

| Source | What Stage 3 implied | What it actually says (verified by direct fetch) |
|---|---|---|
| [Forum thread, "How to create a Task with runtime parameters"](https://community.studio3t.com/t/how-to-create-a-task-with-runtime-parameteres/784) | External/CLI parameterization demand | Posted 2023-12-05. About **date-based filtering** for a daily export (yesterday's documents). Resolved via Studio 3T's built-in **Date Tags** feature. Does not mention CLI, API, or external triggering at all. |
| [UserVoice item, "Task Scheduler in UI to run queries..."](https://3t-io.uservoice.com/forums/265122-share-your-ideas-with-us/suggestions/33329998-task-scheduler-in-ui-to-run-queries-and-extract-re) | External/CLI triggering demand | Posted 2018-02-15. About wanting **in-app** scheduled query execution with CSV/XLSX export for BI-tool ETL. Marked **completed** — Studio 3T's own Task Scheduler (shipped 2019) was the direct response. Not about external/CLI invocation. |

**Correction applied:** Candidate 4's Evidence Strength reverts from Stage 3's revised **5 back to 4** — there is exactly **one** genuine Tier C source (VoC pilot record #2), not three. This is exactly the kind of overstatement this stage exists to catch, and it's disclosed here rather than quietly fixed.

## Finding: DBeaver's CLI capability is confirmed via primary source (holds up)

Directly fetched [DBeaver's Command Line wiki page](https://github.com/dbeaver/dbeaver/wiki/Command-Line) rather than relying on the search summary. Confirmed exact syntax: `-runTask @projectName:taskName`, with `-var variableName=variableValue` for per-invocation overrides (example given in DBeaver's own docs: `-runTask exportFromSakila -var film=sakila.film -var actor=sakila.actor`), plus a `-vars` flag for a properties file. **This feature is gated to DBeaver's PRO edition** — a detail worth carrying into the memo: Studio 3T isn't giving up a free-tier advantage by not having this; it's a paid-tier-vs-paid-tier competitive gap specifically.
**Label: confirmed** (primary source, DBeaver's own GitHub wiki).

## Finding: Candidate 19's specific technical detail is unverified at the primary source

Stage 3 described the existing `scan_pii` implementation (4-tier classification, confidence scores, `isProse` flag, sample redaction) citing a Studio 3T blog post. Attempting to fetch that post directly for this verification pass returned **HTTP 403 Forbidden** — it could not be independently confirmed. The description stands only on the earlier web search's summary of the page, which is a weaker evidentiary basis than a direct read.
**Correction applied:** Candidate 19's Evidence Strength reverts from Stage 3's revised **5 back to 4**. The *existence* of a PII scanner in 3T MCP (`AI-011`) remains solidly confirmed — that claim comes from this repo's own `gap-analysis-not-on-3t-desktop.md` (Tier A, independently built and cross-checked in an earlier research pass), not from the blocked blog post. Only the *specific implementation detail* (four named tiers, etc.) is downgraded to unverified.
**Label:** PII scanner existence in 3T MCP — **confirmed** (Tier A, repo-internal). Specific classification mechanics — **unverified** (blocked primary source).

## Disconfirming-evidence search, per candidate

- **Candidate 4:** the sole supporting Tier C record is from **2022-05-04** — over four years old. No 2026 Studio 3T changelog entry found addressing it (checked in Stage 1e). The record itself notes a **partial workaround already exists** for a related scenario (aggregations extracted into Node.js scripts), which somewhat tempers the severity — the pain is specific to *export tasks*, not automation in general. **Recommendation for the memo: flag evidence age explicitly, don't treat a single 4-year-old thread as proof current demand is unchanged.**
- **Candidate 18:** no direct customer evidence (VoC or community) was found at all for this specific idea in either Stage 1 or Stage 3 — the entire case rests on one Tier B recommendation plus the in-house precedent that 3T Lens already built it. This is a "logical extension, proven pattern" argument, not a "customers are asking" argument. Weaker evidentiary footing than Candidate 4, despite the similar score.
- **Candidate 19:** same shape as Candidate 18 — no Desktop-specific customer demand found. The case is "cheap to build because we built it twice already, and the market context (PII/DSPM tooling) is growing," not "users are asking for this."
- **Candidate 1:** a distinct **product risk**, not just a evidentiary gap: an AI-generated index/query recommendation that is *wrong* could actively degrade production performance (redundant or poorly-chosen indexes carry real write-amplification and storage cost). Any implementation needs a strong "dry-run / preview, no auto-apply" posture — this is a design constraint the memo should state explicitly, not an argument against building it.
- **Candidate 9:** QE/CSFLE has a narrow buyer (compliance-driven segment only) and a security-critical UI is higher-stakes to get right than the others on this shortlist — a misconfigured encryption schema could create a false sense of security, or (with key mismanagement) make data permanently unreadable. This raises the effective bar for "acceptable" delivery quality beyond what the Build Effort score alone captures.

## Severity/Urgency re-derivation from primary text (not my own paraphrase)

- Candidate 4 severity re-checked against the VoC pilot's own severity assignment (3, "forces an external script for a recurring, high-volume use case") — **matches**, no drift.
- Candidate 9's Compass-exclusivity claim re-checked against `reports/cumulative-report.md`'s literal text ("Compass is the only product that provides: Queryable Encryption (QE) and CSFLE in-use encryption configuration") — **matches**, no drift.
- Candidate 1's "3-6 hours/week manual tuning" figure re-checked against `mongodb-developer-workflow-automation`'s framing (query tuning "consuming 3-6 hours/week") — **matches**, no drift.

## Final, corrected scores after verification

| Candidate | Stage 3 score | Stage 4 corrected score | What changed |
|---|---|---|---|
| 4 — Headless CLI/CI-CD automation | 8.00 | **7.50** | Evidence Strength reverted 5→4 (2 of 3 cited community sources didn't hold up); Competitive Urgency 4 confirmed via primary-source DBeaver fetch |
| 18 — Webhook notifications | 7.00 | 7.00 | No change — but evidentiary weakness (zero direct customer signal) now explicitly flagged |
| 19 — PII classification/discovery | 7.00 | **6.50** | Evidence Strength reverted 5→4 (specific implementation detail unverified — primary source blocked) |
| 1 — AI query/index advisor | 5.00 | 5.00 | No change; product-risk (bad recommendations) flagged as a design constraint |
| 9 — QE/CSFLE key-vault UI | 5.00 | 5.00 | No change; delivery-quality bar flagged as higher-stakes than the score alone shows |

Candidate 4 remains the top-scored candidate even after correction, but the corrected picture is more modest and more honestly evidenced than Stage 3's number suggested — one solid but aging customer complaint, plus a now-primary-source-confirmed competitive gap against DBeaver's paid tier specifically.

## Stage 6 — full-review fact-verification addendum

Added after the user reviewed Stage 5's first delivery and required (a) a full review of all ~20 candidates, not just the shortlisted 5, (b) stricter citation discipline — "do not invent — this research is based strictly on data," and (c) expanding the fully-argued ranked list to ~15 candidates. Full requirement text: [research plan, Stage 6](01-research-plan.md#stage-6--full-review-fact-verification--citation-audit-added-2026-07-30-after-stage-5-was-first-delivered).

### The most significant catch: Candidate 1's competitive-urgency claim was wrong

The original Stage 1-4 assessment of the AI query/index performance advisor claimed, based on an external web search for the literal phrase "index advisor"/"query optimizer," that no GUI competitor had shipped an equivalent — read as a first-mover opportunity supporting the "widen the lead" objective.

Re-checking this repo's **own** structured comparison data (`reports/comparisons/low-level-feature-comparison.md`, `IDX-perf-insights` row) — which should have been the first check, before any external search — shows:

- MongoDB Compass: ✅ confirmed, sourced to [Compass's own feature-matrix.md](../../products/third-party/mongodb-compass/features/indexing-performance/feature-matrix.md): *"System suggests modeling/indexing improvements for problematic patterns... Advisory, not auto-remediation."*
- VisuaLeaf: ✅ confirmed, sourced to its own feature-matrix.md: *"4 recommendation types: Missing Index/Compound Index/Covered Query/Unused Index (in profiler)."*

**Root cause of the miss:** the external search used different terminology ("index advisor") than what this repo's own dictionary tracks the capability as (`IDX-perf-insights`), and the check was run against the outside world before it was run against data already sitting in this repository. **Correction applied:** Competitive Urgency revised 2→4, Priority Score revised 5.00→5.67, and the candidate's framing changed from "first-mover, widen the lead" to "confirmed 2-competitor gap-close" — the same category as Candidates 4, 9, and 11. This directly strengthens rather than weakens the case for the final recommendation, since it means Candidate 19 (PII classification) is now the *only* top-5 candidate that survives this same check as genuinely uncontested.

### Two smaller unsourced claims found and fixed

- **Candidate 3 (Git integration):** the claim that "DataGrip inherits full built-in VCS/Git integration via the JetBrains platform" was asserted from general background knowledge in the original pass, with no citation. Verified via direct fetch of JetBrains' own documentation ([Version control integration support](https://www.jetbrains.com/help/datagrip/enabling-version-control.html), [Databases in the Version Control System](https://www.jetbrains.com/help/datagrip/databases-in-the-version-control-system.html)) — the claim holds up and is now properly cited.
- **Candidate 4 (Headless CLI):** the original Competitive Urgency rationale named both "DBeaver Enterprise" and "Navicat" as having partial CLI/scripted-task capability. Only the DBeaver claim was ever verified (via direct fetch of DBeaver's GitHub wiki). Checking `navicat-competitive-intelligence-analysis` directly for this pass found no supporting mention — the Navicat reference was unsourced and has been removed rather than left standing.

### Citation-fix-only corrections (claim was accurate, source attribution was wrong)

- **Candidate 16 (Vector Search tooling):** originally cited "Tier A confirmed via `feature-dictionary.md`'s coverage matrix" — but `feature-dictionary.md` only *defines* the `IDX-vector-search` ID, it doesn't state which product has it. The actual confirming source is `reports/comparisons/low-level-feature-comparison.md`'s per-product status row (Compass ✅) plus `reports/cumulative-report.md`'s explicit "Compass is the only product that provides... Vector Search index creation" finding. Citation corrected; the underlying claim was already correct.
- **Candidate 17 (Enterprise AI gateway):** the DBeaver AI-masking quote was attributed generically to `dbeaver-competitive-intelligence-analysis`; the exact sentence lives in `research/google_research/overview.md`'s condensed summary of that file. Citation narrowed to the specific file where the exact wording is verifiable, and flagged as Tier B-only (not independently cross-checked against Tier A data the way Candidate 1's claim now is).

### What this addendum did *not* change

Every other citation across the 15 fully-argued candidates was re-opened and confirmed to say what was attributed to it — no further corrections were needed for Candidates 4, 18, 19, 9, 3 (beyond the fixes above), 11, 20, 6, 12, 10, 5, 15. The final recommendation (Candidate 19, PII classification/discovery) was not itself the source of any correction in this pass — its citations held up unchanged.

**Note, made visible by hindsight after Stage 8 below:** Candidate 18 was explicitly named above as needing "no further corrections" in the Stage 6 pass. That statement was itself wrong — Stage 6's citation audit re-checked *sources external to this repo* (community forums, competitor docs) for Candidate 18, but never re-checked the one Tier A claim embedded in its card (`SCHED-notifications`/`SCHED-email` "already exist and are confirmed") against this repo's own `feature-matrix.md`. This is disclosed rather than smoothed over: a citation audit that checks external sources but not internal ones has a blind spot, and this is the concrete instance where it mattered.

## Stage 8 — 2026-07-31 dictionary/gap-analysis sync addendum

Added after an unrelated, independently-run full source-code re-audit of Studio 3T Desktop ([research/studio-3t-desktop-review-2026/](../studio-3t-desktop-review-2026/), 2026-07-31) changed `feature-dictionary.md`, `reports/gap-analysis-not-on-3t-desktop.md`, and `reports/cumulative-report.md` — the Tier A sources this whole decision pipeline scores against. This stage is a targeted sync, not a Stage 4 re-run: it checks whether any candidate's factual premises still hold against the corrected Tier A data. Full inventory of what changed upstream: [01-research-plan.md, Stage 8](01-research-plan.md#stage-8--2026-07-31-sync-with-the-desktop-source-code-re-audit).

### The most significant catch: Candidate 18's core premise was never verified, and it's false

Every version of Candidate 18's card, from its first appearance in Stage 1 through the Stage 6/7 full-review passes, described its target state as adding webhooks "alongside Task Scheduler's existing email/in-app notifications" and its Build Effort as "additive to the existing, already-documented notification pipeline (`SCHED-notifications`, `SCHED-email`)." **This was never checked against `products/3t/studio-3t/features/task-scheduler/feature-matrix.md` at any stage** — it was asserted in Stage 1/2 and then carried forward unquestioned through every subsequent review, including the Stage 6 pass whose entire purpose was catching exactly this kind of unverified claim (see the note above).

The 2026-07-31 source-code re-audit checked directly and found: **no SMTP/email-sending code and no in-app notification mechanism exists anywhere in `t3/tasks`, `t3/tasks/gui`, or `t3/taskmanager`.** `SCHED-notifications` and `SCHED-email` are both confirmed absent. A scheduled task's outcome is only visible to a user actively looking at the Task Scheduler UI when it runs.

**Correction applied:** Build Effort revised 2→3 (build-the-substrate-plus-one-channel, not add-a-channel-to-existing-substrate — though 3T Lens's `GOV-003` still provides a proven design to port, keeping this from reaching 4). Severity's rationale corrected (the true baseline — zero notifications of any kind — is worse than "email/in-app only," though this doesn't cross the rubric's Severity-4 threshold). **Priority Score revised 7.00 → 4.67** — the largest single correction in this entire research effort, larger than Candidate 1's Stage 6 correction (5.00→5.67) or Candidate 4's Stage 4 correction (8.00→7.50).

**Root cause of the miss:** unlike Candidate 1's Stage 6 correction (an external search was run before an internal one), this was not a sequencing error — no internal check was ever attempted, at any stage, for this specific claim. The candidate's Tier A citation (`gap-analysis-not-on-3t-desktop.md`'s `GOV-003` "present-elsewhere" entry) is real and correct; the *unrelated*, uncited claim about Desktop's own existing notification pipeline was simply never sourced at all. This is a distinct failure mode from every other correction in this file — not a citation that said something different than claimed, but a claim with no citation behind it that nobody flagged as needing one, because it read as background context rather than a load-bearing fact.

### Full re-check of the other 4 shortlisted candidates against the Stage 8 upstream changes

- **Candidate 4 (CLI/CI-CD automation):** does not cite any F-SCHED notification/history/retry ID; its premise (Task Scheduler, masking, Data Compare are "already built and shipping") is unaffected by the audit. No correction needed.
- **Candidate 19 (PII classification):** cites `GOV-004`/`AI-011`/`GOV-011`, none of which the 2026-07-31 audit touched (those are 3T Lens/3T MCP/3TL Bridge capabilities, outside the Desktop-only source-code audit's scope). No correction needed.
- **Candidate 1 (AI query/index advisor):** cites `IDX-perf-insights`, confirmed still absent on Desktop by the 2026-07-31 audit (unchanged status). No correction needed beyond the existing Stage 6 fix.
- **Candidate 9 (QE/CSFLE key-vault UI):** cites `CONN-in-use-enc`, confirmed still unverified/absent by the 2026-07-31 audit (unchanged status). No correction needed.
- **Candidate 11 (Schema ERD cluster, carried to Stage 5 despite being cut):** the audit directly resolved 4 of its 13 dictionary-linked IDs to confirmed-present (validator authoring/deployment). **Correction applied:** dictionary linkage narrowed to 9 IDs; Priority Score arithmetic unchanged (4.00) since Build Effort stays Large even at the narrower scope — see its card in [04-scored-longlist.md](04-scored-longlist.md#candidate-11-visual-erdjson-schema-editorvalidation-rule-authoring-ui-the-f-schema-cluster--prop-schema-erd-cluster--️-scope-narrowed-in-stage-8) for the full correction.

### Final, corrected scores after Stage 8

| Candidate | Stage 4/6 score | Stage 8 corrected score | What changed |
|---|---|---|---|
| 4 — Headless CLI/CI-CD automation | 7.50 | 7.50 | No change |
| 19 — PII classification/discovery | 6.50 | 6.50 | No change |
| 1 — AI query/index advisor | 5.67 | 5.67 | No change |
| 9 — QE/CSFLE key-vault UI | 5.00 | 5.00 | No change |
| 18 — Webhook notifications | 7.00 | **4.67** | Build Effort corrected 2→3 after its "notifications already exist" premise was found unverified and false |
| 11 — Schema ERD cluster (carried, not shortlisted) | 4.00 | 4.00 | Dictionary linkage narrowed 13→9 IDs; score arithmetic unchanged |

**Net effect on the shortlist:** four of the five originally-shortlisted candidates are unaffected. The fifth, Candidate 18, drops from a tied-for-second 7.00 to 4.67 — below every remaining shortlisted candidate and roughly tied with Candidate 16 (Deeper Vector Search tooling), which was cut at Stage 2. This does not change which candidate is recommended (Candidate 19, unaffected by any Stage 8 finding) but it does mean the shortlist's internal ordering, as presented anywhere downstream (the Stage 5 memo, the dictionary's Proposed Feature Registry), needs to reflect 4.67, not 7.00, for Candidate 18.
