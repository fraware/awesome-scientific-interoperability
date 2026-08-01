# Coverage Baseline

**Baseline date:** 2026-08-01  
**Catalog version:** 2.0.0  
**Main-list entries:** 75  
**Audit command:** `python scripts/audit_coverage.py --as-of 2026-08-01`

This document records reproducible corpus-balance metrics from the structured catalog. Counts and concentration signals support maintainer review; they are not quality scores and do not determine inclusion or exclusion.

## Policy

Classification thresholds and explicit substrate and standard-family mappings live in `config/coverage-policy.yaml`. The audit exits nonzero only for hard data-integrity failures. Editorial concentration warnings are reported but do not fail CI.

## Summary metrics

| Metric | Value |
|--------|------:|
| Total main-list entries | 75 |
| Sections represented | 11 |
| Distinct domain tags | 44 |
| Entries tagged `cross-domain` | 21 (28.0%) |
| Largest scientific domain tag | `computational-workflows` (17 entries, 22.67%) |
| General-purpose substrate share | 8 entries (10.67%) |
| Entries with neither alternatives nor related links | 17 |
| Overdue reviews (as of baseline date) | 0 |

## Active concentration warnings

1. **substrate-concentration** — general-purpose substrates at 10.67%.
2. **implementation-family-concentration** — CWL family has three implementation entries.
3. **isolated-entries** — 17 entries record neither alternatives nor related resource links.

## Concrete gaps

- **Physical sciences and engineering:** thin coverage; NeXus, CIF, and FMI deferred to PR-16B.
- **Statistical and social-science exchange:** DDI Lifecycle and Croissant only; SDMX deferred to PR-16A.
- **Geospatial operations:** STAC, SOSA/SSN, and CF each appear once; OGC API coverage deferred to PR-16C.
- **Experimental and biomedical research objects:** deferred to PR-16D.
- **Cross-linking:** 17 isolated entries weaken problem-index navigation.

## Regeneration

```bash
python scripts/audit_coverage.py --as-of YYYY-MM-DD --json-report coverage-audit.json --markdown-report coverage-audit.md
```
