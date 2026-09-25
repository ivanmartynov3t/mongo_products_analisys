# Coverage check (issue #30): silo Policy Engine / PII Scanner vs our 3T Lens / 3T MCP pages

**Status:** findings from 2026-09-25, silo commit `cde319c742`. Nothing here has changed a matrix yet. Every gap and contradiction is a ❓ lead until a person verifies it against a public or product source, and only then edits the matrix.

## Navigation

- [Coverage scope decision](../docs/coverage-scope.md) · [3T Lens governance matrix](../products/3t/3t-lens/features/governance/feature-matrix.md) · [3T MCP AI matrix](../products/3t/3t-mcp/features/ai/feature-matrix.md)

Scope note (from the files, not inferred beyond them):
- `policy-engine` silo = the `3tio/tools` monorepo ("3T Tools"): Policy Engine, PII Detector (Go) + PII Scanner (Rust), AI Helper, and a Rust MCP server. The brochure names the PII component "3T Lens PII Scanner", so it is compared with our **3T Lens** pages.
- `pii-scanner` silo = `3tio/pii-scanner-lab`. Its `docs/` and `releases/` describe the `stt-cli` binary ("3T MCP documentation", "First public release of 3t-mcp"), so they are compared with our **3T MCP** pages. Its `README.md` / `benches/` describe an internal benchmark harness (`pslab`) and are excluded as internal engineering.
- Our pages cite only studio3t.com (S1). None cite the silo.

Source-URL prefixes: `TOOLS` = `https://github.com/3tio/tools/blob/566d6f25c16450aa449bdf5c614be7ff7d0e8c7c/`; `LAB` = `https://github.com/3tio/pii-scanner-lab/blob/35ab6bb5f42cb9578482bec928d62fac2d663ca9/`. Silo paths are relative to `prod_info_silo/data/3t/`.

Our files: Lens matrix = `products/3t/3t-lens/features/governance/feature-matrix.md`; MCP matrix = `products/3t/3t-mcp/features/ai/feature-matrix.md`.

## Component 1: Policy Engine + PII Detector/Scanner (vs 3T Lens)

