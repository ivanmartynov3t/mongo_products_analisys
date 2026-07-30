# Stage 0 — Research Plan: Which New Feature to Implement for Studio 3T Desktop

## Navigation

- [Repository README](../../README.md)
- [← Dialog & inputs](00-dialog-and-inputs.md)
- [Data inventory & source tiers →](02-data-inventory.md)
- [Candidate long-list →](03-candidate-longlist.md)

## Objective

Identify **one** new capability for the **Studio 3T Desktop IDE** — not currently implemented there — that **widens Studio 3T's existing strategic lead**, is credible for **enterprise/regulated teams** while also plausibly serving **medium-to-large startups**, and is shippable within **1-2 release cycles** (no new infrastructure or separate deployable product). The recommendation must be traceable to evidence, not intuition, and every claim must be labeled confirmed / roadmap-inferred / unverified.

Full derivation of these constraints: [00-dialog-and-inputs.md](00-dialog-and-inputs.md).

## Candidate universe (what counts as a candidate)

1. **Dictionary-tracked gaps** — any of the 108 sub-feature IDs in `gap-analysis-not-on-3t-desktop.md` not confirmed present on Studio 3T Desktop (13 confirmed-absent-portfolio-wide + 17 present-elsewhere-in-3T-family + 78 unverified).
2. **Net-new ideas** — capabilities surfaced by research that have no `feature-dictionary.md` ID yet at all (e.g., an AI-driven index/query optimization advisor, native Git integration). If one of these wins, it gets added to the dictionary first, per the repo's own authoring rule in `.github/copilot-instructions.md`.

