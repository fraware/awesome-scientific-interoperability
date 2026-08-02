# Integration Problem Index

This index maps concrete scientific integration situations to catalog resources. It is manually authored and does not replace the README or catalog records. Recommendations cite catalog boundary notes; no entry is a universal winner for every context.

Use catalog resource ID markers in the form `[resource:ro-crate]` when citing entries. Each problem class below links to relevant README sections and catalog entries.

**Catalog sections covered:** Foundations, Identifiers and Discovery, Metadata and Semantics, Data and Digital Objects, Research Software and Environments, Workflows and Execution, Provenance and Evidence, Knowledge Systems and Publications, Instruments and Laboratories, Agents, Access, and Policy, Validation and Conformance.

---

## 1. Identify researchers, organizations, samples, software, and research objects

[problem:identify-research-objects]

### Situation

You must assign stable, resolvable identifiers to people, institutions, physical samples, scholarly outputs, or exact software artifacts so independent systems can reference the same entity without ambiguous strings.

### Starting point

Begin with the identifier family matched to the object type: [resource:orcid] for researchers, [resource:research-organization-registry-ror] for organizations, [resource:igsn-id] for physical samples, [resource:datacite-metadata-schema-and-rest-api] or [resource:crossref-rest-api-and-metadata] for citable research objects, and [resource:software-hash-identifiers-swhids] for exact source-code snapshots. Use [resource:identifiers-org] to resolve life-science namespace prefixes consistently.

Foundations resources [resource:fair-principles] and [resource:fair-digital-object-framework] frame why persistent, typed identification supports machine action across repositories, but they do not replace object-specific identifier systems.

### When an alternative is stronger

- Publisher-centric scholarly graphs already keyed by DOI: prefer [resource:crossref-rest-api-and-metadata].
- Repository-local dataset registration with relation expression: [resource:datacite-metadata-schema-and-rest-api] is the stronger operational starting point.
- Computational models bundled in COMBINE archives rather than standalone software citation: [resource:combine-omex-archive] may carry identity context alongside model files.
- Cross-domain interoperability planning before choosing identifiers: [resource:cross-domain-interoperability-framework-cdif] and [resource:eosc-interoperability-framework] supply framing profiles that complement, rather than replace, identifier registries.

### Limitations and common category errors

- Treating a landing-page URL as a persistent identifier.
- Using ORCID or ROR where a sample-level or software-artifact identifier is required.
- Assuming DOI registration alone establishes semantic type or access policy.
- Confusing identifier resolution ([resource:identifiers-org]) with metadata alignment (see Problem 3).

### Relevant catalog entries

[resource:orcid] [resource:research-organization-registry-ror] [resource:igsn-id] [resource:datacite-metadata-schema-and-rest-api] [resource:crossref-rest-api-and-metadata] [resource:software-hash-identifiers-swhids] [resource:identifiers-org] [resource:fair-principles] [resource:fair-digital-object-framework] [resource:cross-domain-interoperability-framework-cdif] [resource:eosc-interoperability-framework] [resource:combine-omex-archive]

### Example architecture

A sample repository registers each specimen with [resource:igsn-id], links the collecting investigator via [resource:orcid] and institution via [resource:research-organization-registry-ror], deposits derived sequence data with a DataCite DOI through [resource:datacite-metadata-schema-and-rest-api], and records analysis code with [resource:software-hash-identifiers-swhids] so downstream graphs can resolve every entity type through its appropriate registry.

---

## 2. Discover datasets, tools, workflows, and services

[problem:discover-resources]

### Situation

Users or automated clients must find datasets, software, workflows, or execution services across federated catalogs, registries, and institutional repositories without crawling unstructured web pages.

### Starting point

For catalog-level dataset and service discovery, start with [resource:w3c-data-catalog-vocabulary-dcat] and repository profiles such as [resource:spatiotemporal-asset-catalog-stac] for geospatial assets. For standards and database discovery across domains, [resource:fairsharing] provides curated records and relationships. For executable tools and workflows, [resource:ga4gh-tool-registry-service-trs] and [resource:workflowhub] are strong starting APIs; [resource:ga4gh-service-registry] and [resource:ga4gh-service-info] help locate typed services in federated genomic infrastructure.

Expose resource descriptions to search engines with [resource:bioschemas] profiles built on [resource:schema-org]. [resource:fair-signposting] helps machine clients discover metadata and files from repository landing pages.

### When an alternative is stronger

- Domain-specific survey or social-science archives: [resource:ddi-lifecycle] discovery metadata may be richer than generic DCAT alone.
- Official statistics or macroeconomic indicator feeds: [resource:sdmx] supplies Data Structure Definitions and payload contracts beyond catalog metadata.
- Biodiversity aggregators: [resource:darwin-core] terms often appear in occurrence indexes alongside catalog metadata.
- Machine-learning dataset consumers expecting training-ready packaging: [resource:croissant] descriptions may be more actionable than DCAT distributions alone.
- Federated materials-structure databases: [resource:optimade] provides a standardized REST query contract across providers.
- Workflow execution after discovery: pair registry results with [resource:ga4gh-workflow-execution-service-wes] rather than treating registry metadata as execution contracts.

### Limitations and common category errors

- Confusing a discovery registry with an identifier authority (see Problem 1).
- Treating Bioschemas markup as a substitute for catalog APIs.
- Assuming TRS or WorkflowHub entries guarantee feature-identical execution on every backend.
- Using FAIRsharing as a workflow runner catalog; it indexes standards and databases, not operational execution endpoints.