| # | Capability | Shipped? | Our row(s) | Verdict | Gap detail | Evidence |
|---|---|---|---|---|---|---|
| 1 | Policy templates by category (ACID, SCHEMA, INDEX, SECURITY, NAMING, OPERATIONAL), enable/disable, custom connection-level policy editor | Shipped (`[x]`) | GOV-002 (Lens matrix) | Partly covered | Categories match. Missing: custom policy editor, enable/disable, 17 evaluators, template count. Count conflict inside silo: features/README says 27 templates, integration guide says 26. | `policy-engine/repo_docs/features/README.md` (TOOLS`features/README.md`); `policy-engine/repo_docs/docs/policy-engine-integration.md` (TOOLS`docs/policy-engine-integration.md`) |
| 2 | Built-in evaluators with specific checks (write concern, auth enabled, TTL compliance, redundant/unused index, ESR ordering, replication lag, slow queries, schema type consistency, threshold check) | Shipped (`[x]`) | GOV-002, GOV-006 (Lens matrix) | Partly covered | GOV-006 says only "Index recommendations"; engine details marked "unverified". The docs name the index evaluators (unused, redundant, ESR, no-COLLSCAN). | same two files as #1 |
| 3 | Compliance dashboard with score and open-violation summary | Shipped (`[x]`) | GOV-002 ("one-click compliance health check") | Partly covered | Compliance score and dashboard not mentioned. | `policy-engine/repo_docs/features/README.md` |
| 4 | Violations list with acknowledgement flow | Shipped (`[x]`) | none | Not covered | — | `policy-engine/repo_docs/features/README.md` |
| 5 | Violation observability for admins (actor/client/app/request context) + retention rules (platform/tenant/policy, 1–3650 days, 90-day default) | Status unclear (operator guide describes it as present; not in the features checklist) | none | Not covered | — | `policy-engine/repo_docs/docs/violation-observability-operator-guide.md` (TOOLS`docs/violation-observability-operator-guide.md`) |
| 6 | Alert channels: Slack, email (with recipients), webhook; delivery test | Shipped (`[x]`) | GOV-003 (Lens matrix) | Covered | Only minor: "configurable severity levels per channel" is not stated in the silo docs read (neither confirmed nor contradicted). | `policy-engine/repo_docs/features/README.md` |
| 7 | Scheduled `POLICY_EVALUATE` task type (with email delivery) | Shipped (`[x]`) | none | Not covered | — | `policy-engine/repo_docs/features/README.md`; `policy-engine/repo_docs/docs/policy-engine-integration.md` |
| 8 | Operation-level policies / policy gate blocking task creation | Planned (`[ ]`, "engine ready, client not yet wired") | none | Not covered (correctly absent) | Could be listed as roadmap. | `policy-engine/repo_docs/features/README.md` |
| 9 | PII scan workspace: scan from sidebar/context menu, results in 4 buckets (Critical / PII / Potentially Sensitive / Likely Safe), 5-tab field detail, history, delete | Shipped (`[x]`) | GOV-004 (Lens matrix) | Partly covered | "Sensitivity grouping" and "timestamped scan records" match; the four named buckets, per-field detail tabs and history/delete are missing. | `policy-engine/repo_docs/features/README.md`; `policy-engine/repo_docs/docs/pii-detector-integration.md` (TOOLS`docs/pii-detector-integration.md`) |
| 10 | Detection method: field-name + value patterns (Luhn PAN, IBAN, BIC, EU national IDs), confidence score, plus neural NER on free text; NLP degradation flagged per scan | Name/value regex: Shipped (`[x]`). NER + 17 categories: described in brochure v0.8 and beta readiness (design-partner beta) | GOV-004 (Lens matrix); product-report "uses heuristics" | Partly covered | Our page reduces it to "heuristics". Detection method, confidence score, NER layer and per-scan NLP flag are missing. | `policy-engine/repo_docs/features/README.md`; `policy-engine/repo_docs/docs/pii-scanner-brochure/3T-Lens-PII-Scanner-Brochure-v0.8.md` (TOOLS`docs/pii-scanner-brochure/3T-Lens-PII-Scanner-Brochure-v0.8.md`); `policy-engine/repo_docs/docs/release-readiness/pii-scanner-beta-readiness.md` (TOOLS`docs/release-readiness/pii-scanner-beta-readiness.md`) |
| 11 | Regulation hints (GDPR/CCPA; brochure adds HIPAA) and NIST SP 800-122 impact/identifiability enrichment | GDPR/CCPA: Shipped (`[x]`). NIST/HIPAA: brochure only, status unclear | GOV-004 | Not covered | Not mentioned. | features/README.md; brochure v0.8 |
| 12 | Redacted samples; raw values visible only to platform admin / compliance auditor; role-tiered masking of returned documents | Per beta readiness: redaction at source passes; brochure describes role tiering. Role-tier masking status unclear outside brochure | none | Not covered | — | brochure v0.8; beta-readiness.md |
| 13 | Compliance export (CSV/JSON) + org-wide posture view + `COMPLIANCE_AUDITOR` role | Shipped per beta readiness ("Both shipped. COM-D1 … COM-D2 … are closed") | none | Not covered | — | `policy-engine/repo_docs/docs/release-readiness/pii-scanner-beta-readiness.md` |
| 14 | Append-only audit trail of scan lifecycle (admin API, SIEM shipping) | Beta readiness says M1–M3 shipped incl. G6 (audit events); brochure describes it | GOV-004 ("scan records with timestamps provide an audit trail") | Partly covered | Our "audit trail" is scan timestamps only. The docs describe an append-only, admin-queryable event log. | beta-readiness.md; `policy-engine/repo_docs/docs/release-readiness/pii-scanner-beta-plan.md` (TOOLS`docs/release-readiness/pii-scanner-beta-plan.md`); brochure v0.8 |
| 15 | Sampling controls and coverage: sample size (brochure: default 5,000), full-collection scan, "N of M docs" coverage line, sample cap | Shipped per beta readiness (G4, G7 in M1–M3) | none | Not covered | — | beta-plan.md; beta-readiness.md; brochure v0.8 |
| 16 | PII classification policy: admin-edited frameworks/type rules and per-field bucket pins | Status unclear (documented endpoints; not in checklist) | none | Not covered | — | `policy-engine/repo_docs/docs/pii-detector-integration.md` |
| 17 | Governance Proxy integration: findings feed the proxy's PII cache; fail-closed `REQUIRE_PII` guardrail | Shipped per beta readiness (G5, M1) | none | Not covered | — | beta-plan.md; beta-readiness.md; brochure v0.8 |
| 18 | MCP tools governed by access mode (`MCP_ACCESS_MODE` read/write/admin, default read); tool list per category | Shipped (`[x]` MCP Server section) | GOV-007 (Lens matrix); product-report | Contradicts (count) + Partly covered | Silo says "Complete Tool Reference (60 tools)". Our page says 59 and "full tool list unknown". The silo gives the full list. The silo gating mechanism is a read/write/admin access mode plus Access Manager connection visibility. Our wording "same 3T Access role policies" is not stated in these docs. | `policy-engine/repo_docs/docs/mcp-access-control.md` (TOOLS`docs/mcp-access-control.md`); features/README.md |
| 19 | AI Helper in-app chat with governance/PII tools, access-mode pill and tool-call approval (Ask on writes, etc.) | Shipped (`[x]`) | none on Lens pages | Not covered | The silo does not name this as a 3T Lens capability, so it belongs on Lens only if Lens = this frontend. | features/README.md |

