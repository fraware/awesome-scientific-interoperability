# Review: Validation and Conformance

**Review date:** 2026-08-01  
**Records migrated:** 4  
**Reviewer conflict of interest:** None

## Sources inspected

| ID | Primary sources |
|----|-----------------|
| biosimulators-test-suite | https://docs.biosimulators.org/Biosimulators_test_suite/ ; https://github.com/biosimulators/Biosimulators_test_suite |
| cwl-conformance-tests | https://github.com/common-workflow-language/cwl-v1.2 ; https://www.commonwl.org/v1.2/ConformanceTests.html |
| ro-crate-validator | https://github.com/crs4/rocrate-validator ; https://www.researchobject.org/ro-crate/specification/1.3/ |
| sbml-test-suite | https://sbml.org/software/sbml-test-suite/ ; https://github.com/sbmlteam/sbml-test-suite |

## Contract-testing confirmation

Each resource tests a documented interoperability contract rather than general FAIRness or software-quality scoring:

| ID | Documented contract tested |
|----|----------------------------|
| biosimulators-test-suite | Simulator container interfaces, modeling formats, and execution behavior |
| cwl-conformance-tests | CWL v1.2 workflow-runner requirements |
| ro-crate-validator | RO-Crate profile SHACL shapes and programmatic rules |
| sbml-test-suite | SBML syntactic, semantic, and stochastic simulation equivalence |

## Changes made

- Migrated all four records to v2.
- Set `conformance_status: public-suite` or `public-validator` with direct artifact URLs in `source_urls`.
- Linked BioSimulators and SBML test suites as related within this shard.
- Left `alternatives` and external cross-shard `related_resource_ids` empty with boundary notes (CWL language and RO-Crate packaging entries are outside this PR).

## Unresolved questions

- BioSimulators coverage relative to newer COMBINE standards beyond SBML should be tracked at next review.
- RO-Crate validator profile coverage versus Workflow RO-Crate profiles may expand; confirm at next review.

## Conflicts

None.

## v2.1 provenance migration (2026-08-01)

- Closed isolates: `cwl-conformance-tests` related to CWL and cwltool; `ro-crate-validator` related to RO-Crate and Workflow Run RO-Crate.

## Issue #30 Batch 7 validation evidence (2026-08-01)

- Enriched CWL conformance tests and SBML test suite adoption/implementation links; SBML MI claim adjusted to reference-and-others.