### Relevant catalog entries

[resource:w3c-data-catalog-vocabulary-dcat] [resource:spatiotemporal-asset-catalog-stac] [resource:fairsharing] [resource:optimade] [resource:ga4gh-tool-registry-service-trs] [resource:workflowhub] [resource:ga4gh-service-registry] [resource:ga4gh-service-info] [resource:bioschemas] [resource:schema-org] [resource:fair-signposting] [resource:ddi-lifecycle] [resource:sdmx] [resource:darwin-core] [resource:croissant]

### Example architecture

A national portal publishes DCAT catalogs for institutional datasets, STAC catalogs for satellite collections, registers CWL workflows in [resource:workflowhub] with TRS-compatible APIs, and advertises WES runners through [resource:ga4gh-service-info] endpoints so clients discover, resolve, and optionally submit jobs through separate but linked layers.

---

## 3. Align metadata, terminology, quantities, and units

[problem:align-metadata-semantics]

### Situation

Independent systems must exchange dataset descriptions, observation records, or analysis parameters with shared meaning for terms, quantities, units, and semantic relationships.

### Starting point

For general catalog and service descriptions, combine [resource:schema-org] with domain profiles such as [resource:bioschemas] or [resource:spatiotemporal-asset-catalog-stac]. For controlled vocabularies and ontology graphs, use [resource:simple-knowledge-organization-system-skos] mappings and community ontologies governed by [resource:obo-foundry]. For bioinformatics tool and data typing, [resource:edam-ontology] connects operations, formats, and topics.

For measurable quantities, pair [resource:qudt] (dimensions, quantities, and semantic unit typing) with [resource:unified-code-for-units-of-measure-ucum] (machine-processable unit codes). Domain field conventions such as [resource:climate-and-forecast-cf-metadata-conventions], [resource:darwin-core], [resource:ddi-lifecycle], and [resource:sdmx] supply community-agreed variable and record semantics where generic vocabularies are insufficient.

### When an alternative is stronger

- Sensor and observation platforms: [resource:sosa-ssn] links sensors, observations, samples, and actuators explicitly.
- Machine-learning dataset packaging with training semantics: [resource:croissant] may be stronger than generic Schema.org dataset markup alone.
- Cross-domain reuse planning: [resource:cross-domain-interoperability-framework-cdif] semantic profiles complement but do not replace domain vocabularies.

### Limitations and common category errors

- Treating UCUM codes alone as a full semantic model; QUDT and UCUM are complementary, not interchangeable.
- Applying CF Conventions outside NetCDF-oriented climate and forecast data without profile justification.
- Assuming ontology membership proves experimental equivalence or data quality.
- Using SKOS mapping to paper over incompatible domain definitions without curator review.

### Relevant catalog entries

[resource:schema-org] [resource:bioschemas] [resource:w3c-data-catalog-vocabulary-dcat] [resource:simple-knowledge-organization-system-skos] [resource:obo-foundry] [resource:edam-ontology] [resource:qudt] [resource:unified-code-for-units-of-measure-ucum] [resource:climate-and-forecast-cf-metadata-conventions] [resource:darwin-core] [resource:ddi-lifecycle] [resource:sdmx] [resource:sosa-ssn] [resource:croissant] [resource:cross-domain-interoperability-framework-cdif]

### Example architecture

A workflow registry publishes Bioschemas tool metadata, describes each workflow’s EDAM operations and data types, attaches CF-compliant NetCDF inputs where applicable, and documents unit semantics with UCUM codes cross-referenced to QUDT quantity kinds so downstream engines interpret parameters consistently.

---

## 4. Package data, software, workflows, and contextual entities

[problem:package-research-objects]

### Situation

You must transfer or archive a coherent bundle of files, software, people, instruments, and metadata as one inspectable research object across repositories, journals, or workflow systems.

### Starting point

For general research-object exchange, start with [resource:ro-crate] JSON-LD packaging. Use profiled crates where the use case is narrower: [resource:workflow-ro-crate] for portable workflow definitions, [resource:workflow-run-ro-crate] for executed runs, and [resource:workflow-testing-ro-crate] for portable workflow tests.

For fixity-checked transfer without rich semantic graphs, [resource:bagit] remains appropriate. For durable repository object stores with inventories and rebuildability, prefer [resource:oxford-common-file-layout-ocfl]. For lightweight dataset and tabular resource descriptors, prefer [resource:data-package-standard]. Computational modeling communities may prefer [resource:combine-omex-archive] when bundling models and simulation descriptions. [resource:fair-signposting] complements packaging by helping clients locate crate files and related metadata from landing pages.

### When an alternative is stronger

- Executed CWL runs with PROV-oriented tooling: [resource:cwlprov] may integrate more directly with CWL-centric pipelines than authoring a crate from scratch.
- Exact reproducibility of a computational environment rather than semantic packaging: [resource:reprozip] captures execution-centric bundles.
- Scattering-facility experimental files: [resource:nexus] application definitions over HDF5.
- Crystallographic structure deposition: [resource:crystallographic-information-framework-cif] with IUCr dictionaries.
- Dynamic simulation model exchange: [resource:functional-mock-up-interface-fmi] FMUs between independent CAE tools.

### Limitations and common category errors

