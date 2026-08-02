# Catalog Model v2.1

**Status:** Historical model notes for `catalog_version: 2.1.0`. Live model is [catalog-model-v2.2.md](catalog-model-v2.2.md).  
**Authority:** `docs/engineering-takeover-specification.md` supersedes this document on conflict.

## Why v2.1

v2 recorded independent maturity, implementation, and conformance dimensions, but evidence still drifted as free-text URLs and steward strings. v2.1 adds claim-level provenance registries so a competent user can see **which technical sources support which claims** without reconstructing the research process.

## What changed from v2.0

| v2.0 field | v2.1 replacement |
|---|---|
| `resource_type` (free text) | `resource_kind` (14 controlled values) |
| `stewardship: {name,type,url}` | `steward_id` → `catalog/stewards.yaml` |
| `source_urls: [url, …]` | `source_refs: [{ref_id, role}, …]` → `catalog/references.yaml` |
| Domains (open slugs) | Domains from `config/catalog-taxonomy.yaml` (47 tags) |

Removed as live fields: `resource_type`, `stewardship`, `source_urls`.

## Registries

- `catalog/references.yaml` — deduplicated technical references with stable IDs, URL, type, publisher, `accessed_on`
- `catalog/stewards.yaml` — normalized steward identities with optional aliases
- `config/catalog-taxonomy.yaml` — resource kinds, domains, claim roles, reference types

### Claim roles

`technical-definition`, `stewardship`, `implementation`, `adoption`, `conformance`, `interoperability-testing`, `maintenance`, `limitations`

### Reference types

`specification`, `normative-schema`, `api-documentation`, `implementation-repository`, `adoption-evidence`, `registry-record`, `validator`, `conformance-suite`, `interoperability-result`, `governance-source`, `technical-documentation`

## Integrity rules (blocking)

- Unknown `resource_kind`, domain, claim role, `steward_id`, or `ref_id` fails validation.
- Every main-list resource must have at least one of `alternatives` or `related_resource_ids` (no isolates).
- `conformance_status: public-suite` or `public-validator` requires a `source_refs` entry whose reference `type` is a conformance artifact (`validator`, `conformance-suite`, or `interoperability-result`) and whose role is `conformance` or `interoperability-testing`.
- README `summary` parity and review-interval rules are unchanged from v2.

## Evidence-depth queues (non-blocking initially)

`scripts/audit_data_quality.py` reports:

1. `multiple-independent` claims with fewer than two direct implementation/adoption/registry/interop references
2. `documented-tests` claims without a direct conformance artifact reference

These queues drive issue #30. Do not lower thresholds to clear them. After queues remain clear, maintainers may promote selected depth checks to fail-closed validator rules with fixtures — tracked in the maintenance protocol, not mixed into evidence edits.

## Migration notes (2026-08-01)

- Mapped existing `source_urls` into `source_refs` with honest roles (definition and stewardship first; implementation/conformance only when the URL type supports it).
- Normalized steward spelling variants (for example GA4GH, WorkflowHub, W3C).
- Domain aliases: `workflows` → `computational-workflows`; `scholarly-publishing` → `scholarly-communication`.
- Completed relationship links for previously isolated records (see section review notes).
- Corrected OGC API — Coverages to `emerging` / `reference-and-others` / `none-known` (no public-suite inflation).
- Downgraded several prior `public-suite` / `public-validator` claims to `documented-tests` where no direct artifact URL was present in the corpus.

## Validation

```bash
python scripts/validate_catalog.py
python scripts/validate_watchlist.py
python scripts/check_review_freshness.py --as-of 2026-08-01
python scripts/audit_data_quality.py --as-of 2026-08-01
python scripts/check_links.py --offline --scope all
python -m unittest discover -s tests -v
python scripts/generate_manifest.py
python scripts/verify_manifest.py
```
