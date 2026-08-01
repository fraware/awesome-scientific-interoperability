# Review: Agents, Access, and Policy

**Review date:** 2026-08-01  
**Records migrated:** 4  
**Reviewer conflict of interest:** None

## Sources inspected

| ID | Primary sources |
|----|-----------------|
| ga4gh-data-use-ontology-duo | https://www.ga4gh.org/product/data-use-ontology-duo/ ; https://github.com/EBISPOT/DUO |
| ga4gh-passports | https://www.ga4gh.org/product/ga4gh-passports/ ; https://github.com/ga4gh-duri/ga4gh-passport-standard |
| model-context-protocol-mcp | https://modelcontextprotocol.io/specification/2026-07-28 ; https://github.com/modelcontextprotocol/specification |
| tooluniverse | https://zitniklab.hms.harvard.edu/ToolUniverse/en/ ; https://github.com/mims-harvard/ToolUniverse |

## Fast-moving agent spec recheck

- **MCP:** Canonical URL updated to specification release **2026-07-28** (confirmed against modelcontextprotocol.io and schema.ts in the specification repository). JSON-RPC base protocol with resources, tools, prompts, and optional extensions documented.
- **ToolUniverse:** Documentation confirms MCP integration path and 1000+ tool registry; classified as `emerging` with `single-known` implementation status pending broader independent adoption evidence.

## Changes made

- Migrated all four records to v2.
- Linked DUO and Passports as related governance/authorization resources within this shard.
- Linked MCP and ToolUniverse as related agent-interface resources.
- Set MCP and ToolUniverse to `emerging` with 183-day review interval (review_due_on 2027-01-31).
- Set GA4GH resources to established/maintained with 365-day intervals.

## Unresolved questions

- MCP extension surface (Tasks, Skills over MCP, MCP Apps) evolves quickly; next review should confirm whether scientific profiles emerge.
- ToolUniverse schema openness and independent third-party reuse outside the Zitnik Lab stack need stronger public evidence at next review.

## Conflicts

None.
