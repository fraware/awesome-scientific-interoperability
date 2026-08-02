# Taxonomy

## Foundations

Cross-domain principles and frameworks required to understand interoperable scientific infrastructure.

## Identifiers and Discovery

Persistent identifiers, resolvers, registries, service descriptions, and discovery APIs.

## Metadata and Semantics

Metadata standards, ontologies, controlled vocabularies, units, mappings, and semantic profiles.

## Data and Digital Objects

Data packages, research objects, transfer formats, repository interfaces, and object-level interoperability mechanisms.

## Research Software and Environments

Research-software metadata, content identifiers, executable environments, and portability mechanisms.

## Workflows and Execution

Workflow languages, workflow registries, execution APIs, task APIs, runners, and portable test systems.

## Provenance and Evidence

Provenance models, execution records, trace packages, evidence objects, and tools for inspecting or converting them.

## Knowledge Systems and Publications

Structured publications, scholarly link exchange, scientific assertions, research graphs, and machine-actionable knowledge systems.

## Instruments and Laboratories

Instrument communication, machine-readable procedures, analytical-data standards, laboratory semantics, and clinical-laboratory exchange.

## Agents, Access, and Policy

Agent-tool protocols, scientific tool platforms, federated access assertions, and machine-readable data-use conditions.

## Validation and Conformance

Profile validators, conformance suites, cross-implementation tests, and scientific execution testbeds.

---

## Taxonomy reassessment (2026-08-01)

Maintainers evaluated whether `Agents, Access, and Policy` should split into **Scientific Agents and Automation** and **Identity, Access, and Policy**, and whether **Foundations** warrants a **Reference Architectures** section. The decision uses the main-list corpus as of the reassessment date; later admissions do not silently change section structure without a new reassessment.

### Agents, Access, and Policy — keep combined

**Decision:** Retain the combined section. Do **not** split.

**Threshold:** Split only when **both** proposed sections contain at least three strong main-list entries and each answers a distinct recurring integration problem.

| Proposed section | Strong main-list entries at reassessment | Recurring integration problem |
| --- | --- | --- |
| Scientific Agents and Automation | 2 — Model Context Protocol (MCP), ToolUniverse | How AI agents discover, invoke, and compose scientific tools through documented interfaces |
| Identity, Access, and Policy | 2 — GA4GH Data Use Ontology (DUO), GA4GH Passports | How controlled scientific data services express use conditions and authorize researchers across federated identity |

Both proposed halves fall below the three-entry minimum. The integration problems are distinct, but corpus depth is insufficient. No weak entries were added to satisfy the threshold.

**Evidence for future reassessment:**

- **Agents:** A third strong agent-interface entry with normative specification and multiple independent scientific implementations. Watchlist: `agent2agent-a2a-protocol`, `ieee-p3971`.
- **Access and policy:** A third strong machine-readable access or data-use mechanism beyond the GA4GH pair, with documented cross-repository adoption. Watchlist: Open Digital Rights Language (ODRL), `five-safes-ro-crate`.
- **Emerging entries:** MCP and ToolUniverse carry short review intervals; independent ToolUniverse reuse or scientific MCP profiles could change the agents count.

### Foundations — remains selective

**Decision:** Keep `Foundations` unchanged at four entries (CDIF, EOSC Interoperability Framework, FAIR Digital Object Framework, FAIR Principles).

Each entry is a cross-domain principle or framework specification that orients readers before domain-specific sections. None is a deployable platform or end-to-end system; EOSC Interoperability Framework is an architecture-and-governance document, not a runtime stack. The section remains selective relative to the admission bar in the editorial policy.

### Reference Architectures — not warranted

**Decision:** Do **not** create a `Reference Architectures` section.

**Threshold:** Create the section only when it would contain at least three exceptional entries that improve integration decisions beyond what existing sections already cover.

No main-list entry is classified as a reference architecture. Broad platforms under watch (`galaxy`, `scitoolagent`) lack completed boundary analysis and promotion conditions. ToolUniverse is an emerging scientific tool platform already placed under `Agents, Access, and Policy`; it does not meet the exceptional, multi-pattern bar for a new section anchor. Workflow engines and registries are curated under their mechanism-specific sections rather than as reference architectures.

**Evidence for future reassessment:**

- At least three watchlist or new candidates pass reference-architecture promotion conditions with explicit comparison to existing main-list entries (see `catalog/watchlist.yaml` and [DR-005](decision-records.md#dr-005-reference-architecture-criteria)).

## Domain tags

Controlled scientific-domain tags such as `neuroscience`, `astronomy`, and `bioimaging` classify domain standards. Storage substrates remain represented through those standards rather than standalone container-format entries. Remote query, research-data, laboratory-data, and cross-domain deployment remain separate integration or infrastructure dimensions in `config/catalog-taxonomy.yaml`.
