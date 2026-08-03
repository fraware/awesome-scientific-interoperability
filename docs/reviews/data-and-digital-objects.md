# Review notes: Data and Digital Objects

**Review date:** 2026-08-01
**Reviewer role:** Section reviewer (PR-05 catalog migration B)
**Records migrated:** 7

## Sources inspected

| Resource | Primary sources |
|----------|-----------------|
| BagIt | [RFC 8493](https://datatracker.ietf.org/doc/html/rfc8493); [LibraryOfCongress/bagit-python](https://github.com/LibraryOfCongress/bagit-python) |
| COMBINE/OMEX Archive | [combinearchive.org](https://combinearchive.org/); [SemsProject/CombineArchive](https://github.com/SemsProject/CombineArchive) |
| FAIR Signposting | [signposting.org](https://signposting.org/); [EOSC FAIR Signposting uptake report (Zenodo)](https://doi.org/10.5281/zenodo.10490289) |
| RO-Crate | [RO-Crate 1.3 specification](https://www.researchobject.org/ro-crate/specification/1.3/); [rocrate-validator](https://github.com/crs4/rocrate-validator) |
| Workflow RO-Crate | [WorkflowHub profile page](https://about.workflowhub.eu/Workflow-RO-Crate/); [WorkflowHub](https://workflowhub.eu/) |
| Workflow Run RO-Crate | [Workflow Run RO-Crate profile](https://www.researchobject.org/workflow-run-crate/profiles/workflow_run_crate/); [ResearchObject/workflow-run-crate](https://github.com/ResearchObject/workflow-run-crate) |
| Workflow Testing RO-Crate | [w3id.org/ro/wftest](https://w3id.org/ro/wftest); [LifeMonitor](https://lifemonitor.eu/) |

## Changes made

- Renamed `description` to `summary` (exact README parity preserved).
- Removed v1 scoring fields (`evidence_level`, `maintenance_signal`, `north_star_utility`).
- Added v2 maturity, evidence_types, implementation_status, conformance_status, stewardship, domains, source_urls, alternatives, related_resource_ids, and review_due_on (2027-08-01).
- Distinguished packaging (BagIt, RO-Crate base) from workflow-definition packaging (Workflow RO-Crate) and execution provenance (Workflow Run RO-Crate).
- Linked RO-Crate profile family through `related_resource_ids` within group B; BagIt listed as packaging alternative to RO-Crate.
- CWLProv listed as provenance alternative to Workflow Run RO-Crate (cross-shard reference within PR-05).

## Unresolved questions

- COMBINE Archive formal governance beyond the Rostock-hosted toolkit and community site is not documented on the canonical URL; stewardship recorded as community with boundary note on SED-ML/SBML relations (group A/C not cross-linked yet).
- Independent validator coverage for Workflow RO-Crate and Workflow Testing RO-Crate profiles beyond documented tests is not catalogued as a public suite.

## Conflicts

None.

## v2.1 provenance migration (2026-08-01)

- Migrated all records to `source_refs`, `steward_id`, and controlled `resource_kind` / domains.
- Closed isolates: `combine-omex-archive` related to RO-Crate and BioCompute Objects; `fair-signposting` related to RO-Crate and Schema.org; `crystallographic-information-framework-cif` alternatives/related to NeXus.
- Corrected OGC API - Coverages to emerging / reference-and-others / none-known (no public-suite claim without a direct suite artifact).
- Downgraded CIF, FMI, NeXus, OGC API Features, OPTIMADE, and related prior public-* claims to `documented-tests` where artifact URLs were not already present.

## Issue #30 Batch 3 data objects evidence (2026-08-01): enriched BagIt/CIF/FMI/NeXus/OGC Features/RO-Crate; downgraded FAIR Signposting and workflow RO-Crate profile conformance where no suite artifact.


## Issue #30 residual data-object MI adjustments (2026-08-01)

- FMI and RO-Crate multiple-independent claims adjusted to reference-and-others where typed independence evidence remained below threshold after enrichment.


## Issue #44 Batch A admissions (2026-08-02)

**Status:** AI-assisted author review complete; human maintainer approval required before merge.

| Resource | Primary evidence | Decision |
|---|---|---|
| SBML | Level 3 Version 2 Core Release 2; libSBML; COPASI; Tellurium; SBML Test Suite | Admit as established exchange standard with two separately operated implementations and public suite |
| CellML | CellML 2.0; libCellML; OpenCOR | Admit as established modular model standard; retain `reference-and-others` and `none-known` conformance |
| BIDS | BIDS 1.11.1; MNE-BIDS; HeuDiConv; BIDS Validator | Admit as established dataset and metadata standard with two independent operator identities and public validator |
| NWB | NWB Schema; PyNWB; MatNWB; AqNWB; NWB Inspector | Admit as established neurophysiology exchange standard; retain `reference-and-others` because core APIs share NWB stewardship |

**Boundary decisions:** SBML versus CellML is model-class dependent; BIDS and NWB are complementary; generic HDF5 and NIfTI remain excluded under DR-001.

**Conflict disclosure:** None identified. The records explicitly retain pending human maintainer approval in their review provenance.
## Issue #44 Batch B admissions (2026-08-02)

**Status:** AI-assisted author review complete; human maintainer approval required before merge.

| Resource | Primary evidence | Decision |
|---|---|---|
| OME-NGFF / OME-Zarr | OME-Zarr 0.5; tools registry; ome-zarr-py; bioformats2raw; OME-NGFF Validator | Admit as maintained cloud-native bioimaging exchange; retain `reference-and-others` because only one separately operated implementation is modeled |
| FITS | FITS Standard 4.0; IAU-FWG governance; CFITSIO; Astropy FITS verification | Admit as established astronomy file standard with two independent implementations and public validation |
| IVOA VOTable | VOTable 1.5; Astropy VOTable; STILTS; votlint | Admit as established astronomy table serialization with two independent implementations and public validation |

**Boundary decisions:** OME-TIFF remains the mature single-file bioimaging alternative; Zarr alone is a substrate. ASDF remains a separate astronomy-format candidate. FITS and VOTable are complementary rather than interchangeable.

**Conflict disclosure:** None identified. Human maintainer approval is recorded as a merge prerequisite.
## Issue #44 Batch D candidate additions — pending human review

| Resource | Primary evidence | Conservative classification |
|---|---|---|
| HUPO-PSI mzML | [PSI specification](https://www.psidev.info/mzML); [OpenMS validator](https://openms.de/current_doxygen/html/classOpenMS_1_1Internal_1_1MzMLValidator.html) | Established; multiple independent implementations; public semantic validator |
| CDISC ODM v2.0 | [ODM v2.0](https://www.cdisc.org/standards/data-exchange/odm-xml/odm-v2-0); [LinkML model](https://cdisc-org.github.io/DataExchange-ODM-LinkML/) | Maintained; single known official implementation; no public conformance artifact recorded |

## Issue #44 Batch E candidate additions — pending human review

| Resource | Primary evidence | Conservative classification |
|---|---|---|
| Oxford Common File Layout (OCFL) | [OCFL 1.1](https://ocfl.io/1.1/spec/); [validation codes](https://ocfl.io/1.1/spec/validation-codes.html); [ocfl-py](https://github.com/zimeon/ocfl-py); [ocfl-java](https://github.com/OCFL/ocfl-java) | Established; reference-and-others; public validator for layout/fixity rules |
| Data Package Standard v2 | [Data Package](https://datapackage.org/standard/data-package/); [v2 release](https://datapackage.org/blog/2024-06-26-v2-release/); [Frictionless validate](https://framework.frictionlessdata.io/docs/guides/validating-data.html) | Maintained; reference-and-others; public descriptor validator with uneven v2 software migration |

## SBOL admission — pending human maintainer sign-off (2026-08-03)

**Status:** AI-assisted author review; see [maintainer-signoff-miappe-brapi-sbol.md](maintainer-signoff-miappe-brapi-sbol.md).

| Resource | Primary evidence | Conservative classification |
|---|---|---|
| SBOL 3.1.0 | [Data Model 3.1.0](https://sbolstandard.org/datamodel-specification/version-3.1.0/); [pySBOL3](https://github.com/SynBioDex/pySBOL3); [libSBOLj3](https://github.com/SynBioDex/libSBOLj3) | Established; reference-and-others (same SynBioDex steward family); public validator for data-model rules only |

**Relation fix:** `alternative-to` CellML corrected to `complements` (design exchange is not a competing physiological-model mechanism).

**Conflict disclosure:** None identified. Human maintainer approval required.
