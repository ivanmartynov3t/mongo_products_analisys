# Voice-of-Customer Metrics — Pilot

This report operationalizes a **compliant subset** of the methodology described in [research/gather-metrics-instructions.md](../research/gather-metrics-instructions.md): gathering real, publicly-visible user feedback and mapping it to [feature-dictionary.md](../feature-dictionary.md) sub-feature IDs. It is a small pilot, not a completed metrics program — see [Scope and exclusions](#scope-and-exclusions) and [Limitations](#limitations) below.

## Navigation

- [Cumulative report index](cumulative-report.md)
- [Feature dictionary](../feature-dictionary.md)
- [Gap analysis: not on any 3T product](gap-analysis-not-on-3t-products.md)
- [Gap analysis: not on 3T Desktop](gap-analysis-not-on-3t-desktop.md)

## Scope and exclusions

The `research/` directory contains three planning documents (`gather-metrics-instructions.md`, `report-building-framework.md`, `research-methodology-general.md`) whose origin is unconfirmed — they were found in this repository, not authored in this session. This report adopts only the parts of that framework that are both **compliant** and **actually executable** with the tools available here, and explicitly drops the rest rather than simulating them:

**In scope for this pilot:**
- Studio 3T's own public community forum (`community.studio3t.com` — the successor to the `forum.studio3t.com` domain named in the original instructions, which has migrated).
- Competitor public changelogs (MongoDB Compass, DBeaver, Navicat), for future parity cross-referencing.

**Explicitly out of scope, and why:**
- **G2, Capterra, TrustRadius, Reddit** — all restrict automated scraping in their Terms of Service. This report does not fetch review/comment data from them. (This was the deciding factor behind the "compliant sources only" methodology choice made for this pilot.)
- **Stack Overflow** — checked during this pilot (see [Confirmed source availability](#confirmed-source-availability)); it returns negligible Studio-3T-specific content, so it isn't a viable source and is dropped rather than force-included.
- **CRM/Salesforce pipeline data, Zendesk/Jira support tickets, in-app telemetry, MaxDiff/Conjoint surveys, SUS/NASA-TLX benchmarking** (all described in `research/research-methodology-general.md`) — none of this data is accessible from this environment. No attempt is made to approximate or simulate it.
- **The "Public FPI" / "Composite FPI" scoring formulas** (`research/report-building-framework.md`) — not applied. This pilot reports **per-record findings only, with no aggregate ranking**. A 7-record, single-source sample cannot meet even that framework's own minimum-sample-size threshold ($N_f \ge 5$ *per feature*), so producing a ranked table from it would misrepresent a handful of forum posts as a defensible roadmap signal.
- No fabricated or illustrative quotes appear anywhere below. Every quote, date, and URL in the pilot table was retrieved live from the cited page during this pilot; anything not confirmed on the page is marked accordingly rather than inferred.

## Methodology

For each pilot record:

| Field | Definition |
| --- | --- |
| Feature ID | Closest match in feature-dictionary.md's Sub-feature registry. If no ID cleanly covers the finding, it is marked **no clean match** with the nearest existing IDs noted — never assigned an invented ID. |
| Pain severity (1–5, analyst judgment) | 1 = cosmetic; 2 = minor inconvenience; 3 = workflow drag; 4 = major impairment (forces a secondary tool/workaround); 5 = blocking issue / data loss / crash. Applied by direct reading of each thread, not a formula. |
| Workaround present | Yes/No/Partial, only where the thread itself states one. |
| Enterprise signal | Only marked present when the thread contains an explicit indicator (e.g., named production infrastructure, cluster scale, compliance terms) — never inferred from the feature's category. |
| Date | As shown on the forum post. |
| Quote | Verbatim, short, from the actual page. |

No deduplication tooling was needed at this scale — all 7 threads were manually confirmed to be distinct URLs.

## Confirmed source availability

Checked live during this pilot (2026-07-29):

| Source | Status | Notes |
| --- | --- | --- |
| `community.studio3t.com` | ✅ Reachable, indexed, individual threads fetchable | Domain migrated from `forum.studio3t.com` (named in the original instructions doc) — search/fetch retargeted accordingly. |
| Stack Overflow | ❌ Excluded | Search for `"Studio 3T"` returns only third-party comparison sites (StackShare, SaaSHub) — no Studio-3T-specific Stack Overflow threads surfaced. |
| MongoDB Compass release notes (`mongodb.com/docs/compass/release-notes/`) | ✅ Reachable | Available for future parity cross-referencing; not yet cross-referenced against the records below. |
| DBeaver releases (`github.com/dbeaver/dbeaver/releases`, via `gh api`) | ✅ Reachable | Same as above. |
| Navicat for MongoDB release notes (`navicat.com`) | ✅ Reachable | Same as above. |

## Pilot records

| # | Source | Feature ID | Match | Pain severity | Workaround | Enterprise signal | Date | Quote |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [S1](#source-index) | TRANSFER-masking-types | Approximate (closest existing ID for per-structure masking behavior) | 4 — masking silently applies only to the first object in an array, a correctness gap in a governance-relevant tool | None reported | None stated | 2025-07-29 | "When configuring ma[s]king fields within objects of an array, only those in the first object are being masked." |
| 2 | [S2](#source-index) | No clean match (closest existing: SCHED-task-types, TRANSFER-task-save) | Gap: no dictionary ID covers "trigger a saved export task from outside Studio 3T with runtime parameters" | 3 — forces an external script for a recurring, high-volume use case | Partial — user has a separate workaround for aggregations (extracting query code into Node.js), but none for export tasks specifically | Scale signal only (2,000+ monthly export files) — not an explicit enterprise keyword | 2022-05-04 | "Is it possible to pass an 'Export source' and 'Export target' as parameters to an Export task?" — 3T staff confirmed: "there's no way to run them from outside applications." |
| 3 | [S3](#source-index) | SHELL-engine | Direct | 4 — core shell feature non-functional out of the box in Community Edition | Yes, but introduces a secondary UI regression (missing edit/view/delete buttons, broken table formatting) when applied | None (explicitly Community Edition) | 2025-07-24 | "The shell executable cannot be run due to the following reason: Could not get status from the shell process." |
| 4 | [S4](#source-index) | CONN-ssh | Direct | 4 — all non-authenticated stored connections broke after a product update; only a full reinstall (not a restart) fixed it | Yes (full reinstall) | None stated | 2025-01-21 | "After Studio update to Studio 3T 2025.1 i cannot connect to any stored connection that does not use authentication." |
| 5 | [S5](#source-index) | CONN-proxy | Direct | 3 — GUI honors proxy settings but IntelliShell does not, splitting behavior within one product | None stated (user proposes 3T adopt mongosh's native env-var proxy support) | None stated | 2025-09-06 | "IntelliShell doesn't properly use the proxy settings (and so errors when attempting to connect)" |
| 6 | [S6](#source-index) | No clean match (closest existing analog: AGG-pipeline-opts' `allowDiskUse`, which is aggregation-scoped, not find/sort-scoped) | Gap: no F-QUERY ID for a find/sort-level disk-use setting | 3 — resolved once the non-default setting was found, but the failure mode itself is confusing given a documented 100MB in-memory MongoDB limit | Yes — enabling "Allow disk use" in Find Query Options resolved it | Explicit — "software runs on multiple Kubernetes clusters with dozens of nodes and ~5TB total memory allocation" | 2022-09-07 | ""Query Failed" error when trying to sort" a 1.3M-document collection; resolved and confirmed sorting "in just a few seconds" after enabling the setting. |
| 7 | [S7](#source-index) | CONN-cred-storage | Approximate (closest existing ID; actual defect is connection-profile persistence, not encryption specifically) | 5 — total loss of 20+ saved connections with no vendor explanation | None — user was redirected to official support rather than given a fix in-thread | None stated | 2022-06-30 | "Today I opened Studio 3T and all my 20+ connections are gone. Any way to get them back?" |

### Source index

- S1: https://community.studio3t.com/t/how-to-configure-masking-within-nested-arrays/2303
- S2: https://community.studio3t.com/t/is-it-possible-to-pass-an-export-source-and-export-target-as-parameters-to-an-export-task/133
- S3: https://community.studio3t.com/t/error-unable-to-open-shell-in-community-version/2292
- S4: https://community.studio3t.com/t/cannot-connect-to-ssh-for-connections-without-authorization/2042
- S5: https://community.studio3t.com/t/feature-problem-with-proxy-options-and-suggestion-to-fix/2338
- S6: https://community.studio3t.com/t/query-failed-error-when-trying-to-sort-big-collections/236
- S7: https://community.studio3t.com/t/data-loss-connections-wiped-out-am-i-missing-something/183

## Findings from this pilot

- 5 of 7 records mapped cleanly to an existing dictionary ID; 2 did not (records #2 and #6) and are flagged as candidate gaps in the dictionary itself, not forced into an unrelated ID.
- 1 record (#7) reflects a real, apparently-unresolved data-loss-adjacent defect (all saved connections disappearing) with no vendor explanation visible in the thread — worth a human follow-up regardless of what a larger pilot would show.
- Enterprise-signal keywords, when they appeared at all, were incidental (Kubernetes cluster scale in #6) rather than the norm — consistent with a small, non-representative sample rather than a finding about enterprise prevalence.

## Limitations

- **Sample size**: 7 records from one source. Not statistically meaningful and not a substitute for the full triangulated methodology described in `research/research-methodology-general.md` (which this pilot cannot execute — see Scope and exclusions).
- **No competitor-parity cross-check performed yet.** The three competitor changelog sources were confirmed reachable (see table above) but have not been read against these 7 records in this pass.
- **No aggregate scoring.** By design — see Scope and exclusions.
- **Single-pull snapshot** (2026-07-29). Forum content changes over time; no recurring collection process exists yet.
- **Provenance of the underlying `research/*.md` planning docs remains unconfirmed** — this report does not edit or validate those files, only borrows their compliant, executable parts.

## Next steps (not yet done)

- If this pilot's approach is approved, scale the forum pull to a larger, systematic sample (e.g., N threads per feature area) before any aggregate scoring is attempted.
- Cross-reference the two unmapped records (#2, #6) against `feature-dictionary.md` maintainers to decide whether they warrant new sub-feature IDs.
- Read the three competitor changelogs against the mapped records to populate a real (not templated) parity column.

## Changelog

- **2026-07-29**: Pilot created — 7 real records from `community.studio3t.com`, methodology and scope-exclusions documented, competitor-changelog source availability confirmed but not yet cross-referenced.
