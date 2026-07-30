# Next Feature Recommendation for Studio 3T Desktop

This memo answers a specific question: which new capability should Studio 3T Desktop build next? It is the final deliverable of a six-stage research effort; every intermediate step is preserved as its own file under `research/feature-decision-2026/` for full traceability. Stage 6 was a full review pass added after Stage 5 was first delivered — every claim in every stage was re-audited for a real citation, and the ranked, fully-argued list was expanded from 5 to 15 candidates. Corrections found during that pass are disclosed inline below, not silently smoothed over.

## Navigation

- [Repository README](../README.md)
- [Feature dictionary](../feature-dictionary.md)
- [Discussion record: dialog & inputs](../research/feature-decision-2026/00-dialog-and-inputs.md)
- [Research plan](../research/feature-decision-2026/01-research-plan.md)
- [Stage 0: data inventory](../research/feature-decision-2026/02-data-inventory.md)
- [Stage 1: candidate long-list](../research/feature-decision-2026/03-candidate-longlist.md)
- [Stage 2: scored long-list](../research/feature-decision-2026/04-scored-longlist.md)
- [Stage 3: shortlist deep-dive](../research/feature-decision-2026/05-shortlist-deepdive.md)
- [Stage 4/6: verification notes](../research/feature-decision-2026/06-verification-notes.md)
- [Google research overview](../research/google_research/overview.md)

## Executive summary

**Recommendation: build Automated PII Classification/Discovery for Studio 3T Desktop** — automated scanning of collections that flags fields likely to contain personal/sensitive data (by name and value pattern), so users can see what needs protecting before configuring the existing data-masking tool, instead of manually auditing schemas field-by-field.

This is not the single highest-scoring candidate produced by this research (see below), but it is the highest-scoring candidate that **cleanly satisfies the stated objective** — widen Studio 3T's existing lead, not just close a competitor's gap. That distinction got sharper, not weaker, during the Stage 6 review: re-checking this repo's own structured comparison data (not just external research) found that the #4-ranked candidate (an AI query/index advisor) is *also* a documented 2-competitor gap, not the first-mover play it was originally scored as. After that correction, **every other top-5 candidate turns out to be closing some specific competitor's gap** (DBeaver, Compass, Compass+VisuaLeaf, or the whole 3T portfolio's own F-SCHEMA hole) — PII classification/discovery is the one candidate in the entire top ranks that is genuinely first-to-market among the products this repo tracks. Full reasoning: [Why this, and not the higher-scored alternatives](#final-recommendation-automated-pii-classificationdiscovery).

## Methodology & source reliability

Full detail: [research plan](../research/feature-decision-2026/01-research-plan.md), [data inventory](../research/feature-decision-2026/02-data-inventory.md).

- **Candidate universe:** capabilities Studio 3T Desktop does not have yet — both gaps already tracked in `feature-dictionary.md` and net-new ideas surfaced by research.
- **Sources:** this repo's structured analysis (Tier A: `feature-dictionary.md`, gap-analysis reports, product reports, and — critically — `reports/comparisons/low-level-feature-comparison.md`'s per-competitor status columns), 21 independently-verified, well-cited competitive/market research files (Tier B: `research/google_research/`), a 7-record customer-voice pilot (Tier C), and fresh compliant web research run specifically for this decision (Tier D — vendor docs, changelogs, GitHub wikis, official forums; no direct scraping of G2/Capterra/Reddit).
- **Scoring:** every candidate scored 1-5 on Evidence Strength, Reach, Severity, Competitive Urgency, and Build Effort, rolled into a composite Priority Score = (Evidence + Reach + Severity + Urgency) / Effort. Full rubric definitions in the research plan.
- **Funnel:** 20 headline candidates (plus 78+ smaller dictionary-tracked items triaged as a group) → scored and ranked → top 5 deep-dived with fresh, targeted research → adversarially re-verified → **Stage 6: every citation across all ~20 candidates re-checked, not just the top 5; 15 candidates given full narrative treatment** (up from 5). Multiple corrections were caught and disclosed rather than hidden — see below.
- **Citation discipline (added as an explicit requirement in Stage 6):** every factual claim cites a specific source — a repo file (with the exact row/quote where useful), a `google_research` file (with a direct quote), a VoC record number, or a specific fresh search/fetch performed in this research with its URL. Scoring judgments (the 1-5 numbers themselves) are analytical, not citations, and are labeled as such. Nothing is asserted from general background knowledge without either sourcing it properly or flagging it explicitly as an unverified assumption.

