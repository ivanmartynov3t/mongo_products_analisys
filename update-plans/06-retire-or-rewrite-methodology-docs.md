# Plan 6 — Retire or Rewrite the Non-Compliant Methodology Documents

## Objective

Three files sit directly under `research/`: `gather-metrics-instructions.md`, `report-building-framework.md`, `research-methodology-general.md`. `README.md` already flags all three as unconfirmed origin and, as written, non-executable/non-compliant (they assume scraping G2/Capterra/Reddit — a ToS violation — and CRM/Zendesk/telemetry access this environment does not have). `voice-of-customer-metrics.md` documents what was actually, compliantly adopted from them. That leaves the three source documents themselves in permanent limbo: flagged as broken, never fixed, never removed. This plan forces an explicit decision.

## Decision rule (apply per file, not once for all three)

For each of the three files, choose exactly one disposition using this rule, in order — stop at the first one that applies:

1. **Rewrite as compliant** if the document's core methodology has a legitimate, ToS-respecting equivalent (e.g., a scraping-based data-collection step can often be rewritten as "review the product's own public documentation, forum posts the vendor itself has published, and any research file already in `research/google_research/` that covers the same ground" instead of scraping a third-party site). Apply this to `gather-metrics-instructions.md` first — check whether its "Part 1" scraping framework can be reframed this way before considering the other two options for it.
2. **Mark permanently archival** if the document describes a real, sound methodology that simply requires resources this environment will never have (a live CRM connection, a Zendesk export, in-app telemetry) — keep it as a reference for a future context where those resources exist, but add a prominent header block stating it is not executable here and pointing to `voice-of-customer-metrics.md` as the actually-executed subset. Likely candidates: `report-building-framework.md` (its FPI-scoring math is sound and reusable once real metrics exist) and `research-methodology-general.md` (JTBD/conjoint/telemetry methodology, same reasoning).
3. **Delete** only if neither 1 nor 2 applies — i.e., the document has no salvageable methodology and no future-context value. Do not choose this as a default; it should be the least common outcome of the three.

## Task per file

1. Read the file fully, plus `voice-of-customer-metrics.md`'s "what was actually adopted" section (it already explains, per file, what was compliant vs. dropped — use that as your starting evidence, don't re-derive it).
2. Apply the decision rule above and pick one disposition.
3. Execute it:
   - **Rewrite**: produce a new version of the file (same filename) with the non-compliant steps replaced by compliant equivalents. Add a header noting the rewrite date and what changed, in the same spirit as the existing "unconfirmed origin" flag it's replacing.
   - **Archival**: add a header block (see wording pattern below) — do not alter the body content itself, since its value is as a reference for a future context, not as something to be executed today.
   - **Delete**: remove the file. Before deleting, check whether `README.md`, `feature-dictionary.md`, or any report links to it — if so, update or remove those links in the same commit.
4. Update `README.md`'s description of the file (in its "Methodology documents" bullet list) to match the new disposition — the current text describing all three as "unconfirmed origin... not compliant/executable" will be wrong for any file you rewrite or explicitly archive with more nuance than that blanket statement gives.

## Archival header pattern (for disposition 2)

```
> **Status: archival, not currently executable.** This methodology requires [specific resource — e.g., "a connected CRM/ARR data source and in-app telemetry"] that this environment does not have. Kept for reference if that access becomes available. The compliant subset of this methodology that *was* executed is documented in `../reports/voice-of-customer-metrics.md`. Do not attempt to execute the steps below as written without first re-checking they don't violate a data source's Terms of Service (see `README.md`'s note on this).
```

## What NOT to do

- Do not decide all three files get the same disposition without individually applying the decision rule — they have different content and may reasonably land differently (this plan expects at least one rewrite and at least one archival based on the content already summarized in `README.md`, not three identical outcomes).
- Do not attempt to actually execute a rewritten methodology's data-collection steps as part of this plan — this plan only fixes the documents themselves. Executing a rewritten methodology (e.g., actually going and reading vendor forums) belongs to Plan 3 or a future research pass, not this one.
- Do not delete `voice-of-customer-metrics.md` or change its content — it is the report these methodology docs feed, not one of the three files in scope here.

## Verification before marking this plan done

- Each of the three files has an explicit, dated disposition (visible in the file itself, not just in this plan's execution log).
- No file was deleted while still being linked from `README.md`, `feature-dictionary.md`, or any report.
- `README.md`'s description of the three files matches what they actually say now, not the old blanket "all three non-compliant" framing, unless that framing still literally applies to all three after this plan runs.

## Execution log

- 2026-09-04 — `gather-metrics-instructions.md`: **rewrite as compliant.** Read against `voice-of-customer-metrics.md`'s "what was adopted" section: the compliant parts (own forum, public changelogs) were kept and expanded slightly (added the Stack Overflow finding); the non-compliant parts (Reddit, G2, Capterra, TrustRadius scraping — all ToS violations) were removed from both the source list and the example search queries, with an explicit "removed, and why" note in each spot so a future agent doesn't silently re-add them.
- `report-building-framework.md`: **archival, pending sample size** — a variant of the archival disposition not originally anticipated by the plan's own framing. Re-reading the file found nothing ToS- or access-blocked in it at all (it's pure computation over records the now-compliant gathering pipeline produces); it's inapplicable today only because the pilot's 7-record sample doesn't clear the framework's own `N_f ≥ 5` gate. Documented that distinction explicitly in the header rather than forcing it into the "needs unavailable resources" framing that fit the other archival file.
- `research-methodology-general.md`: **archival, resource-gated** — confirmed by reading the file directly: it requires live interviews/surveys, CRM data, support-ticket systems, and in-app telemetry, none of which exist in this environment and none of which a web-research agent can compliantly substitute.
- Updated `README.md`'s methodology-documents section to describe each file's specific disposition instead of the old blanket "all three non-compliant" line.
