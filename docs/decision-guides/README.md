# Decision guides

Problem-oriented comparison documents for overlapping interoperability mechanisms in the catalog. Each guide compares resources within one integration concern, cites primary sources, and links entries with ``[resource:<catalog-id>]`` markers validated against the catalog.

## Guides

| Guide | Scope |
|-------|-------|
| [Research object packaging](research-object-packaging.md) | RO-Crate profiles, BagIt, COMBINE/OMEX, FAIR Signposting |
| [Provenance and execution evidence](provenance-and-execution-evidence.md) | W3C PROV, P-Plan, CWLProv, Workflow Run RO-Crate, ISO 23494-2, runcrate |
| [Workflows and execution](workflows-and-execution.md) | CWL, WDL, GA4GH TRS/WES/TES/DRS, WorkflowHub, Sapporo, backends |
| [Workflow testing and conformance](workflow-testing-and-conformance.md) | CWL Conformance Tests, Workflow Testing RO-Crate, LifeMonitor |
| [Identifiers and discovery](identifiers-and-discovery.md) | ORCID, ROR, IGSN, DOI/DataCite, Crossref, Identifiers.org, GA4GH discovery, FAIRsharing |
| [Metadata semantics and units](metadata-semantics-and-units.md) | Schema.org, Bioschemas, DCAT, SKOS, OBO, EDAM, QUDT, UCUM, domain conventions |

Additional guides are added in a separate pull request for laboratory and agent boundaries.

## How to use these guides

1. Start from the integration situation (packaging for transfer, execution evidence, discovery, and so on).
2. Read the comparison dimensions in the relevant guide; no single resource wins every dimension.
3. Follow catalog IDs to boundary notes, alternatives, and evidence statuses in the README and YAML shards.
4. Treat packaging or profile conformance as necessary but not sufficient for reproducibility, semantic equivalence, or scientific validity.

## Validation

Resource-ID markers are checked by `scripts/validate_decision_guides.py` in Quality CI. Unknown IDs fail the build.

## Related navigation

- [Integration problems](../integration-problems.md) — problem-class index (when published)
- [Catalog model v2](../catalog-model-v2.md)
- [Querying the catalog](../querying-the-catalog.md)
