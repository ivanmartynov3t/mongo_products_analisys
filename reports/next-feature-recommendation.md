# Next Feature Recommendation for Studio 3T Desktop

This memo answers a specific question: which new capability should Studio 3T Desktop build next? It is the final deliverable of a seven-stage research effort; every intermediate step is preserved as its own file under `research/feature-decision-2026/` for full traceability. Every candidate discussed here is also registered in [`feature-dictionary.md`'s Proposed Feature Registry](../feature-dictionary.md#proposed-feature-registry-research-pipeline) under a permanent `PROP-<slug>` ID with a formal classification — that registry is the single source of truth for the taxonomy used throughout this memo.

## Navigation

- [Repository README](../README.md)
- [Feature dictionary — Proposed Feature Registry](../feature-dictionary.md#proposed-feature-registry-research-pipeline)
- [Discussion record: dialog & inputs](../research/feature-decision-2026/00-dialog-and-inputs.md)
- [Research plan](../research/feature-decision-2026/01-research-plan.md)
- [Stage 0: data inventory](../research/feature-decision-2026/02-data-inventory.md)
- [Stage 1: candidate long-list](../research/feature-decision-2026/03-candidate-longlist.md)
- [Stage 2/6/7: scored long-list](../research/feature-decision-2026/04-scored-longlist.md)
- [Stage 3: shortlist deep-dive](../research/feature-decision-2026/05-shortlist-deepdive.md)
- [Stage 4/6: verification notes](../research/feature-decision-2026/06-verification-notes.md)
- [Google research overview](../research/google_research/overview.md)

## How to read this memo

Three things changed in this revision (Stage 7), in response to specific feedback that the prior version's argumentation and citations were thin and its metrics opaque:

1. **Every candidate now carries a formal classification** — 🌱 **Lead-Widener** / ⚔️ **Gap-Close** / ❔ **Parity-Unverified** (competitive framing), plus 🏠 **Portfolio-Port** / 🆕 **Net-New** (origin), defined once in `feature-dictionary.md` and applied identically here and in every research file. Full legend: [feature-dictionary.md](../feature-dictionary.md#proposed-feature-registry-research-pipeline).
2. **Every metric on the recommended candidate and full shortlist now shows its calculation**, not just the final 1-5 number — which sources were weighed, and why the result is a 4 and not a 3 or 5.
3. **The evidentiary base was deepened by re-reading the full text of `google_research/` files**, not just `overview.md`'s condensed summaries — 6 additional direct quotes across 6 files were found for the recommended candidate alone, none of which had been cited in the prior revision.

## Executive summary

**Recommendation: build Automated PII Classification/Discovery for Studio 3T Desktop** (`PROP-pii-discovery`) — automated scanning of collections that flags fields likely to contain personal/sensitive data (by name and value pattern), so users can see what needs protecting before configuring the existing data-masking tool, instead of manually auditing schemas field-by-field.

**Classification: 🌱 Lead-Widener · 🏠 Portfolio-Port · ✳️ Net-New-Concept · Priority Score 6.50**

This is not the single highest-scoring candidate produced by this research (that is `PROP-cli-automation` at 7.50 — see below). It is the highest-scoring candidate that carries the 🌱 **Lead-Widener** classification cleanly: no product tracked in this repo's own structured comparison data is confirmed to have it. That distinction sharpened, not weakened, across the review stages of this research: re-checking this repo's own structured comparison data (not just external research) found that `PROP-idx-perf-advisor` — originally tagged Lead-Widener — is actually a confirmed 2-competitor ⚔️ Gap-Close once the repo's own `IDX-perf-insights` comparison row was checked. After that correction, **every other candidate in the top 5 carries a ⚔️ Gap-Close or ❔ Parity-Unverified tag** — `PROP-pii-discovery` is the only one that is genuinely uncontested among the products this repo tracks, while also being the cheapest candidate to build (tied for the lowest Build Effort score, 2/5) because its underlying detection logic is already proven **three times** elsewhere inside 3T Software Labs' own product family.

## Methodology & source reliability

Full detail: [research plan](../research/feature-decision-2026/01-research-plan.md), [data inventory](../research/feature-decision-2026/02-data-inventory.md).

- **Candidate universe:** capabilities Studio 3T Desktop does not have yet — both gaps already tracked in `feature-dictionary.md` and net-new ideas surfaced by research.
- **Sources:** this repo's structured analysis (Tier A: `feature-dictionary.md`, gap-analysis reports, product reports, `reports/comparisons/low-level-feature-comparison.md`'s per-competitor status columns), 21 independently-verified, well-cited competitive/market research files (Tier B: `research/google_research/` — verified during this effort to carry 20-65 real, resolvable citations each), a 7-record customer-voice pilot (Tier C), and fresh compliant web research (Tier D — vendor docs, changelogs, GitHub wikis, official forums; no direct scraping of G2/Capterra/Reddit).
- **Scoring:** every candidate scored 1-5 on Evidence Strength, Reach, Severity, Competitive Urgency, and Build Effort, rolled into a composite **Priority Score = (Evidence Strength + Reach + Severity + Competitive Urgency) / Build Effort**. Range: ~0.8 (all 1s over effort 5) to 20 (all 5s over effort 1) — higher means higher priority (high value, low cost). Full rubric with the exact 1-5 definition for every axis: [research plan](../research/feature-decision-2026/01-research-plan.md).
- **Classification (new in Stage 7):** every candidate additionally carries a **Competitive Framing** tag (🌱 Lead-Widener / ⚔️ Gap-Close / ❔ Parity-Unverified) and an **Origin** tag (🏠 Portfolio-Port / 🆕 Net-New), defined in `feature-dictionary.md`'s Proposed Feature Registry and applied identically in every research file and this memo.
- **Funnel:** 20 headline candidates (plus 78+ smaller dictionary-tracked items triaged as a group) → scored and ranked → top 5 deep-dived with fresh, targeted research → adversarially re-verified (Stage 4) → every citation across all ~20 re-checked, not just the top 5, and 15 candidates given full narrative treatment (Stage 6) → classification taxonomy formalized and the full text of `google_research/` re-mined for additional facts on the top candidates (Stage 7, this revision).

## Known limitations

- **No internal/proprietary data.** No CRM/win-loss, support tickets, in-app telemetry, or NPS/CSAT data exists in this environment. Every "Reach" and "Severity" score is inferred from public research and a 7-record forum pilot, not measured usage or revenue impact.
- **The VoC pilot is tiny and skews toward defects, not gaps.** Of its 7 real, cited records, only 1 (`#2`) represented a missing *capability*; the other 6 were bugs or discoverability problems in existing features. See [candidate long-list](../research/feature-decision-2026/03-candidate-longlist.md#1d-voc-pilot-record-tagging).
- **`google_research/` is well-cited secondary research, not primary data.** All 21 files carry real, resolvable citations (20-65 URLs each) — it reflects public competitor documentation, review-mining, and persona research, not Studio 3T's own usage telemetry. Where a `google_research` file itself aggregates "users frequently request X" from G2/Capterra/Reddit (as `studio-3t-review-mining` does), that is still one step removed from a directly-attributable individual complaint — treated in this memo as stronger than a single competitor-description sentence, but weaker than a VoC pilot record.
- **Corrections found and disclosed across the review stages** (all detailed in [06-verification-notes.md](../research/feature-decision-2026/06-verification-notes.md) and [04-scored-longlist.md](../research/feature-decision-2026/04-scored-longlist.md)):
  - Two community links credited as corroborating evidence for `PROP-cli-automation`, based on their search-result titles, turned out on direct fetch to be about unrelated topics.
  - `PROP-idx-perf-advisor` was originally classified 🌱 Lead-Widener based on an external web search using the phrase "index advisor." Re-checking this repo's own `reports/comparisons/low-level-feature-comparison.md` — which should have been checked first — shows MongoDB Compass and VisuaLeaf are both Tier-A-confirmed to already have this (`IDX-perf-insights`); reclassified ⚔️ Gap-Close, Competitive Urgency corrected 2→4, Priority Score 5.00→5.67.
  - A DataGrip/VCS-integration claim and a Navicat CLI-capability claim were both originally asserted from unstated background knowledge. The DataGrip claim is now backed by a direct citation to JetBrains' own documentation; the Navicat claim was checked, found unsupported, and removed.
- **A primary source could not be reached.** A Studio 3T blog post describing PII-scanner implementation detail (four classification tiers, confidence scoring) returned HTTP 403 on direct fetch; that specific detail is marked unverified, though the broader claim (a PII scanner exists in 3T MCP) is independently confirmed by this repo's own structured data (`AI-011`).

## Ranked candidates (15 of 20, full rationale, with classification)

Full 5-axis scoring, classification, and citations for every candidate, including the 5 not expanded here: [Stage 2/6/7 scoring file](../research/feature-decision-2026/04-scored-longlist.md).

| Rank | Candidate (`PROP-` ID) | Classification | Score | Why it ranks here |
|---|---|---|---|---|
| 1 | Headless CLI/CI-CD automation (`cli-automation`) | ⚔️ Gap-Close · 🆕 | 7.50 | Vendor-confirmed customer gap (VoC #2) + a second, independent review-mining finding ("users express a strong need for a headless server daemon") + DBeaver Enterprise ships the exact equivalent (verified via primary source). Deferred as a fast-follow, not this decision's answer. |
| 2 | Webhook notifications (`webhook-notify`) | ❔ Parity-Unverified · 🏠 | 7.00 | Proven pattern (3T Lens's `GOV-003`) and cheap to build, but a full re-scan of all 21 `google_research` files found **zero** additional corroboration beyond the one original recommendation — the thinnest evidence base of the top 5 despite the high score. |
| 3 | **PII classification/discovery (`pii-discovery`)** | 🌱 **Lead-Widener** · 🏠 | 6.50 | **Recommended.** The only top-5 candidate with no confirmed competitor equivalent. Now backed by 6 independent `google_research` files (2 with direct recommendation language) plus 3 in-house precedents. |
| 4 | AI query/index performance advisor (`idx-perf-advisor`) | ⚔️ Gap-Close *(corrected)* · 🆕 | 5.67 | Highest Reach of any candidate, a direct "users frequently request" quote (`studio-3t-review-mining`) — but Compass **and** VisuaLeaf both confirmed to already have it once this repo's own data was checked. |
| 5 | QE/CSFLE key-vault UI (`qe-key-vault-ui`) | ⚔️ Gap-Close · 🆕 | 5.00 | Confirmed Compass-exclusive gap, and Stage 7 re-mining found NoSQLBooster is independently moving the same direction (CSFLE) — a strengthening, not weakening, competitive-urgency picture. Narrow buyer, high-stakes UI to get right. |
| 6 | Deeper Vector Search tooling (`vector-search-tooling`) | ⚔️ Gap-Close · 🆕 | 4.67 | Compass-exclusive, riding a genuine accelerating trend — strongest "just missed the cut" candidate. |
| 7 | Native Git/VCS integration (`git-integration`) | ⚔️ Gap-Close · 🆕 | 4.33 | Real gap vs. DataGrip's JetBrains-platform-inherited VCS (now primary-source-cited), but Studio 3T already shipped partial prior art (2026.4 Git-backed connection folders) of unverified scope. |
| 8 | Visual ERD/JSON-Schema cluster (`schema-erd-cluster`) | ⚔️ Gap-Close · 🆕 | 4.00 | The single most rigorously-confirmed gap in this repo (portfolio-wide, two competitors) — deferred as a **separate future decision**, not lost, because a full build exceeds this decision's effort ceiling. |
| 8 | Enterprise AI gateway/SSO (`ai-gateway-sso`) | 🌱 Lead-Widener · 🆕 | 4.00 | Studio 3T's own product report names this a self-assessed weakness; DBeaver reportedly shares it rather than having solved it. |
| 10 | Schema drift detection (`schema-drift`) | ❔ Parity-Unverified · 🏠 | 3.67 | Proven once in 3T Lens (`GOV-005`), no external corroboration of Desktop-specific demand. |
| 11 | SIEM/audit-log export (`siem-export`) | ❔ Parity-Unverified · 🆕 | 3.33 | Real compliance gap, but enterprise-only reach fails the "also serve startups" requirement. |
| 11 | Schema anti-pattern advisor (`schema-health-advisor`) | ❔ Parity-Unverified · 🆕 | 3.33 | Real production risk (16MB limit, cache thrashing per `mongodb-ai-automation-opportunities`) but single-sourced. |
| 13 | Native BI/dashboard builder (`bi-dashboard`) | ⚔️ Gap-Close · 🆕 | 3.00 | 2 competitors have it, but matching "10+ visualization types" is a substantial build; Studio 3T's existing Excel/CSV export already softens the pain. |
| 14 | Secrets vault integration (`secrets-vault`) | ❔ Parity-Unverified · 🆕 | 2.75 | Real enterprise gap, but the 2026 market bar is dynamic/rotating credentials — a bigger build than it first looks. |
| 15 | VS Code/JetBrains extension (`ide-companion`) | ❔ Parity-Unverified · 🆕 | 2.50 | Real friction, but two plugin platforms to build/maintain, and MongoDB's own extension likely occupies part of this niche. |

**5 further candidates** (`intellishell-debugger`, `synthetic-test-data`, `federated-query`, `jit-dynamic-masking`, `desktop-sso`) scored 1.40-2.33; classification and brief sourced cut-reasons for each are in [04-scored-longlist.md](../research/feature-decision-2026/04-scored-longlist.md) and [feature-dictionary.md](../feature-dictionary.md#proposed-feature-registry-research-pipeline).

## Deep-dive: the recommended candidate, with full calculation transparency

### PII Classification/Discovery (`PROP-pii-discovery`) — 🌱 Lead-Widener · 🏠 Portfolio-Port · Priority Score 6.50

**What it is:** automated scanning that samples a collection, classifies fields by name and value pattern, and flags which are likely to contain personal or sensitive data — before the user ever opens the existing data-masking tool. Today, a user must already know which fields are sensitive to mask them; this closes that sequencing gap.

#### Evidence, in full — six independent sources, not the two originally cited

The first version of this research cited only two Tier A precedents (`AI-011`, `GOV-004`) plus generic Tier D market color. Re-reading the **full text** of the `google_research/` files — not just `overview.md`'s condensed one-line summaries — surfaced direct, substantive support in four additional files that had not been cited for this candidate at all:

1. **In-house precedent, now three-for-three, not two-for-two** (Tier A, `gap-analysis-not-on-3t-desktop.md`): `AI-011` (3T MCP's PII scanner), `GOV-004` (3T Lens's PII classification), and — found via this pass's re-reading of `dbeaver-competitive-intelligence-analysis` and `datagrip-competitive-analysis`, both of which describe it — **`GOV-011`, 3TL Bridge's real-time PII masking**, which those two files describe concretely: *"3TL Bridge masks sensitive data fields (such as credit card numbers and personal identification details) at the pipeline layer"* (`dbeaver-competitive-intelligence-analysis`) and *"3TL Bridge applies field-level data masking—including credit card truncation, customer name tokenization, and synthetic value substitution—at the pipeline layer before schema context or query results reach external LLMs"* (`datagrip-competitive-analysis`). Three separate engineering teams inside 3T Software Labs have now independently built PII-adjacent detection/classification logic.
2. **A direct, named recommendation for this exact capability** (Tier B, `datagrip-competitive-analysis`, "Pillar 1" of its recommendations): *"Studio 3T should introduce **automated client-side PII detection** that intercepts natural-language-to-aggregation requests. Masking sensitive fields (such as email hashes, social security numbers, and financial metrics) locally before schema trees are transmitted to external AI endpoints guarantees compliance with strict corporate regulations including GDPR, HIPAA, and SOC2."* This is not adjacent-theme evidence — it names the capability directly.
3. **Persona-level demand, independently in two files**: `mongodb-gui-user-personas-research` states the Enterprise Cross-Functional Teams persona's goal is *"enforcing regulatory compliance (such as GDPR, HIPAA, and SOC2), **preventing sensitive personally identifiable information (PII) from leaking to developer workstations**"* — a goal that logically depends on first knowing which fields contain PII. The companion file `mongodb-gui-user-personas` independently confirms: *"The most valuable features include **automated data masking rules that anonymize personally identifiable information (PII)** before rendering query results."* Both files rank this persona as the **highest willingness-to-pay segment** ($699/seat to $4,500-$9,000/site licenses), directly matching this decision's primary target segment.
4. **Confirmation this is already load-bearing in Studio 3T's actual market positioning, from two more independent files**: `database-gui-churn-analysis` states Studio 3T *"reserves enterprise governance features—such as **automated data masking to sanitize sensitive personally identifiable information (PII) during exports**—for its highest pricing tiers"* — confirming the existing masking feature is already marketed around PII specifically, so automated discovery is a direct extension of existing positioning, not a new direction. `studio-3t-review-mining`, which aggregates G2/Capterra/TrustRadius review data, independently states: *"Studio 3T's inclusion of field-level data masking (3TL Bridge)... positions Studio 3T as a secure data access layer for institutional procurement teams"* — confirming this is a real reason institutional customers buy Studio 3T today, per aggregated review evidence, not just competitor-analysis narrative.
5. **The competitive gap is confirmed, not assumed**: `reports/comparisons/low-level-feature-comparison.md`'s `AI-010` row (the closest tracked analog to a client-side PII scanner) shows MongoDB Compass explicitly marked ❌ (confirmed absent) and VisuaLeaf ❓ (unverified) — checked directly as part of this research's citation discipline, not inferred from silence.
6. **Market context**: the standalone PII/DSPM discovery software category (BigID, Strac, Varonis, IBM Guardium) is real and growing in 2026 per a fresh web search performed for this research, but it is dominated by platforms bolted onto SaaS/cloud/endpoint estates — none of DBeaver, DataGrip, Navicat, or TablePlus were found (via a separate fresh search) to have a native PII scanner built into the GUI client itself.

#### How each metric was calculated

| Metric | Score | Calculation |
|---|---|---|
| Evidence Strength | **4** | 6 independent sources converge (listed above), 2 of which contain direct recommendation language. Not a 5 because none of the 6 is a Tier C (direct Studio 3T Desktop customer) request specifically for this capability — the demand signal is persona-level, positioning-level, and in-house-precedent-level, not "a named user asked for this." |
| Reach | **4** | The persona research explicitly names this the top purchasing criterion for the highest-willingness-to-pay segment (Enterprise Cross-Functional Teams, $699-$9,000+), and the churn/landscape analyses confirm relevance to "compliance officers" broadly. Not 5 because no source claims relevance to *every* persona (a solo hobbyist has no compliance need). |
| Severity | **3** | Workflow-drag language across sources ("preventing... leaking," parallel finding in `mongodb-compass-competitive-analysis` about "writing custom backend transformation scripts to sanitize data prior to export") describes real, recurring friction with an existing workaround (manual field-by-field inspection) — not rubric-level 4 ("forces switching to a secondary tool"), since no source states teams abandon Studio 3T over this specifically. |
| Competitive Urgency | **2** | Checked this repo's own Tier A data first: Compass ❌, VisuaLeaf ❓ on the closest tracked ID (`AI-010`). No confirmed competitor has this — which is exactly why the classification is 🌱 Lead-Widener, and why this score stays low by design, not by omission. |
| Build Effort | **2** | Three, not two, existing in-house implementations (`AI-011`, `GOV-004`, `GOV-011`) means the classification logic has been built and iterated on three separate times already by 3T Software Labs engineering — the lowest-uncertainty Build Effort estimate of any candidate in the full 20-candidate long-list. |
| **Priority Score** | **6.50** | **(4 + 4 + 3 + 2) / 2 = 13 / 2 = 6.50.** Unchanged since Stage 2 — the Stage 7 re-mining deepened the *justification* for Evidence Strength without moving any individual axis score, since none of the new sources crossed a threshold defined in the rubric (e.g., a Tier C record, which would be needed to reach Evidence Strength 5). |

### Segment fit

Primary: enterprise/regulated teams doing compliance-driven data handling — directly evidenced by `mongodb-gui-user-personas-research`'s persona framing (GDPR/HIPAA/SOC2, $699-$9,000+ willingness to pay) and `database-gui-churn-analysis`'s confirmation that Studio 3T already monetizes PII-adjacent masking at its highest tiers. Secondary: medium-to-large startups operating under GDPR/CCPA who need "know what's sensitive" tooling but can't justify a dedicated DSPM platform contract (inferred from the general 2026 PII/DSPM market growth found via fresh search — this specific startup-segment claim is the weakest-evidenced part of the segment-fit argument and should be treated as a reasonable inference, not a sourced fact).

### Effort & feasibility

- Reuses `SCHEMA-sampling`/`SCHEMA-field-prob` for the sampling step (already built and confirmed for Studio 3T Desktop).
- Reuses classification logic now confirmed proven **three times** in-house (`AI-011`, `GOV-004`, `GOV-011`) — the hard design work (what counts as PII, how to handle free-text fields, confidence scoring) doesn't need to be redone from scratch. The *specific* implementation detail of any one of the three (e.g., exact classification tiers) could not be independently re-verified in this pass — a Studio 3T blog post describing `AI-011`'s internals returned HTTP 403 on direct fetch. Confirming exact reusability with the teams that own `AI-011`, `GOV-004`, and `GOV-011` should be the first implementation step, not an assumption.
- Feeds directly into the existing data-masking tool, closing a real sequencing gap (discover → then mask) rather than existing as a disconnected feature — and directly extends what `database-gui-churn-analysis` confirms is already a top-tier revenue driver for Studio 3T today.

### Suggested dictionary entry

Recommend adding `GOV-pii-discovery` to `feature-dictionary.md`'s Sub-feature registry under **F-GOV** — "Automated PII/sensitive-field discovery: samples a collection and classifies fields by name/value pattern to flag likely-sensitive data" — once implementation begins, per the repo's naming rule that a new sub-feature must be added before (or alongside) being tracked in a product's feature matrix. Until then, it remains `PROP-pii-discovery` in the Proposed Feature Registry with status **Recommended**.

### Risks / open questions

- Exact reusability of `AI-011`/`GOV-004`/`GOV-011`'s classification logic for a fourth product surface (Desktop) is unverified in this research pass — first implementation step should be a direct conversation with those three feature-owning teams, not an assumption that porting is trivial.
- No direct Studio 3T Desktop customer has been observed asking for this specifically — the case rests on persona research, competitive positioning, and proven internal precedent, not an expressed individual demand the way VoC pilot record #2 is for `PROP-cli-automation`. Worth a lightweight validation step (e.g., a quick community/forum post floating the idea) before committing full engineering time.
- False positives/negatives in classification carry reputational risk for a security-adjacent feature — recommend shipping with confidence-scoring/hedging behavior (flagging uncertain fields as "review needed" rather than a false-confident PII/not-PII verdict), consistent with how the existing in-house implementations are understood to behave.

## Shortlist deep-dive: the other 4 (why they didn't win)

Full cards, calculation walkthroughs, and citations for all 5 shortlisted candidates: [04-scored-longlist.md](../research/feature-decision-2026/04-scored-longlist.md#full-research-result-cards).

### `PROP-cli-automation` — Headless CLI/CI-CD pipeline automation — ⚔️ Gap-Close · 7.50
**Why it scores highest:** Evidence Strength 4 = 1 Tier B recommendation + 1 Tier C direct customer record with an explicit 3T-staff confirmation of the gap (VoC #2) + 1 additional Tier B review-mining finding found in this pass's re-reading of `studio-3t-review-mining`: *"Users express a strong need for a headless server daemon or cloud agent capable of executing background data migrations, masked exports, and scheduled synchronization jobs independently of the local laptop state."* Competitive Urgency 3 = DBeaver Pro/Ultimate's `-runTask`/`-var` CLI syntax, confirmed via direct fetch of DBeaver's own GitHub wiki (a primary source, not a secondary description). Build Effort 2 = wraps existing, already-shipping Task Scheduler/masking/Data Compare logic. **Why it's not the recommendation:** its classification is unambiguously ⚔️ Gap-Close (specifically vs. DBeaver's paid tiers) — it answers "what should we catch up on," not "what widens our lead," which was this decision's explicit framing. Flagged as a strong, cheap, well-evidenced **fast-follow** candidate for a separate decision.

### `PROP-webhook-notify` — Webhook notifications — ❔ Parity-Unverified · 7.00
**Why it scores this high:** Reach 4 and Severity 3 are solid-but-unspectacular; Build Effort 2 (additive to existing `SCHED-notifications`) is what pushes the composite score up. **Why it's not the recommendation:** a full re-scan of all 21 `google_research` files for this pass found zero additional evidence beyond the single original `studio-3t-missing-integrations` recommendation — this is, by source count, the weakest-evidenced candidate in the entire top 5, resting on "we proved the pattern works in 3T Lens" rather than any demonstrated demand for it on Desktop specifically.

### `PROP-idx-perf-advisor` — AI query/index performance advisor — ⚔️ Gap-Close (corrected) · 5.67
**Why it scores well:** Reach 5 — the single highest Reach score of any candidate in the long-list, because query/index performance affects literally every persona that runs a query. A newly re-mined quote from `studio-3t-review-mining` — *"Users frequently request an automated indexing and query tuning engine that analyzes execution stats, identifies unindexed collection scans, and provides actionable recommendations"* — is a direct, Studio-3T-specific demand signal, not an inference. **Why it's not the recommendation:** its classification changed from 🌱 Lead-Widener to ⚔️ Gap-Close mid-research, once this repo's own comparison data was checked properly and found Compass and VisuaLeaf both already ship a version of this (`IDX-perf-insights`, confirmed ✅ for both). A real, valuable, well-evidenced candidate — just not first-to-market.

### `PROP-qe-key-vault-ui` — Queryable Encryption/CSFLE key-vault UI — ⚔️ Gap-Close · 5.00
**Why it scores well:** Evidence Strength 5, the maximum awarded to any candidate — dictionary tracking, 2 independent research files, this repo's own `cumulative-report.md` confirming Compass's exclusivity, a fresh 2026 search re-confirming it, and (newly found in this pass, re-reading `nosqlbooster-competitive-intelligence-analysis` in full) a second competitor moving the same direction: *"Adding support for OIDC, AWS IAM credential processes, and Client-Side Field Level Encryption indicates an effort to appeal to enterprise compliance teams."* **Why it's not the recommendation:** it is explicitly ⚔️ Gap-Close (vs. Compass, with NoSQLBooster following), Reach is capped at 3 (enterprise/regulated-only, a poor fit for the required "also serve startups" dimension), and the delivery bar for a security-critical UI is higher-stakes than the raw Build Effort score captures.

## Deferred, not rejected: two candidates worth a separate future decision

- **`PROP-cli-automation`** (7.50, ⚔️ Gap-Close vs. DBeaver): the strongest evidence base in this entire study, and very cheap to build. Worth an explicit fast-follow decision.
- **`PROP-schema-erd-cluster`** (4.00, ⚔️ Gap-Close vs. Compass+VisuaLeaf): the single most rigorously-confirmed finding in this whole repository — the entire 3T product family's only portfolio-wide, Tier-A-confirmed capability gap. Cut here only because a full 13-sub-feature build exceeds this decision's effort ceiling and because it's fundamentally a gap-close, not a lead-widener — not because the evidence is weak. This should be its own dedicated research effort, likely scoped as a multi-quarter bet, not folded into a "1-2 cycle, widen the lead" decision.

## Appendix: file map

| File | Contents |
|---|---|
| [feature-dictionary.md § Proposed Feature Registry](../feature-dictionary.md#proposed-feature-registry-research-pipeline) | The classification taxonomy (single source of truth) and the registry of all 20 `PROP-` IDs with their tags and status |
| [00-dialog-and-inputs.md](../research/feature-decision-2026/00-dialog-and-inputs.md) | Full discussion record — original ask, all clarifying questions and answers |
| [01-research-plan.md](../research/feature-decision-2026/01-research-plan.md) | Stage-by-stage plan, rubric definitions, card template, Stage 6/7 requirements addenda |
| [02-data-inventory.md](../research/feature-decision-2026/02-data-inventory.md) | Source reliability tiers (A-E) |
| [03-candidate-longlist.md](../research/feature-decision-2026/03-candidate-longlist.md) | 20 headline candidates + triaged atomic gaps, VoC tagging, fresh-search drift findings |
| [04-scored-longlist.md](../research/feature-decision-2026/04-scored-longlist.md) | Full 5-axis scoring, classification tags, and calculation walkthroughs for every candidate |
| [05-shortlist-deepdive.md](../research/feature-decision-2026/05-shortlist-deepdive.md) | Fresh targeted research on the top 5, with score revisions |
| [06-verification-notes.md](../research/feature-decision-2026/06-verification-notes.md) | Adversarial re-verification, citation-drift catches and corrections, final scores |
