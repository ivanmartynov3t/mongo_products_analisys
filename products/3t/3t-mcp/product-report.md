# Product Report — 3T MCP

## Navigation

- [Repository README](../../../README.md)
- [Feature dictionary](../../../feature-dictionary.md)
- [3T products index](../README.md)
- [High-level comparison](../../../reports/comparisons/high-level-product-comparison.md)
- [Low-level comparison](../../../reports/comparisons/low-level-feature-comparison.md)

## Product metadata

- Product name: 3T MCP
- Product group: 3t
- Website: https://studio3t.com/3t-mcp/
- Maker: 3T Software Labs
- Category: Standalone MCP server binary (stdio transport) for AI agent access to MongoDB
- Analysis date: 2026-06-22
- Version/release context: Distributed via GitHub releases (3tio/3t-mcp-releases); standalone binary `stt-cli`. Split out of the Studio 3T product report into its own product folder 2026-07-29 (was previously documented as a sub-section of Studio 3T's AI Features).

## Product summary

3T MCP is a standalone command-line binary (`stt-cli`) that exposes read-only MongoDB access to AI coding agents via the Model Context Protocol over stdio transport. It is distributed independently via GitHub releases and requires a free 3T account (browser-based OAuth login). Its capability surface is strictly read-only: collection/database browsing, find query execution and explain, full schema analysis, and a PII scanner that flags fields potentially containing personally identifiable information. It runs entirely locally with no cloud intermediary for MongoDB data.

It is architecturally distinct from the Studio 3T Desktop IDE's built-in Local MCP Server (HTTP transport, no auth required for local loopback access) — see [Studio 3T's AI feature matrix](../studio-3t/features/ai/feature-matrix.md) (AI-007–AI-009). Per studio3t.com, 3T MCP is one of three products in the "Build" track, alongside the Studio 3T Desktop IDE and 3T Explore; "Build" is the product track name, not a product name.

## Feature inventory

Feature IDs and folder names from [feature-dictionary.md](../../../feature-dictionary.md).

| Feature ID | Feature | Matrix | Report | Status |
| --- | --- | --- | --- | --- |
| F-AI | AI Features | [feature-matrix.md](features/ai/feature-matrix.md) | [feature-report.md](features/ai/feature-report.md) | Completed |

## Product-level conclusions

### Strategic strengths

- stdio transport is compatible with a wider range of AI coding environments than HTTP-only MCP servers.
- Read-only by design (no writes/deletes/modifications) limits blast radius for autonomous AI agent use.
- Runs entirely locally with no cloud intermediary — reduces data exposure for MongoDB data itself.
- Built-in PII scanner surfaces candidate PII fields without requiring a separate governance product.

### Strategic risks / gaps

- Requires a 3T account (OAuth login) — an extra credential/dependency versus the Desktop IDE's Local MCP Server, which needs no auth for local loopback access.
- PII scanner identifies candidate fields by name/pattern heuristics only; results require human review and are not an authoritative compliance determination.
- stdio-only transport means HTTP-only MCP clients need a bridge adapter.

### Open questions

- Full pricing/licensing terms for the required 3T account are unverified.
- Whether stt-cli capabilities evolve independently of, or in lockstep with, the Desktop IDE's Local MCP Server tool list is unverified.
