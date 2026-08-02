# Coverage Baseline

**Baseline date:** 2026-08-01  
**Catalog version:** 2.2.0  
**Main-list entries:** 87  
**Audit command:** `python scripts/audit_coverage.py --as-of 2026-08-01`

This document records reproducible corpus-balance metrics from the structured catalog. Counts and concentration signals support maintainer review; they are not quality scores and do not determine inclusion or exclusion.

## Policy

Classification thresholds and explicit substrate and standard-family mappings live in `config/coverage-policy.yaml`. Family concentration is evaluated per role-sensitive bucket (`runner`, `conformance`, `multi-engine-service`) rather than one undifferentiated implementation pile. The audit exits nonzero only for hard data-integrity failures. Editorial concentration warnings are reported but do not fail CI.

## Summary metrics

| Metric | Value |
|--------|------:|
| Total main-list entries | 87 |
| Sections represented | 11 |
| Distinct taxonomy tags | 47 |
| Entries tagged `cross-domain` | 23 (26.4%) |
| Largest scientific/integration tag (excl. cross-domain) | `computational-workflows` (18 entries, 20.69%) |
| General-purpose substrate share | 8 entries (9.2%) |
| Entries with no typed relations | 0 |
| Overdue reviews (as of baseline date) | 0 |
| Evidence entries without source URLs | 0 |

## Active concentration warnings

None. CWL family role buckets are within `max_per_family_role_bucket` (2). Adjudication: [reviews/cwl-family-concentration.md](reviews/cwl-family-concentration.md).

## Domain gap reviews (PR-16A–D, merged)

- **PR-16A:** SDMX added; DDI-CDI on watchlist.
- **PR-16B:** FMI, CIF, NeXus, OPTIMADE added.
- **PR-16C:** OGC API — Features, Coverages, SensorThings, openEO added.
- **PR-16D:** ISA-JSON, BioCompute Objects, DICOMweb added.

Remaining thin areas and watchlist candidates are documented under `docs/candidate-reviews/` and `docs/watchlist.md`.
