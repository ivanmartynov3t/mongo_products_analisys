# Stage 4 — Adversarial Self-Verification (+ Stage 6 full-review addendum)

## Navigation

- [← Shortlist deep-dive](05-shortlist-deepdive.md)
- [Final memo →](../../reports/next-feature-recommendation.md)
- [Stage 6 addendum ↓](#stage-6-full-review-fact-verification-addendum)

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
