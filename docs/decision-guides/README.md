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
| [Laboratory interoperability](laboratory-interoperability.md) | SiLA 2, OPC UA LADS, Autoprotocol, AnIML, ADF, FHIR, LOINC |
| [Scientific agents and tool interfaces](scientific-agents-and-tool-interfaces.md) | MCP, ToolUniverse, emerging watchlist protocols |
| [Controlled data access](controlled-data-access.md) | GA4GH Passports, DUO, emerging policy packaging |
| [Computational models and simulation experiments](systems-biology-models.md) | SBML, CellML, SED-ML, COMBINE Archive, conformance suites |
| [Neuroscience dataset and neurophysiology exchange](neuroscience-data-standards.md) | BIDS, NWB, DICOMweb, NeXus |
| [Astronomy data files, tables, and query services](astronomy-data-and-services.md) | FITS, VOTable, TAP, STAC; ObsCore/SAMP/ASDF boundaries |
| [Bioimaging data exchange](bioimaging-data.md) | OME-NGFF, DICOMweb, NeXus, RO-Crate; OME-TIFF/Zarr boundaries |
| [Genomic representation and access](genomic-representation-and-access.md) | VRS, Phenopackets, htsget, refget, DRS; Beacon/HTS/Crypt4GH/RNAget boundaries |

## How to use these guides

1. Start from the integration situation (packaging for transfer, execution evidence, discovery, and so on).
2. Read the comparison dimensions in the relevant guide; no single resource wins every dimension.
3. Follow catalog IDs to boundary notes, typed relations (`profile-of`, `implements`, `validates`, `alternative-to`, …), and evidence statuses in the README and YAML shards.
4. Treat packaging or profile conformance as necessary but not sufficient for reproducibility, semantic equivalence, or scientific validity.

## Validation

Resource-ID markers are checked by `scripts/validate_decision_guides.py` in Quality CI. Unknown IDs fail the build.

## Related navigation

- [Integration problems](../integration-problems.md) — problem-class index
- [Catalog model v2](../catalog-model-v2.md)
- [Querying the catalog](../querying-the-catalog.md)
| [Ecology and sequence-context metadata](ecology-and-sequence-context-metadata.md) | MIxS, EML, Darwin Core, IGSN, ISA-JSON |
| [Mass-spectrometry data exchange](mass-spectrometry-data.md) | mzML, AnIML, Allotrope Data Format |
| [Clinical research data models](clinical-research-data-models.md) | FHIR, CDISC ODM, OMOP CDM, Phenopackets |
