# Awesome Scientific Interoperability [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> Scientific interoperability enables independently developed data, software, workflows, instruments, knowledge systems, and agents to exchange, interpret, execute, preserve, and compose information through documented contracts.

This list selects standards, protocols, formats, schemas, APIs, ontologies, registries, implementations, mappings, and test suites that materially support those relationships. Every entry answers two questions: **what interoperates with what, and through which mechanism?**

## Contents

- [Selection Standard](#selection-standard)
- [Foundations](#foundations)
- [Identifiers and Discovery](#identifiers-and-discovery)
- [Metadata and Semantics](#metadata-and-semantics)
- [Data and Digital Objects](#data-and-digital-objects)
- [Research Software and Environments](#research-software-and-environments)
- [Workflows and Execution](#workflows-and-execution)
- [Provenance and Evidence](#provenance-and-evidence)
- [Knowledge Systems and Publications](#knowledge-systems-and-publications)
- [Instruments and Laboratories](#instruments-and-laboratories)
- [Agents, Access, and Policy](#agents-access-and-policy)
- [Validation and Conformance](#validation-and-conformance)

## Selection Standard

An entry must expose a reusable and publicly inspectable interoperability mechanism, demonstrate credible maintenance or stewardship, and add decision value beyond stronger resources already included. General scientific software, broad open-science guidance, private connectors, and projects whose interoperability contribution cannot be stated precisely are excluded. See the [editorial policy](docs/editorial-policy.md) for the complete standard.

## Foundations

- [Cross-Domain Interoperability Framework (CDIF)](https://cdif.codata.org/) - Discovery, integration, provenance, and semantic profiles for reusing research data across scientific domains.
- [EOSC Interoperability Framework](https://eosc.eu/eosc-interoperability-framework/) - Technical, semantic, organizational, and legal guidance for federating European research data and services.
- [FAIR Digital Object Framework](https://fairdo.org/specifications/) - Typed and persistently identified digital objects designed for machine action across repositories and automated services.
- [FAIR Principles](https://www.go-fair.org/fair-principles/) - Principles for machine-actionable findability, accessibility, interoperability, and reuse across digital research objects and services.

## Identifiers and Discovery

- [Crossref REST API and Metadata](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) - Open scholarly metadata API linked through DOIs and relationships; connects scholarly works, publishers, discovery systems, and research graphs.
- [DataCite Metadata Schema and REST API](https://support.datacite.org/docs/api) - DOI metadata schema and APIs for registration, discovery, and relation expression; connects research objects, repositories, discovery services, and citation systems.
- [FAIRsharing](https://fairsharing.org/) - Curated records and relationships among research standards, databases, and policies; connects standards, databases, repositories, policies, and users.
- [GA4GH Service Info](https://www.ga4gh.org/product/service-info/) - Common endpoint for service identity, version, organization, and type metadata; connects genomic cloud services, clients, and registries.
- [GA4GH Service Registry](https://www.ga4gh.org/product/service-registry/) - Common API for discovering standards-compliant services; connects clients, genomic services, and federated registries.
- [GA4GH Tool Registry Service (TRS)](https://www.ga4gh.org/product/tool-registry-service-trs/) - Standard API for discovering and retrieving versioned tools and workflows; connects workflow registries, tools, workflow engines, and clients.
- [Identifiers.org](https://identifiers.org/) - Registry of identifier namespaces with standardized resolution; connects Life-science identifiers, databases, and applications.
- [IGSN ID](https://ev.igsn.org/about-igsns) - Globally unique persistent identifiers and metadata for material samples; connects physical samples, datasets, publications, and repositories.
- [ORCID](https://info.orcid.org/what-is-orcid/) - Persistent researcher identifiers and public/member APIs; connects researchers, publishers, funders, and repositories.
- [Research Organization Registry (ROR)](https://ror.org/about/) - Open organization identifiers, metadata, and APIs; connects research organizations, publishers, funders, and repositories.

## Metadata and Semantics

- [Bioschemas](https://bioschemas.org/profiles/) - Schema.org profiles for datasets, tools, workflows, training materials, and scientific resources; connects Life-science resources, search engines, and registries.
- [Climate and Forecast (CF) Metadata Conventions](https://cfconventions.org/) - Standardized variable descriptions, units, coordinates, and metadata conventions; connects NetCDF datasets, climate and forecast tools, and archives.
- [Croissant](https://docs.mlcommons.org/croissant/docs/croissant-spec-1.1.html) - Machine-readable dataset descriptions built on Schema.org; connects machine-learning datasets, repositories, training frameworks, and consumers.
- [Darwin Core](https://dwc.tdwg.org/) - Shared terms for biodiversity occurrence, taxonomy, location, and event data; connects biodiversity observations, collections, aggregators, and repositories.
- [DDI Lifecycle](https://ddialliance.org/Specification/DDI-Lifecycle/) - Lifecycle metadata model covering conceptualization, collection, processing, and dissemination; connects social-science data, surveys, archives, and analysis systems.
- [EDAM Ontology](https://edamontology.org/) - Controlled concepts connecting scientific operations, data types, formats, and topics; connects bioinformatics tools, data, formats, operations, and workflow registries.
- [OBO Foundry](https://obofoundry.org/) - Shared principles, identifiers, and governance for interoperable open biomedical ontologies.
- [QUDT](https://www.qudt.org/) - Ontologies for quantities, units, dimensions, and data types that preserve measurement meaning across scientific systems.
- [Schema.org](https://schema.org/) - Shared web vocabulary used by scientific profiles to expose structured resources to search engines and machine clients.
- [Simple Knowledge Organization System (SKOS)](https://www.w3.org/TR/skos-reference/) - RDF model for publishing, mapping, and exchanging thesauri, taxonomies, and controlled vocabularies.
- [SOSA/SSN](https://www.w3.org/TR/vocab-ssn/) - W3C and OGC ontologies connecting sensors, observations, samples, actuators, and platforms.
- [SpatioTemporal Asset Catalog (STAC)](https://stacspec.org/) - Common metadata model and APIs for spatiotemporal assets; connects geospatial assets, catalogs, clients, and cloud storage.
- [Unified Code for Units of Measure (UCUM)](https://ucum.org/) - Machine-processable codes for unambiguous exchange and computation of measurement units.
- [W3C Data Catalog Vocabulary (DCAT)](https://www.w3.org/TR/vocab-dcat-3/) - RDF vocabulary for exchanging catalog, dataset, distribution, and data-service descriptions across federated catalogs.

## Data and Digital Objects

- [BagIt](https://datatracker.ietf.org/doc/html/rfc8493) - Manifest-based packaging format for transferring digital content with fixity and completeness checks.
- [COMBINE/OMEX Archive](https://combinearchive.org/) - Archive format bundling models, simulations, metadata, and related files; connects computational models, simulation descriptions, data, and metadata.
- [FAIR Signposting](https://signposting.org/) - Typed HTTP Link relations that let machine clients discover identifiers, metadata, licenses, and files from repository landing pages.
- [RO-Crate](https://www.researchobject.org/ro-crate/specification/1.3/) - JSON-LD packaging for exchanging data, software, workflows, people, instruments, and provenance as a coherent research object.
- [Workflow RO-Crate](https://about.workflowhub.eu/Workflow-RO-Crate/) - RO-Crate profile for publishing portable workflow definitions, metadata, diagrams, examples, and tests.
- [Workflow Run RO-Crate](https://www.researchobject.org/workflow-run-crate/profiles/workflow_run_crate/) - RO-Crate profile for exchanging workflow-run inputs, outputs, software, execution records, and provenance across workflow systems.
- [Workflow Testing RO-Crate](https://w3id.org/ro/wftest) - Portable research-object profile for exchanging workflow test suites, inputs, expected outputs, and test services.

## Research Software and Environments

- [Apptainer / Singularity Image Format](https://apptainer.org/docs/user/latest/introduction.html) - Portable container images and runtime designed for scientific and HPC environments; connects scientific software environments, HPC systems, and container registries.
- [Citation File Format (CITATION.cff)](https://citation-file-format.github.io/) - Repository-local YAML metadata that connects software projects with citation, archival, and publishing systems.
- [CodeMeta](https://codemeta.github.io/) - Shared research-software metadata vocabulary and crosswalks connecting repositories, registries, and citation systems.
- [ReproZip](https://www.reprozip.org/) - Captures files, dependencies, and execution traces into portable experiment packages; connects computational experiments, execution environments, and reproduction tools.
- [Software Hash Identifiers (SWHIDs)](https://www.swhid.org/) - Intrinsic persistent identifiers that connect exact source-code artifacts with archives, publications, and research records.

## Workflows and Execution

- [Common Workflow Language (CWL)](https://www.commonwl.org/) - Portable declarative standard for describing command-line tools and workflows across independent runners and computing environments.
- [cwltool](https://github.com/common-workflow-language/cwltool) - Reference CWL runner connecting specification validation, conformance testing, workflow execution, and provenance capture.
- [GA4GH Data Repository Service (DRS)](https://www.ga4gh.org/product/data-repository-service-drs/) - Standard API for resolving and accessing data objects across repositories, clouds, and workflow systems.
- [GA4GH Task Execution Service (TES)](https://www.ga4gh.org/product/task-execution-service-tes/) - Standard API that separates workflow orchestration from individual task execution across compute backends.
- [GA4GH Workflow Execution Service (WES)](https://www.ga4gh.org/product/workflow-execution-service-wes/) - Standard API for submitting, monitoring, and retrieving workflow runs from heterogeneous execution services.
- [LifeMonitor](https://lifemonitor.eu/) - Monitoring service that executes portable workflow tests described with Workflow Testing RO-Crate.
- [Sapporo](https://github.com/sapporo-wes/sapporo) - Reference WES implementation that exposes CWL, WDL, Nextflow, and Snakemake runners through one execution API.
- [WfExS-backend](https://github.com/inab/WfExS-backend) - Workflow execution backend connecting multiple workflow engines with reproducible environments and RO-Crate evidence packages.
- [Workflow Description Language (WDL)](https://openwdl.org/) - Workflow language implemented by multiple engines for executing scientific pipelines across cloud and high-performance computing backends.
- [WorkflowHub](https://workflowhub.eu/) - FAIR workflow registry connecting RO-Crate packaging, Bioschemas metadata, GA4GH TRS discovery, and external execution services.

## Provenance and Evidence

- [CWLProv](https://cwltool.readthedocs.io/en/latest/CWLProv.html) - PROV-based profile that packages CWL workflow execution records as portable research objects.
- [ISO 23494-2:2026 Common Provenance Model](https://www.iso.org/standard/87714.html) - International provenance standard for tracing biological materials and derived data across laboratories, biobanks, and software systems.
- [P-Plan](https://www.opmw.org/model/p-plan/) - W3C PROV extension linking prospective plans, workflow structures, variables, and execution provenance.
- [runcrate](https://www.researchobject.org/runcrate/) - Tools for inspecting, replaying, and converting Workflow Run RO-Crate and CWLProv execution records.
- [W3C PROV](https://www.w3.org/TR/prov-o/) - Cross-domain data model, ontology, and serializations for exchanging provenance among independent producers and consumers.

## Knowledge Systems and Publications

- [Journal Article Tag Suite (JATS)](https://jats.nlm.nih.gov/) - XML standard for exchanging scholarly articles and associated metadata among publishers, repositories, and indexing systems.
- [Nanopublications](https://nanopub.net/) - Immutable RDF publications that combine a scientific assertion with provenance and publication information.
- [Open Research Knowledge Graph (ORKG)](https://www.orkg.org/) - Structured scholarly representations and APIs for exchanging scientific claims, comparisons, and research contributions.
- [OpenAIRE Research Graph](https://graph.openaire.eu/) - Open scholarly graph integrating publications, datasets, software, projects, organizations, and services through shared metadata and APIs.
- [Scholix](https://github.com/scholix/schema) - Common information model and exchange framework for links between scholarly literature and research data.

## Instruments and Laboratories

- [Allotrope Data Format](https://docs.allotrope.org/) - Common data format, ontologies, and metadata models for exchanging analytical laboratory data across instruments and applications.
- [Analytical Information Markup Language (AnIML)](https://www.animl.org/) - XML-based standard for exchanging analytical chemistry and instrument data across vendor systems.
- [Autoprotocol](https://github.com/autoprotocol/autoprotocol-python) - Machine-readable language for expressing platform-independent laboratory procedures for automated execution.
- [HL7 FHIR](https://hl7.org/fhir/) - Modular resources and APIs for exchanging clinical and laboratory information across independent health systems.
- [LOINC](https://loinc.org/) - Universal codes for exchanging laboratory tests, measurements, and clinical observations.
- [OPC UA Laboratory and Analytical Device Standard (LADS)](https://opcfoundation.org/markets-collaboration/lads/) - OPC UA companion specification for standardized control, status, and data access across laboratory devices.
- [SiLA 2](https://sila2.gitlab.io/sila_base/) - Open gRPC-based standard for controlling laboratory devices and services through extensible feature definitions.

## Agents, Access, and Policy

- [GA4GH Data Use Ontology (DUO)](https://www.ga4gh.org/product/data-use-ontology-duo/) - Ontology for expressing data-use permissions and restrictions so repositories and access systems can match requests computationally.
- [GA4GH Passports](https://www.ga4gh.org/product/ga4gh-passports/) - Machine-readable researcher visas and access assertions for interoperable controlled-data authorization.
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/specification/2026-07-28) - Open protocol for exposing tools, resources, prompts, and capabilities to AI applications through a standardized client-server interface.
- [ToolUniverse](https://zitniklab.hms.harvard.edu/ToolUniverse/en/) - Scientific tool platform that standardizes discovery, invocation, composition, and monitoring across heterogeneous tools, models, APIs, and datasets.

## Validation and Conformance

- [BioSimulators Test Suite](https://docs.biosimulators.org/Biosimulators_test_suite/) - Automated execution tests for standardized simulator interfaces, modeling formats, containers, and scientific assertions.
- [CWL Conformance Tests](https://github.com/common-workflow-language/cwl-v1.2) - Versioned test suite for checking workflow-runner behavior against Common Workflow Language requirements.
- [RO-Crate Validator](https://github.com/crs4/rocrate-validator) - Profile-aware validator for base RO-Crate and scientific extensions using SHACL and programmatic checks.
- [SBML Test Suite](https://sbml.org/software/sbml-test-suite/) - Public syntactic, deterministic semantic, and stochastic tests for comparing independent systems-biology simulators.

## Related Lists

- [Awesome FAIR](https://github.com/Materials-Data-Science-and-Informatics/awesome-fair) - FAIR data, metadata, standards, and implementation resources.
- [Awesome Open Science Software](https://github.com/silky/awesome-open-science) - Software supporting open scientific practice.
- [Awesome Reproducible Research](https://github.com/leipzig/awesome-reproducible-research) - Tools and practices for computational reproducibility.
- [Awesome Scientific Computing](https://github.com/nschloe/awesome-scientific-computing) - Numerical and scientific-computing software across programming languages.

## Contributing

Read [contributing.md](contributing.md) before proposing a resource. A proposal must identify the connected systems or objects, the documented mechanism, primary technical sources, current maintenance evidence, and a concrete reason the resource belongs among the strongest examples in its category.

## Footnotes

- The manually edited README is authoritative. The [machine-readable catalog](catalog/resources.yaml) exists for validation, maintenance, and downstream analysis; it does not generate this list.
- Navigate by concrete integration problem through the [integration problem index](docs/integration-problems.md).
- Promising resources that do not yet satisfy the main-list bar are tracked in [docs/watchlist.md](docs/watchlist.md).
- Editorial decisions follow the [project charter](docs/project-charter.md), [taxonomy](docs/taxonomy.md), and [conflict-of-interest policy](docs/conflicts-of-interest.md).
- Release checks and publication instructions are recorded in the [validation report](docs/validation-report.md) and [publishing guide](docs/publishing.md).