- Assuming RO-Crate conformance proves scientific reproducibility or semantic equivalence.
- Using Workflow RO-Crate where a executed-run profile ([resource:workflow-run-ro-crate]) is required.
- Treating BagIt manifests as a substitute for provenance graphs (see Problem 7).
- Treating OCFL layout validation as semantic packaging completeness, or Data Package descriptor validation as proof that referenced datasets are available and scientifically correct.
- Publishing a crate without validating against [resource:ro-crate-validator] for the intended profile.

### Relevant catalog entries

[resource:ro-crate] [resource:workflow-ro-crate] [resource:workflow-run-ro-crate] [resource:workflow-testing-ro-crate] [resource:bagit] [resource:oxford-common-file-layout-ocfl] [resource:data-package-standard] [resource:combine-omex-archive] [resource:fair-signposting] [resource:crystallographic-information-framework-cif] [resource:functional-mock-up-interface-fmi] [resource:nexus] [resource:cwlprov] [resource:reprozip] [resource:ro-crate-validator]

### Example architecture

An analysis platform exports a Workflow Run RO-Crate containing input files, container images, CWL process definitions, PROV records, and ORCID-linked authors; the repository exposes Signposting links to the crate and validates the profile before ingest.

---

## 5. Describe and cite research software and environments

[problem:describe-cite-software]

### Situation

You must document software authorship, version, dependencies, and execution environment so collaborators, archives, and citation systems can credit and reuse the software accurately.

### Starting point

For repository-local citation metadata, start with [resource:citation-file-format-citation-cff]. For crosswalks to broader registries and citation ecosystems, add [resource:codemeta]. Pin exact source artifacts with [resource:software-hash-identifiers-swhids] when version integrity matters more than package-name strings.

For portable execution environments in HPC or shared clusters, [resource:apptainer-singularity-image-format] is the catalog’s primary container mechanism. When the goal is capturing a full experiment for reproduction rather than publishing metadata alone, [resource:reprozip] complements descriptive metadata.

### When an alternative is stronger

- Software embedded in a broader research object: include [resource:ro-crate] software entities alongside data and workflows.
- Workflow-centric publication: [resource:workflow-ro-crate] already describes tools and tests as part of a portable workflow package.
- Publisher DOI registration for software releases: integrate [resource:datacite-metadata-schema-and-rest-api] or [resource:crossref-rest-api-and-metadata] with CFF/CodeMeta fields.

### Limitations and common category errors

- Treating CITATION.cff or CodeMeta as proof of runtime reproducibility without environment capture.
- Citing a repository URL where a SWHID or versioned DOI is required for exact artifact identification.
- Assuming container images alone document scientific semantics or workflow logic.

### Relevant catalog entries

[resource:citation-file-format-citation-cff] [resource:codemeta] [resource:software-hash-identifiers-swhids] [resource:apptainer-singularity-image-format] [resource:reprozip] [resource:ro-crate] [resource:workflow-ro-crate] [resource:datacite-metadata-schema-and-rest-api] [resource:crossref-rest-api-and-metadata]

### Example architecture

A lab repository requires CITATION.cff on each tool, maps fields to CodeMeta for registry export, builds Apptainer images for execution, registers releases with DataCite, and stores SWHIDs in RO-Crate metadata for immutable citation in publications.

---

## 6. Exchange and execute workflows across engines and backends

[problem:execute-workflows]

### Situation

You need to describe portable workflows, publish them for discovery, submit runs to heterogeneous execution services, and access remote data objects consistently across repositories and clouds.

### Starting point

For portable workflow definitions, start with [resource:common-workflow-language-cwl] or, in WDL-centric communities, [resource:workflow-description-language-wdl]. Publish discoverable workflows through [resource:workflowhub] using [resource:workflow-ro-crate] packaging and [resource:ga4gh-tool-registry-service-trs]-compatible APIs.

For execution interoperability, use [resource:ga4gh-workflow-execution-service-wes] to submit and monitor runs and [resource:ga4gh-task-execution-service-tes] when orchestration must delegate individual tasks to separate backends. Resolve data locations with [resource:ga4gh-data-repository-service-drs]. Reference implementations such as [resource:sapporo], [resource:wfexs-backend], and [resource:cwltool] demonstrate composition patterns but do not prove every engine behaves identically.

Continuous testing of published workflows can flow through [resource:lifemonitor] with [resource:workflow-testing-ro-crate] test suites.

### When an alternative is stronger

- CWL-only shops needing provenance-native execution records: [resource:cwltool] with [resource:cwlprov] may be more direct than a generic WES wrapper.
- Multi-engine backend integration with RO-Crate evidence packages: [resource:wfexs-backend] targets that integration explicitly.
- WDL-first cloud pipelines: [resource:workflow-description-language-wdl] with a WDL-capable WES implementation such as [resource:sapporo].

### Limitations and common category errors

- Treating language portability as scientific result equivalence across engines.
- Using TRS discovery as proof that all optional CWL or WDL features are supported.
- Ignoring DRS access policy when wiring workflows to controlled datasets (see Problem 11).
- Confusing workflow languages with execution APIs; WES/TES standardize service interfaces, not workflow semantics.

### Relevant catalog entries

