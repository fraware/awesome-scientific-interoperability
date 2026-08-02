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
