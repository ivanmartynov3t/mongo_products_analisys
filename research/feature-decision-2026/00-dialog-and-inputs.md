# Stage -1 — Discussion Record: Dialog & Inputs

## Navigation

- [Repository README](../../README.md)
- [Research plan →](01-research-plan.md)
- [Data inventory & source tiers →](02-data-inventory.md)

## Purpose

This file is the durable record of the discussion that shaped this research effort — the original ask, the clarifying questions asked, and the user's actual answers (including nuances beyond the offered options). It exists so anyone picking this work up later (including a future session) understands *why* the plan and scoring model look the way they do, without having to re-derive it from a chat transcript that won't persist.

## Original request (2026-07-30)

> "Now I want you to see what data we have, and do research and deep web search how better use the data to finally make very justified decision about which new feature to implement for our desktop studio 3t app."

Explicit process requirements the user attached to that ask:
- Step-by-step research, gathering from different sources first.
- A **unified format** for research results, with **metrics** on each research result.
- Assess what data we have vs. what we might still need to collect.
- **Discuss before planning** — ask questions one by one, covering different aspects of the topic in detail, each with **3 answer options and one marked default**.
- Get deep understanding of existing research methods (the `research/` methodology docs) and all existing data **first**, with explicit attention to `google_research/`, before asking questions.

## Pre-question investigation (what I did before asking anything)

Per the instruction to understand existing methods and data before discussing, I:
1. Re-read the three methodology docs (`gather-metrics-instructions.md`, `report-building-framework.md`, `research-methodology-general.md`) already in `research/`.
2. Verified the **credibility of `google_research/`** directly rather than trusting prior summaries: counted citations in all 21 files — every file carries 20-65 real, resolvable URLs (GitHub issues, vendor docs/changelogs, G2 pricing pages, engineering blogs). Confirmed this is genuine cited secondary research, not fabricated narrative.
3. Re-read `feature-dictionary.md`'s coverage matrix, both gap-analysis reports, the VoC pilot, and Studio 3T's own `product-report.md` (including its "Strategic risks/gaps" and "Open questions" sections).
4. Synthesized the finding that drove the whole framing: rich, well-sourced **public** signal exists, but there is a real gap in **primary/internal** signal (telemetry, CRM, tickets, interviews) — that gap needed to be a discussion point, not something quietly absorbed into a plan.

## Round 1 — Decision framing

**Q1. What's the primary objective driving this feature decision?**
Options offered: (a) Close a competitive gap *(default)* / (b) Widen a strategic lead / (c) Reduce friction for existing users
**Answer: (b) Widen a strategic lead.** User explicitly did not take the default — this is not a defensive move, it should extend an area where Studio 3T already leads rather than catch up on something competitors have.

**Q2. Should candidate search be constrained to one area, or fully open?**
Options offered: (a) Fully open *(default)* / (b) Constrain to F-SCHEMA (the one confirmed portfolio-wide gap) / (c) User names specific areas
**Answer: Fully open, with an added constraint the options didn't cover:** *"but we focus only on features / subfeatures we haven't implemented yet for product."* — i.e., scope is open across all 11 feature areas, but restricted to net-new capability, not enhancements to existing features. This became its own follow-up question (see below) because it has two possible readings.

**Q3. Which customer segment should the feature primarily serve?**
Options offered: (a) Enterprise/regulated *(default)* / (b) Individual developers/startups / (c) Segment-agnostic
**Answer: (a) Enterprise/regulated, plus an addition:** *"but touch some medium/huge startups which need some functionality."* — primary segment is enterprise/regulated, but the feature must also plausibly serve scaled (not tiny) startups with similar needs.

**Q4. Effort/timeframe ceiling?**
Options offered: (a) Medium, 1-2 release cycles *(default)* / (b) Small quick-win / (c) Large multi-quarter bet
**Answer: (a) Medium, 1-2 release cycles** — accepted as given.

## Round 2 — Data & methodology

Before this round, I flagged the ambiguity in Q2's answer and asked directly:

**Q5. Should candidates be limited to gaps already tracked in `feature-dictionary.md` (108 IDs), or also include net-new ideas from research with no dictionary ID yet?**
Options offered: (a) Both *(default)* / (b) Dictionary gaps only / (c) Net-new ideas only
**Answer: (a) Both.** If a net-new idea wins, it gets added to `feature-dictionary.md` first, per the repo's own existing convention.