Out of scope (no Lens-page counterpart expected): viewer/compare/tasks/import/profiler/lab features in the same monorepo; OpenAPI Phase 2–4 (planned); internal build, CI and benchmarks.

## Component 2: 3T MCP / `stt-cli` (pii-scanner-lab silo, vs 3T MCP)

| # | Capability | Shipped? | Our row(s) | Verdict | Gap detail | Evidence |
|---|---|---|---|---|---|---|
| 1 | Single binary: CLI + MCP server over stdio for Claude Desktop, Cursor, VS Code | Shipped (v0.2.1 "First public release") | AI-010 (MCP matrix) | Covered | — | `pii-scanner/repo_docs/docs/index.md` (LAB`docs/index.md`); `pii-scanner/repo_docs/releases/v0.2.1.md` (LAB`releases/v0.2.1.md`) |
| 2 | Login/logout to a 3T account via browser, session stored locally; call-home authorisation, JWT signature verification | Shipped (v0.2.2) | AI-010 | Covered (partly) | Call-home authorisation step and JWT verification not mentioned. | `pii-scanner/repo_docs/docs/cli-reference.md` (LAB`docs/cli-reference.md`); `pii-scanner/repo_docs/releases/0.2.2.md` (LAB`releases/0.2.2.md`) |
| 3 | EULA acceptance required on first data command / tool call | Shipped (0.2.3) | none | Not covered | — | `pii-scanner/repo_docs/releases/0.2.3.md` (LAB`releases/0.2.3.md`) |
| 4 | Multi-connection `connections.yaml` (`connections list/add/remove`, `env:` credentials, `--config` per project, strict key validation) | Shipped (v0.2.1, 0.2.3) | none | Not covered | Our page does not describe how connections are configured. | cli-reference.md; releases/0.2.3.md; releases/v0.2.1.md |
| 5 | List databases / collections (with stats) / indexes | Shipped (v0.2.1) | AI-011 | Partly covered | `list_indexes` / `indexes list` not mentioned. | releases/v0.2.1.md; cli-reference.md |
| 6 | Find query execution and explain | Shipped (v0.2.1) | AI-011 | Covered | — | releases/v0.2.1.md; cli-reference.md |
| 7 | Aggregation pipeline execution with pagination and response-size limits | Shipped (v0.2.1) | none | Not covered | AI-011 lists find only; `aggregate` tool missing. | releases/v0.2.1.md; cli-reference.md |
| 8 | Write capability behind opt-in: `--allow-writes` on `mcp` and `aggregate execute` (`$out`/`$merge` otherwise rejected); per-query/aggregate document and byte limits | Documented in CLI reference (current docs); release in which it arrived is unclear | AI-011 ("Strictly read-only … not configurable"); product report | Contradicts | The docs show a configurable write opt-in. Read-only is the default, not a fixed limit. | `pii-scanner/repo_docs/docs/cli-reference.md` |
| 9 | Schema analysis: occurrence probability, BSON type breakdown, top values, numeric bins; sample size and method (random/first/last/all) | Shipped (v0.2.1) | AI-011 | Partly covered | Sampling options and statistics not described. | `pii-scanner/repo_docs/docs/analyze-schema.md` (LAB`docs/analyze-schema.md`) |
| 10 | PII scan: 8 name categories + value patterns (email, phone, IBAN, card with Luhn, JWT, IPv4/6, bcrypt, UUID), confidence 0–1, GDPR/PCI-DSS hints, redacted samples, `--deep-scan`, `--json` | Shipped (v0.2.1) | AI-011; product report | Contradicts (method) + Partly covered | Our page says the method is "unspecified … vendor does not publish". `docs/scan-pii.md` documents it as two passes, field-name then value pattern. Regulation hints, redaction and JSON output are missing. | `pii-scanner/repo_docs/docs/scan-pii.md` (LAB`docs/scan-pii.md`) |
| 11 | Self-update (`stt-cli update`) and update notice | Shipped (0.2.3 fix to notice) | none | Not covered | — | cli-reference.md; releases/0.2.3.md |
| 12 | Troubleshooting/error hints (connection, config, timeout, MCP client setup) | Shipped (0.2.3 "Clearer … error hints") | none | Not covered (low priority) | — | `pii-scanner/repo_docs/docs/troubleshooting.md` (LAB`docs/troubleshooting.md`); releases/0.2.3.md |