[resource:common-workflow-language-cwl] [resource:workflow-description-language-wdl] [resource:workflowhub] [resource:workflow-ro-crate] [resource:ga4gh-tool-registry-service-trs] [resource:ga4gh-workflow-execution-service-wes] [resource:ga4gh-task-execution-service-tes] [resource:ga4gh-data-repository-service-drs] [resource:sapporo] [resource:wfexs-backend] [resource:cwltool] [resource:lifemonitor] [resource:workflow-testing-ro-crate] [resource:cwlprov]

### Example architecture

Authors publish a CWL workflow in WorkflowHub, a WES service accepts runs via GA4GH APIs, TES workers execute containerized tasks on cloud backends, DRS resolves input objects from federated repositories, and LifeMonitor executes Workflow Testing RO-Crate suites on a schedule.

---

## 7. Capture provenance, execution evidence, and traceability

[problem:capture-provenance]

### Situation

Downstream systems must understand what activities produced a dataset or result, with enough detail to audit, replay, or trace biological materials and derived data across institutions.

### Starting point

For general provenance graphs, start with [resource:w3c-prov] and workflow-plan extensions such as [resource:p-plan]. For CWL execution records packaged as research objects, use [resource:cwlprov] and the [resource:workflow-run-ro-crate] profile; [resource:runcrate] helps inspect and convert those records.

For biological material and sample lineage across laboratories and biobanks, [resource:iso-23494-2-2026-common-provenance-model] provides a domain standard complementary to generic PROV graphs.

Foundations guidance in [resource:fair-digital-object-framework] and [resource:cross-domain-interoperability-framework-cdif] motivates traceable digital objects but does not replace provenance models.

### When an alternative is stronger

- End-to-end research-object publication with files and metadata: [resource:ro-crate] plus Workflow Run RO-Crate rather than standalone PROV serializations alone.
- Prospective workflow documentation before execution: [resource:p-plan] linked to [resource:common-workflow-language-cwl] process definitions.
- Laboratory sample custody with regulatory traceability requirements: ISO 23494-2 over generic PROV alone.

### Limitations and common category errors

- Assuming provenance completeness equals reproducibility or correctness.
- Mixing prospective plans and retrospective execution records without clear profiles.
- Treating packaging conformance as proof that replay will produce identical scientific outputs.
- Using generic PROV where biological material tracking policies require ISO 23494-2 semantics.

### Relevant catalog entries

[resource:w3c-prov] [resource:p-plan] [resource:cwlprov] [resource:workflow-run-ro-crate] [resource:runcrate] [resource:ro-crate] [resource:iso-23494-2-2026-common-provenance-model] [resource:fair-digital-object-framework] [resource:cross-domain-interoperability-framework-cdif] [resource:common-workflow-language-cwl]

### Example architecture

A workflow engine emits CWLProv bundles during execution, maps activities and agents into W3C PROV, wraps inputs and outputs in a Workflow Run RO-Crate, links biobank sample handling steps to ISO 23494-2 records, and exposes the crate through a repository with Signposting discovery links.

---

## 8. Exchange publications, claims, and scholarly links

[problem:exchange-publications-claims]

### Situation

Publishers, repositories, and knowledge systems must exchange article content, structured claims, citation links between literature and data, and aggregated research graphs.

### Starting point

For publisher and repository article exchange, start with [resource:journal-article-tag-suite-jats]. For literature–data link payloads, use [resource:scholix]. For open graph aggregation across publications, datasets, software, and organizations, [resource:openaire-research-graph] provides a federated model and APIs.

For structured comparisons and claim-centric representations, [resource:open-research-knowledge-graph-orkg] is a strong starting point. Fine-grained assertion exchange with embedded provenance may use [resource:nanopublications] where RDF-based immutable assertions fit the architecture.

Link scholarly objects to identifiers through [resource:crossref-rest-api-and-metadata] and [resource:datacite-metadata-schema-and-rest-api] rather than ad hoc citation strings alone.

### When an alternative is stronger

- Full research-object packaging with data and software alongside publications: [resource:ro-crate] bundles may carry richer context than article XML alone.
- Machine-readable software citation inside articles: integrate [resource:citation-file-format-citation-cff] and [resource:codemeta] metadata referenced from JATS-related material sections.
- Domain vocabulary alignment for indexed resources: combine article links with [resource:schema-org] or [resource:bioschemas] exposure for discovery.

### Limitations and common category errors

- Treating bibliographic graphs as experimental provenance (see Problem 7).
- Assuming Scholix or OpenAIRE linkage implies access authorization to underlying datasets.
- Using nanopublications where mutable collaborative claim editing is required without an explicit immutability model.
- Confusing article exchange (JATS) with repository packaging profiles (RO-Crate).

### Relevant catalog entries

[resource:journal-article-tag-suite-jats] [resource:scholix] [resource:openaire-research-graph] [resource:open-research-knowledge-graph-orkg] [resource:nanopublications] [resource:crossref-rest-api-and-metadata] [resource:datacite-metadata-schema-and-rest-api] [resource:ro-crate] [resource:citation-file-format-citation-cff] [resource:codemeta] [resource:schema-org] [resource:bioschemas]

### Example architecture

A publisher exports JATS XML, registers DOIs through Crossref, embeds Scholix links to related datasets, exposes ORKG comparisons for key claims, and publishes an OpenAIRE-compatible graph connecting articles, data, software, and organizations.

---

## 9. Integrate instruments, analytical data, and laboratory automation

[problem:integrate-laboratory-systems]

### Situation

Laboratory integrations must move control commands, instrument output, analytical semantics, and automated procedure definitions across vendor systems and software orchestrators.

