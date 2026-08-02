# Changelog

All notable editorial, schema, and maintenance changes for this repository are documented here. The list does not claim completeness of the scientific interoperability landscape.

## Unreleased — Issue #44 corpus expansion

### Batch A: systems biology and neuroscience

- Proposed five evidence-backed main-list additions: SBML, SED-ML, CellML, BIDS, and NWB.
- Added 32 technical references, 9 steward identities, 14 implementation/validator identities, and the `neuroscience` scientific-domain tag.
- Added two decision guides and two integration-problem paths covering computational-model exchange and neuroscience data.
- Removed admitted resources from the expansion-candidate registry; 56 researched candidates remain.
- Human maintainer approval remains required before merge.

### Batch B: astronomy and bioimaging

- Proposed OME-NGFF, FITS, IVOA TAP, and IVOA VOTable as distinct bioimaging-file, astronomy-file, table-serialization, and query-service mechanisms.
- Added astronomy and bioimaging decision guides and integration-problem paths.
- Added claim-specific references, operator-normalized implementations, direct validators, typed relations, and role-sensitive coverage families.
- Preserved OME-TIFF, ObsCore, SAMP, ASDF, and generic Zarr as structured boundary candidates.

### Batch C: genomic representation and access

- Proposed VRS, Phenopackets, htsget, and refget Sequences as representation, phenotype-exchange, regional-access, and content-identity mechanisms.
- Added claim-specific references, implementation identities, typed relations, a decision guide, and integration problem 17.
- Preserved Beacon v2, HTS formats, Crypt4GH, and RNAget as structured boundary candidates.
- The stacked Batch C candidate tree contains 100 resources and 48 unresolved candidates; Batches A through C remain pending human maintainer approval.

### Batch D: ecology, analytical data, and clinical research

- Proposed MIxS, EML, HUPO-PSI mzML, OMOP Common Data Model, and CDISC ODM as five distinct context, dataset, analytical-exchange, harmonization, and study-operation mechanisms.
- Added claim-specific references, operator identities, direct validators, typed relations, three decision guides, and integration problems 18 through 20.
- Preserved MIAPPE, BrAPI, mzIdentML, mzTab, nmrML, CML, Define-XML, and openEHR as structured boundary candidates.
- Human maintainer approval remains required before merge.

### Batch E: preservation and packaging

- Proposed Oxford Common File Layout (OCFL) and Data Package Standard v2 as distinct repository-layout and lightweight dataset-descriptor mechanisms.
- Retained OCFL as `reference-and-others` with one separately operated implementation identity and direct validation-code evidence.
- Encoded Data Package v2's uneven software migration and descriptor-scoped validator boundary explicitly.
- Added a repository-preservation and data-packaging decision guide plus packaging problem-path updates.
- Human maintainer approval remains required before merge.

### Batch F: computational-neuroscience model exchange

- Proposed NeuroML and SONATA as complementary declarative-semantic and performance-representation mechanisms.
- Added conservative operator-normalized implementation identities for pyNeuroML, BMTK, and independently governed NetPyNE support.
- Assigned NeuroML `public-validator` status through direct schema-validation evidence and retained SONATA at `none-known` public conformance status.
- Added a computational-neuroscience decision guide, integration problem 21, typed relations, a coverage family, and adversarial batch tests.
- Preserved openMINDS and NIfTI as structured watchlist candidates; human maintainer approval remains required before merge.
- Replaced the obsolete fixed unresolved-candidate floor with conservation of the 61-record research program and a progression-safe 80% family-diversity invariant.

## [1.1.0] — 2026-08-01

First decision-oriented release after catalog v2 migration, domain gap reviews, and maintainer governance formalization. Supersedes the v1.0.0 release candidate documented in `docs/validation-report.md` (initial public corpus: 75 main-list entries; no prior annotated tag).

### Editorial and corpus

- **Main-list entries:** 75 → **87** (+12). No main-list removals; `archive.md` unchanged.
- **PR-16A (statistical and social science):** SDMX added to main list; DDI-CDI placed on watchlist.
- **PR-16B (physical science and engineering):** FMI, CIF, NeXus, OPTIMADE added.
- **PR-16C (geospatial and environmental):** OGC API — Features, Coverages, SensorThings, openEO added.
- **PR-16D (experimental and biomedical):** ISA-JSON, BioCompute Objects, DICOMweb added.
- **PR-17 (taxonomy reassessment):** Kept combined **Agents, Access, and Policy** section; no Reference Architectures section; recorded in `docs/taxonomy.md`.

### Catalog model v2 (PR-03 through PR-07)

- Migrated all main-list records to catalog v2 (`catalog_version: 2.0.0`) across 11 section-scoped shards.
- Enforced stewardship, evidence types, implementation and conformance status, review dates, cross-references, and README parity.
- Retired legacy catalog fields (`evidence_level`, `maintenance_signal`, `north_star_utility`, flat `description`).
- **PR-02 link remediation:** Autoprotocol canonical URL moved to maintained GitHub repository; Scholix canonical URL moved to schema repository.

### Decision support

- **Integration problem index** (`docs/integration-problems.md`): 12 recurring integration problems with validated `[resource:…]` references (PR-09).
- **Decision guides** (PR-10–PR-13): nine topic guides under `docs/decision-guides/` covering research-object packaging, provenance, workflows, identifiers, semantics, laboratories, agents, and controlled-data access.
- **Query CLI** (`scripts/query_catalog.py`, PR-08): filter catalog by section, layer, domain, connects, evidence, or id.

### Watchlist and coverage

- **Structured watchlist** (PR-14): `catalog/watchlist.yaml` with JSON Schema, prose parity in `docs/watchlist.md`, and **17** monitored candidates.
- **Coverage audit** (PR-15): deterministic concentration and gap reporting via `scripts/audit_coverage.py`; baseline updated in `docs/coverage-baseline.md`.

### Governance (PR-18)

- `docs/reviewer-roles.md`, `docs/decision-records.md`, `docs/human-review-log.md`.
- `.github/CODEOWNERS`, remove-resource and taxonomy-change issue templates.
- Extended contributing, conflicts-of-interest, maintenance-protocol, and publishing documentation.

### Validation and CI

- **64** deterministic unit tests across seven modules (see `docs/validation-report.md` for §12 coverage notes).
- Quality workflow: catalog validation, offline links, problem-index and decision-guide checks, watchlist, review freshness, coverage audit, manifest verification, and native Awesome lint.
- **Network link audit** (Links workflow run `30723706703`, 2026-08-01): 87 URLs checked; **0** unresolved blocking failures (78 ok, 7 redirected, 2 access-policy).

### Known limitations

- 18 main-list entries record neither alternatives nor related resource links (concentration warning only).
- CWL standard family has three implementation entries (above configured threshold of two).
- Emerging entries (Autoprotocol, MCP, ToolUniverse) carry shorter review intervals.
- Central Awesome submission is not yet eligible; see `docs/publishing.md`.
- This release does not certify completeness, certification, or exhaustive landscape coverage.

## [1.0.0] — 2026-08-01

Initial public release candidate.

- **75** main-list entries across 11 sections in pre-v2 catalog model.
- Native Awesome lint, offline URL validation, manifest verification, and four unit tests.
- Engineering takeover specification and launch hardening (PR-01 baseline).

[1.1.0]: https://github.com/fraware/awesome-scientific-interoperability/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/fraware/awesome-scientific-interoperability/releases/tag/v1.0.0
