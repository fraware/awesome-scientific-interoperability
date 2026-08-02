# Comprehensive corpus expansion review — 2026

## Objective

This review expands the evidence base behind Awesome Scientific Interoperability without weakening the main-list admission standard. It records strong omissions, adjacent standards that require a boundary decision, and emerging candidates that should remain under observation. It does not automatically add any resource to the README or canonical catalog.

The expansion registry is machine-readable under `catalog/expansion-candidates.yaml` and its thematic shards in `catalog/candidates/`. The validator rejects duplicate identities, detects overlap with the live catalog and watchlist, requires deeper source coverage for admission candidates, and preserves minimum breadth across scientific interoperability families.

## Corpus result

The review contains:

- **35 unresolved candidates**;
- **35 distinct unresolved interoperability families**;
- **0 P0 admission candidates**;
- **24 P1 boundary-review candidates**;
- **15 P2 candidates**;
- **0 `admission-pr`**, **28 `boundary-review`**, and **13 `watchlist`** unresolved dispositions.
- **22 completed candidate IDs** tracked against the original 61-resource research program.

Comprehensiveness here means systematic coverage of consequential interoperability mechanisms. It does not mean listing every scientific format, software package, ontology, or implementation.

## Admission method

A P0 candidate must satisfy all of the following before a focused admission PR is opened:

1. It exposes a public, inspectable contract such as a specification, schema, API, exchange format, or conformance mechanism.
2. The connected scientific objects or systems and the mechanism joining them can be stated precisely.
3. It fills a material integration problem that the current main-list corpus does not answer adequately.
4. It has credible stewardship and implementation or institutional-adoption evidence.
5. It adds decision value beyond an existing resource or a more appropriate family-level representative.
6. At least three primary technical sources are recorded in the candidate registry.

P1 resources have credible technical value but need an explicit decision about family granularity, overlap, scope, or evidence depth. P2 resources are important research infrastructure candidates whose scientific specificity, maintenance, implementation independence, or editorial fit remains insufficient for immediate admission.

## Principal gaps found

### Systems biology and computational model exchange

Batch A admits SBML, SED-ML, and CellML, adding direct representation of model structure, simulation-experiment description, and modular mathematical-model exchange across systems biology and physiological modeling.

Boundary candidates include NeuroML, SBOL, BioPAX, SBGN, SSP, and DCP. These should be assessed by distinct role: model structure, experiment description, design exchange, pathway knowledge, visual notation, system composition, and distributed co-simulation.

### Neuroscience

Batch A admits two principal neuroscience data standards that answer different integration problems:

- **BIDS** standardizes dataset organization, filenames, sidecar metadata, modalities, and derivatives.
- **NWB** standardizes neurophysiology acquisition, processing, analysis, and experimental metadata through an extensible schema and container.

NeuroML and SONATA require a separate model-exchange boundary review. NIfTI and HDF5 should generally be treated as substrates beneath BIDS or NWB unless a storage-format comparison becomes an explicit user problem.

### Bioimaging

The stacked Batch B draft proposes OME-NGFF as the cloud-native bioimaging mechanism. It standardizes multidimensional array layout and metadata over Zarr for object stores and distributed analysis systems. Batch G admits OME-TIFF as the installed-base file representation, complementary to OME-NGFF rather than a duplicate family entry.

### Astronomy

The stacked Batch B draft proposes three astronomy mechanisms and preserves three adjacent boundary decisions. The review separates functional roles:

- **FITS** — file and metadata exchange;
- **VOTable** — tabular serialization;
- **TAP** — federated table query services;
- **ObsCore/ObsTAP** — observation discovery profile;
- **SAMP** — application messaging;
- **ASDF** — modern hierarchical scientific data exchange.

Batch B proposes FITS, VOTable, and TAP. Batch G completes the role-sensitive boundary by admitting ObsCore for observation discovery, SAMP for application messaging, and ASDF for hierarchical schema-and-extension data exchange.

### Genomic representation, discovery, and access

The stacked Batch C draft proposes four additional GA4GH mechanisms that cover central genomic interoperability layers:

