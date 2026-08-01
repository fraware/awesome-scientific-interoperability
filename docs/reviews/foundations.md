# Review notes: Foundations

**Review date:** 2026-08-01  
**Reviewer role:** Section reviewer (PR-04 catalog migration A)  
**Records migrated:** 4

## Sources inspected

| Resource | Primary sources |
|----------|-----------------|
| Cross-Domain Interoperability Framework (CDIF) | [CDIF Handbook v1.1](https://cdif.codata.org/); [WorldFAIR CDIF release (Zenodo)](https://doi.org/10.5281/zenodo.11236871); [CODATA CDIF initiative page](https://codata.org/initiatives/making-data-work/cdif/) |
| EOSC Interoperability Framework | [EOSC Association interoperability framework report](https://eosc.eu/eosc-interoperability-framework/); [Zenodo report DOI](https://doi.org/10.5281/zenodo.10843882) |
| FAIR Digital Object Framework | [FDO Forum specifications](https://fairdo.org/specifications/); [FDO Requirement Specification (Zenodo)](https://doi.org/10.5281/zenodo.7781925) |
| FAIR Principles | [GO FAIR FAIR Principles page](https://www.go-fair.org/fair-principles/); [Wilkinson et al. Scientific Data paper](https://www.nature.com/articles/sdata201618) |

## Changes made

- Renamed `description` to `summary` (exact README parity preserved).
- Removed v1 scoring fields (`evidence_level`, `maintenance_signal`, `north_star_utility`).
- Added v2 maturity, evidence_types, implementation_status, conformance_status, stewardship, domains, source_urls, alternatives, related_resource_ids, and review_due_on (2027-08-01).
- Linked CDIF, EOSC, and FDO through `related_resource_ids`; FAIR Principles linked to FDO and FAIRsharing.
- Recorded CODATA, EOSC Association, FDO Forum, and GO FAIR Foundation stewardship from canonical specification sites.

## Unresolved questions

- CDIF conformance tooling is emerging (validation tools noted in v1.1 release notes) but no public suite is catalogued yet; conformance_status remains `none-known`.
- FDO formal specification is being revised (2026 note on fairdo.org); maturity recorded as `maintained` pending next recommendation cycle.

## Conflicts

None.