**Q6. How much weight should the existing 21 `google_research` files carry vs. fresh web research?**
Options offered: (a) Existing files as base + targeted fresh search *(default)* / (b) Redo broad research from scratch / (c) Existing files only, no new search
**Answer: (a)** — accepted as given.

**Q7. For fresh web research, how strict should source compliance be?**
Options offered: (a) Compliant public sources only *(default)* / (b) Compliant + user-pasted excerpts from review sites / (c) Best-effort direct fetch from review sites, accepting ToS risk
**Answer: (a)** — accepted as given. This matches the policy the VoC pilot already established (`gather-metrics-instructions.md` explicitly instructs scraping G2/Capterra/Reddit, which their own Terms of Service prohibit — that instruction is not followed here either, consistent with the prior pilot's decision).

**Q8. Any internal/proprietary data available (support tickets, CRM win-loss, telemetry, NPS)?**
Options offered: (a) None available *(default)* / (b) User can share some / (c) Flag what's missing instead
**Answer: (a) None available** — accepted as given. Logged as a hard limitation on the whole exercise (see Stage 0/`02-data-inventory.md`, Tier E).

## Round 3 — Scoring model & output shape

**Q9. Scoring/metrics framework?**
Options offered: (a) Adapted FPI, evidence-only inputs *(default)* / (b) Simple qualitative 1-5 rubric across 5 axes / (c) RICE or ICE
**Answer: Both (a) and (b) combined** — explicitly: *"Score each candidate 1-5 on: Evidence strength / Reach / Severity / Competitive urgency / Build effort... and... Adapted FPI... both."* Resolved as: the 5-axis rubric **is** the evidence-backed input layer, rolled up into a single adapted-FPI-style composite Priority Score. See `01-research-plan.md` for the exact formula and rubric definitions.

**Q10. Multi-agent Workflow orchestration, or single sequential thread?**
Options offered: (a) Single-thread *(default)* / (b) Multi-agent Workflow / (c) Hybrid
**Answer: (a) Single-thread** — accepted as given. All extraction/scoring/verification work is done directly (Read/Grep/WebSearch/WebFetch), not delegated to background agents, so the user can follow and interject at any point.

**Q11. Deliverable shape?**
Options offered: (a) Full decision memo *(default)* / (b) Scored shortlist only, user picks / (c) Both, staged
**Answer: (a) Full decision memo** — accepted as given.

**Q12. Funnel size (candidates before narrowing to one)?**
Options offered: (a) ~8-12 *(default)* / (b) 3-5 / (c) 15+
**Answer: (c) 15+** — user explicitly did not take the default; wants an exhaustive canvass before any cuts.

## Post-discussion clarifications (mid-turn messages)

After the three rounds, the user sent (repeated, with escalating specificity):

1. *"as a result we get a very detailed research plan, describing in details goal and format of each research stage, multi steps, and very detailed, all conclusions double checked and have deep support and argumented from data we have or will get"* — requesting the plan itself be exhaustively detailed per-stage (goal + output format each), with an explicit double-check/verification stage, not just a final scored answer.
2. *"for each intermediate steps create files with full detailed research sub-results"* — requesting every stage's output be persisted as its own file, not folded silently into only the final memo.
3. *"create a directory for research results in @research and document there the dialog and input I have / write .md file with research plan in all details, super specific"* — this file, and `01-research-plan.md`, are the direct response to that instruction.

## How these decisions map to file structure

| File | Corresponds to |
|---|---|
| `00-dialog-and-inputs.md` | This file — the discussion record |
| `01-research-plan.md` | The super-detailed, per-stage plan (clarification #1 above) |
| `02-data-inventory.md` | Stage 0 output — source tiers, informed by Q5-Q8 |
| `03-candidate-longlist.md` | Stage 1 output — informed by Q2/Q5/Q12 (open scope, both gap types, 15+ target) |
| `04-scored-longlist.md` | Stage 2 output — informed by Q9 (rubric + composite) and Q4 (effort ceiling filter) |
| `05-shortlist-deepdive.md` | Stage 3 output — informed by Q6/Q7 (fresh, compliant-source research) |
| `06-verification-notes.md` | Stage 4 output — the explicit double-check pass requested in clarification #1 |
| `reports/next-feature-recommendation.md` | Stage 5 — final memo, informed by Q1/Q3/Q11 (widen-lead framing, dual-segment fit, full memo) |
