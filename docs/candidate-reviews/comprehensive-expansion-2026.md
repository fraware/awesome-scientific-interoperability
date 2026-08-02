# Comprehensive corpus expansion review — 2026

## Objective

This review expands the evidence base behind Awesome Scientific Interoperability without weakening the main-list admission standard. It records strong omissions, adjacent standards that require a boundary decision, and emerging candidates that should remain under observation. It does not automatically add any resource to the README or canonical catalog.

The expansion registry is machine-readable under `catalog/expansion-candidates.yaml` and its thematic shards in `catalog/candidates/`. The validator rejects duplicate identities, detects overlap with the live catalog and watchlist, requires deeper source coverage for admission candidates, and preserves minimum breadth across scientific interoperability families.

## Corpus result

The review contains:

- **61 candidates**;
- **58 distinct interoperability families**;
- **20 P0 admission candidates**;
- **26 P1 boundary-review candidates**;
- **15 P2 candidates**;
- **20 `admission-pr`**, **28 `boundary-review`**, and **13 `watchlist`** dispositions.

Comprehensiveness here means systematic coverage of consequential interoperability mechanisms. It does not mean listing every scientific format, software package, ontology, or implementation.

## Admission method

A P0 candidate must satisfy all of the following before a focused admission PR is opened:

1. It exposes a public, inspectable contract such as a specification, schema, API, exchange format, or conformance mechanism.
2. The connected scientific objects or systems and the mechanism joining them can be stated precisely.
3. It fills a material integration problem that the present 87-resource corpus does not answer adequately.
4. It has credible stewardship and implementation or institutional-adoption evidence.
5. It adds decision value beyond an existing resource or a more appropriate family-level representative.
6. At least three primary technical sources are recorded in the candidate registry.

P1 resources have credible technical value but need an explicit decision about family granularity, overlap, scope, or evidence depth. P2 resources are important research infrastructure candidates whose scientific specificity, maintenance, implementation independence, or editorial fit remains insufficient for immediate admission.

## Principal gaps found

### Systems biology and computational model exchange

The list contains the SBML Test Suite but omits SBML itself. It also lacks SED-ML and CellML, leaving no direct representation of the core model and simulation-experiment exchange contracts used across systems biology and physiological modeling.

P0 candidates:

- Systems Biology Markup Language (SBML);
- Simulation Experiment Description Markup Language (SED-ML);
- CellML.

Boundary candidates include NeuroML, SBOL, BioPAX, SBGN, SSP, and DCP. These should be assessed by distinct role: model structure, experiment description, design exchange, pathway knowledge, visual notation, system composition, and distributed co-simulation.

### Neuroscience

The current corpus has no principal neuroscience data standard. BIDS and NWB answer different integration problems and both merit focused admission review:

- **BIDS** standardizes dataset organization, filenames, sidecar metadata, modalities, and derivatives.
- **NWB** standardizes neurophysiology acquisition, processing, analysis, and experimental metadata through an extensible schema and container.

NeuroML and SONATA require a separate model-exchange boundary review. NIfTI and HDF5 should generally be treated as substrates beneath BIDS or NWB unless a storage-format comparison becomes an explicit user problem.

### Bioimaging

OME-NGFF is the strongest missing cloud-native bioimaging mechanism. It standardizes multidimensional array layout and metadata over Zarr for object stores and distributed analysis systems. OME-TIFF remains a major installed-base format and should be adjudicated against OME-NGFF rather than admitted reflexively as a second family entry.

### Astronomy

Astronomy is absent despite operating one of the most mature scientific interoperability ecosystems. The review separates functional roles:

- **FITS** — file and metadata exchange;
- **VOTable** — tabular serialization;
- **TAP** — federated table query services;
- **ObsCore/ObsTAP** — observation discovery profile;
- **SAMP** — application messaging;
- **ASDF** — modern hierarchical scientific data exchange.

The first admission batch should contain FITS, VOTable, and TAP. ObsCore, SAMP, and ASDF require a family-granularity decision so the list explains complementary roles without overrepresenting one standards body.

