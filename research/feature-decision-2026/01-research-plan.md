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

1. **Dictionary-tracked gaps** — any of the sub-feature IDs in `gap-analysis-not-on-3t-desktop.md` not confirmed present on Studio 3T Desktop. **Corrected 2026-07-31 (Stage 8):** the 2026-07-31 Studio 3T Desktop source-code re-audit changed this count from 108 (13 confirmed-absent-portfolio-wide + 17 present-elsewhere-in-3T-family + 78 unverified) to **89** (9 confirmed-absent-portfolio-wide + 17 present-elsewhere-in-3T-family + 9 confirmed-absent-from-Desktop-specifically-portfolio-status-unverified + 54 unverified) — see [Stage 8 addendum](#stage-8--2026-07-31-sync-with-the-desktop-source-code-re-audit) below for what moved and why.
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

### Stage 7 — Formal classification, deeper evidentiary depth & calculation transparency *(added 2026-07-30, after Stage 6 was delivered)*

The user reviewed Stage 6's output and imposed four further, binding requirements:

1. **A formal classification system for proposed features, defined in `feature-dictionary.md` itself, and used consistently across every research file and the final memo.** Not just prose labels invented per-candidate — a registered taxonomy with a legend, applied identically everywhere a candidate is discussed. Delivered as the **Proposed Feature Registry** section of `feature-dictionary.md`: a `PROP-<slug>` ID per candidate, plus three classification axes (**Competitive Framing**: Lead-Widener / Gap-Close / Parity-Unverified; **Origin**: Portfolio-Port / Net-New; **Dictionary linkage**: Dictionary-Tracked / Net-New-Concept) and a **Pipeline Status** (Proposed / Shortlisted / Recommended / Deferred / Cut / Implemented).
2. **Deeper research verification with more rigorous, human-readable argumentation.** The user's assessment: "Level of argumenting and citations is poor." This means going back into the **full text** of the relevant `google_research/` files (not just `overview.md`'s condensed summaries, and not just the excerpts already quoted) to pull additional direct quotes, numbers, and specifics that strengthen or complicate each candidate's case — "read the google research directory again and use as much facts as possible related to each proposal."
3. **"Deep sections" per proposal** — the top candidates (at minimum the recommendation and the shortlist) get materially expanded write-ups: more quotes, more competitive detail, more explicit reasoning chains connecting evidence to score, not just a paragraph summary.
4. **Explicit calculation transparency in the final memo.** The user's specific complaint: "not clear in reports/next-feature-recommendation.md how metrics calculated." The memo must show, for each metric on each featured candidate, not just the final 1-5 number but the reasoning step that produced it — which source(s) were weighed, why they landed on that number and not one adjacent to it, and the arithmetic for the composite Priority Score spelled out (not just stated as a result).

**Goal:** a reader with no prior context should be able to open `feature-dictionary.md`, see exactly what "Gap-Close" or "Lead-Widener" means and which candidates carry which tag; open the memo and see, for the recommended feature, not just "Reach: 4" but the specific evidence and reasoning that produced a 4 rather than a 3 or 5; and trust that every quote came from a file that still exists and says what's claimed.
**Method:**
- Design the classification taxonomy once, in `feature-dictionary.md`, as the single source of truth — every other file references it rather than redefining it.
- Re-read the full raw text of the `google_research/` files backing the recommendation and shortlist (not relying solely on `overview.md` or previously-pulled excerpts), specifically hunting for additional quotable facts: numbers, named competitor behaviors, direct customer-facing language.
- Rewrite `04-scored-longlist.md`'s candidate cards to (a) carry the three classification tags plus pipeline status, matching the dictionary's registry exactly, and (b) show the calculation reasoning per axis, not just the final number.
- Rewrite `reports/next-feature-recommendation.md` to surface classification tags in the ranked table, add a per-metric "how this was calculated" explanation for the recommended candidate and full shortlist, and substantially deepen the evidentiary sections with the newly-mined facts.
**Output format:** `feature-dictionary.md`'s new Proposed Feature Registry section (the taxonomy's single source of truth); revised `04-scored-longlist.md` with classification tags and calculation walkthroughs on every card; revised `reports/next-feature-recommendation.md` with a classification column, per-metric calculation transparency, and deep evidentiary sections citing newly re-mined `google_research/` facts.
**Files touched:** `feature-dictionary.md` (new registry), `01-research-plan.md` (this section), `04-scored-longlist.md`, `reports/next-feature-recommendation.md`.

### Stage 8 — 2026-07-31 sync with the Desktop source-code re-audit

Independently of this decision effort, a separate full source-code re-audit of Studio 3T Desktop against `products/3t/studio-3t/` ran on 2026-07-31 (see [research/studio-3t-desktop-review-2026/](../studio-3t-desktop-review-2026/)) and materially changed `feature-dictionary.md`, `reports/gap-analysis-not-on-3t-desktop.md`, and `reports/cumulative-report.md` — the exact Tier A sources this whole decision pipeline scores candidates against. This stage is a targeted sync pass, not a re-run of Stages 1-7: it re-checks every candidate's factual premises against the corrected Tier A data and fixes what no longer holds, disclosing each fix rather than silently editing scores.

