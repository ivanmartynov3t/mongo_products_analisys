# Taxonomy reconciliation with prod_info_silo

**Scope:** vocabulary only — IDs, names, definitions and silo detection patterns shared between [`feature-dictionary.md`](../feature-dictionary.md) and `prod_info_silo/config/taxonomy.yaml`. Tracks issue [#15](https://github.com/ivanmartynov3t/mongo_products_analisys/issues/15); plan: [`update-plans/07-taxonomy-reconciliation.md`](../update-plans/07-taxonomy-reconciliation.md). Reconciled 2026-09-24.

**This report changes no capability status.** The silo detecting that a document mentions a capability is not evidence that a product has it; any claim still needs a human-checked source and enters as ❓ until verified.

## Navigation

- [Feature dictionary](../feature-dictionary.md) — section "Taxonomy reconciliation with prod_info_silo"
- [Machine-readable table](taxonomy-reconciliation.tsv) — read by the weekly triage (#18)
- [Low-level feature comparison](comparisons/low-level-feature-comparison.md) · [High-level product comparison](comparisons/high-level-product-comparison.md)
- [Gap analysis: not on any 3T product](gap-analysis-not-on-3t-products.md)
- [Studio 3T product report](../products/3t/studio-3t/product-report.md)
- Tool: [`tools/taxonomy-reconcile/`](../tools/taxonomy-reconcile/README.md)

## Result

| | Count |
|---|---|
| Silo IDs before (268 sub-features + 14 proposed) | 282 |
| Silo IDs missing from our dictionary | **0** |
| Silo IDs whose definition matches ours | **282 of 282** (11 are shortened forms of our text, same meaning) |
| Our IDs the silo did not have | 82 |
| → feed-upstream (now added to the silo) | 8 |
| → retired as synonyms (rows kept, marked *Retired*) | 20 |
| → child-of another ID (finer analysis detail; the silo detects the parent) | 27 |
| → analysis-only / Tier 2 (proposals, source-code-only distinctions) | 27 |
| Dictionary IDs the silo can now detect (directly, or via parent/survivor) | **278 of 364** |
| Silo IDs with zero documents in the silo catalog | 72 of 282 before → **53 of 290** after |

### Headline findings

1. **The vocabularies agree on meaning; they disagree on detection.** Every one of the 282 silo IDs has the same definition here. But **72 of 282 silo IDs (26%) had zero documents in the silo's own catalog** (`catalog_index.json`, 8,108 classified documents); an independent regex walk over all 8,176 files found 66 of them with zero matches. The silo could never surface evidence for them.
2. **Most dead patterns are too literal, not wrong.** 19 were revived (18 rewritten from sampled evidence, `AGG-stage-count` by the boundary-bug fix); after the change **53 of 290** silo IDs have zero documents, and all 8 new IDs are detected. The remaining dead patterns are kept as they are because a looser definition probe found fewer than 5 documents or fewer than 6/8 on-topic — many are source-code-level distinctions ("internal-only") that vendor docs never describe.
3. **A word-boundary bug affected 22 silo patterns** (20 sub-features and the `F-AGG`/`F-SCHEMA` feature patterns). Patterns such as `\b(\$match|…)\b` can never match after whitespace, because `\b` needs a word character next to `$`. Fixed with `(?<!\w)`/`(?!\w)` lookarounds (0 documents lost). Acceptance on the real classifier then showed that in 6 IDs the revived alternatives (`find()`, `sort()`, `NOW()`, `$`) matched code samples, not the capability (0/8–3/6 on-topic); for those the fix was reverted and the previous behaviour kept. The fix stays for 14 sub-features and the 2 feature patterns (e.g. `AGG-stage-count` 0 → 118 documents, 8/8 on-topic).
4. **Four silo patterns were over-broad** (sampled ≤ 5/8 on-topic): `AI-nl-query` fired on any "AI Helper/assistant" mention (~1/8), `CONN-sidebar-ops` on "connection tree"/"Database Navigator", `CONN-tls` on any bare "TLS/SSL", `CONN-topology` on "direct connection". Tightened.
5. **The issue comment's premise was only partly right.** "Deprecate numbered/synonym IDs" held for only 4 of 22 numbered IDs (`AI-0xx`, `GOV-0xx`): 4 are finer-grained children of a silo ID, 3 were fed upstream, and 11 are distinct product-specific capabilities kept as analysis-only.
6. **Retiring every silo-duplicate would have destroyed analysis detail.** Matrices must be low-level and implementation-aware; e.g. the Studio 3T scheduler matrix documents once/daily/interval/weekly/monthly recurrence separately with different evidence. Such IDs are recorded as *child-of* the silo parent (`SCHED-types-time`) instead of being merged away.
7. **Our own documents had already flagged the synonyms.** The Studio 3T scheduler matrix called `SCHED-task-actions` an "Alias of SCHED-actions", the governance matrix called `GOV-protect-mode` a "Likely duplicate", and the gap report listed 17 dictionary alias pairs — the same pairs this reconciliation found (for 4 `AI-0xx` pairs the direction is now reversed: the descriptive ID survives).

## Changes made

**prod_info_silo** (`config/taxonomy.yaml`, `tests/test_taxonomy.py`):
- Added 8 sub-features with our IDs (identity mapping): `AI-local-mcp`, `AI-stt-cli`, `GOV-ai-controls`, `GOV-003`, `GOV-004`, `GOV-006`, `SCHED-actions`, `SCHED-history`. The silo's `PROP-pii-discovery`, `PROP-idx-perf-advisor` and `PROP-webhook-notify` stay as proposals, mirroring this dictionary's Proposed Feature Registry; the shipped counterparts are the new `GOV-004`, `GOV-006`, `GOV-003`.
- Widened 26 patterns, fixed the boundary bug in 14 sub-features and 2 feature-level patterns (reverted in 6 after acceptance), tightened 4.
- Added 41 positive/negative regression tests from sampled real phrasings. Suite: 175 passed.
- Rebuilt the catalog with the existing pipeline (`run_pipeline.sh --force`, validate mode — no scraping), then a second forced run to confirm the data is stable (only generated dashboards changed).
- **Acceptance** on the silo's own catalog: 8 newly tagged documents read per changed ID; every kept change is ≥ 6/8 on-topic. Two widenings failed first and were tightened (`SQL-migration` 5/8, `GOV-collection-sync` 3/8 → both 8/8).

**This repository:**
- `feature-dictionary.md`: 20 synonym rows marked *Retired → alias of X*; reconciliation section; Changelog entry.
- Living matrices and reports migrated to surviving IDs (22 files). Three alias rows merged into their survivor with their evidence preserved; no status upgraded.
- Deliberately **not** rewritten: `research/` findings, `update-plans/` logs and changelog history. They are historical records; retired IDs still resolve through the dictionary.

## Method

- **Definitions.** Our name + description compared with the silo's for every shared ID; the 11 pairs with under 50% word overlap were read manually (all are shortened forms of our text).
- **Detection.** Every silo pattern was run over all 8,176 scraped `.md` documents. The silo classifier tags a document on a single pattern hit in title/headings/body (`taxonomy.py`, score ≥ 1.0), so per-document counting matches its behaviour. Acceptance of changes uses the silo's own catalog output.
- **Our extras.** For each of the 82 IDs: references in this repository, similarity to every other ID, co-use in the same matrix (never co-used + same meaning = synonym), and a hand-written definition probe over the corpus.
- **Marginal value.** Share of probe hits already caught by the *same-meaning* silo ID. An earlier version counted "tagged by any silo ID", which made everything look covered because long documents collect dozens of unrelated tags; that measure was discarded.
- **Precision.** 5 random hits (all hits) or 8 random hits (only hits the silo did not catch), read manually. Rule: feed upstream or rewrite a pattern only at ≥ 6/8 and ≥ 5 documents.

### Limitations

- Probes are hand-written; different wording would change counts. Treat counts as directional.
- 5–8 samples per ID give wide confidence intervals; borderline items are marked in the reason column.
- Snippet de-duplication (±60 characters) is approximate — versioned vendor docs and mirrored pages inflate raw counts.
- Evidence runs used all 8,176 `.md` files; the silo classifier excludes 69 of them (52 generated dashboards and 17 `repo_source_strings.md` source-string extracts). Counts shift by at most one document per excluded file, but some sampled snippets came from source strings. `probes.py` now applies the silo's exclusions.
- Many 3T hits come from internal repository docs (Lens, Policy Engine) rather than public pages.
- The silo classifies its own root `data/DIFF.md` dashboard as a document (its exclusion rule covers `data/README.md` and per-product dashboards only); this is why two untouched IDs changed by one document. Reported as a silo follow-up, not changed here.
- Numbered IDs `GOV-003`/`GOV-004`/`GOV-006` keep product-specific descriptions ("3T Lens …") while the silo pattern detects the capability class in any product.

## How the weekly triage (#18) uses this

Run `uv run tools/taxonomy-reconcile/reconcile.py --check`. It exits non-zero and lists every silo ID not yet in the dictionary, every dictionary ID without a decision, and every decision pointing at an unknown ID. Those are the new signals; everything in the table below is known and is not re-raised.

## Full table

Generated by `tools/taxonomy-reconcile/reconcile.py` — do not edit by hand. "Silo detects via" is the silo ID whose catalog count stands in for this ID (itself, its parent, or its survivor).

<!-- BEGIN GENERATED TABLE -->

| ID | Verdict | Maps to | Silo detects via (docs) | Silo action | Reason |
|---|---|---|---|---|---|
| `AGG-change-target` | same definition |  | AGG-change-target (1) |  | names/descriptions match (silo text is a shortened form where different) |
| `AGG-chart-builder` | same definition |  | AGG-chart-builder (10) | widened | pattern narrower than definition; new pattern sampled >= 6/8 |
| `AGG-clipboard` | same definition |  | AGG-clipboard (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `AGG-code-gen` | same definition |  | AGG-code-gen (12) |  | names/descriptions match (silo text is a shortened form where different) |
| `AGG-code-tab` | same definition |  | AGG-code-tab (5) |  | names/descriptions match (silo text is a shortened form where different) |
| `AGG-create-view` | same definition |  | AGG-create-view (2) | boundary-bug fixed | names/descriptions match (silo text is a shortened form where different) |
| `AGG-date-tags` | same definition |  | AGG-date-tags (4) |  | names/descriptions match (silo text is a shortened form where different) |
| `AGG-editor-layout` | same definition |  | AGG-editor-layout (201) |  | names/descriptions match (silo text is a shortened form where different) |
| `AGG-export-results` | same definition |  | AGG-export-results (1) |  | names/descriptions match (silo text is a shortened form where different) |
| `AGG-js-import-export` | same definition |  | AGG-js-import-export (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `AGG-keyboard` | same definition |  | AGG-keyboard (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `AGG-mapreduce-editor` | same definition |  | AGG-mapreduce-editor (108) |  | names/descriptions match (silo text is a shortened form where different) |
| `AGG-pagination` | same definition |  | AGG-pagination (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `AGG-pipeline-opts` | same definition |  | AGG-pipeline-opts (57) |  | names/descriptions match (silo text is a shortened form where different) |
| `AGG-result-formats` | same definition |  | AGG-result-formats (8) |  | names/descriptions match (silo text is a shortened form where different) |
| `AGG-save-load` | same definition |  | AGG-save-load (6) |  | names/descriptions match (silo text is a shortened form where different) |
| `AGG-stage-count` | same definition |  | AGG-stage-count (118) | boundary-bug fixed | names/descriptions match (silo text is a shortened form where different) |
| `AGG-stage-mgmt` | same definition |  | AGG-stage-mgmt (24) |  | names/descriptions match (silo text is a shortened form where different) |
| `AGG-stage-modes` | same definition |  | AGG-stage-modes (5) |  | names/descriptions match (silo text is a shortened form where different) |
| `AGG-stage-preview` | same definition |  | AGG-stage-preview (10) |  | names/descriptions match (silo text is a shortened form where different) |
| `AGG-stage-toggle` | same definition |  | AGG-stage-toggle (2) |  | names/descriptions match (silo text is a shortened form where different) |
| `AGG-timer-cancel` | same definition |  | AGG-timer-cancel (1) |  | names/descriptions match (silo text is a shortened form where different) |
| `AGG-vqb-sync` | same definition |  | AGG-vqb-sync (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `AI-001` | retire (synonym) | `AI-providers` | AI-providers (136) |  | Same provider-set definition; silo pattern already catches 72% of hits |
| `AI-002` | child-of | `AI-multi-config` | AI-multi-config (1) |  | Runtime config controls (temperature/enable) within AI configs; Enable/config controls are covered by AI-multi-config (98% family coverage) |
| `AI-003` | child-of | `AI-nl-query` | AI-nl-query (154) |  | Studio 3T NL generation workflow spanning query/pipeline/script; NL query/pipeline generation = AI-nl-query + AI-nl-pipeline; 75% covered |
| `AI-004` | analysis-only |  | — |  | Apply-generated-result; probe precision 1/5, source-code distinction |
| `AI-005` | analysis-only |  | — |  | Local AI history restore; Studio 3T source-only, 18 hits |
| `AI-006` | analysis-only |  | — |  | AI shortcuts; 4 hits in whole corpus |
| `AI-007` | retire (synonym) | `AI-local-mcp` | AI-local-mcp (135) |  | Same "local MCP server" meaning; never in same matrix as AI-local-mcp |
| `AI-008` | retire (synonym) | `AI-mcp-tools` | AI-local-mcp (135) |  | Same MCP tool-catalog meaning; never co-used |
| `AI-009` | retire (synonym) | `AI-mcp-client` | AI-local-mcp (135) |  | Same MCP-client-compat meaning; never co-used |
| `AI-010` | child-of | `AI-stt-cli` | AI-stt-cli (40) |  | Binary surface of stt-cli; co-exists with AI-011 in the 3T MCP matrix; stt-cli binary = AI-stt-cli |
| `AI-011` | child-of | `AI-stt-cli` | AI-stt-cli (40) |  | Feature set of stt-cli; co-exists with AI-010 in the 3T MCP matrix; stt-cli feature set = AI-stt-cli |
| `AI-012` | analysis-only |  | — |  | 3T Explore AI agent; 5 hits, all already family-tagged |
| `AI-agentic-mode` | same definition |  | AI-agentic-mode (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `AI-chart-render` | same definition |  | AI-chart-render (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `AI-context-turns` | retire (synonym) | `AI-conversation` | AI-conversation (33) |  | Identical definition to AI-conversation; orphan |
| `AI-conversation` | same definition |  | AI-conversation (33) | widened | pattern narrower than definition; new pattern sampled >= 6/8 |
| `AI-error-fix` | same definition |  | AI-error-fix (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `AI-explanation` | same definition |  | AI-explanation (0) |  | names/descriptions match (silo text is a shortened form where different) |
| `AI-guardrail-layer` | same definition |  | AI-guardrail-layer (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `AI-inline-completion` | same definition |  | AI-inline-completion (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `AI-key-storage` | same definition |  | AI-key-storage (1) |  | names/descriptions match (silo text is a shortened form where different) |
| `AI-local-mcp` | feed-upstream |  | AI-local-mcp (135) | added to silo | Only new ID worth adding: generic MCP server; silo AI-offline-mcp (Studio 3T-bundled) catches 5%; 75 distinct uncaught snippets, 7/8 precise, 15 products |
| `AI-mcp-client` | child-of | `AI-local-mcp` | AI-local-mcp (135) |  | Facet of the local MCP server; its phrasing is folded into the silo AI-local-mcp pattern; Fold into upstream AI-local-mcp patterns (24/31 docs overlap); client lists are matrix detail |
| `AI-mcp-tools` | child-of | `AI-local-mcp` | AI-local-mcp (135) |  | Facet of the local MCP server; its phrasing is folded into the silo AI-local-mcp pattern; Fold into upstream AI-local-mcp patterns (44/73 docs overlap); tool counts are matrix-level detail; 5/8 precise |
| `AI-model-chooser` | child-of | `AI-models` | AI-models (72) |  | Gap report: "user-selectable model per config" aspect differs from AI-models ("models available"); Same meaning as AI-models; widen AI-models pattern (catches 23%; 23 distinct uncaught, 7/8) |
| `AI-models` | same definition |  | AI-models (72) | widened | pattern narrower than definition; new pattern sampled >= 6/8 |
| `AI-multi-config` | same definition |  | AI-multi-config (1) |  | names/descriptions match (silo text is a shortened form where different) |
| `AI-multi-conversation` | same definition |  | AI-multi-conversation (29) | widened | pattern narrower than definition; new pattern sampled >= 6/8 |
| `AI-named-configs` | retire (synonym) | `AI-multi-config` | AI-multi-config (1) |  | Same "multiple named AI configs" definition |
| `AI-nl-pipeline` | same definition |  | AI-nl-pipeline (6) | widened | pattern narrower than definition; new pattern sampled >= 6/8 |
| `AI-nl-query` | same definition |  | AI-nl-query (154) | boundary-bug fixed; tightened | ~1/8 on-topic: bare "AI Helper/assistant" mentions |
| `AI-offline-mcp` | same definition |  | AI-offline-mcp (12) |  | names/descriptions match (silo text is a shortened form where different) |
| `AI-plan-gate` | retire (synonym) | `AI-plan-req` | — |  | Near-identical definition to AI-plan-req; never co-used |
| `AI-plan-req` | analysis-only |  | — |  | Precise (5/5) but all 24 hits are DBeaver edition banners; single-vendor |
| `AI-privacy` | same definition |  | AI-privacy (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `AI-prompt-templates` | same definition |  | AI-prompt-templates (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `AI-providers` | same definition |  | AI-providers (136) |  | names/descriptions match (silo text is a shortened form where different) |
| `AI-safety-guards` | same definition |  | AI-safety-guards (4) |  | names/descriptions match (silo text is a shortened form where different) |
| `AI-sample-context` | same definition |  | AI-sample-context (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `AI-sample-data-toggle` | retire (synonym) | `AI-sample-context` | AI-sample-context (0) |  | Same sample-data opt-in definition |
| `AI-schema-aware` | same definition |  | AI-schema-aware (9) | widened | pattern narrower than definition; new pattern sampled >= 6/8 |
| `AI-schema-context` | retire (synonym) | `AI-schema-aware` | AI-schema-aware (9) |  | Same meaning as AI-schema-aware; widen pattern (0% caught) - but 7 distinct snippets, 1 vendor (DataGrip) |
| `AI-stt-cli` | feed-upstream |  | AI-stt-cli (40) | added to silo | 3T MCP binary; 0% caught by PROP-cli-automation/SCHED-cli-headless; 8 distinct snippets, all 3T docs |
| `AI-tab-context` | same definition |  | AI-tab-context (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `AI-voice-query` | same definition |  | AI-voice-query (8) | widened | pattern narrower than definition; new pattern sampled >= 6/8 |
| `CONN-access-manager-integration` | same definition |  | CONN-access-manager-integration (17) |  | names/descriptions match (silo text is a shortened form where different) |
| `CONN-auth-enterprise` | same definition |  | CONN-auth-enterprise (811) |  | names/descriptions match (silo text is a shortened form where different) |
| `CONN-auth-std` | same definition |  | CONN-auth-std (375) |  | names/descriptions match (silo text is a shortened form where different) |
| `CONN-color-coding` | same definition |  | CONN-color-coding (24) |  | names/descriptions match (silo text is a shortened form where different) |
| `CONN-compat-cosmos` | same definition |  | CONN-compat-cosmos (88) |  | names/descriptions match (silo text is a shortened form where different) |
| `CONN-compat-docdb` | same definition |  | CONN-compat-docdb (118) |  | names/descriptions match (silo text is a shortened form where different) |
| `CONN-compat-ferretdb` | same definition |  | CONN-compat-ferretdb (10) |  | names/descriptions match (silo text is a shortened form where different) |
| `CONN-compat-redis` | same definition |  | CONN-compat-redis (145) |  | names/descriptions match (silo text is a shortened form where different) |
| `CONN-cred-storage` | same definition |  | CONN-cred-storage (57) | widened | pattern narrower than definition; new pattern sampled >= 6/8 |
| `CONN-git-repo-sharing` | same definition |  | CONN-git-repo-sharing (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `CONN-import-clients` | same definition |  | CONN-import-clients (21) |  | names/descriptions match (silo text is a shortened form where different) |
| `CONN-in-use-enc` | same definition |  | CONN-in-use-enc (142) |  | names/descriptions match (silo text is a shortened form where different) |
| `CONN-multi-active` | same definition |  | CONN-multi-active (88) |  | names/descriptions match (silo text is a shortened form where different) |
| `CONN-org-folders` | same definition |  | CONN-org-folders (60) |  | names/descriptions match (silo text is a shortened form where different) |
| `CONN-pool-params` | same definition |  | CONN-pool-params (86) |  | names/descriptions match (silo text is a shortened form where different) |
| `CONN-portability` | same definition |  | CONN-portability (2) |  | names/descriptions match (silo text is a shortened form where different) |
| `CONN-proxy` | same definition |  | CONN-proxy (166) |  | names/descriptions match (silo text is a shortened form where different) |
| `CONN-read-pref` | same definition |  | CONN-read-pref (146) |  | names/descriptions match (silo text is a shortened form where different) |
| `CONN-readonly-lock` | same definition |  | CONN-readonly-lock (197) |  | names/descriptions match (silo text is a shortened form where different) |
| `CONN-role-docs` | same definition |  | CONN-role-docs (1) |  | names/descriptions match (silo text is a shortened form where different) |
| `CONN-search-nav` | same definition |  | CONN-search-nav (6) |  | names/descriptions match (silo text is a shortened form where different) |
| `CONN-session-restore` | same definition |  | CONN-session-restore (6) |  | names/descriptions match (silo text is a shortened form where different) |
| `CONN-sidebar-ops` | same definition |  | CONN-sidebar-ops (153) | tightened | 3/8: "connection tree", "Database Navigator", "connect to" |
| `CONN-ssh` | same definition |  | CONN-ssh (398) |  | names/descriptions match (silo text is a shortened form where different) |
| `CONN-team-sharing` | same definition |  | CONN-team-sharing (64) |  | names/descriptions match (silo text is a shortened form where different) |
| `CONN-test-steps` | same definition |  | CONN-test-steps (471) |  | names/descriptions match (silo text is a shortened form where different) |
| `CONN-tls` | same definition |  | CONN-tls (639) | tightened | 5/8: bare TLS/SSL/PEM |
| `CONN-topology` | same definition |  | CONN-topology (481) | tightened | 4/8: generic "direct connection" |
| `CONN-uri-export` | same definition |  | CONN-uri-export (9) |  | names/descriptions match (silo text is a shortened form where different) |
| `CONN-uri-paste` | same definition |  | CONN-uri-paste (241) |  | names/descriptions match (silo text is a shortened form where different) |
| `GOV-002` | analysis-only |  | — |  | Lens-internal; 3T repo docs only, 73% family-tagged |
| `GOV-003` | feed-upstream | `PROP-webhook-notify` | GOV-003 (40) | added to silo | Shipped in 3T Lens/Policy Engine; silo lists it only as PROP-webhook-notify -> promote PROP to sub-feature (catches 23%) |
| `GOV-004` | feed-upstream | `PROP-pii-discovery` | GOV-004 (123) | added to silo | Shipped in Lens/PII Scanner; PROP-pii-discovery already catches 75% -> promote PROP to sub-feature |
| `GOV-005` | analysis-only |  | — |  | 8 hits; source-audit distinction |
| `GOV-006` | feed-upstream | `PROP-idx-perf-advisor` | GOV-006 (31) | added to silo | Shipped (Lens, VisuaLeaf); PROP-idx-perf-advisor catches 0% -> promote + widen pattern |
| `GOV-007` | analysis-only |  | — |  | 6 hits, all tagged |
| `GOV-010` | analysis-only |  | — |  | 4 hits, all tagged |
| `GOV-011` | analysis-only |  | — |  | 2 hits, both tagged by GOV-data-masking |
| `GOV-012` | analysis-only |  | — |  | 2 hits |
| `GOV-013` | analysis-only |  | — |  | Survivor of GOV-platform-k8s (broader: Helm + scaling + observability; exception to descriptive-name rule); Same Helm/K8s meaning; probe 1/5 (K8s mostly = DBeaver connection type) |
| `GOV-ai-controls` | feed-upstream |  | GOV-ai-controls (32) | added to silo | Disable/approve AI; AI-privacy (schema-only vs samples) is a different meaning and catches 0%; 27 distinct, 7/8, 9 products |
| `GOV-air-gapped` | same definition |  | GOV-air-gapped (6) |  | names/descriptions match (silo text is a shortened form where different) |
| `GOV-audit-log` | same definition |  | GOV-audit-log (77) |  | names/descriptions match (silo text is a shortened form where different) |
| `GOV-cli-policy` | analysis-only |  | — |  | 2 hits |
| `GOV-collection-compare` | same definition |  | GOV-collection-compare (146) | widened | pattern narrower than definition; new pattern sampled >= 6/8 |
| `GOV-collection-sync` | same definition |  | GOV-collection-sync (63) | widened | pattern narrower than definition; added "sync differences" / "compare and sync" (first attempt 3/8 at acceptance, tightened) |
| `GOV-cred-protection` | same definition |  | GOV-cred-protection (14) |  | names/descriptions match (silo text is a shortened form where different) |
| `GOV-cred-storage-os` | child-of | `CONN-cred-storage` | CONN-cred-storage (57) |  | OS-keychain mechanism of credential storage; Same meaning as CONN-cred-storage (cross-family); widen pattern (catches 21%) |
| `GOV-data-masking` | same definition |  | GOV-data-masking (145) |  | names/descriptions match (silo text is a shortened form where different) |
| `GOV-isolated-edition` | analysis-only |  | — |  | 103 hits are one repeated Compass banner; single-vendor |
| `GOV-network-policy` | same definition |  | GOV-network-policy (26) |  | names/descriptions match (silo text is a shortened form where different) |
| `GOV-platform-access` | same definition |  | GOV-platform-access (26) |  | names/descriptions match (silo text is a shortened form where different) |
| `GOV-platform-bridge` | child-of | `GOV-platform-cdc` | GOV-platform-cdc (15) |  | Bridge integration surface around the CDC engine; 86% already caught by GOV-platform-cdc; orphan |
| `GOV-platform-cdc` | same definition |  | GOV-platform-cdc (15) |  | names/descriptions match (silo text is a shortened form where different) |
| `GOV-platform-explore` | analysis-only |  | — |  | 0 corpus hits; source-only |
| `GOV-platform-k8s` | retire (synonym) | `GOV-013` | — |  | Narrower synonym of GOV-013 (1 reference); Survivor of GOV-013; probe precision 1/5 -> not worth upstream |
| `GOV-platform-lens` | same definition |  | GOV-platform-lens (46) |  | names/descriptions match (silo text is a shortened form where different) |
| `GOV-platform-oidc` | child-of | `CONN-auth-enterprise` | CONN-auth-enterprise (811) |  | Platform multi-provider OIDC; silo parent catches 95%; CONN-auth-enterprise (includes MongoDB OIDC) already catches 95%; orphan |
| `GOV-protect-mode` | retire (synonym) | `GOV-readonly-mode` | GOV-readonly-mode (6) |  | Own Studio 3T matrix row already says "Likely duplicate of GOV-readonly-mode" |
| `GOV-rbac-actions` | analysis-only |  | — |  | Probe 2/5 (role names in code samples); 87% tagged |
| `GOV-rbac-inheritance` | same definition |  | GOV-rbac-inheritance (1) |  | names/descriptions match (silo text is a shortened form where different) |
| `GOV-rbac-roles` | same definition |  | GOV-rbac-roles (17) | boundary-bug fixed | names/descriptions match (silo text is a shortened form where different) |
| `GOV-rbac-tree` | same definition |  | GOV-rbac-tree (1) |  | names/descriptions match (silo text is a shortened form where different) |
| `GOV-rbac-users` | same definition |  | GOV-rbac-users (66) | boundary-bug fixed | names/descriptions match (silo text is a shortened form where different) |
| `GOV-readonly-mode` | same definition |  | GOV-readonly-mode (6) |  | names/descriptions match (silo text is a shortened form where different) |
| `GOV-secrets-vault` | same definition |  | GOV-secrets-vault (17) |  | names/descriptions match (silo text is a shortened form where different) |
| `GOV-staged-commit` | same definition |  | GOV-staged-commit (80) |  | names/descriptions match (silo text is a shortened form where different) |
| `GOV-startup-policy` | analysis-only |  | — |  | 2 hits (Compass only) |
| `GOV-telemetry` | same definition |  | GOV-telemetry (2) |  | names/descriptions match (silo text is a shortened form where different) |
| `GOV-telemetry-config` | retire (synonym) | `GOV-telemetry` | GOV-telemetry (2) |  | Same telemetry opt-out meaning |
| `IDX-advanced-opts` | same definition |  | IDX-advanced-opts (11) |  | names/descriptions match (silo text is a shortened form where different) |
| `IDX-atlas-search` | same definition |  | IDX-atlas-search (41) |  | names/descriptions match (silo text is a shortened form where different) |
| `IDX-build-mode` | same definition |  | IDX-build-mode (2) |  | names/descriptions match (silo text is a shortened form where different) |
| `IDX-collation-opts` | same definition |  | IDX-collation-opts (13) |  | names/descriptions match (silo text is a shortened form where different) |
| `IDX-copy-paste` | same definition |  | IDX-copy-paste (6) |  | names/descriptions match (silo text is a shortened form where different) |
| `IDX-explain-brief` | same definition |  | IDX-explain-brief (158) |  | names/descriptions match (silo text is a shortened form where different) |
| `IDX-explain-full` | same definition |  | IDX-explain-full (62) |  | names/descriptions match (silo text is a shortened form where different) |
| `IDX-explain-sources` | same definition |  | IDX-explain-sources (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `IDX-geo-opts` | same definition |  | IDX-geo-opts (4) |  | names/descriptions match (silo text is a shortened form where different) |
| `IDX-hide-unhide` | same definition |  | IDX-hide-unhide (6) |  | names/descriptions match (silo text is a shortened form where different) |
| `IDX-inventory` | same definition |  | IDX-inventory (129) | boundary-bug fixed | names/descriptions match (silo text is a shortened form where different) |
| `IDX-log-parser` | same definition |  | IDX-log-parser (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `IDX-perf-insights` | same definition |  | IDX-perf-insights (0) |  | names/descriptions match (silo text is a shortened form where different) |
| `IDX-profiler-analysis` | same definition |  | IDX-profiler-analysis (3) |  | names/descriptions match (silo text is a shortened form where different) |
| `IDX-profiler-config` | same definition |  | IDX-profiler-config (57) |  | names/descriptions match (silo text is a shortened form where different) |
| `IDX-profiler-drilldown` | same definition |  | IDX-profiler-drilldown (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `IDX-profiler-export` | same definition |  | IDX-profiler-export (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `IDX-profiler-live` | same definition |  | IDX-profiler-live (20) | boundary-bug fixed | names/descriptions match (silo text is a shortened form where different) |
| `IDX-props-collation` | same definition |  | IDX-props-collation (0) |  | names/descriptions match (silo text is a shortened form where different) |
| `IDX-props-hidden` | same definition |  | IDX-props-hidden (4) | boundary-bug fixed | names/descriptions match (silo text is a shortened form where different) |
| `IDX-props-partial` | same definition |  | IDX-props-partial (27) |  | names/descriptions match (silo text is a shortened form where different) |
| `IDX-props-unique-sparse` | same definition |  | IDX-props-unique-sparse (23) |  | names/descriptions match (silo text is a shortened form where different) |
| `IDX-quick-actions` | same definition |  | IDX-quick-actions (2) |  | names/descriptions match (silo text is a shortened form where different) |
| `IDX-realtime-perf` | same definition |  | IDX-realtime-perf (13) |  | names/descriptions match (silo text is a shortened form where different) |
| `IDX-stop-ops` | same definition |  | IDX-stop-ops (17) | boundary-bug fixed | names/descriptions match (silo text is a shortened form where different) |
| `IDX-text-opts` | same definition |  | IDX-text-opts (5) |  | names/descriptions match (silo text is a shortened form where different) |
| `IDX-type-2d` | same definition |  | IDX-type-2d (11) |  | names/descriptions match (silo text is a shortened form where different) |
| `IDX-type-2dsphere` | same definition |  | IDX-type-2dsphere (5) |  | names/descriptions match (silo text is a shortened form where different) |
| `IDX-type-compound` | same definition |  | IDX-type-compound (49) |  | names/descriptions match (silo text is a shortened form where different) |
| `IDX-type-hashed` | same definition |  | IDX-type-hashed (4) |  | names/descriptions match (silo text is a shortened form where different) |
| `IDX-type-haystack` | same definition |  | IDX-type-haystack (6) |  | names/descriptions match (silo text is a shortened form where different) |
| `IDX-type-multikey` | same definition |  | IDX-type-multikey (13) |  | names/descriptions match (silo text is a shortened form where different) |
| `IDX-type-single` | same definition |  | IDX-type-single (9) |  | names/descriptions match (silo text is a shortened form where different) |
| `IDX-type-text` | same definition |  | IDX-type-text (106) |  | names/descriptions match (silo text is a shortened form where different) |
| `IDX-type-ttl` | same definition |  | IDX-type-ttl (46) |  | names/descriptions match (silo text is a shortened form where different) |
| `IDX-type-wildcard` | same definition |  | IDX-type-wildcard (5) | boundary bug left in place | Fixing \b next to "(" / "$" revived alternatives such as find()/sort()/NOW()/$ that matched code samples (0/8 to 3/6 on-topic); previous behaviour kept, latent dead alternatives documented |
| `IDX-vector-search` | same definition |  | IDX-vector-search (33) |  | names/descriptions match (silo text is a shortened form where different) |
| `PROP-ai-gateway-sso` | same definition |  | PROP-ai-gateway-sso (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `PROP-bi-dashboard` | same definition |  | PROP-bi-dashboard (43) | widened | pattern narrower than definition; new pattern sampled >= 6/8 |
| `PROP-cli-automation` | same definition |  | PROP-cli-automation (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `PROP-desktop-sso` | analysis-only |  | — |  | Proposed feature; silo has no concept of our proposals by design |
| `PROP-federated-query` | same definition |  | PROP-federated-query (1) |  | names/descriptions match (silo text is a shortened form where different) |
| `PROP-git-integration` | same definition |  | PROP-git-integration (70) | widened | pattern narrower than definition; new pattern sampled >= 6/8 |
| `PROP-ide-companion` | analysis-only |  | — |  | Proposed feature; silo has no concept of our proposals by design |
| `PROP-idx-perf-advisor` | same definition |  | PROP-idx-perf-advisor (25) | widened | pattern narrower than definition; new pattern sampled >= 6/8 |
| `PROP-intellishell-debugger` | analysis-only |  | — |  | Proposed feature; silo has no concept of our proposals by design |
| `PROP-jit-dynamic-masking` | analysis-only |  | — |  | Proposed feature; silo has no concept of our proposals by design |
| `PROP-pii-discovery` | same definition |  | PROP-pii-discovery (86) |  | names/descriptions match (silo text is a shortened form where different) |
| `PROP-qe-key-vault-ui` | same definition |  | PROP-qe-key-vault-ui (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `PROP-schema-drift` | same definition |  | PROP-schema-drift (6) |  | names/descriptions match (silo text is a shortened form where different) |
| `PROP-schema-erd-cluster` | same definition |  | PROP-schema-erd-cluster (141) | widened | pattern narrower than definition; new pattern sampled >= 6/8 |
| `PROP-schema-health-advisor` | analysis-only |  | — |  | Proposed feature; silo has no concept of our proposals by design |
| `PROP-secrets-vault` | same definition |  | PROP-secrets-vault (35) |  | names/descriptions match (silo text is a shortened form where different) |
| `PROP-siem-export` | analysis-only |  | — |  | Proposed feature; silo has no concept of our proposals by design |
| `PROP-synthetic-test-data` | same definition |  | PROP-synthetic-test-data (53) |  | names/descriptions match (silo text is a shortened form where different) |
| `PROP-vector-search-tooling` | same definition |  | PROP-vector-search-tooling (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `PROP-webhook-notify` | same definition |  | PROP-webhook-notify (8) |  | names/descriptions match (silo text is a shortened form where different) |
| `QUERY-ai-builder` | same definition |  | QUERY-ai-builder (3) | boundary-bug fixed | names/descriptions match (silo text is a shortened form where different) |
| `QUERY-batch-edit` | same definition |  | QUERY-batch-edit (3) |  | names/descriptions match (silo text is a shortened form where different) |
| `QUERY-cancel` | same definition |  | QUERY-cancel (5) |  | names/descriptions match (silo text is a shortened form where different) |
| `QUERY-charts-dashboards` | same definition |  | QUERY-charts-dashboards (3) |  | names/descriptions match (silo text is a shortened form where different) |
| `QUERY-collation` | same definition |  | QUERY-collation (240) |  | names/descriptions match (silo text is a shortened form where different) |
| `QUERY-copy-options` | same definition |  | QUERY-copy-options (74) |  | names/descriptions match (silo text is a shortened form where different) |
| `QUERY-date-tags` | same definition |  | QUERY-date-tags (24) | boundary bug left in place | Fixing \b next to "(" / "$" revived alternatives such as find()/sort()/NOW()/$ that matched code samples (0/8 to 3/6 on-topic); previous behaviour kept, latent dead alternatives documented |
| `QUERY-doc-dialog` | same definition |  | QUERY-doc-dialog (9) |  | names/descriptions match (silo text is a shortened form where different) |
| `QUERY-export-lang` | same definition |  | QUERY-export-lang (14) |  | names/descriptions match (silo text is a shortened form where different) |
| `QUERY-filter-bar` | same definition |  | QUERY-filter-bar (238) | boundary bug left in place | Fixing \b next to "(" / "$" revived alternatives such as find()/sort()/NOW()/$ that matched code samples (0/8 to 3/6 on-topic); previous behaviour kept, latent dead alternatives documented |
| `QUERY-fluent-api` | same definition |  | QUERY-fluent-api (4) |  | names/descriptions match (silo text is a shortened form where different) |
| `QUERY-history` | same definition |  | QUERY-history (231) |  | names/descriptions match (silo text is a shortened form where different) |
| `QUERY-inline-edit` | same definition |  | QUERY-inline-edit (144) |  | names/descriptions match (silo text is a shortened form where different) |
| `QUERY-manager` | same definition |  | QUERY-manager (215) |  | names/descriptions match (silo text is a shortened form where different) |
| `QUERY-max-time` | same definition |  | QUERY-max-time (150) |  | names/descriptions match (silo text is a shortened form where different) |
| `QUERY-multi-update` | same definition |  | QUERY-multi-update (71) | boundary-bug fixed | names/descriptions match (silo text is a shortened form where different) |
| `QUERY-open-in` | same definition |  | QUERY-open-in (9) |  | names/descriptions match (silo text is a shortened form where different) |
| `QUERY-pagination` | same definition |  | QUERY-pagination (178) |  | names/descriptions match (silo text is a shortened form where different) |
| `QUERY-perf-timer` | same definition |  | QUERY-perf-timer (21) |  | names/descriptions match (silo text is a shortened form where different) |
| `QUERY-projection` | same definition |  | QUERY-projection (344) |  | names/descriptions match (silo text is a shortened form where different) |
| `QUERY-run-variants` | same definition |  | QUERY-run-variants (38) | boundary bug left in place | Fixing \b next to "(" / "$" revived alternatives such as find()/sort()/NOW()/$ that matched code samples (0/8 to 3/6 on-topic); previous behaviour kept, latent dead alternatives documented |
| `QUERY-saved` | same definition |  | QUERY-saved (49) |  | names/descriptions match (silo text is a shortened form where different) |
| `QUERY-skip-limit` | same definition |  | QUERY-skip-limit (193) | boundary bug left in place | Fixing \b next to "(" / "$" revived alternatives such as find()/sort()/NOW()/$ that matched code samples (0/8 to 3/6 on-topic); previous behaviour kept, latent dead alternatives documented |
| `QUERY-sort` | same definition |  | QUERY-sort (273) | boundary bug left in place | Fixing \b next to "(" / "$" revived alternatives such as find()/sort()/NOW()/$ that matched code samples (0/8 to 3/6 on-topic); previous behaviour kept, latent dead alternatives documented |
| `QUERY-undo-redo` | same definition |  | QUERY-undo-redo (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `QUERY-value-search` | same definition |  | QUERY-value-search (1) |  | names/descriptions match (silo text is a shortened form where different) |
| `QUERY-view-explain` | same definition |  | QUERY-view-explain (72) |  | names/descriptions match (silo text is a shortened form where different) |
| `QUERY-view-gridfs` | same definition |  | QUERY-view-gridfs (14) |  | names/descriptions match (silo text is a shortened form where different) |
| `QUERY-view-json` | same definition |  | QUERY-view-json (715) |  | names/descriptions match (silo text is a shortened form where different) |
| `QUERY-view-split` | same definition |  | QUERY-view-split (13) |  | names/descriptions match (silo text is a shortened form where different) |
| `QUERY-view-table` | same definition |  | QUERY-view-table (377) |  | names/descriptions match (silo text is a shortened form where different) |
| `QUERY-view-tree` | same definition |  | QUERY-view-tree (219) |  | names/descriptions match (silo text is a shortened form where different) |
| `QUERY-vqb-bidirectional` | same definition |  | QUERY-vqb-bidirectional (4) |  | names/descriptions match (silo text is a shortened form where different) |
| `QUERY-vqb-core` | same definition |  | QUERY-vqb-core (302) |  | names/descriptions match (silo text is a shortened form where different) |
| `QUERY-vqb-plan` | same definition |  | QUERY-vqb-plan (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `QUERY-vqb-proj-sort` | same definition |  | QUERY-vqb-proj-sort (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `SCHED-actions` | feed-upstream |  | SCHED-actions (18) | added to silo | Task run/pause/clone/delete; no same-meaning silo ID (SCHED-status-states catches 17%); 9 distinct, 8/8 |
| `SCHED-batch` | child-of | `SCHED-exec-config` | SCHED-exec-config (141) |  | One field of execution config; distinct source evidence; Batch size is one field of SCHED-exec-config; 100% covered |
| `SCHED-cli-headless` | same definition |  | SCHED-cli-headless (4) |  | names/descriptions match (silo text is a shortened form where different) |
| `SCHED-compare-results` | child-of | `GOV-collection-compare` | GOV-collection-compare (146) |  | Compare results view; scheduler-matrix detail; Cross-family duplicate; widen silo GOV-collection-compare instead (catches 3%) |
| `SCHED-compare-schedule` | child-of | `SCHED-task-types` | SCHED-task-types (31) |  | Compare saved as a scheduled task (corrected: not GOV-collection-compare); Cross-family duplicate |
| `SCHED-compare-setup` | child-of | `GOV-collection-compare` | GOV-collection-compare (146) |  | Compare setup step; scheduler-matrix detail; Cross-family duplicate; 155 untagged, 5/5 -> widen silo pattern |
| `SCHED-compare-sync` | child-of | `GOV-collection-sync` | GOV-collection-sync (63) |  | Sync actions from compare results; Cross-family duplicate; widen silo GOV-collection-sync (catches 16%) |
| `SCHED-concurrent` | child-of | `SCHED-exec-config` | SCHED-exec-config (141) |  | One field of execution config; distinct source evidence; Concurrency is one field of SCHED-exec-config |
| `SCHED-cron` | same definition |  | SCHED-cron (12) |  | names/descriptions match (silo text is a shortened form where different) |
| `SCHED-email` | child-of | `SCHED-notifications` | SCHED-notifications (0) |  | Provider-level detail of notifications; Own matrix row: "same evidence as SCHED-notifications" |
| `SCHED-exec-config` | same definition |  | SCHED-exec-config (141) |  | names/descriptions match (silo text is a shortened form where different) |
| `SCHED-history` | feed-upstream |  | SCHED-history (111) | added to silo | Execution history/logs; not covered by SCHED-status-states/progress (10%); 40 distinct, 6/8, vendor docs (DBeaver, VisuaLeaf) |
| `SCHED-history-retention` | analysis-only |  | — |  | Hits are mostly query-history retention, not scheduler |
| `SCHED-notifications` | same definition |  | SCHED-notifications (0) |  | names/descriptions match (silo text is a shortened form where different) |
| `SCHED-plan-limits` | analysis-only |  | — |  | 5/5 but all DBeaver edition banners; single-vendor |
| `SCHED-preset-types` | retire (synonym) | `SCHED-types-time` | SCHED-types-time (76) |  | Identical definition to SCHED-types-time |
| `SCHED-progress` | same definition |  | SCHED-progress (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `SCHED-recur-daily` | child-of | `SCHED-types-time` | SCHED-types-time (76) |  | One recurrence value; matrix keeps per-value evidence; Sub-value of SCHED-types-time; probe ~1/6 precise |
| `SCHED-recur-interval` | child-of | `SCHED-types-time` | SCHED-types-time (76) |  | One recurrence value; matrix keeps per-value evidence; Sub-value; probe 0/5 precise |
| `SCHED-recur-monthly` | child-of | `SCHED-types-time` | SCHED-types-time (76) |  | One recurrence value; matrix keeps per-value evidence; Sub-value of SCHED-types-time |
| `SCHED-recur-once` | child-of | `SCHED-types-time` | SCHED-types-time (76) |  | One recurrence value; matrix keeps per-value evidence; Sub-value of SCHED-types-time |
| `SCHED-recur-weekly` | child-of | `SCHED-types-time` | SCHED-types-time (76) |  | One recurrence value; matrix keeps per-value evidence; Sub-value; probe 2/5 precise |
| `SCHED-retry` | child-of | `SCHED-exec-config` | SCHED-exec-config (141) |  | One field of execution config; distinct source evidence; Retry is one field of SCHED-exec-config |
| `SCHED-script-tasks` | child-of | `SCHED-task-types` | SCHED-task-types (31) |  | One task type with its own unit structure; Script is one of SCHED-task-types; 71% covered |
| `SCHED-status-states` | same definition |  | SCHED-status-states (41) |  | names/descriptions match (silo text is a shortened form where different) |
| `SCHED-task-actions` | retire (synonym) | `SCHED-actions` | SCHED-actions (18) |  | Own matrix row literally says "Alias of SCHED-actions" |
| `SCHED-task-save` | retire (synonym) | `TRANSFER-task-save` | TRANSFER-task-save (69) |  | Same meaning as silo TRANSFER-task-save (cross-family); widen it - catches 5%, 39 distinct uncaught, 8/8 |
| `SCHED-task-types` | same definition |  | SCHED-task-types (31) |  | names/descriptions match (silo text is a shortened form where different) |
| `SCHED-timezone` | same definition |  | SCHED-timezone (5) |  | names/descriptions match (silo text is a shortened form where different) |
| `SCHED-types-time` | same definition |  | SCHED-types-time (76) | widened | pattern narrower than definition; new pattern sampled >= 6/8 |
| `SCHEMA-anomaly-detection` | same definition |  | SCHEMA-anomaly-detection (2) |  | names/descriptions match (silo text is a shortened form where different) |
| `SCHEMA-bson-types` | same definition |  | SCHEMA-bson-types (735) |  | names/descriptions match (silo text is a shortened form where different) |
| `SCHEMA-date-dist` | same definition |  | SCHEMA-date-dist (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `SCHEMA-deploy-validator` | same definition |  | SCHEMA-deploy-validator (7) | widened | pattern narrower than definition; new pattern sampled >= 6/8 |
| `SCHEMA-designer-auto` | same definition |  | SCHEMA-designer-auto (2) |  | names/descriptions match (silo text is a shortened form where different) |
| `SCHEMA-designer-canvas` | same definition |  | SCHEMA-designer-canvas (123) |  | names/descriptions match (silo text is a shortened form where different) |
| `SCHEMA-designer-color` | same definition |  | SCHEMA-designer-color (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `SCHEMA-designer-layouts` | same definition |  | SCHEMA-designer-layouts (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `SCHEMA-designer-links` | same definition |  | SCHEMA-designer-links (5) |  | names/descriptions match (silo text is a shortened form where different) |
| `SCHEMA-designer-portability` | same definition |  | SCHEMA-designer-portability (37) |  | names/descriptions match (silo text is a shortened form where different) |
| `SCHEMA-doc-export` | same definition |  | SCHEMA-doc-export (3) |  | names/descriptions match (silo text is a shortened form where different) |
| `SCHEMA-explore-docs` | same definition |  | SCHEMA-explore-docs (4) | widened | pattern narrower than definition; new pattern sampled >= 6/8 |
| `SCHEMA-field-constraints` | same definition |  | SCHEMA-field-constraints (139) |  | names/descriptions match (silo text is a shortened form where different) |
| `SCHEMA-field-prob` | same definition |  | SCHEMA-field-prob (4) |  | names/descriptions match (silo text is a shortened form where different) |
| `SCHEMA-file-export` | same definition |  | SCHEMA-file-export (1) |  | names/descriptions match (silo text is a shortened form where different) |
| `SCHEMA-geo-analysis` | same definition |  | SCHEMA-geo-analysis (6) |  | names/descriptions match (silo text is a shortened form where different) |
| `SCHEMA-histogram` | same definition |  | SCHEMA-histogram (6) |  | names/descriptions match (silo text is a shortened form where different) |
| `SCHEMA-import-from-db` | same definition |  | SCHEMA-import-from-db (0) |  | names/descriptions match (silo text is a shortened form where different) |
| `SCHEMA-json-editor` | same definition |  | SCHEMA-json-editor (0) |  | names/descriptions match (silo text is a shortened form where different) |
| `SCHEMA-rename-discover` | same definition |  | SCHEMA-rename-discover (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `SCHEMA-sampling` | same definition |  | SCHEMA-sampling (137) |  | names/descriptions match (silo text is a shortened form where different) |
| `SCHEMA-stats-notes` | same definition |  | SCHEMA-stats-notes (2) |  | names/descriptions match (silo text is a shortened form where different) |
| `SCHEMA-top-values` | same definition |  | SCHEMA-top-values (7) |  | names/descriptions match (silo text is a shortened form where different) |
| `SCHEMA-type-prob` | same definition |  | SCHEMA-type-prob (10) |  | names/descriptions match (silo text is a shortened form where different) |
| `SCHEMA-validation-limits` | same definition |  | SCHEMA-validation-limits (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `SCHEMA-validation-model` | same definition |  | SCHEMA-validation-model (54) | boundary-bug fixed | names/descriptions match (silo text is a shortened form where different) |
| `SCHEMA-validation-strictness` | same definition |  | SCHEMA-validation-strictness (18) |  | names/descriptions match (silo text is a shortened form where different) |
| `SCHEMA-validation-ui` | same definition |  | SCHEMA-validation-ui (14) | widened | pattern narrower than definition; new pattern sampled >= 6/8 |
| `SCHEMA-verify` | same definition |  | SCHEMA-verify (4) |  | names/descriptions match (silo text is a shortened form where different) |
| `SCHEMA-view-editor` | same definition |  | SCHEMA-view-editor (10) |  | names/descriptions match (silo text is a shortened form where different) |
| `SCHEMA-view-from-sql` | same definition |  | SCHEMA-view-from-sql (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `SCHEMA-views-tree` | same definition |  | SCHEMA-views-tree (1) |  | names/descriptions match (silo text is a shortened form where different) |
| `SHELL-auto-reconnect` | retire (synonym) | `SHELL-reconnect` | SHELL-reconnect (11) |  | Same definition |
| `SHELL-autocomplete` | same definition |  | SHELL-autocomplete (166) |  | names/descriptions match (silo text is a shortened form where different) |
| `SHELL-background` | same definition |  | SHELL-background (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `SHELL-background-exec` | retire (synonym) | `SHELL-background` | SHELL-background (0) |  | Word-for-word same description as SHELL-background |
| `SHELL-bookmarks` | same definition |  | SHELL-bookmarks (1) |  | names/descriptions match (silo text is a shortened form where different) |
| `SHELL-debugger` | same definition |  | SHELL-debugger (33) |  | names/descriptions match (silo text is a shortened form where different) |
| `SHELL-destructive-guard` | same definition |  | SHELL-destructive-guard (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `SHELL-engine` | same definition |  | SHELL-engine (410) |  | names/descriptions match (silo text is a shortened form where different) |
| `SHELL-history` | same definition |  | SHELL-history (14) |  | names/descriptions match (silo text is a shortened form where different) |
| `SHELL-integrations` | same definition |  | SHELL-integrations (15) | widened | pattern narrower than definition; new pattern sampled >= 6/8 |
| `SHELL-minimap` | same definition |  | SHELL-minimap (1) |  | names/descriptions match (silo text is a shortened form where different) |
| `SHELL-modes` | same definition |  | SHELL-modes (7) |  | names/descriptions match (silo text is a shortened form where different) |
| `SHELL-npm-utils` | same definition |  | SHELL-npm-utils (21) | boundary-bug fixed | names/descriptions match (silo text is a shortened form where different) |
| `SHELL-oidc-auth` | same definition |  | SHELL-oidc-auth (15) | widened | pattern narrower than definition; new pattern sampled >= 6/8 |
| `SHELL-open-from` | retire (synonym) | `SHELL-integrations` | SHELL-integrations (15) |  | Covered by SHELL-integrations ("open from other tools") |
| `SHELL-persistent-vars` | retire (synonym) | `SHELL-sessions-vars` | SHELL-sessions-vars (0) |  | Same definition |
| `SHELL-reconnect` | same definition |  | SHELL-reconnect (11) | widened | pattern narrower than definition; new pattern sampled >= 6/8 |
| `SHELL-result-tab-limit` | same definition |  | SHELL-result-tab-limit (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `SHELL-result-tabs` | same definition |  | SHELL-result-tabs (2) |  | names/descriptions match (silo text is a shortened form where different) |
| `SHELL-result-views` | same definition |  | SHELL-result-views (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `SHELL-run-all` | same definition |  | SHELL-run-all (4) |  | names/descriptions match (silo text is a shortened form where different) |
| `SHELL-run-cursor` | same definition |  | SHELL-run-cursor (11) | widened | pattern narrower than definition; new pattern sampled >= 6/8 |
| `SHELL-run-select` | same definition |  | SHELL-run-select (16) |  | names/descriptions match (silo text is a shortened form where different) |
| `SHELL-save-load` | same definition |  | SHELL-save-load (3) |  | names/descriptions match (silo text is a shortened form where different) |
| `SHELL-sessions` | retire (synonym) | `SHELL-sessions-multi` | SHELL-sessions-multi (10) |  | Same definition |
| `SHELL-sessions-multi` | same definition |  | SHELL-sessions-multi (10) |  | names/descriptions match (silo text is a shortened form where different) |
| `SHELL-sessions-vars` | same definition |  | SHELL-sessions-vars (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `SHELL-storedjs-rename` | same definition |  | SHELL-storedjs-rename (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `SHELL-validation` | same definition |  | SHELL-validation (1) |  | names/descriptions match (silo text is a shortened form where different) |
| `SQL-code-gen` | same definition |  | SQL-code-gen (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `SQL-export-field-map` | same definition |  | SQL-export-field-map (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `SQL-export-monitor` | analysis-only |  | — |  | Probe finds "export to SQL", not monitoring; definition not doc-detectable |
| `SQL-export-relations` | same definition |  | SQL-export-relations (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `SQL-export-targets` | same definition |  | SQL-export-targets (1) |  | names/descriptions match (silo text is a shortened form where different) |
| `SQL-expressions` | same definition |  | SQL-expressions (621) |  | names/descriptions match (silo text is a shortened form where different) |
| `SQL-federated-query` | same definition |  | SQL-federated-query (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `SQL-join-mapping` | same definition |  | SQL-join-mapping (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `SQL-migration` | same definition |  | SQL-migration (67) | widened | pattern narrower than definition; added "SQL migration" (the "SQL to MongoDB" alternative was dropped at acceptance: 5/8) |
| `SQL-migration-1to-many` | child-of | `SQL-migration` | SQL-migration (67) |  | Mapping mode inside the migration wizard; Detail of SQL-migration wizard; 13 distinct uncaught, precision 3/5 (ER-diagram noise) |
| `SQL-migration-1to1` | child-of | `SQL-migration` | SQL-migration (67) |  | Mapping mode inside the migration wizard; Detail of SQL-migration wizard; 6 distinct uncaught |
| `SQL-migration-schema` | child-of | `SQL-migration` | SQL-migration (67) |  | Schema-mapping stage of the migration wizard; Same meaning as SQL-migration; widen pattern (catches 29%; 59 distinct uncaught, 7/8) |
| `SQL-query-manager` | same definition |  | SQL-query-manager (3) |  | names/descriptions match (silo text is a shortened form where different) |
| `SQL-reschema` | same definition |  | SQL-reschema (6) |  | names/descriptions match (silo text is a shortened form where different) |
| `TRANSFER-collection-history` | same definition |  | TRANSFER-collection-history (97) |  | names/descriptions match (silo text is a shortened form where different) |
| `TRANSFER-export-bson` | same definition |  | TRANSFER-export-bson (29) | widened | pattern narrower than definition; new pattern sampled >= 6/8 |
| `TRANSFER-export-csv` | same definition |  | TRANSFER-export-csv (29) |  | names/descriptions match (silo text is a shortened form where different) |
| `TRANSFER-export-excel` | same definition |  | TRANSFER-export-excel (11) |  | names/descriptions match (silo text is a shortened form where different) |
| `TRANSFER-export-json` | same definition |  | TRANSFER-export-json (17) |  | names/descriptions match (silo text is a shortened form where different) |
| `TRANSFER-export-mongo` | same definition |  | TRANSFER-export-mongo (0) |  | names/descriptions match (silo text is a shortened form where different) |
| `TRANSFER-export-sql` | same definition |  | TRANSFER-export-sql (19) |  | names/descriptions match (silo text is a shortened form where different) |
| `TRANSFER-export-sql-stmts` | same definition |  | TRANSFER-export-sql-stmts (1) | boundary-bug fixed | names/descriptions match (silo text is a shortened form where different) |
| `TRANSFER-export-src` | same definition |  | TRANSFER-export-src (57) |  | names/descriptions match (silo text is a shortened form where different) |
| `TRANSFER-field-mapping` | same definition |  | TRANSFER-field-mapping (78) |  | names/descriptions match (silo text is a shortened form where different) |
| `TRANSFER-gridfs-crud` | same definition |  | TRANSFER-gridfs-crud (22) |  | names/descriptions match (silo text is a shortened form where different) |
| `TRANSFER-import-bson` | same definition |  | TRANSFER-import-bson (89) |  | names/descriptions match (silo text is a shortened form where different) |
| `TRANSFER-import-csv` | same definition |  | TRANSFER-import-csv (40) |  | names/descriptions match (silo text is a shortened form where different) |
| `TRANSFER-import-json` | same definition |  | TRANSFER-import-json (56) |  | names/descriptions match (silo text is a shortened form where different) |
| `TRANSFER-import-modes` | same definition |  | TRANSFER-import-modes (16) |  | names/descriptions match (silo text is a shortened form where different) |
| `TRANSFER-import-mongo` | same definition |  | TRANSFER-import-mongo (2) |  | names/descriptions match (silo text is a shortened form where different) |
| `TRANSFER-import-sql` | same definition |  | TRANSFER-import-sql (3) |  | names/descriptions match (silo text is a shortened form where different) |
| `TRANSFER-incremental` | same definition |  | TRANSFER-incremental (7) |  | names/descriptions match (silo text is a shortened form where different) |
| `TRANSFER-masking-inline` | same definition |  | TRANSFER-masking-inline (6) |  | names/descriptions match (silo text is a shortened form where different) |
| `TRANSFER-masking-tool` | same definition |  | TRANSFER-masking-tool (13) |  | names/descriptions match (silo text is a shortened form where different) |
| `TRANSFER-masking-types` | same definition |  | TRANSFER-masking-types (17) |  | names/descriptions match (silo text is a shortened form where different) |
| `TRANSFER-plan-limits` | analysis-only |  | — |  | Probe 1/5; single-vendor |
| `TRANSFER-task-save` | same definition |  | TRANSFER-task-save (69) | widened | pattern narrower than definition; new pattern sampled >= 6/8 |
| `TRANSFER-test-data-gen` | same definition |  | TRANSFER-test-data-gen (55) |  | names/descriptions match (silo text is a shortened form where different) |
| `TRANSFER-transform-filter` | same definition |  | TRANSFER-transform-filter (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `TRANSFER-transform-js` | same definition |  | TRANSFER-transform-js (0) | no corpus evidence; pattern kept | 0 docs; definition probe < 5 docs or < 6/8 |
| `TRANSFER-transform-pipeline` | same definition |  | TRANSFER-transform-pipeline (5) | widened | pattern narrower than definition; new pattern sampled >= 6/8 |
| `TRANSFER-transform-types` | same definition |  | TRANSFER-transform-types (1) |  | names/descriptions match (silo text is a shortened form where different) |

<!-- END GENERATED TABLE -->