## Known limitations

- **No internal/proprietary data.** No CRM/win-loss, support tickets, in-app telemetry, or NPS/CSAT data exists in this environment. Every "Reach" and "Severity" score is inferred from public research and a 7-record forum pilot, not measured usage or revenue impact. This is the single biggest thing that would change this analysis if it became available.
- **The VoC pilot is tiny and skews toward defects, not gaps.** Of its 7 real, cited records, only 1 represented a missing *capability*; the other 6 were bugs or discoverability problems in existing features. That 6-of-7 finding is itself worth attention independent of this decision (see [candidate long-list](../research/feature-decision-2026/03-candidate-longlist.md#1d-voc-pilot-record-tagging)), but it also means this decision leans more heavily on secondary research (Tier B/D) than direct customer voice (Tier C) than would be ideal.
- **`google_research/` is well-cited secondary research, not primary data.** Verified during this effort that all 21 files carry real, resolvable citations (20-65 URLs each) — it reflects public competitor documentation and community sentiment, not Studio 3T's own usage data.
- **Corrections found and disclosed during the Stage 6 full review** (all detailed in [06-verification-notes.md](../research/feature-decision-2026/06-verification-notes.md) and the affected cards in [04-scored-longlist.md](../research/feature-decision-2026/04-scored-longlist.md)):
  - Two community links credited as corroborating evidence for the #1-ranked candidate, based on their search-result titles, turned out on direct fetch to be about unrelated topics — score corrected down (this was the original Stage 4 catch, carried forward).
  - **The #4-ranked candidate (AI query/index advisor) was originally scored as if no competitor had it**, based on an external web search using the phrase "index advisor." Re-checking this repo's own `reports/comparisons/low-level-feature-comparison.md` — which should have been checked first — shows MongoDB Compass and VisuaLeaf are both Tier-A-confirmed to already have this (`IDX-perf-insights`). Its Competitive Urgency score was corrected from 2 to 4 and its Priority Score from 5.00 to 5.67; the whole "first-mover" framing for it was retracted.
  - A competitive claim about DataGrip's Git/VCS integration, and a claim that Navicat has partial CLI/task-triggering capability, were both originally asserted from unstated background knowledge rather than a checked source. The DataGrip claim was re-verified and is now backed by a direct citation to JetBrains' own documentation; the Navicat claim was checked against its source file, found unsupported, and removed.
- **A primary source could not be reached.** A Studio 3T blog post describing PII-scanner implementation detail returned HTTP 403 on direct fetch; that specific detail is marked unverified rather than asserted as fact, even though the broader claim (a PII scanner exists in 3T MCP) is independently confirmed by this repo's own structured data.

## Ranked candidates (15 of 20, full rationale)

Full 5-axis scoring and citations for every candidate, including the 5 not expanded here: [Stage 2](../research/feature-decision-2026/04-scored-longlist.md).

| Rank | Candidate | Score | Why it ranks here, in one line |
|---|---|---|---|
| 1 | Headless CLI / CI-CD pipeline automation | 7.50 | Vendor-confirmed customer gap (VoC #2) + DBeaver Enterprise already ships the exact equivalent (verified via primary source) — but it's a **gap-close vs. DBeaver**, not a lead-widener |
| 2 | Slack/Teams/Jira/PagerDuty webhook notifications | 7.00 | Proven pattern (3T Lens already has it) and cheap to build, but **zero direct customer evidence** was found for Desktop specifically |
| 3 | **Automated PII classification/discovery** | 6.50 | **Recommended.** The one candidate in the top ranks with no confirmed competitor equivalent — genuinely widens the existing masking/governance lead, and the detection logic is already proven twice in-house |
| 4 | AI-driven query/index performance advisor | 5.67 *(corrected from 5.00)* | Highest Reach of any candidate and real quantified pain (3-6 hrs/week), but Stage 6 found Compass **and** VisuaLeaf already have this — a 2-competitor gap-close, not first-mover |
| 5 | Queryable Encryption (QE)/CSFLE key-vault UI | 5.00 | Confirmed Compass-exclusive gap with real compliance severity, but narrow buyer (enterprise-only) and a high-stakes UI to get right |
| 6 | Deeper Vector Search tooling | 4.67 | Compass-exclusive gap (Tier A confirmed) riding a genuine accelerating trend — strongest "just missed the cut" candidate |
| 7 | Native Git/version-control integration | 4.33 | Real workflow gap vs. DataGrip's platform-inherited VCS integration (now properly sourced), but Studio 3T already shipped partial prior art (2026.4 Git-backed connection folders) whose actual scope is unverified |
| 8 | Visual ERD/JSON-Schema editor (F-SCHEMA cluster) | 4.00 | The single most rigorously-confirmed gap in this whole repo (portfolio-wide, two competitors), but a full build exceeds the effort ceiling and it's fundamentally a gap-close — flagged for a **separate future decision**, not lost |
| 8 | Enterprise AI gateway/SSO for AI Helper | 4.00 | Studio 3T's own product report names this as a self-assessed weakness; DBeaver reportedly shares the same weakness rather than having solved it |
| 10 | Schema drift detection / versioned field history | 3.67 | Proven once already in 3T Lens, no external corroboration of Desktop-specific demand |
| 11 | Centralized SIEM/audit-log export | 3.33 | Real compliance gap, but enterprise-only reach fails the "also serve startups" requirement |
| 11 | AI schema anti-pattern/health advisor | 3.33 | Real production risk (16MB limit, cache thrashing) but single-sourced; genuine bundling synergy with #4 for a future combined advisor |
| 13 | Native BI/dashboard builder | 3.00 | 2 competitors (1 confirmed) have it, but matching "10+ visualization types" is a substantial build, and Studio 3T's existing Excel/CSV export already softens the pain |
| 14 | Secrets vault integration | 2.75 | Real enterprise security gap, but the 2026 market bar is dynamic/rotating credentials specifically — a bigger build than it first looks |
| 15 | VS Code/JetBrains companion extension | 2.50 | Real context-switching friction, but two separate plugin platforms to build and maintain, and MongoDB's own official extension likely already occupies part of this niche |

**5 further candidates** (IntelliShell debugger, synthetic test-data generator, federated cross-database querying, JIT access/dynamic masking, Desktop app-level SSO) scored 1.40-2.33 and remain in [Stage 2](../research/feature-decision-2026/04-scored-longlist.md) with brief sourced cut-reasons rather than full expansion — each rests on a single source and was cut on effort or reach grounds before it seemed worth the deeper research investment.

## Shortlist deep-dive outcomes (candidates 1-5 above)

Full cards, sources, and rationale for every axis: [Stage 3](../research/feature-decision-2026/05-shortlist-deepdive.md) and [Stage 4/6](../research/feature-decision-2026/06-verification-notes.md).

### 1. Headless CLI / CI-CD pipeline automation (7.50)
Lets external systems (GitHub Actions, GitLab CI, Jenkins) trigger existing Task Scheduler jobs, masking runs, and Data Compare with runtime parameters. **Confirmed via direct primary-source fetch**: DBeaver's Pro/Ultimate editions already ship this exact capability (`-runTask @project:task -var name=value`, per DBeaver's own GitHub wiki). Real, vendor-confirmed customer pain exists (VoC pilot record #2, a user asking for exactly this, 3T staff confirming "no way to run them from outside applications") — but that record is from **2022-05-04**, over four years old, and two other community links initially thought to corroborate it turned out, on direct verification, not to be related (disclosed in Stage 4). Very low build effort — this is an API/CLI wrapper around logic that already works. **This is fundamentally closing a documented DBeaver capability gap, not widening a lead.**

### 2. Slack/Teams/Jira/PagerDuty webhook notifications (7.00)
Extends the existing Task Scheduler's email/in-app notifications to webhooks. Proven pattern — 3T Lens already has this (`GOV-003`, confirmed via this repo's own gap-analysis) — and cheap to build (additive to existing notification infrastructure). But **zero direct customer evidence was found** for this specific idea, in either the VoC pilot or a targeted community search; the case rests entirely on "we already built this pattern elsewhere" plus one research recommendation (`studio-3t-missing-integrations`), not expressed user demand.

### 3. Automated PII classification/discovery (6.50) — recommended
See full case below.

### 4. AI-driven query/index performance advisor (5.67, corrected)
A background advisor that reads existing Explain Plan/Profiler data and recommends index changes. The original assessment claimed no GUI competitor had shipped an equivalent — **this was wrong.** Stage 6 checked this repo's own `reports/comparisons/low-level-feature-comparison.md` directly and found MongoDB Compass's own feature matrix confirms "System suggests modeling/indexing improvements for problematic patterns" (Advisory, not auto-remediation), and VisuaLeaf's confirms "4 recommendation types: Missing Index/Compound Index/Covered Query/Unused Index." This candidate still has the highest Reach of any candidate and real, quantified pain (`mongodb-developer-workflow-automation`: 3-6 hrs/week manual tuning per developer) — it's a strong candidate on its own terms, just not evidence for "widen the lead." Any build needs a strict "recommend, never auto-apply" posture, since a wrong index recommendation can actively harm production performance.

### 5. Queryable Encryption (QE)/CSFLE key-vault configuration UI (5.00)
Confirmed, Compass-exclusive gap (this repo's own `cumulative-report.md`: "Compass is the only product that provides... Queryable Encryption (QE) and CSFLE in-use encryption configuration"; independently re-confirmed via a fresh 2026 search finding no evidence Studio 3T has any equivalent). Real compliance-driven severity for regulated industries. Narrow buyer (enterprise/regulated almost exclusively — weaker fit for the "also serve scaled startups" requirement than the others), and a higher-stakes UI to get right (a misconfigured encryption schema has real security consequences), which raises its effective delivery bar above what the raw effort score captures.

## Final recommendation: Automated PII Classification/Discovery

### The case

Add automated scanning to Studio 3T Desktop that samples a collection, classifies fields by name and value pattern, and flags which are likely to contain personal or sensitive data — before the user ever opens the existing data-masking tool. Today, a user must already know which fields are sensitive to mask them; this closes that sequencing gap.

- **Widens an existing lead, doesn't just close a gap — and this held up under scrutiny.** Studio 3T's own product report names built-in data masking as a strategic strength ("data masking is built in at the import, export, and standalone tool layers — not a bolt-on"). This repo's own structured comparison data (`reports/comparisons/low-level-feature-comparison.md`, `AI-010`/`GOV-004` rows) confirms MongoDB Compass is explicitly marked **absent** for an equivalent PII-scanning capability, and VisuaLeaf is unconfirmed either way — unlike the #1 and #4 candidates, this claim survived the Stage 6 re-check against our own data, not just an external search. The broader 2026 PII/DSPM discovery market is real and growing (BigID, Strac, Varonis, per Stage 3's fresh search), but it's dominated by standalone platforms, not built into database GUI clients.
- **Proven, low-risk, low-effort:** the core detection logic isn't hypothetical — it already exists and works in production twice elsewhere in the 3T family (3T MCP's PII scanner, `AI-011`; 3T Lens's PII classification, `GOV-004`, both confirmed via this repo's own gap-analysis). This is substantially a port/integrate job onto Desktop's existing schema-sampling infrastructure (`SCHEMA-sampling`, `SCHEMA-field-prob`), not new invention — the highest-confidence Build Effort estimate (2/5) of any candidate considered.
- **Serves both required segments:** enterprise/regulated teams get a real compliance/audit workflow improvement; GDPR/CCPA-conscious scaled startups get the same benefit without needing a dedicated DSPM vendor.
- **Fits the 1-2 release cycle ceiling:** no new infrastructure, no new deployable product — a new capability inside the existing Desktop IDE, reusing proven logic and existing sampling infrastructure.

### Segment fit

Primary: enterprise/regulated teams doing compliance-driven data handling (the same audience Studio 3T's masking, RBAC, and enterprise-auth features already target). Secondary: medium-to-large startups operating under GDPR/CCPA who need "know what's sensitive" tooling but can't justify a dedicated DSPM platform contract.

### Effort & feasibility

- Reuses `SCHEMA-sampling`/`SCHEMA-field-prob` for the sampling step (already built and confirmed for Studio 3T).
- Reuses classification logic already proven in `AI-011` (3T MCP) and `GOV-004` (3T Lens) — the hard design work (what counts as PII, confidence scoring, handling free-text fields safely) doesn't need to be redone from scratch. Note: the *specific* implementation detail of the existing scanner (four classification tiers, confidence scoring) could not be independently re-verified in this pass — the Studio 3T blog post describing it returned HTTP 403 on direct fetch. Confirming exact reusability with the team that owns `AI-011`/`GOV-004` should be the first implementation step, not an assumption.
- Feeds directly into the existing data-masking tool, closing a real sequencing gap (discover → then mask) rather than existing as a disconnected feature.

### Suggested dictionary entry

This is a net-new capability for Studio 3T Desktop specifically, though the underlying pattern exists elsewhere in the family. Recommend adding to `feature-dictionary.md` under **F-GOV**, something like `GOV-pii-discovery` — "Automated PII/sensitive-field discovery: samples a collection and classifies fields by name/value pattern to flag likely-sensitive data" — following the repo's existing rule that a new sub-feature must be added to the dictionary before (or alongside) being tracked in a product's feature matrix.

### Risks / open questions

- Exact reusability of the `AI-011`/`GOV-004` classification logic for a different product surface is unverified in this research pass (the source describing its internals returned HTTP 403) — first implementation step should be a direct conversation with those feature owners, not an assumption that porting is trivial.
- No direct Studio 3T Desktop customer has been observed asking for this specifically — the case rests on proven internal precedent plus market context, not expressed demand. Worth a lightweight validation step (e.g., a quick community/forum post floating the idea) before committing full engineering time.
- False positives/negatives in classification carry reputational risk for a security-adjacent feature — recommend shipping with the existing scanner's confidence-scoring/hedging behavior (flagging uncertain fields as "review needed" rather than asserting a false-confident PII/not-PII verdict) rather than a simplified reimplementation.

### Why not the higher-scored alternatives

**Headless CLI/CI-CD pipeline automation** (rank 1, 7.50) is the strongest candidate on raw evidence — a vendor-confirmed customer gap plus a directly-verified DBeaver Enterprise equivalent, at very low build cost. It did not win this recommendation because, after verification, it is unambiguously a **gap-close against a specific competitor**, not the lead-widening move the user asked this research to find. It's worth a **separate, fast-follow decision** given how cheap and well-evidenced it is — just not the answer to *this* question.

**AI-driven query/index performance advisor** (rank 4, 5.67) looked like a strong "widen the lead" candidate through Stage 4, until the Stage 6 re-check of this repo's own comparison data showed Compass and VisuaLeaf both already have it. Real value, real reach — but also a gap-close, once the facts were checked properly.

**Queryable Encryption UI** (rank 5, 5.00) and **the F-SCHEMA/visual-ERD cluster** (rank 8, 4.00) are both confirmed, real gaps versus specific competitors (Compass; Compass+VisuaLeaf respectively) — legitimate future work, especially F-SCHEMA given how rigorously it's confirmed in this repo's own gap-analysis reports, but neither is a "widen the lead" story either.

That leaves PII classification/discovery as the only top-8 candidate that is genuinely uncontested by any competitor this repo tracks, while also being cheap, low-risk, and a direct extension of a capability area Studio 3T already leads in.

## Appendix: file map

| File | Contents |
|---|---|
| [00-dialog-and-inputs.md](../research/feature-decision-2026/00-dialog-and-inputs.md) | Full discussion record — original ask, all clarifying questions and answers |
| [01-research-plan.md](../research/feature-decision-2026/01-research-plan.md) | Stage-by-stage plan, rubric definitions, card template, Stage 6 requirements addendum |
| [02-data-inventory.md](../research/feature-decision-2026/02-data-inventory.md) | Source reliability tiers (A-E) |
| [03-candidate-longlist.md](../research/feature-decision-2026/03-candidate-longlist.md) | 20 headline candidates + triaged atomic gaps, VoC tagging, fresh-search drift findings |
| [04-scored-longlist.md](../research/feature-decision-2026/04-scored-longlist.md) | Full 5-axis scoring and narrative rationale for 15 of 20 candidates, corrections from Stage 6 |
| [05-shortlist-deepdive.md](../research/feature-decision-2026/05-shortlist-deepdive.md) | Fresh targeted research on the top 5, with score revisions |
| [06-verification-notes.md](../research/feature-decision-2026/06-verification-notes.md) | Adversarial re-verification, citation-drift catches and corrections, final scores |
