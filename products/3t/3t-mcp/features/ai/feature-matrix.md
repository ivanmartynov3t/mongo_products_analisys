# Feature Matrix — 3T MCP / AI Features

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Source index

- S1: https://studio3t.com/3t-mcp/

## Capability matrix

| Capability ID | Capability | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AI-010 | 3T MCP — standalone binary | Supported | Binary: stt-cli. Distributed via GitHub releases (3tio/3t-mcp-releases). macOS/Linux install: curl installer script. Windows install: PowerShell installer script. Transport: stdio (unlike Desktop IDE's HTTP MCP server). Auth: stt-cli login → browser-based OAuth; credentials stored locally; requires 3T account. | Requires a 3T account (free registration). stdio transport; HTTP-only clients need a bridge adapter. | confirmed | S1 | Standalone product; separate install. |
| AI-011 | 3T MCP — capabilities | Supported | Collection browsing (list all databases and collections), Query execution (run find queries; explain query plan), Schema analysis (full field shapes, types, nested structures), PII scanner (finds fields potentially containing PII across collections). Strictly read-only — no writes, deletes, or modifications. Runs entirely locally — no cloud intermediary, no outbound data flow. | Read-only constraint is by design and not configurable. PII scanner identifies candidate fields using an unspecified heuristic approach (the vendor does not publish the exact matching mechanism — e.g., whether it's name-based, pattern-based, or both); results require human review. | confirmed | S1 | Standalone product. |

## Feature-level conclusion

### Confirmed strengths

- stdio transport broadens AI coding environment compatibility versus HTTP-only servers.
- Read-only design plus local-only execution minimizes risk for AI agent automation.

### Confirmed limitations

- Requires a 3T account (OAuth login).
- PII scanner results require human review (heuristic-based; exact matching mechanism unpublished).

### Open questions / unknowns

- Pricing/licensing terms for the 3T account requirement.
