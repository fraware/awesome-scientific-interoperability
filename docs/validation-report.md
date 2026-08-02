# Validation Report

**State:** Stacked Issue #44 Batch B candidate tree
**Validation date:** 2026-08-02
**Catalog version:** 2.2.0
**Human review status:** Pending maintainer approval before merge

## Corpus counts

| Item | Count |
|---|---:|
| Main-list catalog entries | 96 |
| README list entries (parity) | 96 |
| Section-scoped resource shards | 11 |
| Technical references | 369 |
| Steward identities | 98 |
| Implementation/validator identities | 40 |
| Watchlist items | 17 |
| Expansion candidates remaining | 52 |
| Decision guides (excluding index) | 13 |
| Integration problems | 16 |
| Deterministic unit tests | 109 |

## Batch A and Batch B additions

- Systems Biology Markup Language (SBML)
- Simulation Experiment Description Markup Language (SED-ML)
- CellML
- Brain Imaging Data Structure (BIDS)
- Neurodata Without Borders (NWB)
- OME-NGFF / OME-Zarr
- Flexible Image Transport System (FITS)
- IVOA Table Access Protocol (TAP)
- IVOA VOTable

The records include claim-specific references, normalized stewards, implementation identities, typed relations, four-dimensional taxonomy, review provenance, and two new decision paths. SBML and BIDS retain `multiple-independent` only through distinct independently operated implementations. SED-ML, CellML, and NWB use narrower implementation claims where the evidence does not justify stronger independence.

## Completed local checks

- JSON Schema and semantic validation passed for all 96 resources.
- README/catalog name, URL, section, and summary parity passed at 96/96.
- Reference, steward, and implementation registries resolved without unknown IDs.
- Independent-implementation checks passed using distinct operator identities outside the specification steward.
- Public-suite, public-validator, and documented-tests claims resolve to direct artifact-class evidence.
- Typed relations resolve without isolates or self-links.
- Four taxonomy dimensions accept all live values, including the `neuroscience`, `astronomy`, and `bioimaging` scientific domains.
- Decision-guide and integration-problem resource markers resolve.
- Watchlist validation and expansion-candidate validation pass.
- Review freshness passes as of 2026-08-02.
- Data-quality audit reports zero integrity errors and zero evidence-depth queues.
- Coverage audit reports no concentration or integrity warnings.
- Offline syntax validation covers 393 unique HTTPS URLs across canonical, watchlist, steward, implementation, and evidence references.
- All 109 deterministic unit tests pass.
- Manifest generation and verification are required on the exact final PR head.

## Network link audit status

The last completed network audit remains the historical v1.1.0 run:

- **Workflow run:** `30723706703`
- **Date:** 2026-08-01
- **Corpus:** 87 main-list canonical URLs
- **Blocking failures:** 0
- **Classifications:** 78 ok, 7 redirected, 2 access-policy

Batch A adds new URLs. This report does not claim that those URLs have passed a network audit. The Links workflow must be run on the merged or exact PR head, and its JSON/Markdown artifacts must be retained before the next release.

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

The nine Batch A and Batch B records were prepared through AI-assisted primary-source review and carry author-level review provenance. They must not be represented as independently reviewed. A human maintainer must inspect the primary sources, accept or revise each admission decision, and record approval before merge.

## Release constraints

- This report does not claim completeness, certification, or exhaustive landscape coverage.
- Central Awesome submission remains closed pending the timing and honesty gates in `docs/publishing.md`.
- No main-list resource is automatically admitted from the expansion registry.