- **VRS** — normalized variation representation and computed identifiers;
- **Phenopackets** — phenotype, disease, biosample, pedigree, and genomic interpretation exchange;
- **htsget** — regional retrieval of genomic read and variation data;
- **refget** — checksum-addressed reference-sequence identification and retrieval.

Beacon v2, the HTS file-format family, Crypt4GH, and RNAget remain boundary or watchlist candidates because the catalog must control GA4GH family concentration and distinguish discovery, files, encryption, and data-access APIs.

### Ecology, environment, and agriculture

Batch D proposes EML and MIxS as complementary mechanisms for ecology dataset metadata and contextual sequence metadata.

MIAPPE and BrAPI form a coherent plant-science pair but need an adoption and overlap review. GeoPackage, GeoParquet, SensorML, WaterML, OGC API Records, OGC API EDR, and GeoSciML are retained as boundary or watchlist candidates under an explicit OGC family policy.

### Chemistry, proteomics, and analytical instruments

Batch D proposes HUPO-PSI mzML as the mass-spectrometry primary-data exchange standard, with AnIML and Allotrope retained as broader analytical-data comparisons.

mzIdentML, mzTab, nmrML, and CML remain boundary candidates. The catalog should represent the PSI ecosystem by functional role and avoid admitting every related format without a concrete integration problem.

### Clinical and observational research

Batch D proposes two complementary clinical-research mechanisms beyond FHIR:

- **CDISC ODM** — clinical study operational-data and metadata exchange and archival;
- **OMOP Common Data Model** — harmonization of longitudinal observational health data for federated analysis.

These mechanisms are complementary. ODM transports and archives study structures and records; OMOP normalizes source data into a shared analytical model. Define-XML and openEHR remain subordinate or watchlist candidates pending a narrower use-case decision.

### Repository preservation and lightweight packaging

OCFL and Data Package address gaps left by BagIt and RO-Crate:

- **OCFL** standardizes durable, versioned repository object layout, inventories, fixity, and rebuildability.
- **Data Package** provides a lightweight JSON descriptor for datasets, resources, schemas, dialects, licensing, and distribution metadata.

OCFL is already on the structured watchlist; the expansion registry records that overlap explicitly. PREMIS, SHACL, Zarr, NetCDF, HDF5, Arrow, and Parquet require substrate or preservation-boundary decisions and should not enter the main list solely because they are widely used.

## Batch A proposed in draft (2026-08-02)

The first five P0 candidates are represented in the stacked candidate tree and removed from its unresolved registry:

1. Systems Biology Markup Language (SBML)
2. Simulation Experiment Description Markup Language (SED-ML)
3. CellML
4. Brain Imaging Data Structure (BIDS)
5. Neurodata Without Borders (NWB)

Their proposed records include claim-specific references, implementation identities, typed relations, controlled taxonomy, review provenance, and direct decision paths. Human maintainer approval remains required.

## Recommended PR sequence

### Batch A — systems biology and neuroscience anchors — completed

Candidate set:

- SBML;
- SED-ML;
- CellML;
- BIDS;
- NWB.

Required comparisons:

- SBML versus CellML;
- SED-ML versus workflow and execution provenance;
- BIDS versus NWB;
- domain profiles versus HDF5 and NIfTI substrates.

### Batch B — astronomy and bioimaging — proposed in stacked draft

Candidate set:

- OME-NGFF;
- FITS;
- VOTable;
- TAP.

Required comparisons:

- OME-NGFF versus OME-TIFF and Zarr;
- FITS versus ASDF;
- VOTable serialization versus TAP query services;
- TAP versus ObsCore profiles and SAMP messaging.

### Batch C — genomic representation and access — proposed in stacked draft

**Batch C implementation status:** represented in the stacked Issue #44 Batch C candidate tree; human review remains required.

Candidate set:

- VRS;
- Phenopackets;
- htsget;
- refget.

Required comparisons:

- VRS versus ordinary variant file serialization;
- Phenopackets versus FHIR and general phenotype ontologies;
- htsget versus DRS;
- refget versus Identifiers.org and SWHIDs;
- family concentration across all GA4GH entries.

