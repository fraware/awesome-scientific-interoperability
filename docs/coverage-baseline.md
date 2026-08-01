# Coverage Baseline

**Baseline date:** 2026-08-01  
**Catalog version:** 2.0.0  
**Main-list entries:** 87  
**Audit command:** `python scripts/audit_coverage.py --as-of 2026-08-01`

This document records reproducible corpus-balance metrics from the structured catalog. Counts and concentration signals support maintainer review; they are not quality scores and do not determine inclusion or exclusion.

## Policy

Classification thresholds and explicit substrate and standard-family mappings live in `config/coverage-policy.yaml`. The audit exits nonzero only for hard data-integrity failures. Editorial concentration warnings are reported but do not fail CI.

## Summary metrics

| Metric | Value |
|--------|------:|
| Total main-list entries | 87 |
| Sections represented | 11 |
| Distinct domain tags | 48 |
| Entries tagged `cross-domain` | 23 (26.4%) |
| Largest scientific domain tag | `computational-workflows` (17 entries, 19.54%) |
| General-purpose substrate share | 8 entries (9.2%) |
| Entries with neither alternatives nor related links | 18 |
| Overdue reviews (as of baseline date) | 0 |
| Evidence entries without source URLs | 0 |

## Active concentration warnings

1. **implementation-family-concentration** — CWL family has three implementation entries (threshold 2).
2. **isolated-entries** — 18 entries record neither alternatives nor related resource links.

## Domain gap reviews (PR-16A–D, merged)

- **PR-16A:** SDMX added; DDI-CDI on watchlist.
- **PR-16B:** FMI, CIF, NeXus, OPTIMADE added.
- **PR-16C:** OGC API — Features, Coverages, SensorThings, openEO added.
- **PR-16D:** ISA-JSON, BioCompute Objects, DICOMweb added.

Remaining thin areas and watchlist candidates are documented under `docs/candidate-reviews/` and `docs/watchlist.md`.

## Regeneration

```bash
python scripts/audit_coverage.py --as-of YYYY-MM-DD --json-report coverage-audit.json --markdown-report coverage-audit.md
```