Explicitly **out of scope**: enhancements/fixes to capabilities Studio 3T Desktop already has (that's a different kind of roadmap decision, not this one).

## Source reliability tiers (summary — full detail in [02-data-inventory.md](02-data-inventory.md))

| Tier | Source | Character |
|---|---|---|
| A | `feature-dictionary.md`, gap-analysis reports, `product-report.md` files | Primary, structured, source-cited |
| B | `research/google_research/*` (21 files) | Secondary, well-cited (20-65 URLs/file), AI-synthesized market/competitive research |
| C | `reports/voice-of-customer-metrics.md` | Primary but tiny (N=7 real quotes) |
| D | Fresh compliant web search (this effort) | Same character as B, dated 2026-07-30 |
| E | CRM/tickets/telemetry/NPS | **Unavailable** — hard limitation, logged not papered over |

## The Unified Research Result Card

Every candidate, at every stage from Stage 1 onward, is expressed in this exact format so results are comparable and auditable:

```markdown
### Candidate: <name>
- Feature area: <existing F-ID/sub-feature ID(s), or "NEW — needs dictionary entry">
- Description: 2-3 sentences, what it is and what it does for the user
- Segment fit: enterprise/regulated | medium-large startup | both
- Sources: [Tier-tagged list, each a live link] e.g. (B: dbeaver-competitive-intelligence-analysis), (A: gap-analysis-not-on-3t-desktop.md#...), (C: VoC record #4)
- Evidence Strength (1-5): <score> — <one-line rationale citing which sources>
- Reach (1-5): <score> — <rationale>
- Severity (1-5): <score> — <rationale>
- Competitive Urgency (1-5): <score> — <rationale>
- Build Effort (1-5, lower = easier): <score> — <rationale>
- Priority Score: <(Evidence + Reach + Severity + Urgency) / Effort>
- Verification notes: <populated in Stage 4 only>
```

## Scoring rubric (fixed definitions — reused identically for every candidate)

| Score | Evidence Strength | Reach | Severity | Competitive Urgency | Build Effort |
|---|---|---|---|---|---|
| 1 | Single weak/unverified mention | 1 persona, niche/edge case | Cosmetic, nice-to-have | No competitor has it, no visible trend | Trivial — config/UI tweak, days |
| 2 | 1 strong (Tier A/B/C) source, or 2+ weak | 2 personas | Minor inconvenience, easy workaround | 1 competitor has a basic version | Small — 1 sprint, built on existing infra |
| 3 | 2+ independent credible sources agree | 3-4 personas, incl. a target segment | Workflow drag; workaround exists but costs real time | 2-3 competitors have it, or an emerging trend (per tech-trends research) | Medium — fits the 1-2 release cycle ceiling |
| 4 | 3+ sources, incl. at least one direct customer-voice source (Tier C, GitHub issue, forum) | 5+ personas, strong fit both target segments | Major impairment — forces switching to a secondary/competitor tool | Most direct competitors have it; established market expectation | Large — new subsystem/architecture change, **exceeds ceiling** |
| 5 | Broad convergence: research (B) + direct customer complaint (C) + competitor confirmation (B/D) all agree | Universal — virtually every persona and both target segments | Blocking/deal-losing — directly cited as a churn/lost-sale reason | Universal competitor baseline AND an actively growing trend | Very large — multi-quarter/new infrastructure, **exceeds ceiling** |

**Composite Priority Score** = `(Evidence Strength + Reach + Severity + Competitive Urgency) / Build Effort`
Range: min ≈ 0.8 (all 1s over effort 5), max = 20 (all 5s over effort 1). Higher = higher priority (high value, low cost).

**Effort ceiling rule:** candidates scoring Build Effort 4-5 remain visible in the long-list (Stage 1-2) for transparency, but are excluded from the Stage 3 shortlist with an explicit one-line reason — never silently dropped.

**Confidence is not a separate score** — it's expressed through Evidence Strength (which already encodes source-count and source-type diversity) plus the Verification notes field populated in Stage 4. Keeping it to one axis avoids double-counting the same signal under two different names.

## Stage-by-stage plan

### Stage 1 — Broad candidate canvass (target: 15+ raw candidates)
**Goal:** exhaustive long-list before any narrowing.
**Method:**
- 1a. Extract all 108 tracked IDs from `gap-analysis-not-on-3t-desktop.md`, grouped by feature area.
- 1b. Re-scan all 21 `google_research` files for every explicit "should build X" / gap / missing-capability statement (going past `overview.md`'s condensed summaries into full files where a recommendation needs more than one line).
- 1c. Pull Studio 3T's own `product-report.md` "Strategic risks/gaps" and "Open questions."
- 1d. Tag which of the 7 VoC pilot records represent a *missing capability* (candidate) vs. a *bug in an existing feature* (out of scope per the candidate-universe rule above).
- 1e. Fresh compliant web search for competitor features shipped **since** the `google_research` analysis dates (~mid-2026), to catch drift the existing files can't reflect.
**Output format:** flat table — name, one-line description, feature area, source tags, segment hint. A dedup pass merges same-idea candidates surfaced by multiple sources into one entry (keeping every source tag).
**File:** [03-candidate-longlist.md](03-candidate-longlist.md)

### Stage 2 — Score every candidate
**Goal:** convert every deduped candidate into a full Research Result Card, ranked.
**Method:** apply the fixed rubric above to every candidate, computing the Priority Score; apply the effort-ceiling rule to mark shortlist-eligible vs. cut(reason).
**Output format:** long-list table sorted by Priority Score, with a shortlisted/cut column; full cards for every candidate.
**File:** [04-scored-longlist.md](04-scored-longlist.md)

### Stage 3 — Shortlist deep-dive (top 3-5 candidates)
**Goal:** gather deeper, fresher evidence on only the strongest candidates before committing — the "will get" data collection.
**Method**, per shortlisted candidate:
- Targeted fresh web search on current competitor implementation depth/UX.
- Search for any 2026 Studio 3T / 3T Software Labs roadmap signal.
- Direct search of `community.studio3t.com` for related requests/complaints (same compliant source the VoC pilot already used).
- Technical feasibility sanity-check against Studio 3T's documented architecture (JVM desktop client; existing Aggregation Editor/VQB/IntelliShell internals per the feature reports).
**Output format:** expanded card per shortlisted candidate — same fields, each rationale now backed by Stage 3 evidence; scores re-affirmed or adjusted with a note on what changed and why.
**File:** [05-shortlist-deepdive.md](05-shortlist-deepdive.md)

### Stage 4 — Adversarial self-verification (the double-check pass)
**Goal:** actively try to break each shortlisted candidate's case before committing. Because orchestration is single-threaded (no independent verifier agent), this is done explicitly as its own pass rather than skipped.
**Method**, per shortlisted candidate:
- Re-open every cited source and confirm it actually supports the specific claim attributed to it (catch citation drift/overstatement).
- Actively search for disconfirming evidence (a competitor deprecating the feature, low real usage signal, an architectural reason it might not fit Studio 3T).
- Re-derive Severity and Competitive Urgency directly from raw source text rather than from my own earlier paraphrase of it, to avoid compounding paraphrase drift.
- Label every claim confirmed / roadmap-inferred / unverified.
**Output format:** a "Verification notes" block per shortlisted candidate — what held up, what was downgraded, what remains unverified.
**File:** [06-verification-notes.md](06-verification-notes.md)

### Stage 5 — Final recommendation & memo
**Goal:** commit to one recommendation, write the full decision memo.
**Method:** pick the highest post-verification Priority Score candidate that also clearly satisfies the "widen the lead" objective and dual-segment fit; if the top-scored candidate doesn't cleanly satisfy the objective framing, the tradeoff is argued explicitly rather than silently overridden.
**Output format (memo):** Navigation → Executive summary → Methodology & source reliability → Known limitations → Long-list table → Shortlist cards with verification notes → Final recommendation (full case, segment fit, effort/feasibility, suggested dictionary ID(s), risks/open questions) → source appendix.
**File:** `reports/next-feature-recommendation.md`

### Stage 6 — Full review, fact-verification & citation audit *(added 2026-07-30, after Stage 5 was first delivered)*

The user reviewed Stage 5's output and imposed three additional, binding requirements on the whole research effort, retroactively as well as going forward:

1. **Full review of all aspects, with fact verification.** Every stage file gets re-audited, not just the shortlist. Any claim that cannot be traced to a specific source is either fixed with a real citation, re-verified via a fresh search/fetch, or explicitly softened/removed — never left standing on the strength of the writing alone.
2. **More human-readable arguments for *why* each candidate ranks where it does**, not just the 5-axis numeric scores. Numbers alone are not the deliverable; the prose case behind them is.
3. **Expand the ranked, fully-argued list from 5 (the Stage 3/4 shortlist) to approximately 15 candidates.** The other ~5-10 headline candidates that were previously only given an abbreviated one-line cut reason (in `04-scored-longlist.md`'s "cut, cards abbreviated" section) get full narrative treatment too.
4. **Strict citation discipline: "do not invent — this research is based strictly on data."** Every factual claim (not scoring judgment, which is inherently analytical) must cite a specific source: a repo file (with section/line reference where useful), a `google_research` file, a VoC pilot record number, or a specific fresh search/fetch performed in this session with its URL. General background knowledge not traceable to an actual source consulted in this research is not an acceptable citation — if a claim can't be sourced this way, it is flagged as an assumption or removed.

**Goal:** the finished research artifact should let a skeptical reader trace every non-scoring claim back to where it came from, and see the reasoning in prose, not just infer it from a table of numbers.
**Method:** re-read Stages 1-4 and the Stage 5 memo end-to-end; for each candidate, check every citation resolves and says what's attributed to it (extending the Stage 4 methodology, which had only been applied to the 5 shortlisted candidates, to all ~20); expand cards for the next-ranked ~10 candidates beyond the original shortlist into full narrative form; correct anything that doesn't hold up, with the correction disclosed rather than silently fixed (consistent with how the Stage 4 citation-drift catch was already handled).
**Output format:** corrections applied directly to Stages 1-4 files where a specific error is found (with the fix visible, e.g. a citation added or a claim corrected), an expanded ranked section in the Stage 5 memo covering ~15 candidates with prose rationale each, and this section recording that the requirement was added and why.
**Files touched:** all of them, as needed — this is a review pass across the whole effort, not a new isolated stage file.

## File map

| Stage | File | Status |
|---|---|---|
| — | `00-dialog-and-inputs.md` | done |
| — (this file) | `01-research-plan.md` | done |
| 0 | `02-data-inventory.md` | done |
| 1 | `03-candidate-longlist.md` | done, revised in Stage 6 |
| 2 | `04-scored-longlist.md` | done, revised in Stage 6 |
| 3 | `05-shortlist-deepdive.md` | done |
| 4 | `06-verification-notes.md` | done, extended in Stage 6 |
| 5 | `../../reports/next-feature-recommendation.md` | done, revised in Stage 6 |