### Batch D — ecology, proteomics, and clinical research

Candidate set:

- MIxS;
- EML;
- mzML;
- OMOP CDM;
- CDISC ODM.

Required comparisons:

- MIxS versus IGSN, ISA-JSON, and Darwin Core;
- EML versus Darwin Core and DCAT;
- mzML versus AnIML and Allotrope;
- OMOP versus FHIR;
- ODM versus FHIR, OMOP, and Define-XML.

### Batch E — preservation and lightweight packaging

Candidate set:

- OCFL;
- Data Package.

Required comparisons:

- OCFL versus BagIt and semantic research-object packaging;
- Data Package versus RO-Crate, Croissant, and generic tabular schemas.

### Batch F — boundary adjudication

Evaluate P1 candidates by family, with explicit admit, watchlist, or reject decisions:

- NeuroML and SONATA;
- OME-TIFF;
- SAMP, ObsCore, and ASDF;
- Beacon v2 and HTS specifications;
- MIAPPE and BrAPI;
- SBOL, BioPAX, SBGN, mzIdentML, mzTab, nmrML, and CML;
- GeoPackage, GeoParquet, SensorML, and WaterML;
- SSP and DCP;
- Zarr, PREMIS, and SHACL.

### Batch G — explicit substrate and long-tail exclusions

Record durable decisions for NetCDF, HDF5, Arrow, Parquet, NIfTI, Crypt4GH, RNAget, OGC API Records, OGC API EDR, GeoSciML, Define-XML, openEHR, openMINDS, ASAM MDF, and PID Kernel Information. Several may remain important dependencies without deserving independent main-list entries.

## Data-quality controls

Every admission PR should:

1. Reconfirm the current specification version and governance source.
2. Add reference records for technical definition, stewardship, implementations, adoption, and conformance only where the source supports that exact role.
3. Avoid inferring implementation independence from multiple repositories controlled by the same organization.
4. State the mechanism, connected systems, decision basis, and boundary note independently.
5. Add typed alternatives and complementary relationships once the engineering model supports them.
6. Update the relevant integration-problem index and decision guide.
7. Regenerate reproducible baselines and the repository manifest.
8. Run all repository quality workflows on the exact final head.

## Explicit scope decisions

- Prefer domain profiles over generic substrates when profiles contain the semantics users need. CF is generally more decision-relevant than NetCDF; BIDS and NWB are more decision-relevant than NIfTI or HDF5; OME-NGFF is more decision-relevant than Zarr alone.
- Represent standards ecosystems by distinct functional roles. Astronomy, GA4GH, OGC, PSI, CDISC, and COMBINE resources require family-level review.
- Separate exchange from analytical harmonization. FHIR and ODM move operational records; OMOP maps data into a common analytical structure.
- Treat implementation popularity as insufficient. Main-list inclusion depends on a documented interoperability mechanism and distinctive decision value.
- Preserve negative decisions. A candidate rejected because it is a generic substrate or duplicates a stronger family entry should retain that rationale in structured form.

## Definition of completion

The expansion track is complete when every P0 candidate has one durable outcome:

- admitted through a focused green PR;
- moved to the watchlist with explicit missing evidence and promotion conditions; or
- rejected through a recorded boundary decision.

P1 and P2 records remain machine-readable so new evidence can change their disposition without repeating the landscape search.
## Batch B outcome — astronomy and bioimaging

The stacked Batch B candidate tree proposes admission of OME-NGFF, FITS, IVOA TAP, and IVOA VOTable. The four IDs are removed from unresolved candidate shards and recorded in `completed_candidate_ids`; the validator now enforces `unresolved candidates + completed candidate IDs = 61`, preserving the full research universe as the queue declines.

Boundary outcomes retained for later adjudication:

- OME-TIFF remains a major installed-base bioimaging format and is compared directly against OME-NGFF.
- ObsCore remains a TAP profile decision, not an automatic peer protocol entry.
- SAMP remains an application-messaging decision.
- ASDF remains a modern hierarchical astronomy-format candidate requiring archive-adoption review.

