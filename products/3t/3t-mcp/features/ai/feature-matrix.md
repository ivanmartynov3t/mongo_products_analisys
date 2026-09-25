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
- Analysis date: 2026-07-29
- Version/release context: —

## Source index

- S1: https://studio3t.com/3t-mcp/
- S2: https://github.com/3tio/pii-scanner-lab/blob/35ab6bb5f42cb9578482bec928d62fac2d663ca9/docs/cli-reference.md (internal repo, via prod_info_silo `data/3t/pii-scanner`)
- S3: https://github.com/3tio/pii-scanner-lab/blob/35ab6bb5f42cb9578482bec928d62fac2d663ca9/docs/scan-pii.md (internal repo)
- S4: https://github.com/3tio/pii-scanner-lab/blob/35ab6bb5f42cb9578482bec928d62fac2d663ca9/docs/analyze-schema.md (internal repo)
- S5: https://github.com/3tio/pii-scanner-lab/blob/35ab6bb5f42cb9578482bec928d62fac2d663ca9/releases/0.2.3.md and releases/v0.2.1.md (internal repo)

## Capability matrix

| Capability ID | Capability | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AI-010 | 3T MCP — standalone binary | Supported | Binary: stt-cli. Distributed via GitHub releases (3tio/3t-mcp-releases). macOS/Linux install: curl installer script. Windows install: PowerShell installer script. Transport: stdio (unlike Desktop IDE's HTTP MCP server). Auth: stt-cli login → browser-based OAuth; credentials stored locally; requires 3T account. | Requires a 3T account (free registration). stdio transport; HTTP-only clients need a bridge adapter. | confirmed | S1 | Standalone product; separate install. |
| AI-011 | 3T MCP — capabilities | Supported | Collection browsing (list databases and collections, with stats), index listing (`indexes list` / `list_indexes`, S2), query execution (run find queries; explain query plan), aggregation pipeline execution with pagination and response-size limits (`aggregate execute`, S2), schema analysis (field shapes, types, nested structures; occurrence probability, BSON type breakdown, top values, numeric bins; sample size and method random/first/last/all, S4), PII scanner (see Notes). Read-only by default: write stages (`$out`, `$merge`) are rejected unless `--allow-writes` is passed to `mcp` or `aggregate execute` (S2). Runs entirely locally — no cloud intermediary, no outbound data flow. | Read-only is the default, not a fixed limit — writes are an explicit opt-in (S2; S1 describes the product as strictly read-only). Per-query document and byte limits apply (S2). PII results require human review. | confirmed (S1 items); ❓ unverified against a public source (internal repo docs only, #31) for S2–S4 additions | S1, S2, S3, S4 | PII method (S3): two passes — field-name signals in 8 categories, then value patterns (email, phone, IBAN, card with Luhn check, JWT, IPv4/IPv6, bcrypt, UUID); confidence score 0–1; GDPR / PCI-DSS hints per field; redacted samples; `--deep-scan` and `--json` options. Replaces the earlier "mechanism unpublished" note (#31). |
| AI-013 | 3T MCP — connection config and lifecycle | Supported | Multiple named connections in `connections.yaml` (`connections list/add/remove`, `env:` credential references, per-project `--config`, strict key validation); EULA acceptance required on the first data command or MCP tool call (v1.0, opens a browser page); self-update with `stt-cli update` and an update notice. | EULA must be accepted before any data access. | ❓ unverified against a public source (internal repo docs only, #31) | S2, S5 | Introduced in releases v0.2.1–0.2.3 (S5). |

## Feature-level conclusion

### Confirmed strengths

- stdio transport broadens AI coding environment compatibility versus HTTP-only servers.
- Read-only by default (writes need an explicit `--allow-writes`) plus local-only execution minimizes risk for AI agent automation.

### Confirmed limitations

- Requires a 3T account (OAuth login).
- PII scanner results require human review (field-name plus value-pattern heuristics with a confidence score; S3).

### Open questions / unknowns

- Pricing/licensing terms for the 3T account requirement.
