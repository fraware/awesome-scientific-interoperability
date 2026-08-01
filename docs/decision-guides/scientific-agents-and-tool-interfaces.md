# Scientific agents and tool interfaces

Compare general agent-tool protocols, scientific tool platforms, and emerging watchlist candidates. Catalog entries: [resource:model-context-protocol-mcp], [resource:tooluniverse].

**Primary sources inspected:** [MCP specification 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28), [ToolUniverse documentation](https://zitniklab.hms.harvard.edu/ToolUniverse/en/), watchlist entries [Agent2Agent (A2A)](https://a2a-protocol.org/v1.0.0/), [IEEE P3971](https://standards.ieee.org/ieee/3971/12500/), [Science Context Protocol (arXiv)](https://arxiv.org/abs/2512.24189), [SciToolAgent repository](https://github.com/hicai-zju/scitoolagent).

## Critical boundary

**Agent-tool invocation does not establish scientific validity, authorization, provenance, or safe physical execution.** A successful MCP `tools/call` or ToolUniverse invocation only means the wire protocol accepted a request—it does not verify that:

- the tool implementation matches published methods;
- the caller is permitted to access underlying data or instruments;
- outputs were recorded in an audit-grade provenance graph;
- laboratory or clinical actions are safe, approved, or reversible.

Layer [resource:w3c-prov] / [resource:workflow-run-ro-crate] for evidence, [resource:ga4gh-passports] / DUO for authorization, and laboratory governance for physical actuation.

## Catalogued resources

| Resource | Maturity (catalog, 2026-08-01) | Role | Limitations |
|----------|-------------------------------|------|-------------|
| [resource:model-context-protocol-mcp] | Emerging (`review_due_on: 2027-01-31`) | General capability discovery, tools, resources, prompts between clients and servers | Domain-agnostic; scientific semantics require profiles; not an authz framework |
| [resource:tooluniverse] | Emerging (`review_due_on: 2027-01-31`) | Scientific tool discovery, invocation, composition across APIs/models/datasets | Platform-centered; documents MCP integration but independent schema reuse still maturing |

Both entries were reviewed **as of 2026-08-01** against published specifications and reference implementations. Re-check specification versions before production commitments.

## Emerging watchlist candidates (not main-list resources)

These appear on the repository [watchlist](../watchlist.md) only. **Do not treat them as production standards solely because they are listed here.**

| Candidate | As-of status (2026-08-01) | Notes |
|-----------|---------------------------|-------|
| [Agent2Agent (A2A) Protocol](https://a2a-protocol.org/v1.0.0/) | Emerging multi-agent messaging | Monitor for substantive scientific adoption; no catalog entry yet |
| [IEEE P3971](https://standards.ieee.org/ieee/3971/12500/) | Unpublished IEEE draft project | Not a finished standard; do not specify as mandatory |
| [Science Context Protocol](https://arxiv.org/abs/2512.24189) | Preprint / proposal (2025) | Monitor alongside IEEE P3971; no normative spec in catalog |
| [SciToolAgent](https://github.com/hicai-zju/scitoolagent) | Research reference architecture | Useful as an example system, not a foundational interchange standard |

## Comparison dimensions

| Dimension | [resource:model-context-protocol-mcp] | [resource:tooluniverse] |
|-----------|--------------------------------------|-------------------------|
| **Primary artifact** | JSON-RPC-style client/server protocol for tools/resources | Curated scientific tool graph with invocation adapters |
| **Scope** | Domain-agnostic agent surface | Life-sciences and multi-domain scientific tools |
| **Discovery** | Server-advertised capability lists | Platform registry with metadata |
| **Scientific semantics** | Requires domain profiles and careful tool descriptions | Embeds scientific tool metadata; still agent-mediated |
| **Conformance** | Documented tests for protocol; emerging ecosystem | No public conformance suite catalogued |
| **Strongest use case** | Expose vetted APIs to agent clients with a common wire format | Orchestrate heterogeneous scientific tools in research agents |
| **Inappropriate use case** | Sole authorization layer for controlled data | Replacement for workflow languages ([resource:common-workflow-language-cwl]) or lab device standards ([resource:sila-2]) |

## Physical-world and point-of-no-return concerns

Integrations that reach instruments, patients, or irreversible syntheses need explicit controls **outside** MCP/ToolUniverse:

1. Human approval gates and role-based authority
2. Rate limits and dry-run modes
3. Provenance capture ([Provenance and execution evidence](provenance-and-execution-evidence.md))
4. Mapping to device-compatible procedures ([Laboratory interoperability](laboratory-interoperability.md))

## Decision paths

- **Expose existing REST tools to agents with minimal custom glue:** Evaluate [resource:model-context-protocol-mcp] servers; wrap tools with schemas that preserve units and entity types ([Metadata semantics and units](metadata-semantics-and-units.md)).
- **Orchestrate many scientific APIs in agent workflows:** Compare [resource:tooluniverse] against bespoke MCP servers; verify licensing and data-use terms separately ([Controlled data access](controlled-data-access.md)).
- **Standardize multi-agent messaging in science:** Track A2A and IEEE P3971 watchlist status; do not specify draft projects as mandatory interfaces **as of 2026-08-01**.

## Example architecture

Read-only literature tools are exposed via MCP with explicit parameter schemas. Controlled genomic queries require [resource:ga4gh-passports] tokens validated before the MCP server forwards requests. A workflow runner—not the agent wire protocol—records [resource:workflow-run-ro-crate] provenance for each tool invocation batch. Laboratory actuation routes through SiLA or Autoprotocol adapters with human approval, not direct open-ended tool calls.