The Batch B records remain AI-assisted author review pending human maintainer approval.


## Batch C outcome — genomic representation and access

The stacked Batch C candidate tree proposes admission of VRS, Phenopackets, htsget, and refget Sequences. The four IDs are removed from unresolved candidate shards and recorded in `completed_candidate_ids`; the conservation invariant remains `unresolved candidates + completed candidate IDs = 61`.

Boundary outcomes retained for later adjudication:

- Beacon v2 remains a federated discovery decision.
- SAM/BAM/CRAM and VCF/BCF remain a file-family granularity decision.
- Crypt4GH remains a controlled-access encryption-container decision.
- RNAget remains a transcriptomics-access adoption decision.

The Batch C records remain AI-assisted author review pending human maintainer approval.

## Batch D implementation status

The stacked Issue #44 Batch D candidate tree proposes admission of MIxS, EML, HUPO-PSI mzML, OMOP Common Data Model, and CDISC ODM. The five IDs are removed from unresolved candidate shards and recorded in `completed_candidate_ids`; the conservation invariant remains `unresolved candidates + completed candidate IDs = 61`. Human maintainer review remains required.

## Batch E implementation status

The stacked Issue #44 Batch E candidate tree proposes admission of Oxford Common File Layout (OCFL) and Data Package Standard v2. Both IDs are removed from the preservation-infrastructure candidate shard and recorded in `completed_candidate_ids`; the conservation invariant remains `unresolved candidates + completed candidate IDs = 61`. OCFL is promoted off the structured watchlist. Evidence remains AI-assisted author review pending human maintainer approval.


## Batch F implementation status

The stacked Issue #44 Batch F candidate tree proposes admission of NeuroML and SONATA as complementary computational-neuroscience model-exchange mechanisms. NeuroML is admitted as the declarative semantic model contract with public schema validation. SONATA is admitted as the performance-oriented representation for large instantiated networks, configurations, inputs, and simulation reports, with `none-known` public conformance status. Both IDs are removed from the systems-biology-neuroscience candidate shard and recorded in `completed_candidate_ids`; the conservation invariant remains `unresolved candidates + completed candidate IDs = 61`. Evidence remains AI-assisted author review pending human maintainer approval.


## Batch G implementation status

The stacked Issue #44 Batch G candidate tree proposes admission of OME Data Model and OME-TIFF, IVOA ObsCore/ObsTAP, IVOA SAMP, and ASDF. The four mechanisms retain separate decision roles: installed-base microscopy files, federated observation discovery, interactive astronomy application messaging, and hierarchical schema-aware scientific data. Their IDs are removed from the bioimaging-astronomy candidate shard and recorded in `completed_candidate_ids`; the conservation invariant remains `unresolved candidates + completed candidate IDs = 61`. Evidence remains AI-assisted author review pending human maintainer approval.

## Deferred family adjudication (2026-08-02)

Seven deferred-family-review records received durable outcomes without main-list admission:

- GA4GH Beacon v2 and OGC GeoPackage moved to the structured watchlist with concrete promotion and rejection conditions.
- BioPAX and GeoParquet closed as rejected-out-of-scope.
- SSP and DCP closed as rejected-represented-by FMI.
- openMINDS closed as represented by BIDS and NWB.

MIAPPE, BrAPI, and SBOL remain deferred only for a focused admission PR in the same review cycle. Evidence remains AI-assisted author review pending human maintainer approval.

## Plant/agriculture and SBOL admissions (2026-08-02)

Focused admission of MIAPPE, BrAPI, and SBOL closes the remaining deferred plant/agriculture and biological-design family reviews:

- MIAPPE supplies the plant-phenotyping metadata exemplar complementary to EML, MIxS, and ISA-JSON.
- BrAPI supplies the breeding-database API exemplar with separately operated Cassavabase and IPK implementations.
- SBOL supplies synthetic-biology design exchange complementary to SBML/CellML executable models.

Evidence remains AI-assisted author review pending human maintainer approval. No `multiple-independent` claim is made for MIAPPE or SBOL; BrAPI independence is limited to distinct server operators documented in the BrAPI servers directory.
