# Validation Report

**State:** Stacked Issue #44 Batch C candidate tree
**Validation date:** 2026-08-02
**Catalog version:** 2.2.0
**Human review status:** Pending maintainer approval before merge

## Corpus counts

| Item | Count |
|---|---:|
| Main-list catalog entries | 100 |
| README list entries (parity) | 100 |
| Section-scoped resource shards | 11 |
| Technical references | 391 |
| Steward identities | 101 |
| Implementation/validator identities | 49 |
| Watchlist items | 17 |
| Expansion candidates remaining | 48 |
| Decision guides (excluding index) | 14 |
| Integration problems | 17 |
| Deterministic unit tests | 114 |

## Proposed Batch A through Batch C additions

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

The records include claim-specific references, normalized stewards, implementation identities, typed relations, controlled taxonomy, review provenance, direct decision paths, and conservative conformance classifications. Strong implementation-independence claims require separately operated implementation identities. Public-suite, public-validator, and documented-test claims require direct artifacts.

## Completed local checks

- JSON Schema and semantic validation passed for all 100 resources.
- README/catalog name, URL, section, and summary parity passed at 100/100.
- All 391 references, 101 stewards, and 49 implementation identities resolve without unknown IDs.
- Independent-implementation checks passed using distinct operator identities outside each specification steward.
- Public-suite, public-validator, and documented-tests claims resolve to direct artifact-class evidence.
- Typed relations resolve without isolates or self-links.
- Decision-guide and integration-problem resource markers resolve.
- Watchlist validation and expansion-candidate conservation validation pass.
- Review freshness passes as of 2026-08-02.
- Data-quality audit reports zero integrity errors and zero evidence-depth queues.
- Coverage audit reports no concentration or integrity warnings.
- Offline syntax validation covers 417 unique HTTPS URLs across canonical, watchlist, steward, implementation, and evidence references.
- All 114 deterministic unit tests pass.
- Manifest generation and verification are required on the exact final PR head.

## Network link audit status

The last completed network audit remains the historical v1.1.0 run:

- **Workflow run:** `30723706703`
- **Date:** 2026-08-01
- **Corpus:** 87 main-list canonical URLs
- **Blocking failures:** 0
- **Classifications:** 78 ok, 7 redirected, 2 access-policy

Batches A through C add new URLs. This report does not claim that those URLs have passed a live network audit. The Links workflow must run on the exact final mergeable head, and its JSON and Markdown artifacts must be retained before the next release.

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

The thirteen proposed Batch A through Batch C records were prepared through AI-assisted primary-source review and carry author-level review provenance. They must not be represented as independently reviewed. Human maintainers must inspect the primary sources, implementation operators, evidence classifications, family boundaries, typed relations, and decision-guide recommendations before approval.

## Release constraints

- This report does not claim completeness, certification, or exhaustive landscape coverage.
- Central Awesome submission remains closed pending the timing and honesty gates in `docs/publishing.md`.
- No main-list resource is automatically admitted from the expansion registry.
