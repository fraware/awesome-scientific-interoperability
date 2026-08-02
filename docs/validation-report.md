# Validation Report

**State:** Stacked Issue #44 Batch E candidate tree
**Validation date:** 2026-08-02
**Catalog version:** 2.2.0
**Human review status:** Pending maintainer approval before merge

## Corpus counts

| Item | Count |
|---|---:|
| Main-list catalog entries | 107 |
| README list entries (parity) | 107 |
| Section-scoped resource shards | 11 |
| Technical references | 435 |
| Steward identities | 117 |
| Implementation/validator identities | 68 |
| Watchlist items | 16 |
| Expansion candidates remaining | 41 |
| Decision guides (excluding index) | 18 |
| Integration problems | 20 |
| Deterministic unit tests | 124 |

## Proposed Batch A through Batch E additions

### Batch A — systems biology and neuroscience

- Systems Biology Markup Language (SBML)
- Simulation Experiment Description Markup Language (SED-ML)
- CellML
- Brain Imaging Data Structure (BIDS)
- Neurodata Without Borders (NWB)

### Batch B — astronomy and bioimaging

- OME-NGFF / OME-Zarr
- Flexible Image Transport System (FITS)
- IVOA Table Access Protocol (TAP)
- IVOA VOTable

### Batch C — genomic representation and access

- GA4GH Variation Representation Specification (VRS)
- GA4GH Phenopackets
- GA4GH htsget
- GA4GH refget Sequences

### Batch D — ecology, analytical data, and clinical research

- Minimum Information about any (X) Sequence (MIxS)
- Ecological Metadata Language (EML)
- HUPO-PSI mzML
- OMOP Common Data Model
- CDISC Operational Data Model (ODM)

### Batch E — preservation and packaging

- Oxford Common File Layout (OCFL)
- Data Package Standard

The records include claim-specific references, normalized stewards, implementation identities, typed relations, controlled taxonomy, review provenance, direct decision paths, and conservative conformance classifications. Strong implementation-independence claims require separately operated implementation identities. Public-suite, public-validator, and documented-test claims require direct artifacts.

## Completed local checks

- JSON Schema and semantic validation passed for all 107 resources.
- README/catalog name, URL, section, and summary parity passed at 107/107.
- All 435 references, 117 stewards, and 68 implementation identities resolve without unknown IDs.
- Independent-implementation checks passed using distinct operator identities outside each specification steward.
- Public-suite, public-validator, and documented-tests claims resolve to direct artifact-class evidence.
- Typed relations resolve without isolates or self-links.
- Decision-guide and integration-problem resource markers resolve.
- Watchlist validation and expansion-candidate conservation validation pass.
- Review freshness passes as of 2026-08-02.
- Data-quality audit reports zero integrity errors and zero evidence-depth queues.
- Coverage audit reports no concentration or integrity warnings.
- Offline syntax validation covers 467 unique HTTPS URLs across canonical, watchlist, steward, implementation, and evidence references.
- All 124 deterministic unit tests pass.
- Manifest verified for 169 tracked release files.

## Network link audit status

The last completed network audit remains the historical v1.1.0 run:

- **Workflow run:** `30723706703`
- **Date:** 2026-08-01
- **Corpus:** 87 main-list canonical URLs
- **Blocking failures:** 0
- **Classifications:** 78 ok, 7 redirected, 2 access-policy

Batches A through E add new URLs. This report does not claim that those URLs have passed a live network audit. The Links workflow must run on the exact final mergeable head, and its JSON and Markdown artifacts must be retained before the next release.

## Quality workflow alignment

| Check | Implementation |
|---|---|
| Catalog, registries, independence, typed relations, review provenance | `scripts/validate_catalog.py` and unit tests |
| Fail-closed evidence depth | `scripts/audit_data_quality.py --fail-on warning` |
| Decision support | `validate_problem_index.py`, `validate_decision_guides.py` |
| Expansion registry | `validate_expansion_candidates.py` |
| Watchlist and freshness | `validate_watchlist.py`, `check_review_freshness.py` |
| Offline URL scope | `check_links.py --offline --scope all` |
| Coverage balance | `audit_coverage.py` |
| Manifest integrity | `generate_manifest.py`, `verify_manifest.py` |
| Awesome formatting | native `npx --yes awesome-lint` in GitHub Actions |

## Review constraint

The twenty proposed Batch A through Batch E records were prepared through AI-assisted primary-source review and carry author-level review provenance. They must not be represented as independently reviewed. Human maintainers must inspect the primary sources, implementation operators, evidence classifications, family boundaries, typed relations, and decision-guide recommendations before approval.

## Release constraints

- This report does not claim completeness, certification, or exhaustive landscape coverage.
- Central Awesome submission remains closed pending the timing and honesty gates in `docs/publishing.md`.
- No main-list resource is automatically admitted from the expansion registry.