### Starting point

For live device integration and feature-based control, start with [resource:sila-2] or, in OPC UA environments, [resource:opc-ua-laboratory-and-analytical-device-standard-lads]. For vendor-neutral analytical data exchange, evaluate [resource:analytical-information-markup-language-animl] and [resource:allotrope-data-format] depending on whether XML analytical records or HDF5-based ADF best match the instrument ecosystem.

For automated procedure representation independent of a specific robot platform, [resource:autoprotocol] provides a machine-readable starting point. Clinical observation coding may require [resource:loinc] and, where health-system integration is in scope, [resource:hl7-fhir] resources—recognizing FHIR’s clinical exchange boundary rather than generic analytical semantics.

### When an alternative is stronger

- Analytical data archival with rich ontologies in HDF5 ecosystems: [resource:allotrope-data-format].
- Standardized XML analytical interchange across chromatography and spectroscopy vendors: [resource:analytical-information-markup-language-animl].
- Observation and specimen semantics tied to sensors: [resource:sosa-ssn] alongside instrument payloads.
- Packaging instrument outputs with workflows and provenance: [resource:ro-crate] instrument entities and [resource:workflow-run-ro-crate].

### Limitations and common category errors

- Assuming device communication standards standardize experimental meaning or protocol validity.
- Treating Autoprotocol procedure documents as proof of device compatibility without driver/feature verification.
- Using LOINC or FHIR where purely analytical R&D interchange (AnIML/ADF) is the actual requirement.
- Conflating SiLA 2 feature definitions with laboratory scheduling or LIMS business logic.

### Relevant catalog entries

[resource:sila-2] [resource:opc-ua-laboratory-and-analytical-device-standard-lads] [resource:analytical-information-markup-language-animl] [resource:allotrope-data-format] [resource:autoprotocol] [resource:loinc] [resource:hl7-fhir] [resource:sosa-ssn] [resource:ro-crate] [resource:workflow-run-ro-crate]

### Example architecture

A contract research platform exposes SiLA 2 features for plate handlers, converts spectrometer output to AnIML, maps reported tests to LOINC where clinical reporting is required, expresses higher-level methods in Autoprotocol, and archives each run as a Workflow Run RO-Crate linking instruments, operators, and derived datasets.

---

## 10. Expose scientific tools and capabilities to AI agents

[problem:expose-tools-to-agents]

### Situation

You must expose databases, APIs, workflows, and analysis tools to AI applications through a reusable interface that supports discovery, invocation, and monitoring without bespoke connectors for every resource.

### Starting point

For general agent-to-tool connectivity, start with [resource:model-context-protocol-mcp] to expose tools, resources, and prompts through a standardized client-server protocol. For scientific tool composition across heterogeneous APIs and models, evaluate [resource:tooluniverse] when the integration problem spans curated scientific tools rather than a single service boundary.

Pair agent interfaces with existing discovery and registry layers ([resource:ga4gh-tool-registry-service-trs], [resource:workflowhub], [resource:fairsharing]) instead of re-encoding catalog semantics inside ad hoc tool schemas.

### When an alternative is stronger

- Workflow execution with provenance requirements: route agent actions through [resource:ga4gh-workflow-execution-service-wes] and capture [resource:workflow-run-ro-crate] evidence rather than direct script invocation alone.
- Controlled datasets: agent tool access must compose with [resource:ga4gh-passports] and [resource:ga4gh-data-use-ontology-duo] (see Problem 11).
- Domain metadata grounding for tool selection: integrate [resource:edam-ontology] or [resource:bioschemas] descriptions so agents map tasks to appropriate tools.

### Limitations and common category errors

- Treating tool invocation protocols as proof of scientific validity, authorization, or safe laboratory execution.
- Exposing irreversible physical-world actions without human approval and provenance capture.
- Assuming MCP alone replaces repository, workflow, or identifier layers documented elsewhere in this index.
- Ignoring version drift between agent-discovered tools and registered workflow or container artifacts.

### Relevant catalog entries

[resource:model-context-protocol-mcp] [resource:tooluniverse] [resource:ga4gh-tool-registry-service-trs] [resource:workflowhub] [resource:fairsharing] [resource:ga4gh-workflow-execution-service-wes] [resource:workflow-run-ro-crate] [resource:ga4gh-passports] [resource:ga4gh-data-use-ontology-duo] [resource:edam-ontology] [resource:bioschemas]

### Example architecture

A research assistant uses MCP to call a curated ToolUniverse registry entry, which resolves a WorkflowHub TRS tool, submits a WES job, retrieves outputs via DRS, and stores a Workflow Run RO-Crate audit record linked to the agent session metadata.

---

## 11. Express controlled-data authorization and data-use conditions

[problem:controlled-data-access]

### Situation

Controlled-access repositories must communicate who may use a dataset, under which conditions, and how authorization decisions propagate across federated services and analysis platforms.

### Starting point

Express machine-readable use conditions with [resource:ga4gh-data-use-ontology-duo] and researcher authorization assertions with [resource:ga4gh-passports], building on institutional identity infrastructure rather than replacing it. EOSC and FAIR framing from [resource:eosc-interoperability-framework] and [resource:fair-principles] helps position authorization within broader interoperability layers but does not supply authorization tokens by itself.

