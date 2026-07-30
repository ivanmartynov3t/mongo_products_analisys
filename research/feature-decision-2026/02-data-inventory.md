# Stage 0 — Data Inventory & Source Reliability Baseline

## Navigation

- [Repository README](../../README.md)
- [Feature dictionary](../../feature-dictionary.md)
- [Google research overview](../google_research/overview.md)
- [← Dialog & inputs](00-dialog-and-inputs.md) · [← Research plan](01-research-plan.md)
- [Next stage: candidate long-list](03-candidate-longlist.md)

## Purpose

Before generating or scoring any candidate feature, establish what evidence actually exists in and around this repository, and how much weight each source type can carry. This baseline is referenced by every later stage's "Evidence Strength" scoring — a candidate's score is only as good as the tier of its supporting sources.

## Decision context (from discussion with the user, 2026-07-30)

| Parameter | Decision |
|---|---|
| Objective | Widen Studio 3T's strategic lead (not a defensive gap-fill) |
| Candidate scope | Capabilities Studio 3T Desktop does **not** have yet — both dictionary-tracked gaps and net-new ideas |
| Primary segment | Enterprise / regulated teams |
| Secondary segment | Medium-to-large startups needing similar functionality |
| Effort ceiling | Medium — shippable in 1-2 release cycles, no new infrastructure/deployable product |
| Research base | Existing repo research as foundation + targeted fresh web search |
| Web source policy | Compliant public sources only (vendor docs/changelogs, GitHub issues, official blogs/press) — no direct G2/Capterra/Reddit/TrustRadius scraping |
| Internal data | None available (no CRM, support tickets, telemetry, NPS) |
| Scoring model | Adapted FPI: 5 evidence-backed axes → composite Priority Score (see Stage 2) |
| Orchestration | Single-threaded, sequential, user can interject at any stage |
| Funnel size | 15+ raw candidates → scored long-list → 3-5 shortlist → 1 recommendation |
| Deliverable | Full decision memo in `reports/`, with all intermediate stage files kept as sub-results |

## Source reliability tiers

| Tier | Source | What it is | Reliability character | Recency |
|---|---|---|---|---|
| **A — Primary, structured** | `feature-dictionary.md`, `reports/gap-analysis-not-on-3t-*.md`, `products/**/product-report.md` | This repo's own source-cited, confirmed/unverified-labeled analysis | High — every claim traceable to a specific product doc/matrix, built and cross-checked over multiple passes (see the 2026-07-29 deep-file verification note in `low-level-feature-comparison.md`) | Current as of 2026-07-29 |
| **B — Secondary, cited market research** | `research/google_research/*` (21 files) | AI-assisted "deep research" style competitive/market analyses | High-for-secondary-research — verified during this session: every file carries 20-65 real, resolvable citations (GitHub issues, vendor docs/changelogs, G2 pricing pages, engineering blogs). Not primary data; reflects public sentiment and competitor documentation, not Studio 3T's own usage data | Analysis dates range ~2026-06-22 to 2026-07-29 (file mtimes) |
| **C — Primary, narrow-sample** | `reports/voice-of-customer-metrics.md` | 7 real, cited quotes from `community.studio3t.com` | High per-record (verbatim quotes, live URLs) but statistically tiny (N=7, single source domain); explicitly a pilot, not a program | Pilot run 2026-07-29 |
| **D — To be gathered** | Fresh web search (this research) | Compliant public sources only, run during Stages 1e/3 to catch drift since Tier B's analysis dates and to deep-dive the shortlist | Same reliability character as Tier B, but current as of today | 2026-07-30 |
| **E — Not available** | CRM/ARR/win-loss, support tickets (Zendesk/Jira), in-app telemetry, NPS/CSAT/SUS surveys | Described as ideal inputs in `research/research-methodology-general.md` and `research/report-building-framework.md`'s FPI formula | **Absent.** Confirmed with the user (2026-07-30) that none of this exists in this environment. This is a hard limitation on the whole exercise, not a gap to quietly paper over — see the Known Limitations section of the final memo. | N/A |

## What this baseline changes downstream

- **Evidence Strength scoring (Stage 2)** privileges candidates supported by Tier A+B+C convergence over candidates resting on a single Tier B mention.
- **Severity scoring** leans on Tier C's existing 1-5 pain-severity convention (already defined in the VoC pilot) for consistency, applied qualitatively to Tier B evidence where no direct quote exists.
- **The FPI adaptation is deliberately evidence-only**: the literal formula in `research/report-building-framework.md` assumes Tier E inputs (raw telemetry/ARR counts) that don't exist here. Those terms are dropped rather than estimated — inventing plausible-looking numbers for data we don't have would violate this repo's own "confirmed vs. unverified" discipline.
- **Every final claim** in the Stage 5 memo will be labeled confirmed (Tier A/B/C/D with a live citation) / roadmap-inferred (reasonable extrapolation, flagged as such) / unverified — never asserted as fact from a Tier E gap.