Roadmap: `pii-scanner/repo_docs/ROADMAP.md` (LAB`ROADMAP.md`) describes an architecture that pushes risk tags to OpenMetadata. It does not say whether this is planned or shipped, so its status is unclear. Our pages do not mention it.

## Verdict counts

- Lens (19): Covered 1 · Partly covered 6 · Not covered 11 (one of them correctly absent because it is planned) · Contradicts 1 (#18, also partly covered)
- MCP (12): Covered 3 (one with a minor gap) · Partly covered 2 · Not covered 5 · Contradicts 2 (#8 read-only claim; #10 "method unpublished")

## Concrete gaps to fix

1. 3T MCP AI-011 and the product report: replace "Strictly read-only … not configurable" with "read-only by default; `--allow-writes` opt-in", and add the query/aggregate limits (cli-reference.md).
2. 3T MCP AI-011: document the PII method (name categories + value patterns, confidence, GDPR/PCI-DSS hints, redaction) and remove "mechanism unpublished" (scan-pii.md).
3. 3T MCP: add the `aggregate` and `list_indexes` tools, `connections.yaml` multi-connection config, EULA requirement and `update` (v0.2.1, 0.2.3).
4. 3T Lens GOV-007: the silo says 60 tools and lists them all. It gates tools by a read/write/admin access mode. Fix the count and resolve the "unknown breakdown" question (mcp-access-control.md).
5. 3T Lens GOV-004: add the four buckets, detection method (incl. NER, beta), regulation/NIST enrichment, masking/redaction, CSV/JSON export, compliance-auditor org view, append-only audit trail, coverage reporting, and Governance Proxy PII-cache/`REQUIRE_PII` integration. Mark beta status per the readiness doc ("Conditional GO for a design-partner beta").
6. 3T Lens: add rows for the violations list/acknowledgement, violation observability and retention, the compliance score dashboard, and scheduled `POLICY_EVALUATE` tasks. Add the task-creation policy gate as roadmap.
7. 3T Lens GOV-006: name the index evaluators (unused, redundant, ESR, COLLSCAN) instead of "unverified".
8. Add silo sources to the Source index of both matrices. Today only studio3t.com is cited.