When datasets are exposed to agents or workflows, combine DUO and Passports with service discovery ([resource:ga4gh-service-info]) and data access APIs ([resource:ga4gh-data-repository-service-drs]) so policy travels with resolution and execution requests.

### When an alternative is stronger

- Repository-level metadata registration without live authorization: [resource:datacite-metadata-schema-and-rest-api] rights fields complement but do not replace Passports.
- Semantic alignment of dataset descriptions for policy matching: [resource:w3c-data-catalog-vocabulary-dcat] and domain profiles may help discovery, not access decisions alone.
- Packaging controlled releases for audit: [resource:ro-crate] with explicit licensing and policy entities alongside data files.

### Limitations and common category errors

- Treating DUO terms as authorization transport; DUO expresses conditions, while Passports carry access assertions over identity federation.
- Assuming genomic patterns generalize to every controlled-access domain without boundary review.
- Publishing DOIs or Signposting links without enforcing policy at the data-access API layer.
- Conflating agent tool access (see Problem 10) with dataset authorization.

### Relevant catalog entries

[resource:ga4gh-data-use-ontology-duo] [resource:ga4gh-passports] [resource:eosc-interoperability-framework] [resource:fair-principles] [resource:ga4gh-service-info] [resource:ga4gh-data-repository-service-drs] [resource:datacite-metadata-schema-and-rest-api] [resource:w3c-data-catalog-vocabulary-dcat] [resource:ro-crate]

### Example architecture

A biobank tags each dataset with DUO codes, validates GA4GH Passports presented by analysis platforms, exposes DRS objects only after policy checks, and publishes DCAT metadata with rights information while keeping authorization enforcement on the access API.

---

## 12. Validate conformance and compare independent implementations

[problem:validate-conformance]

### Situation

You must verify that files, workflows, simulators, or research objects conform to documented profiles and compare behavior across independent implementations rather than assuming compatibility from format labels alone.

### Starting point

For RO-Crate and scientific profiles, start with [resource:ro-crate-validator]. For CWL runners, use [resource:cwl-conformance-tests] alongside reference execution with [resource:cwltool]. For systems-biology simulators, [resource:sbml-test-suite] compares independent implementations against shared test vectors. For modeling pipelines with standardized simulator interfaces, evaluate [resource:biosimulators-test-suite].

Continuous workflow testing in registries can combine [resource:workflow-testing-ro-crate] with [resource:lifemonitor] monitoring services.

### When an alternative is stronger

- Packaging validation before domain execution tests: [resource:ro-crate-validator] before workflow or simulator suites.
- Execution-record inspection after runs: [resource:runcrate] on Workflow Run RO-Crate or CWLProv outputs.
- End-to-end workflow portability claims: run [resource:cwl-conformance-tests] and LifeMonitor test crates, not only syntactic crate validation.

### Limitations and common category errors

- Treating syntactic conformance as semantic equivalence or reproducibility.
- Using a reference implementation passing tests as proof that all independent implementations behave identically.
- Applying SBML or BioSimulators suites to non-modeling artifacts such as generic RO-Crates.
- Skipping profile selection when invoking the RO-Crate validator.

### Relevant catalog entries

[resource:ro-crate-validator] [resource:cwl-conformance-tests] [resource:cwltool] [resource:sbml-test-suite] [resource:biosimulators-test-suite] [resource:workflow-testing-ro-crate] [resource:lifemonitor] [resource:runcrate] [resource:common-workflow-language-cwl]

### Example architecture

Contributors submit Workflow RO-Crate packages to a registry that validates profiles with RO-Crate Validator, executes CWL conformance tests on registered runners, runs BioSimulators tests for embedded SBML models, and publishes LifeMonitor badges based on Workflow Testing RO-Crate suites.

---

## Maintenance

Update this index when catalog boundary notes change or when new main-list entries alter starting recommendations. Run `python scripts/validate_problem_index.py` locally and in CI after edits. Query the structured catalog with `python scripts/query_catalog.py` for filterable views of the entries cited here.

---

## 13. Exchange computational models and reproducible simulation experiments

[problem:exchange-computational-models]

### Situation

Independent modeling tools must exchange a quantitative model, describe the simulation procedure to run, package all required artifacts, and test whether different engines interpret the contracts consistently.

### Starting point

Use [resource:systems-biology-markup-language-sbml] for biochemical and systems-biology reaction-network models and [resource:cellml] for modular equation-based physiological models with explicit units and imports. Describe model changes, simulations, repeated tasks, data processing, and requested outputs with [resource:simulation-experiment-description-markup-language-sed-ml]. Package the complete study with [resource:combine-omex-archive].

Validate implementation behavior separately with [resource:sbml-test-suite] and [resource:biosimulators-test-suite]. These suites test documented contracts; they do not establish scientific correctness of a model or equivalence for untested optional features.

### When an alternative is stronger

- General data-processing pipelines rather than mathematical simulation experiments: use [resource:common-workflow-language-cwl] or [resource:workflow-description-language-wdl].
- Executed workflow provenance rather than prospective simulation intent: use [resource:workflow-run-ro-crate], [resource:cwlprov], or [resource:w3c-prov].
- Cross-tool engineering model exchange and co-simulation: [resource:functional-mock-up-interface-fmi] is stronger than SBML or CellML.

### Limitations and common category errors

- Treating SED-ML as a model language or execution trace.
- Treating COMBINE Archive as proof that every contained model is supported by every simulator.
- Assuming SBML-to-CellML conversion preserves every package, event, unit, and modularity construct.
- Using conformance results as evidence of biological validity.

