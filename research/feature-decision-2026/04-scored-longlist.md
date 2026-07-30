# Stage 2 — Scored Long-List

## Navigation

- [← Candidate long-list](03-candidate-longlist.md)
- [← Research plan (rubric definitions)](01-research-plan.md)
- [Next stage: shortlist deep-dive →](05-shortlist-deepdive.md)

## Ranked summary

Priority Score = (Evidence Strength + Reach + Severity + Competitive Urgency) / Build Effort. Effort-ceiling rule: Build Effort 4-5 stays visible but is cut from the shortlist with a reason (never silently dropped).

**Note:** Candidate 1's score below is the Stage 6 corrected value (5.67, not the original 5.00) — see its card for the correction. Table order reflects original Stage 2 ranking to keep Stage 3/4's "top 5" selection traceable; see [Stage 6 summary](#stage-6-re-ranking-after-fact-verification) for the corrected overall order.

| Rank (orig.) | # | Candidate | Evidence | Reach | Severity | Urgency | Effort | Priority Score | Shortlist? |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 4 | Headless CLI / CI-CD pipeline automation | 4 | 4 | 3 | 3 | 2 | **7.00** | ✅ |
| 1 | 18 | Slack/Teams/Jira/PagerDuty webhook notifications | 4 | 4 | 3 | 3 | 2 | **7.00** | ✅ |
| 3 | 19 | Automated PII classification/discovery | 4 | 4 | 3 | 2 | 2 | **6.50** | ✅ |
| 4 | 1 | AI-driven query/index performance advisor | ~~4~~ | 5 | 4 | ~~2~~→4 | 3 | ~~5.00~~ → **5.67** | ✅ |
| 4 | 9 | Queryable Encryption / CSFLE key-vault UI | 5 | 3 | 4 | 3 | 3 | **5.00** | ✅ |
| 6 | 16 | Deeper Vector Search tooling | 4 | 3 | 3 | 4 | 3 | 4.67 | cut — rank 6, only 5 slots (see funnel note) |
| 7 | 3 | Native Git/version-control integration | 3 | 4 | 3 | 3 | 3 | 4.33 | cut — rank 7 |
| 8 | 11 | Visual ERD/JSON-Schema editor (F-SCHEMA cluster) | 5 | 4 | 3 | 4 | 4 | 4.00 | **cut — effort exceeds ceiling at full scope; carried to Stage 5 for explicit discussion (see note)** |
| 8 | 17 | Enterprise AI gateway/SSO for AI Helper | 4 | 3 | 3 | 2 | 3 | 4.00 | cut — rank 8 |
| 10 | 20 | Schema drift detection / versioned field history | 3 | 3 | 3 | 2 | 3 | 3.67 | cut |
| 11 | 6 | Centralized SIEM/audit-log export | 3 | 2 | 3 | 2 | 3 | 3.33 | cut |
| 11 | 12 | AI schema anti-pattern/health advisor | 2 | 3 | 3 | 2 | 3 | 3.33 | cut |
| 13 | 10 | Native BI/dashboard builder | 3 | 4 | 2 | 3 | 4 | 3.00 | cut — effort exceeds ceiling |
| 14 | 5 | Secrets vault integration | 3 | 3 | 3 | 2 | 4 | 2.75 | cut — effort exceeds ceiling |
| 15 | 15 | VS Code/JetBrains companion extension | 2 | 3 | 2 | 3 | 4 | 2.50 | cut — effort exceeds ceiling |
| 16 | 2 | IntelliShell interactive debugger | 3 | 2 | 2 | 2 | 4 | 2.25 | cut — effort exceeds ceiling |
| 17 | 13 | Synthetic/constrained test-data generator | 2 | 2 | 2 | 1 | 3 | 2.33 | cut |
| 18 | 14 | Federated cross-database querying | 2 | 3 | 3 | 2 | 5 | 2.00 | cut — effort exceeds ceiling |
| 19 | 7 | JIT access + dynamic query-layer masking | 2 | 2 | 3 | 2 | 5 | 1.80 | cut — effort exceeds ceiling |
| 20 | 8 | Desktop app-level SSO/IdP federation | 2 | 2 | 2 | 1 | 5 | 1.40 | cut — effort exceeds ceiling, architectural mismatch |

**Funnel decision (as originally made, before Stage 6 correction):** the top 5 within the effort ceiling (Candidates 4, 18, 19, 1, 9) went to Stage 3. Candidate 11 was cut from the numeric shortlist (effort exceeds ceiling at full 13-ID scope) but carried forward as a named discussion point in Stage 5, because it is the single most rigorously-confirmed finding in this entire repository (portfolio-wide, Tier A confirmed-absent) and deserves an explicit argued tradeoff against the "widen the lead" objective rather than a silent drop. Candidate 1's Stage 6 score correction (5.00→5.67) does not change which 5 candidates were shortlisted — it was already in the top 5 before the correction, just for a partly wrong reason (see its card).

### Stage 6 re-ranking after fact-verification

| Rank | Candidate | Score | Note |
|---|---|---|---|
| 1 | 4 — Headless CLI/CI-CD automation | 7.00 (7.50 after Stage 3/4 deep-dive, see [05](05-shortlist-deepdive.md)/[06](06-verification-notes.md)) | |
| 2 | 18 — Webhook notifications | 7.00 | |
| 3 | 19 — PII classification/discovery | 6.50 (7.00 after Stage 3, corrected back to 6.50 in Stage 4 — see [06](06-verification-notes.md)) | recommended |
| 4 | 1 — AI query/index advisor | **5.67** (corrected in Stage 6, was 5.00) | now understood as a gap-closer, not a lead-widener |
| 5 | 9 — QE/CSFLE key-vault UI | 5.00 | |

## Full Research Result Cards

### Candidate 1: AI-driven query/index performance advisor — **corrected in Stage 6 fact-verification, score revised up**
- Feature area: F-IDX (`IDX-perf-insights`)
- Description: An assistant that runs `explain()`/profiler analysis in the background, detects slow queries and index misconfiguration (e.g. reversed ESR ordering, missing compound indexes), and proposes concrete index changes — closing the loop that today requires manually reading raw explain output and applying the Equality-Sort-Range rule by hand.
- Segment fit: both
- Sources: (B) `studio-3t-review-mining`, `nosqlbooster-competitive-analysis`, `nosqlbooster-competitive-intelligence-analysis`, `mongodb-ai-automation-opportunities`, `mongodb-evolution-and-roadmap`; **(A) `reports/comparisons/low-level-feature-comparison.md`, `IDX-perf-insights` row — ✅ confirmed for both MongoDB Compass and VisuaLeaf**, sourced to [Compass's own feature-matrix.md](../../products/third-party/mongodb-compass/features/indexing-performance/feature-matrix.md) ("System suggests modeling/indexing improvements for problematic patterns... Advisory, not auto-remediation") and VisuaLeaf's own feature-matrix.md ("4 recommendation types: Missing Index/Compound Index/Covered Query/Unused Index")
- **⚠️ Stage 6 correction:** the original card (Stages 1-4) claimed "no GUI competitor has shipped a named equivalent" based on an external web search for the literal phrase "index advisor"/"query optimizer." That search missed that this repo's own, independently cross-checked structured comparison (Tier A) already confirms **both MongoDB Compass and VisuaLeaf** have this capability under the dictionary ID `IDX-perf-insights` — the external search used the wrong terminology and, more importantly, should never have been the first check; this repo's own data should have been consulted before an external search. This is disclosed as a real miss, not quietly fixed.
- Evidence Strength: **4** — 5 B-tier sources independently converge on this theme (though 2 are near-duplicate NoSQLBooster passes), now additionally grounded by the Tier A comparison confirming the capability is real and already shipped by 2 competitors; no direct Tier C customer quote specifically requesting it for Studio 3T, so short of 5.
- Reach: **5** — relevant to virtually every persona (backend devs, DBAs, data engineers) and both target segments; performance is a universal concern. *(unchanged)*
- Severity: **4** — `mongodb-developer-workflow-automation` quantifies manual query tuning at 3-6 hours/week; this is a real, recurring cost, not cosmetic. *(unchanged)*
- Competitive Urgency: **2 → 4** — corrected. Both products this repo tracks as third-party competitors (MongoDB Compass, VisuaLeaf) are Tier-A-confirmed to already have this. Per the rubric, 2-of-2 tracked competitors having it is "most direct competitors have it; established market expectation," not "no competitor has it."
- Build Effort: **3** — fits the ceiling if scoped as "v1: rule-based index recommendations from data already collected by the existing Explain Plan / Query Profiler infrastructure" rather than a full autonomous closed-loop agent. *(unchanged)*
- **Revised Priority Score: (4+5+4+4)/3 = 17/3 = 5.67** (up from 5.00)
- **Reframing:** this is no longer a "widen the lead / first-mover" candidate — it is a **confirmed 2-competitor capability gap**, the same shape as Candidates 4, 9, and 11. It scores well on its own merits (highest Reach of any candidate, quantified severity, now-confirmed urgency), but does not fit the user's stated primary objective for *this* decision any better than the others in that category.

### Candidate 18: Slack/Teams/Jira/PagerDuty webhook notifications
- Feature area: F-SCHED/F-GOV — proven concept elsewhere in the 3T family (`GOV-003`, built into 3T Lens)
- Description: Add webhook-based notification channels (Slack, Teams, Jira, PagerDuty) to the existing Task Scheduler, alongside its current email/in-app notifications, so task success/failure/warning alerts land where teams already work.
- Segment fit: both
- Sources: (A) `gap-analysis-not-on-3t-desktop.md` — `GOV-003` confirmed built in 3T Lens, absent on Desktop; (B) `studio-3t-missing-integrations`
- Evidence Strength: **4** — proven, working precedent inside the 3T product family itself (not a hypothetical), plus an independent research recommendation specifically for Desktop.
- Reach: **4** — anyone using Task Scheduler benefits; both enterprise ops teams and smaller Slack-based teams.
- Severity: **3** — today's email/in-app-only notification model is a workflow drag (requires actively checking email/app instead of getting alerted where the team already communicates); not blocking.
- Competitive Urgency: **3** — standard expectation across modern devtools generally, though not MongoDB-GUI-specific competitive pressure.
- Build Effort: **2** — additive to the existing `SCHED-notifications`/`SCHED-email` infrastructure; "just" adds webhook config + payload templates to an already-built notification pipeline.
- Priority Score: (4+4+3+3)/2 = **7.00**

### Candidate 19: Automated PII classification/discovery
- Feature area: F-GOV — proven concept elsewhere in the 3T family, **twice** (`GOV-004` via 3T Lens, `AI-011` PII scanner via 3T MCP)
- Description: Automated scanning of collections to flag fields likely to contain PII (names, emails, SSNs, etc.) with sensitivity grouping — a discovery/audit step that today must be done manually before a user can even configure Studio 3T's existing data-masking tool correctly.
- Segment fit: both (enterprise/regulated primary, but GDPR/CCPA-conscious scaled startups too)
- Sources: (A) `gap-analysis-not-on-3t-desktop.md` — `GOV-004` (3T Lens) and `AI-011` (3T MCP) both confirmed elsewhere in the family, neither on Desktop
- Evidence Strength: **4** — proven twice independently in-house (different products, different teams' implementations); no external Tier B/C corroboration of Desktop-specific demand, so short of 5.
- Reach: **4** — compliance-relevant across enterprise and scaled-startup segments alike; also directly strengthens the existing masking tool's usability for every persona that uses it.
- Severity: **3** — workflow drag: users must manually inspect schemas to identify sensitive fields today before masking anything.
- Competitive Urgency: **2** — not confirmed whether DBeaver/DataGrip/Navicat have an equivalent; no strong evidence either way.
- Build Effort: **2** — the underlying scanning heuristic already exists twice in the product family; this is substantially a port/adapt job, not new invention. Likely the single lowest-effort candidate in the set.
- Priority Score: (4+4+3+2)/2 = **6.50**

### Candidate 4: Headless CLI / CI-CD pipeline automation
- Feature area: F-SCHED/F-TRANSFER/F-GOV — NEW
- Description: A CLI/API surface that lets external systems (GitHub Actions, GitLab CI, Jenkins) trigger existing Task Scheduler jobs, masking runs, and Data Compare operations with runtime parameters — turning Studio 3T's already-built automation engine into something that can be invoked from outside the desktop app.
- Segment fit: both — enterprise CI/CD-governed pipelines and startups running everything through GitHub Actions alike
- Sources: (B) `studio-3t-missing-integrations`; **(C) VoC pilot record #2** — a real user asked exactly this ("pass an 'Export source' and 'Export target' as parameters to an Export task?"), and 3T's own staff confirmed in-thread "there's no way to run them from outside applications."
- Evidence Strength: **4** — direct customer ask *plus* an explicit vendor-side confirmation of the gap is unusually definitive for a single Tier C record, combined with an independent Tier B recommendation.
- Reach: **4** — strong fit for both target segments (enterprise compliance pipelines, startup CI/CD-heavy workflows); not universal across every persona (e.g., less relevant to a student learning MongoDB).
- Severity: **3** — the VoC record itself was rated severity 3 in the original pilot ("forces an external script for a recurring, high-volume use case ... 2,000+ monthly export files").
- Competitive Urgency: **3** — DBeaver Enterprise has partial CLI/scripted-task capability (confirmed directly via primary source in Stage 3 — see below); this is also a well-documented DevOps-integration industry trend. *(Correction: the original Stage 2 pass also named Navicat here without a source — checked `navicat-competitive-intelligence-analysis` directly during this review and found no mention of a CLI/scripted-task-trigger capability; that reference is removed as unsupported rather than left standing.)*
- Build Effort: **2** — this is fundamentally an API/CLI wrapper around Task Scheduler, masking, and Data Compare logic that **already exists and already works** — the new work is an invocation surface and an auth/token model, not new core logic.
- Priority Score: (4+4+3+3)/2 = **7.00**

### Candidate 9: Queryable Encryption (QE)/CSFLE key-vault configuration UI
- Feature area: F-CONN (`CONN-in-use-enc`, unverified)
- Description: A configuration UI for setting up client-side field-level encryption — choosing a KMS provider (AWS/Azure/GCP/local), defining which fields are encrypted, and managing key rotation — targeting MongoDB's Queryable Encryption (the actively-recommended successor to CSFLE).
- Segment fit: enterprise/regulated (compliance-driven: banking, healthcare, defense per `mongodb-evolution-and-roadmap`)
- Sources: (A) `feature-dictionary.md` `CONN-in-use-enc` (unverified); (B) `mongodb-evolution-and-roadmap`, `mongodb-gui-technology-trends`; confirmed via `reports/cumulative-report.md` that Compass is exclusively the only product in this analysis offering this; (D) fresh 2026 search confirming Compass's continued QE/CSFLE support and that QE (not CSFLE) is MongoDB's own recommended forward path
- Evidence Strength: **5** — broad convergence: dictionary tracking + 2 independent research files + a directly-confirmed competitor-exclusive claim + fresh-search verification all agree.
- Reach: **3** — strongly fits the primary (enterprise/regulated) segment; weaker fit for typical individual devs or early-stage startups, though regulated-industry startups (fintech/healthtech) would care.
- Severity: **4** — for regulated industries this can be a hard compliance requirement; today it can force a team to keep Compass installed specifically for QE-related workflows even if they use Studio 3T for everything else — a genuine "forced to a secondary tool" scenario, not hypothetical (Compass's exclusivity here is Tier-A confirmed).
- Competitive Urgency: **3** — exactly 1 competitor (Compass) has it today, but it's MongoDB's own strategic direction built into the server and its own GUI — a stronger signal than an isolated competitor feature.
- Build Effort: **3** — MongoDB's drivers already provide the client-side encryption libraries; Studio 3T's job is a configuration/management UI on top of existing driver capability (similar shape to how Compass itself did it), not building cryptography from scratch.
- Priority Score: (5+3+4+3)/3 = **5.00**

### Candidate 16: Deeper Vector Search tooling
- Feature area: F-IDX (`IDX-vector-search`, unverified)
- Description: A dedicated Vector Search index creation wizard, kNN/similarity query builder, and a recall-vs-RAM profiler for hybrid vector+scalar+text queries.
- Segment fit: both — AI/RAG-building startups and enterprise AI initiatives alike
- Sources: **(A) `reports/comparisons/low-level-feature-comparison.md`, `IDX-vector-search` row** — ✅ confirmed for Compass only ("Confirmed — same Atlas/local constraints"), sourced to [Compass's feature-matrix.md](../../products/third-party/mongodb-compass/features/indexing-performance/feature-matrix.md); also independently corroborated in `reports/cumulative-report.md`'s "Compass is the only product that provides... Atlas Search and Vector Search index creation"; (B) `datagrip-competitive-analysis`, `mongodb-evolution-and-roadmap`, `mongodb-gui-technology-trends`
- Evidence Strength: **4** — 3+ independent sources converge, including a direct Tier A confirmation.
- Reach: **3** — strong for the growing AI/RAG-building segment specifically across both target segments; not universal (traditional CRUD-app developers/DBAs less affected).
- Severity: **3** — real workflow drag for teams building vector-search features, who today fall back to raw shell/Atlas UI.
- Competitive Urgency: **4** — Compass already has Vector Search index creation (Tier A confirmed, citation corrected above — the original card mis-cited this to `feature-dictionary.md`, which only defines the ID and doesn't itself say who has it; the actual confirming source is the low-level comparison table plus `cumulative-report.md`), and `mongodb-gui-technology-trends` frames this as an accelerating 2025-2030 trend.
- Build Effort: **3** — MongoDB already provides the Vector Search index type/operators; this is a UI layer on existing server/driver capability, similar in shape to Candidate 9.
- Priority Score: (4+3+3+4)/3 = **4.67**
- **Not carried to Stage 3** — ranked 6th, outside the 5-candidate funnel; noted here as the strongest "just missed the cut" candidate given its otherwise solid profile.

### Candidate 3: Native Git/version-control integration
- Feature area: F-QUERY/F-AGG/F-SCHED — NEW, partially overlaps `mongodb-developer-workflow-automation`'s "declarative migration frameworks" theme
- Description: Version-controlled storage for saved queries, aggregation pipelines, and scheduler configs, with a commit/diff workflow — extending the git-backed-folder concept Studio 3T already shipped for connections.
- Segment fit: both
- Sources: (B) `studio-3t-missing-integrations`, `mongodb-developer-workflow-automation`; (D) **Studio 3T 2026.4 changelog** — confirmed partial prior art: "local file support... including Git-backed folders" for connections; (D) **verified via JetBrains' own DataGrip documentation** ([Version control integration support](https://www.jetbrains.com/help/datagrip/enabling-version-control.html), [Databases in the Version Control System](https://www.jetbrains.com/help/datagrip/databases-in-the-version-control-system.html)) — Git is a bundled, enabled-by-default plugin in DataGrip, with a dedicated feature for tracking database objects in VCS
- Evidence Strength: **3** — 2 independent B sources agree, but the Tier D finding of partial existing prior art introduces real status uncertainty (does 2026.4's Git-backed-folder support already cover more than connections? unverified — flagged explicitly for Stage 3).
- Reach: **4** — broad: devs, data engineers, DBAs, and consultants managing change-controlled environments; enterprise compliance also wants change history.
- Severity: **3** — workflow drag/audit gap for change-management-conscious teams; workaround today is manually copying query/pipeline text into an external repo.
- Competitive Urgency: **3** — confirmed via direct fetch of JetBrains' own documentation: DataGrip bundles Git integration by default, plus a dedicated "databases in VCS" feature — a real competitive point since a DataGrip user gets this "for free" via the platform, while Studio 3T's saved artifacts live in an app-local store without native VCS hooks. (This claim was unsourced background assertion in the original Stage 2 pass — now backed by a direct primary-source citation.)
- Build Effort: **3** — the 2026.4 prior art (Git-backed folders for connections) suggests the underlying mechanism is already partially built, making extension to queries/pipelines more tractable than starting from zero; a full in-app diff/PR workflow would push this higher, so scope is important.
- Priority Score: (3+4+3+3)/3 = **4.33**
- **Not carried to Stage 3** — ranked 7th; the prior-art uncertainty (does 2026.4 already partially satisfy this?) would need resolving before this could be prioritized further anyway.

### Candidate 11: Visual ERD/JSON-Schema editor/validation-rule authoring UI (the F-SCHEMA cluster)
- Feature area: F-SCHEMA — the 13 IDs confirmed absent across the **entire** 3T portfolio
- Description: A visual entity-relationship diagram designer (infinite canvas, auto-detected relationships), a tree-based JSON Schema editor with full BSON type/constraint support, and a validation-rule authoring/deployment workflow ($jsonSchema, strictness levels, verification against live data).
- Segment fit: both
- Sources: **(A) `gap-analysis-not-on-3t-products.md`/`gap-analysis-not-on-3t-desktop.md`** — the single confirmed-absent finding across the *whole* 3T product family, no exceptions; (B) `navicat-competitive-intelligence-analysis`, `mongodb-gui-competitor-landscape-analysis`
- Evidence Strength: **5** — this is the highest-confidence Tier A finding in this entire research effort, corroborated by 2 independent competitor research passes, and the feature area is a confirmed, named strength of **two** different competitors (Compass has validation UI, VisuaLeaf has the full ERD/JSON-Schema-editor cluster).
- Reach: **4** — schema design/validation is broadly relevant across backend devs, data engineers, DBAs, and consultants.
- Severity: **3** — real competitive exposure (this is literally the one thing the whole 3T portfolio can't do that direct competitors can), but not blocking for existing Studio 3T users, who have workarounds (hand-written `$jsonSchema`, or switching to Compass/VisuaLeaf for that specific task).
- Competitive Urgency: **4** — an established market expectation among 2 direct competitors.
- Build Effort: **4** — 13 distinct sub-feature IDs (canvas, auto-diagramming, relationship detection, layouts, portability, plus the separate validation-authoring sub-cluster) is a large surface area; even a narrowed "just the JSON-Schema editor + validation authoring" v1 slice is substantial, and evaluating the cluster *as a whole* (as the gap-analysis frames it) puts this at Large, exceeding the medium ceiling.
- Priority Score: (5+4+3+4)/4 = **4.00**
- **Cut from the numeric shortlist** (effort exceeds ceiling at full scope) **but explicitly carried to Stage 5** for discussion — see the rank-order note above. This is the one candidate where the numeric cut and the repo's own editorial emphasis (two dedicated gap-analysis reports built around exactly this finding) are in tension, and that tension deserves to be argued in the final memo rather than silently resolved by the formula.

### Candidate 17: Enterprise AI gateway/SSO for AI Helper
- Feature area: F-AI — NEW
- Description: Let Studio 3T's AI Helper point at a centrally-managed, org-controlled key source/gateway instead of requiring every individual user to obtain and paste their own external LLM API key.
- Segment fit: enterprise/regulated primary, moderate fit for scaled startups running centralized dev tooling
- Sources: **(A) Studio 3T's own `product-report.md`**, "Strategic risks/gaps": *"AI Helper requires external API keys (Azure/OpenAI/Anthropic) — no bundled LLM; incurs per-token cost and requires user-managed key security."*; (B) `studio-3t-missing-integrations` (enterprise AI gateway/SSO recommendation)
- Evidence Strength: **4** — Studio 3T's own documented self-assessed weakness, independently corroborated by outside research.
- Reach: **3** — strong for the primary segment (centralized AI governance/cost control matters to enterprise IT), moderate for the secondary segment.
- Severity: **3** — today every user manages their own key and cost; for enterprise rollouts at scale this is real procurement/security friction (inconsistent key management, shadow-IT risk).
- Competitive Urgency: **2** — per `research/google_research/overview.md`'s summary of `dbeaver-competitive-intelligence-analysis`: "AI Assistant sends prompts and schema/data to external LLMs without governed masking" — suggesting competitors share this weakness rather than having solved it, which argues for reading this as a "widen the lead" opportunity rather than a "catch up" one. (Unlike Candidate 1, this comparison has not been independently cross-checked against this repo's own Tier A structured data, since DBeaver is not one of the two products tracked in `feature-dictionary.md`'s formal comparison — treat this urgency score as resting on Tier B research only, one tier lower in rigor than Candidate 1's corrected assessment.)
- Build Effort: **3** — scoped modestly (Desktop gains the *ability* to point at a centrally configured/rotated key source, rather than Studio 3T building the gateway/governance service itself, which conceptually overlaps with what 3T Access already does), this fits the ceiling.
- Priority Score: (4+3+3+2)/3 = **4.00**
- **Not carried to Stage 3** — tied for rank 8, outside the 5-candidate funnel.

### Candidate 20: Schema drift detection / versioned field history
- Feature area: F-SCHEMA/F-GOV — proven concept elsewhere in the 3T family (`GOV-005` via 3T Lens)
- Description: Snapshot schema analysis results over time and diff them, surfacing schema drift (new/removed/type-changed fields) before it causes production surprises.
- Segment fit: both
- Sources: (A) `gap-analysis-not-on-3t-desktop.md` — `GOV-005` confirmed in 3T Lens, absent on Desktop
- Evidence Strength: **3** — proven once elsewhere in-house, no independent Tier B/C corroboration specifically for Desktop.
- Reach: **3** — relevant to backend devs, data engineers, and DBAs; less central for pure query-writing use cases.
- Severity: **3** — schema drift causing production surprises is a documented pain point in `mongodb-developer-workflow-automation`'s broader schema-governance framing.
- Competitive Urgency: **2** — no named GUI competitor confirmed to have this specific capability.
- Build Effort: **3** — builds on existing `SCHEMA-sampling`/`SCHEMA-field-prob` infrastructure Studio 3T already has; the new work is the snapshot/versioning/diff layer.
- Priority Score: (3+3+3+2)/3 = **3.67**

### Candidate 6: Centralized SIEM/audit-log export — **expanded in Stage 6**
- Feature area: F-GOV — NEW (distinct from 3T Lens's own separate, already-built-elsewhere audit trail)
- Description: Native, configurable audit-log streaming from Studio 3T Desktop directly to enterprise SIEM platforms (Splunk, Datadog, Grafana) via webhooks or standard log drivers, instead of requiring administrators to build custom log-scraping pipelines.
- Segment fit: enterprise/regulated — this is a narrow, compliance-specific need with little relevance to smaller startups.
- Sources: (B) `studio-3t-enterprise-gap-analysis`: *"Studio 3T lacks native, configurable audit log streaming adapters within its desktop application, requiring platform administrators to build custom log-scraping pipelines or rely on third-party log collectors to capture application telemetry."*
- The argument for it: Security Operations Centers standardize on centralized SIEM tooling, and the source material frames this as a structural, not cosmetic, gap for "medium and large organizations seeking enterprise-wide database governance... and SIEM compliance auditing." It would directly strengthen Studio 3T's existing enterprise-auth/governance positioning.
- The argument against it: this reads as a narrow, single-segment ask (SOC-level compliance tooling is not something most individual devs or smaller startups will ever configure), and no VoC or community evidence corroborates active customer demand for it specifically — the case rests entirely on one research file's structural framing.
- Evidence Strength: **3** — one detailed, specific B-tier source; no independent corroboration or direct customer evidence.
- Reach: **2** — enterprise/regulated only; poor fit for the "also serve medium-large startups" requirement, which weighs directly against this candidate given the stated segment criteria.
- Severity: **3** — a real compliance/audit gap for the segment it affects, per the source's own framing ("Studio 3T lacks native... adapters"), but not a blocking issue for day-to-day product use.
- Competitive Urgency: **2** — no specific MongoDB GUI competitor is named in any source as already having this; the source frames it as a general enterprise-database-platform expectation, not a named competitor's shipped feature.
- Build Effort: **3** — scoped as "structured audit events + one or two standard export formats," this is additive to whatever audit logging Studio 3T already has, not a from-scratch subsystem; a deeper native integration with each named SIEM vendor would cost more.
- Priority Score: (3+2+3+2)/3 = **3.33**
- **Cut** — weak Reach (fails the dual-segment requirement) is the deciding factor, not effort.

### Candidate 12: AI-driven schema anti-pattern/health advisor — **expanded in Stage 6**
- Feature area: F-SCHEMA/F-AI — NEW, distinct from Candidate 11 (this is runtime diagnostics on data already in the database, not a design/validation-authoring UI)
- Description: Background analysis of live collections (via `collStats`, sampling, and schema inspection) that flags known anti-patterns — unbounded arrays, excessive `$lookup` chaining, bloated documents approaching the 16MB limit — with concrete remediation suggestions (e.g., the Subset Pattern or referenced relationships).
- Segment fit: both — this is a general MongoDB data-modeling health concern, not segment-specific.
- Sources: (B) `mongodb-ai-automation-opportunities`: *"By invoking database inspection commands—such as `collection-schema`, `collection-storage-size`, and `db-stats`—an AI agent systematically scans collections for known schema anti-patterns... if an agent detects an array field growing proportionally with document updates, it flags an unbounded array pattern and recommends restructuring the model using referenced relationships or the Subset Pattern."*
- The argument for it: real, quantifiable production risk (16MB document limit, WiredTiger cache thrashing per the source), and genuine synergy with Candidate 1 — both could share the same underlying "background analysis engine" reading schema/profiler data, making a combined "AI Performance & Schema Health Advisor" a plausible, larger-scoped v2 if both are pursued.
- The argument against it: only one research source discusses this specific capability (no independent corroboration, no VoC/community evidence, and no competitor is named as having it, positive or negative), so this rests on thinner ground than most of the shortlist.
- Evidence Strength: **2** — single source, no independent corroboration.
- Reach: **3** — relevant to any team with a growing MongoDB deployment; less acute for small/early-stage collections.
- Severity: **3** — the source frames unaddressed anti-patterns as causing "severe performance degradation in production," a real (if gradual) risk.
- Competitive Urgency: **2** — no named competitor confirmed to have this specific capability in any source consulted.
- Build Effort: **3** — could reuse Studio 3T's existing `SCHEMA-sampling`/`SCHEMA-field-prob` infrastructure for the inspection step, similar in shape to Candidate 1's reuse of Explain/Profiler data.
- Priority Score: (2+3+3+2)/3 = **3.33**
- **Cut** — Evidence Strength is the weakest link; worth revisiting bundled with Candidate 1 in a future decision, not as a standalone pick now.

### Candidate 10: Native BI/dashboard builder — **expanded in Stage 6**
- Feature area: F-QUERY (`QUERY-charts-dashboards`)
- Description: Chart-building and dashboard-composition tooling directly on collection/query/pipeline data (bar, line, pie, heatmap, pivot tables, etc.), styled after Navicat's built-in BI workspace, so users don't need to export to an external BI tool for basic visualization.
- Segment fit: both.
- Sources: **(A) `reports/comparisons/low-level-feature-comparison.md`, `QUERY-charts-dashboards` row** — ✅ confirmed for VisuaLeaf only (Compass and Studio 3T both ❓/unconfirmed), sourced to [VisuaLeaf's feature-matrix.md](../../products/third-party/visual-eaf/features/querying/feature-matrix.md); (B) `navicat-competitive-intelligence-analysis`: *"Navicat includes a built-in BI workspace that transforms stored database records into visual charts and interactive dashboards... The workspace supports over 10 visualization types, including Bar, Line, Area, Combination, Pie, Donut, Scatter, Heatmap, Treemap, KPI cards, and Pivot Tables."*
- The argument for it: two real products (one Tier-A-confirmed — VisuaLeaf — one Tier-B-documented — Navicat) already do this well, and it removes a genuine "export to Excel/Tableau" workaround step for users who just want a quick visual.
- The argument against it: Studio 3T already supports exporting to Excel/CSV (`TRANSFER-export-excel`/`TRANSFER-export-csv`, both already implemented), so the workaround is not costly — no VoC or community evidence suggests this is an active pain point, and "over 10 visualization types" plus "interconnected dashboards" (per the Navicat source) implies a substantial UI surface to match, not a small add-on.
- Evidence Strength: **3** — one Tier A confirmation (VisuaLeaf) plus one detailed Tier B source (Navicat); no direct customer-voice corroboration.
- Reach: **4** — dashboards/charts have broad appeal across almost every persona.
- Severity: **2** — a real but low-severity gap; the existing export-to-external-BI-tool workaround is not costly (Studio 3T already has confirmed CSV/Excel export).
- Competitive Urgency: **3** — 2 competitors (1 Tier A-confirmed, 1 Tier B-documented) have this.
- Build Effort: **4** — matching "10+ visualization types" and "interconnected dashboards" (per the Navicat source) is a substantial, standalone UI subsystem — this exceeds the medium ceiling as scoped by the competitive bar itself.
- Priority Score: (3+4+2+3)/4 = **3.00**
- **Cut — effort exceeds ceiling.**

### Candidate 5: Secrets vault integration — **expanded in Stage 6**
- Feature area: F-CONN/F-GOV — NEW
- Description: Native connectors to enterprise secret managers (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault) so Studio 3T retrieves short-lived, dynamically-rotated database credentials at connection time instead of storing static credentials locally.
- Segment fit: enterprise/regulated primarily; weak fit for typical startups, which rarely run their own Vault/Secrets Manager infrastructure at smaller scale.
- Sources: (B) `studio-3t-enterprise-gap-analysis`: *"Studio 3T lacks native secret manager integrations (such as HashiCorp Vault, AWS Secrets Manager, or CyberArk) to retrieve dynamic, short-lived database credentials automatically upon connection startup."*; `studio-3t-missing-integrations`: *"Modern infrastructure patterns rely on dynamic secret engines—such as HashiCorp Vault, AWS Secrets Manager, and Azure Key Vault—to generate short-lived credentials, manage dynamic database leases, and rotate client certificates programmatically."*; (D) fresh 2026 search confirming the secrets-management market's bar is dynamic/rotating credentials specifically, not static retrieval
- The argument for it: two independent research passes converge on the same specific gap, framed as a real security-posture issue ("endpoint credential exposure") for security-conscious enterprises.
- The argument against it: the Tier D search confirms the credible version of this feature requires implementing dynamic-secret lease/rotation protocols against multiple vendor backends — a meaningfully large effort, not "read one static secret." No VoC or community evidence corroborates active demand.
- Evidence Strength: **3** — 2 independent B sources agree, both citing the same specific vendor list.
- Reach: **3** — enterprise/regulated primarily; some fit with larger, security-mature startups, but the requirement for "also serve medium-large startups" is a stretch here.
- Severity: **3** — a real security/compliance concern for the segment it affects ("endpoint credential exposure" per the source), but not a workflow blocker.
- Competitive Urgency: **2** — no MongoDB GUI competitor confirmed to have this in any source consulted; this is rare even in broader desktop devtools generally.
- Build Effort: **4** — per the Tier D market-context finding, a credible implementation needs dynamic/rotating credential support across multiple vendor backends, not simple static secret retrieval — this exceeds the medium ceiling.
- Priority Score: (3+3+3+2)/4 = **2.75**
- **Cut — effort exceeds ceiling.**

### Candidate 15: VS Code / JetBrains companion extension — **expanded in Stage 6**
- Feature area: new product surface — NEW
- Description: A companion extension in the VS Code Marketplace / JetBrains Plugin Repository bringing IntelliShell, query/aggregation code generation, and the AI Helper into the primary IDE, so developers don't have to context-switch to the standalone Studio 3T application.
- Segment fit: individual developers, startups — this is a developer-experience play, not an enterprise-procurement one.
- Sources: (B) `studio-3t-missing-integrations`: *"Studio 3T currently lacks companion extensions in the VS Code Marketplace or JetBrains Plugin Repository. Developers building backend services must exit their application environment, launch Studio 3T, draft and test aggregation pipelines, export the generated driver code, and return to their IDE to integrate the logic. This context switching disrupts developer focus."*
- The argument for it: a clearly-articulated, real developer-workflow friction point, directly sourced.
- The argument against it: MongoDB Inc. itself already publishes an official "MongoDB for VS Code" extension occupying much of this niche (general knowledge, not independently re-verified with a fresh fetch in this pass — flagged as such rather than asserted with false confidence); building and maintaining a second, separate plugin-platform codebase (VS Code's extension API and JetBrains' plugin SDK are entirely different platforms) is an ongoing maintenance cost, not a one-time build.
- Evidence Strength: **2** — single source.
- Reach: **3** — broad among developers who live in these IDEs; less relevant to DBAs/consultants who already use the full desktop app.
- Severity: **2** — real but non-blocking context-switching friction.
- Competitive Urgency: **3** — MongoDB's own official VS Code extension is a plausible existing occupant of this niche (unverified in this pass, noted as an assumption, not a confirmed fact) — scored as if a moderate competitive bar already exists rather than a green field.
- Build Effort: **4** — two entirely separate plugin platforms (VS Code extension API, JetBrains Plugin SDK) each with their own ongoing maintenance burden — this exceeds the medium ceiling as a single 1-2 cycle effort.
- Priority Score: (2+3+2+3)/4 = **2.50**
- **Cut — effort exceeds ceiling.**

### Candidates 2, 13, 14, 7, 8 — cut, cards remain abbreviated (evidentiary base too thin to expand further)

- **2 (IntelliShell debugger):** effort 4, exceeds ceiling — real breakpoint debugging requires dedicated debugger-protocol infrastructure (2.25). Sources: `nosqlbooster-competitive-analysis`, `nosqlbooster-competitive-intelligence-analysis` (both B-tier, describing the same NoSQLBooster feature).
- **13 (Synthetic test data):** low across the board, single source (`mongodb-ai-automation-opportunities`), no competitor confirmed (2.33).
- **14 (Federated querying):** effort 5, exceeds ceiling by a wide margin — a federated query engine is a major architecture undertaking. Source: `datagrip-competitive-analysis` (2.00).
- **7 (JIT access + dynamic masking):** effort 5 — this is control-plane functionality already properly homed in 3T Lens/3T Access; porting it to Desktop would mean rebuilding that architecture. Source: `studio-3t-enterprise-gap-analysis` (1.80).
- **8 (Desktop SSO):** effort 5, weakest overall profile — likely a category-confusion candidate; Studio 3T Desktop is a license-key-based local app, not an account-based SaaS surface the way 3T Lens/Access are. Source: `studio-3t-enterprise-gap-analysis` (1.40).

## Atomic dictionary gaps — blanket assessment

The ~78 unverified + remaining present-elsewhere IDs not absorbed into a headline candidate (full list in Stage 1) were reviewed as a group rather than individually carded. Collectively: most score low on Reach (single-control/format items, e.g. `QUERY-collation`, `SHELL-minimap`) and low on Severity (no corroborating pain evidence in any tier). None individually approaches the shortlist threshold. **Recommendation:** treat these as a standing backlog for routine roadmap grooming, separate from this "widen the lead" decision — re-visiting them is a different, smaller-grained kind of decision than the one this research is answering.
