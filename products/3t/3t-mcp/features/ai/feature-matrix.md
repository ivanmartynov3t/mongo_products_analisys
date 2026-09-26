# Feature Matrix — 3T MCP / AI Features

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Feature metadata

- Product name: 3T MCP
- Product group: 3t
- Feature ID: F-AI (see [feature-dictionary.md](../../../../../feature-dictionary.md))
- Feature folder: `ai`
- Analysis date: 2026-09-25
- Version/release context: —

## Source index

Every fact in the matrix carries its own `(S#)`. **Public** sources can be opened by any reader; **internal** sources are private 3T repositories, read through `prod_info_silo`.

Public:

- S1: https://studio3t.com/3t-mcp/ — product page (silo: `data/3t/3t-mcp/3t-mcp.md@6f6e0f57`, captured 2026-09-10)
- S2: https://github.com/3tio/3t-mcp-releases — public releases repository, README (read 2026-09-25)
- S3: https://github.com/3tio/3t-mcp-releases/releases — release notes: v0.2.1 (2026-05-27), 0.2.2 (2026-05-29), 0.2.3 (2026-07-17)

Internal (same text also in the private `3tio/3t-build-mcp-server` repository; silo `data/3t/pii-scanner`):

- S4: https://github.com/3tio/pii-scanner-lab/blob/35ab6bb5f42cb9578482bec928d62fac2d663ca9/docs/cli-reference.md
- S5: https://github.com/3tio/pii-scanner-lab/blob/35ab6bb5f42cb9578482bec928d62fac2d663ca9/docs/scan-pii.md
- S6: https://github.com/3tio/pii-scanner-lab/blob/35ab6bb5f42cb9578482bec928d62fac2d663ca9/docs/analyze-schema.md

## Capability matrix

| Capability ID | Capability | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AI-010 | 3T MCP — standalone binary | Supported | Binary `stt-cli`, distributed via GitHub releases `3tio/3t-mcp-releases` (S1, S2). macOS/Linux: curl installer script; Windows: PowerShell installer script (S1, S2). Runs locally as a standard MCP stdio process (S2); stdio, unlike the Desktop IDE's HTTP MCP server (S1). Auth: `stt-cli login`, browser-based, credentials stored locally; requires a 3T account (S1, S2). | Requires a 3T account (free registration) (S1). HTTP-only clients need a bridge adapter. | confirmed (public) (S1, S2) | S1, S2 | Standalone product; separate install. |
| AI-011 | 3T MCP — capabilities | Supported | Collection browsing: list databases and collections (S1, S2). Index listing, `list_indexes` (S2). Find queries and query-plan explain (S1, S2). Aggregation pipelines with document and byte caps — `--max-documents-per-aggregate` default 100, `--max-bytes-per-aggregate` default 16 MB (S2). Schema analysis: field names, BSON types, occurrence rates, nested structure; `sampleSize` 10–10000 (default 1000) and `sampleMethod` random / first / last / all (S2). PII scanner (see Notes) (S1, S2). Runs entirely locally — no cloud intermediary, no outbound data flow (S1, S2). | **Write behaviour — two public sources disagree:** the product page says "Every tool is strictly read-only" and "read-only — always" (S1); the releases README says write stages (`$out`, `$merge`) are "disabled by default" and allowed when the server starts with `--allow-writes` (S2). This matrix records "read-only by default, writes opt-in" (S2). PII results need human review. | confirmed (public) (S1, S2) | S1, S2, S4, S6 | Top values and numeric bins in schema output appear only internally (S6) — ❓ internal only. PII method (S2, also S5): classifies each field by name in 8 categories (`secret`, `direct_pii`, `contact_pii`, `name_pii`, `financial`, `health`, `sensitive_demographic`, `location`), then value patterns (email, phone, IBAN, credit card with Luhn check, JWT, IPv4/6, bcrypt hash, UUID and more); confidence score 0–1; GDPR / PCI-DSS hints; redacted samples; `deepScan` collects 200 string samples per field instead of 50. |
| AI-013 | 3T MCP — connection config and lifecycle | Supported | Named connections in `~/.stt-mcp/connections.yaml`, each with a short ID; `connections add/list/remove`; `env:` prefix reads a password from an environment variable; `--config PATH` for a custom file; `--validate` checks the file (S2). Unknown keys rejected since 0.2.3 (S3). EULA (v1.0) acceptance required on the first CLI data command or MCP tool call, since 0.2.3 (S3). Self-update with `stt-cli update` (S2); update notice on the first run after a release, since 0.2.3 (S3). | EULA must be accepted before any data access (S3). `connections.yaml` is plain text (S2). | confirmed (public) (S2, S3) | S2, S3, S4 | Same details in the internal CLI reference (S4). |

## Feature-level conclusion

### Confirmed strengths

- stdio transport broadens AI coding environment compatibility versus HTTP-only servers.
- Read-only by default (writes need an explicit `--allow-writes`) plus local-only execution minimizes risk for AI agent automation.

### Confirmed limitations

- Requires a 3T account (OAuth login).
- PII scanner results require human review (field-name plus value-pattern heuristics with a confidence score; S2).

### Open questions / unknowns

- Pricing/licensing terms for the 3T account requirement.
- Write behaviour: the product page says always read-only (S1), the releases README documents `--allow-writes` (S2). Which is intended?