### Relevant catalog entries

[resource:systems-biology-markup-language-sbml] [resource:cellml] [resource:simulation-experiment-description-markup-language-sed-ml] [resource:combine-omex-archive] [resource:sbml-test-suite] [resource:biosimulators-test-suite] [resource:common-workflow-language-cwl] [resource:workflow-description-language-wdl] [resource:functional-mock-up-interface-fmi]

### Example architecture

A model repository stores an SBML or CellML model, a SED-ML experiment, and supporting data inside a COMBINE Archive. Continuous integration checks the SBML engine against the SBML Test Suite and executes compatible archive cases through the BioSimulators Test Suite, recording tool and specification versions separately.

---

## 14. Organize neuroscience datasets and exchange neurophysiology recordings

[problem:exchange-neuroscience-data]

### Situation

A neuroscience program must organize multi-subject datasets, preserve modality metadata, exchange continuous neurophysiology and derived results, and connect research datasets with clinical imaging infrastructure.

### Starting point

Use [resource:brain-imaging-data-structure-bids] for dataset-level organization, filenames, modality metadata, sidecars, and derivatives. Use [resource:neurodata-without-borders-nwb] for typed neurophysiology acquisition, stimulus, behavior, processing, and analysis structures inside extensible files. Use [resource:dicomweb] when clinical imaging studies must move through DICOM services.

BIDS and NWB solve different layers and may be composed. BIDS is generally stronger for dataset layout and pipeline discovery; NWB is stronger for rich internal neurophysiology structures and cross-language access.

### When an alternative is stronger

- Beamline or scattering-facility experiments: use [resource:nexus].
- Generic research-object packaging across data, software, people, and workflows: use [resource:ro-crate].
- Exact workflow execution evidence: use [resource:workflow-run-ro-crate] or [resource:cwlprov].

### Limitations and common category errors

- Treating BIDS validation as scientific or acquisition-quality validation.
- Treating HDF5 or NIfTI alone as substitutes for BIDS or NWB semantics.
- Discarding DICOM metadata during conversion without a traceability plan.
- Assuming NWB replaces dataset-level organization or BIDS replaces typed signal structures.

### Relevant catalog entries

[resource:brain-imaging-data-structure-bids] [resource:neurodata-without-borders-nwb] [resource:dicomweb] [resource:nexus] [resource:ro-crate] [resource:workflow-run-ro-crate] [resource:cwlprov]

### Example architecture

A repository ingests scanner data through DICOMweb, converts deidentified acquisitions into a BIDS dataset, validates the resulting layout, and stores electrophysiology sessions in NWB. A RO-Crate publication layer links datasets, software, investigators, and provenance without replacing either domain standard.

---

## 15. Exchange astronomy files, tables, and federated query results

[problem:exchange-astronomy-data]

### Situation

An astronomy program must preserve instrument or mission products, exchange richly annotated catalog tables, and let clients query holdings across independently operated data centers.

### Starting point

Use [resource:flexible-image-transport-system-fits] for durable images, spectra, cubes, and table files. Use [resource:ivoa-votable] for table results with Virtual Observatory metadata and serializations. Use [resource:ivoa-table-access-protocol-tap] when clients need synchronous or asynchronous remote queries, ADQL, uploads, metadata discovery, or spatial cross-matching.

The mechanisms compose. A TAP service commonly returns VOTable results whose rows identify FITS products. Record the role of each layer independently so file conformance, response serialization, and service behavior are not conflated.

### When an alternative is stronger

- Earth-observation and general spatiotemporal asset catalogs: use [resource:spatiotemporal-asset-catalog-stac].
- Generic catalog federation outside astronomy: use [resource:w3c-data-catalog-vocabulary-dcat].
- Packaging files with software and provenance: use [resource:ro-crate].

### Limitations and common category errors

- Treating VOTable as a service protocol or TAP as a file format.
- Treating FITS header validity as complete scientific metadata quality.
- Adding ObsCore, SAMP, and every IVOA companion without a distinct integration decision.
- Assuming every TAP validator stage covers every query language, profile, and registration behavior.

### Relevant catalog entries

[resource:flexible-image-transport-system-fits] [resource:ivoa-votable] [resource:ivoa-table-access-protocol-tap] [resource:spatiotemporal-asset-catalog-stac] [resource:w3c-data-catalog-vocabulary-dcat] [resource:ro-crate]

### Example architecture

A mission archive stores calibrated products as FITS, exposes catalog and observation tables through TAP, serializes query results as VOTable, and packages release documentation, software, and provenance in RO-Crate. ObsCore is applied as a table profile where uniform observation discovery is required.

---

## 16. Exchange cloud-native bioimaging data

[problem:exchange-bioimaging-data]

### Situation

A microscopy program must exchange multidimensional images, resolution pyramids, labels, plates, wells, axes, and coordinate metadata through object stores and distributed analysis tools.

### Starting point

Use [resource:ome-ngff] for cloud-native OME-Zarr bioimaging data. Declare the OME-Zarr metadata version, Zarr version, and optional features supported by each producer and consumer. Validate the resulting hierarchy and metadata, then test representative datasets across the actual readers and writers in the workflow.

Use [resource:dicomweb] for clinical DICOM studies and service operations, [resource:nexus] for neutron, X-ray, or muon facility application definitions, and [resource:ro-crate] to package images with software, people, instruments, workflows, and provenance.