**What changed upstream, in one place:**

| Area | Was | Now (2026-07-31) | Candidates it touches |
|---|---|---|---|
| F-SCHEMA validator authoring/deployment (`SCHEMA-validation-model/-strictness/-ui`, `SCHEMA-deploy-validator`, `SCHEMA-validation-limits`) | Documented absent — part of the "13 confirmed-absent" F-SCHEMA cluster | **Confirmed present** on Studio 3T Desktop | Candidate 11 (`PROP-schema-erd-cluster`) — its dictionary-linked cluster shrinks from 13 IDs to **9** |
| F-SCHED notifications (`SCHED-notifications`, `SCHED-email`) | Assumed present in Stages 2-4 ("today's model is email/in-app only") — **this assumption was never checked against source, it was simply asserted** | **Confirmed absent** — no SMTP/email/notification code exists anywhere in the scheduler subsystem | Candidate 18 (`PROP-webhook-notify`) — Build Effort and Priority Score both revised, see [04](04-scored-longlist.md#candidate-18-slackteamsjirapagerduty-webhook-notifications--prop-webhook-notify) |
| F-SCHED other scheduler internals (9 IDs: status states, exec config, retry, concurrent, batch, history, history-retention, plus the two above) | Unverified | **Confirmed absent from Desktop specifically** (portfolio-wide status still unverified) | Strengthens, not weakens, the evidentiary case for scheduler-adjacent candidates — "confirmed absent" is stronger Evidence Strength than "unverified" per the Stage 2 rubric |
| F-IDX (10 previously-unverified IDs) | Unverified | 4 confirmed present (`IDX-type-hashed`, `IDX-advanced-opts` partial, `IDX-realtime-perf`, `IDX-stop-ops`), 6 confirmed absent | No headline candidate directly absorbed these beyond Candidates 1/16 (both unaffected — `IDX-perf-insights`/`IDX-vector-search` remain confirmed absent) |
| F-GOV (11 previously-unverified IDs) | Unverified (governance matrix was an unauthored placeholder) | Matrix fully authored — most resolved to confirmed-present (RBAC tree/inheritance/actions, telemetry, network policy) or confirmed-absent (`GOV-cli-policy`, `GOV-isolated-edition`) | No headline candidate directly absorbed these; affects the atomic-gaps blanket assessment only |
| F-AGG (4 previously-unverified IDs) | Unverified | 3 confirmed present (`AGG-pagination`, `AGG-timer-cancel`, `AGG-stage-count`), 1 confirmed absent (`AGG-chart-builder`) | Not absorbed into any headline candidate |
| Total dictionary-tracked gap IDs (`gap-analysis-not-on-3t-desktop.md`) | 108 (13 + 17 + 78) | **89** (9 confirmed-absent-portfolio-wide + 17 present-elsewhere + 9 confirmed-absent-Desktop-specific + 54 unverified) | Candidate-universe framing in this file's own Objective section, above |

Full per-file corrections: [03-candidate-longlist.md](03-candidate-longlist.md), [04-scored-longlist.md](04-scored-longlist.md), [05-shortlist-deepdive.md](05-shortlist-deepdive.md), [06-verification-notes.md](06-verification-notes.md#stage-8--2026-07-31-dictionary-gap-analysis-sync-addendum).

**What this stage explicitly did not do:** re-run Stage 1's canvass to look for new candidates the audit's 17 newly-confirmed sub-feature IDs (e.g. `AI-agentic-mode`, `SHELL-bookmarks`) might suggest — those are now-confirmed *strengths*, not gaps, so they don't feed this "what's missing" pipeline directly, but they are a legitimate input to a *future* long-list canvass. Noted here so that future work isn't lost, not treated as in-scope for this sync.

## File map

| Stage | File | Status |
|---|---|---|
| — | `00-dialog-and-inputs.md` | done |
| — (this file) | `01-research-plan.md` | done, Stage 8 sync added 2026-07-31 |
| 0 | `02-data-inventory.md` | done, Stage 8 sync note added 2026-07-31 |
| 1 | `03-candidate-longlist.md` | done, revised in Stage 6, synced in Stage 8 |
| 2 | `04-scored-longlist.md` | done, revised in Stage 6, deepened in Stage 7, corrected in Stage 8 |
| 3 | `05-shortlist-deepdive.md` | done, corrected in Stage 8 |
| 4 | `06-verification-notes.md` | done, extended in Stage 6, extended in Stage 8 |
| 5 | `../../reports/next-feature-recommendation.md` | done, revised in Stage 6, deepened in Stage 7 — **not yet synced to Stage 8, see note below** |
| 7 | `../../feature-dictionary.md` (Proposed Feature Registry section) | done, `PROP-webhook-notify` priority score synced in Stage 8 |

**Known follow-up, out of scope for this pass:** `reports/next-feature-recommendation.md` (the Stage 5 memo) still cites Candidate 18's pre-Stage-8 score/framing in its ranked table and shortlist section. This file update pass was scoped to `research/feature-decision-2026/` specifically; the memo should be re-synced in a follow-up pass before it's treated as current.
