# Coverage Baseline

**Baseline date:** 2026-08-02
**Catalog version:** 2.2.0
**Main-list entries:** 92
**Audit command:** `python scripts/audit_coverage.py --as-of 2026-08-02`

This document records reproducible corpus-balance metrics from the structured catalog. Counts and concentration signals support maintainer review; they are not quality scores and do not determine inclusion or exclusion.

## Policy

Classification thresholds and explicit substrate and standard-family mappings live in `config/coverage-policy.yaml`. Family concentration is evaluated per role-sensitive bucket instead of one undifferentiated implementation count. The audit exits nonzero only for hard data-integrity failures. Editorial concentration warnings are reported without deciding inclusion.

## Summary metrics

| Metric | Value |
|---|---:|
| Total main-list entries | 92 |
| Sections represented | 11 |
| Distinct controlled taxonomy values | 48 |
| Entries tagged `cross-domain` | 23 (25.0%) |
| Largest scientific/integration tag (excluding `cross-domain`) | `computational-workflows` (18 entries, 19.57%) |
| General-purpose substrate share | 8 entries (8.7%) |
| Entries with no typed relations | 0 |
| Overdue reviews (as of baseline date) | 0 |
| Evidence entries without source references | 0 |

## Active concentration warnings

None. The role-sensitive family audit reports no concentration warning on the Batch A tree.

## Batch A coverage effect

Issue #44 Batch A adds five mechanisms in two previously thin areas:

- **Computational-model exchange:** SBML, SED-ML, and CellML distinguish model structure, simulation-experiment description, and modular mathematical models.
- **Neuroscience data exchange:** BIDS and NWB distinguish dataset organization and neurophysiology data containers.

The additions preserve explicit boundaries against generic substrates such as HDF5 and NIfTI and against execution-provenance records such as Workflow Run RO-Crate.

## Prior domain gap reviews

- **PR-16A:** SDMX added; DDI-CDI on watchlist.
- **PR-16B:** FMI, CIF, NeXus, OPTIMADE added.
- **PR-16C:** OGC API — Features, Coverages, SensorThings, openEO added.
- **PR-16D:** ISA-JSON, BioCompute Objects, DICOMweb added.

The remaining researched queue is maintained in `catalog/expansion-candidates.yaml` and `docs/candidate-reviews/comprehensive-expansion-2026.md`.