### When an alternative is stronger

- Mature single-file microscopy exchange and broad installed-base readers: OME-TIFF may remain stronger.
- Clinical imaging identity, metadata, and regulated service workflows: use [resource:dicomweb].
- Generic chunked arrays without bioimaging semantics: Zarr may be sufficient as a storage substrate, though it does not replace OME-NGFF.

### Limitations and common category errors

- Treating generic Zarr readability as OME-Zarr conformance.
- Assuming all readers support the same OME-Zarr versions and optional metadata.
- Treating validation as proof of lossless conversion or scientifically correct coordinates.
- Using RO-Crate as an image representation instead of a contextual package.

### Relevant catalog entries

[resource:ome-ngff] [resource:dicomweb] [resource:nexus] [resource:ro-crate]

### Example architecture

A microscopy facility converts acquisition files to versioned OME-Zarr, validates the hierarchy, writes compatibility fixtures for its production viewers, and stores datasets in object storage. A RO-Crate layer connects each image collection to acquisition instruments, conversion software, analysis workflows, and provenance.
## 17. Represent genomic variation and exchange phenotype context while accessing distributed sequence data

Use [resource:ga4gh-variation-representation-specification-vrs] for normalized variation concepts and computed identifiers, [resource:ga4gh-phenopackets] for phenotype and interpretation records, [resource:ga4gh-htsget] for region-scoped read or variant retrieval, and [resource:ga4gh-refget-sequences] for content-derived reference-sequence identity and retrieval. [resource:ga4gh-data-repository-service-drs] complements htsget when complete data objects must be resolved. See the [genomic representation and access guide](decision-guides/genomic-representation-and-access.md).

## 18. Preserve sequence-sample and ecological dataset context

[problem:preserve-sequence-and-ecology-context]

Use [resource:minimum-information-about-any-sequence-mixs] for sequence-associated sample and environmental metadata, [resource:ecological-metadata-language-eml] for complete ecological dataset descriptions, [resource:igsn-id] for persistent sample identity, [resource:darwin-core] for biodiversity records, and [resource:isa-json] for investigation, study, and assay structure. See the [ecology and sequence-context guide](decision-guides/ecology-and-sequence-context-metadata.md).

## 19. Exchange mass-spectrometry primary data

[problem:exchange-mass-spectrometry-data]

Use [resource:hupo-psi-mzml] to exchange spectra, chromatograms, binary arrays, instrument settings, acquisition context, and processing metadata across converters, analysis tools, and repositories. Compare [resource:analytical-information-markup-language-animl] and [resource:allotrope-data-format] when the integration spans broader analytical techniques. See the [mass-spectrometry guide](decision-guides/mass-spectrometry-data.md).

## 20. Separate clinical exchange, study operations, and observational analytics

[problem:integrate-clinical-research-data]

Use [resource:hl7-fhir] for operational healthcare exchange, [resource:cdisc-operational-data-model-odm] for clinical-study interchange and archival, [resource:omop-common-data-model] for harmonized observational analytics, and [resource:ga4gh-phenopackets] for phenotype-centered genomic records. See the [clinical research data models guide](decision-guides/clinical-research-data-models.md).

## 21. Exchange computational-neuroscience models across simulators and scales

[problem:exchange-computational-neuroscience-models]

### Situation

A modeling program must preserve explicit cellular and network semantics, execute models in independently developed simulators, and exchange instantiated large-scale circuits and simulation products without confusing model validity with behavioral equivalence.

### Starting point

Use [resource:neuroml] for declarative neuronal cells, morphologies, membrane properties, channels, networks, inputs, units, and simulation definitions. Use [resource:sonata] when large instantiated networks, configurations, inputs, spikes, and time-series reports require HDF5-backed performance representation.

The mechanisms are complementary. Retain a canonical semantic representation where feasible, record conversion and profile decisions, and test representative models in every target simulator.

### When an alternative is stronger

- Experimental neurophysiology acquisition and analysis data: use [resource:neurodata-without-borders-nwb].
- Subject, session, modality, and derivative organization: use [resource:brain-imaging-data-structure-bids].
- General systems-biology reaction or physiological equation models: use [resource:systems-biology-markup-language-sbml] or [resource:cellml].
- Exact conversion and execution evidence: use [resource:workflow-run-ro-crate] or [resource:cwlprov].

### Limitations and common category errors

- Treating NeuroML schema validation as proof of numerical equivalence across simulators.
- Treating SONATA implementation tests as a public format-wide conformance suite.
- Treating HDF5 readability as evidence of SONATA or NWB semantics.
- Omitting converter versions, extension profiles, unsupported constructs, or parameter mappings.
- Using an experimental-data standard as the canonical computational model language.

### Relevant catalog entries

[resource:neuroml] [resource:sonata] [resource:neurodata-without-borders-nwb] [resource:brain-imaging-data-structure-bids] [resource:systems-biology-markup-language-sbml] [resource:cellml] [resource:workflow-run-ro-crate] [resource:cwlprov]

### Example architecture

A repository validates canonical NeuroML models and runs cross-simulator fixtures. A versioned conversion step emits SONATA networks for large-scale BMTK or NetPyNE execution, records mappings and unsupported constructs, and packages execution evidence with Workflow Run RO-Crate. Experimental comparison data remains in NWB, with BIDS or RO-Crate supplying study-level organization.
