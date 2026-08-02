# Catalog Model v2

**Status:** Superseded for live fields by [catalog model v2.1](catalog-model-v2.1.md) (`catalog_version: 2.1.0`).  
**Authority:** `docs/engineering-takeover-specification.md` supersedes this document on conflict.

This page remains as the v2.0 field history. Use v2.1 for `resource_kind`, `steward_id`, `source_refs`, and registry rules.

## Why v2

v1 `evidence_level`, `maintenance_signal`, and `north_star_utility` mixed lifecycle maturity, implementation evidence, and editorial utility into opaque scores. v2 records independent dimensions so human curators can defend inclusion without implying an automated quality score.

## Field reference

| Field | Notes |
|-------|-------|
| `id` | Stable slug |
| `name` | Canonical name |
| `url` | Canonical technical HTTPS URL |
| `section` | Taxonomy enum |
| `resource_type` | Human-readable class |
| `interoperability_layers` | Syntactic, Semantic, Operational, Evidentiary, Organizational |
| `connects` | At least two object/system classes |
| `mechanism` | Precise documented contract |
| `summary` | Must exactly equal the README sentence |
| `maturity` | `established` \| `maintained` \| `emerging` |
| `evidence_types` | Factual signals, not an inclusion score |
| `implementation_status` | Independence of implementations |
| `conformance_status` | Public suite/validator/tests/none |
| `stewardship` | `{name, type, url}` |
| `domains` | Normalized lowercase slugs |
| `source_urls` | ≥1 primary technical source |
| `alternatives` | Catalog IDs or `[]` with boundary note |
| `related_resource_ids` | Catalog IDs or `[]` |
| `decision_basis` | Why this is among the strongest options |
| `boundary_note` | Limitation or closest alternative |
| `reviewed_on` | Actual human review date |
| `review_due_on` | Later than `reviewed_on`; must not precede today |
| `primary_source_inspected` | Must be `true` |

Removed v1 fields: `description`, `evidence_level`, `maintenance_signal`, `north_star_utility`.

## Review-interval rules

- Established or maintained resources: maximum 365 days.
- Emerging resources in `Instruments and Laboratories` or `Agents, Access, and Policy`: maximum 183 days.
- `review_due_on` must be strictly later than `reviewed_on`.
- CI fails when `review_due_on` precedes the current date (`scripts/check_review_freshness.py`, `--as-of` for tests).

## Evidence consistency

- `implementation_status: multiple-independent` requires at least two `source_urls`.
- `conformance_status: public-suite` or `public-validator` requires at least one `source_urls` entry pointing at the artifact or an authoritative page that identifies it.
- Prefer `unknown` / `none-known` over invented evidence.

## Cross-references

- `alternatives` and `related_resource_ids` reference other catalog IDs.
- Empty arrays are valid when the boundary note explains the absence of a close alternative.
- Self-references are rejected by `scripts/validate_catalog.py`.

## Validation

```bash
python scripts/validate_catalog.py
python scripts/check_review_freshness.py
python scripts/validate_catalog.py --fixtures-dir tests/fixtures/v2
```

Schema: `schema/catalog.schema.json`. Fixture coverage: `tests/fixtures/v2/`.