### Genomic representation, discovery, and access

The existing GA4GH entries cover service discovery, workflow execution, object resolution, authorization, and data-use semantics. They do not cover several central genomic interoperability layers:

- **VRS** — normalized variation representation and computed identifiers;
- **Phenopackets** — phenotype, disease, biosample, pedigree, and genomic interpretation exchange;
- **htsget** — regional retrieval of genomic read and variation data;
- **refget** — checksum-addressed reference-sequence identification and retrieval.

Beacon v2, the HTS file-format family, Crypt4GH, and RNAget remain boundary or watchlist candidates because the catalog must control GA4GH family concentration and distinguish discovery, files, encryption, and data-access APIs.

### Ecology, environment, and agriculture

The current list includes Darwin Core but lacks ecology dataset metadata and contextual sequence metadata.

P0 candidates:

- **Ecological Metadata Language (EML)** — dataset methods, coverage, provenance, tables, and distribution metadata;
- **MIxS** — contextual metadata for sequenced samples and environmental packages.

MIAPPE and BrAPI form a coherent plant-science pair but need an adoption and overlap review. GeoPackage, GeoParquet, SensorML, WaterML, OGC API Records, OGC API EDR, and GeoSciML are retained as boundary or watchlist candidates under an explicit OGC family policy.

### Chemistry, proteomics, and analytical instruments

HUPO-PSI mzML is the strongest missing analytical-data exchange standard. It connects instrument output, spectra, chromatograms, metadata, controlled vocabularies, repositories, and analysis tools. It provides decision value beyond the broader AnIML and Allotrope entries.

mzIdentML, mzTab, nmrML, and CML remain boundary candidates. The catalog should represent the PSI ecosystem by functional role and avoid admitting every related format without a concrete integration problem.

### Clinical and observational research

FHIR covers healthcare resource exchange, but two different research problems remain missing:

- **CDISC ODM** — clinical study operational-data and metadata exchange and archival;
- **OMOP Common Data Model** — harmonization of longitudinal observational health data for federated analysis.

These mechanisms are complementary. ODM transports and archives study structures and records; OMOP normalizes source data into a shared analytical model. Define-XML and openEHR remain subordinate or watchlist candidates pending a narrower use-case decision.

### Repository preservation and lightweight packaging

OCFL and Data Package address gaps left by BagIt and RO-Crate:

- **OCFL** standardizes durable, versioned repository object layout, inventories, fixity, and rebuildability.
- **Data Package** provides a lightweight JSON descriptor for datasets, resources, schemas, dialects, licensing, and distribution metadata.

OCFL is already on the structured watchlist; the expansion registry records that overlap explicitly. PREMIS, SHACL, Zarr, NetCDF, HDF5, Arrow, and Parquet require substrate or preservation-boundary decisions and should not enter the main list solely because they are widely used.

## P0 admission queue

The complete first-order queue is:

1. Systems Biology Markup Language (SBML)
2. Simulation Experiment Description Markup Language (SED-ML)
3. CellML
4. Brain Imaging Data Structure (BIDS)
5. Neurodata Without Borders (NWB)
6. OME-NGFF
7. Flexible Image Transport System (FITS)
8. IVOA Table Access Protocol (TAP)
9. IVOA VOTable
10. GA4GH Variation Representation Specification (VRS)
11. GA4GH Phenopackets
12. GA4GH htsget
13. GA4GH refget Sequences
14. Minimum Information about any (X) Sequence (MIxS)
15. Ecological Metadata Language (EML)
16. HUPO-PSI mzML
17. Oxford Common File Layout (OCFL)
18. Data Package Standard
19. OMOP Common Data Model
20. CDISC Operational Data Model (ODM)

This queue is a research conclusion, not an instruction to merge twenty entries at once. Each resource must be migrated into the live catalog model used by the engineering work, connected through typed relationships when available, and validated against the exact main head.

## Recommended PR sequence

### Batch A — systems biology and neuroscience anchors

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

### Batch B — astronomy and bioimaging

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

### Batch C — genomic representation and access

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
