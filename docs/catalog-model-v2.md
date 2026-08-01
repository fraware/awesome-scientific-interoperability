# Catalog Model v2

**Status:** Specified in PR-03; live shards remain on v1 until PR-04–PR-07.  
**Authority:** `docs/engineering-takeover-specification.md` supersedes this document on conflict.

## Why v2

v1 `evidence_level`, `maintenance_signal`, and `north_star_utility` mixed lifecycle maturity, implementation evidence, and editorial utility into opaque scores. v2 records independent dimensions so human curators can defend inclusion without implying an automated quality score.

## Field-by-field migration

| v1 field | v2 field / action | Notes |
|----------|-------------------|-------|
| `id` | `id` | Unchanged stable slug |
| `name` | `name` | Canonical name |
| `url` | `url` | Canonical technical HTTPS URL |
| `section` | `section` | Existing taxonomy enum |
| `resource_type` | `resource_type` | Human-readable class |
| `interoperability_layers` | `interoperability_layers` | Unchanged enums |
| `connects` | `connects` | At least two object/system classes |
| `mechanism` | `mechanism` | Precise documented contract |
| `description` | `summary` | Must equal the README sentence |
| `evidence_level` | **remove** | Replace with `evidence_types` + statuses |
| `maintenance_signal` | **remove** | Replace with `maturity` |
| `north_star_utility` | **remove** | Express utility in `decision_basis` |
| _(new)_ | `maturity` | `established` \| `maintained` \| `emerging` |
| _(new)_ | `evidence_types` | Factual signals, not an inclusion score |
| _(new)_ | `implementation_status` | Independence of implementations |
| _(new)_ | `conformance_status` | Public suite/validator/tests/none |
| _(new)_ | `stewardship` | `{name, type, url}` |
| _(new)_ | `domains` | Normalized lowercase slugs |
| _(new)_ | `source_urls` | ≥1 primary technical source |
| _(new)_ | `alternatives` | Catalog IDs or `[]` with boundary note |
| _(new)_ | `related_resource_ids` | Catalog IDs or `[]` |
| `decision_basis` | `decision_basis` | Why this is among the strongest options |
| `boundary_note` | `boundary_note` | Limitation or closest alternative |
| `reviewed_on` | `reviewed_on` | Actual human review date |
| _(new)_ | `review_due_on` | Later than `reviewed_on` |
| `primary_source_inspected` | `primary_source_inspected` | Must be `true` |

## Review-interval rules

- Established or maintained resources: maximum 365 days.
- Emerging resources in `Instruments and Laboratories` or `Agents, Access, and Policy`: maximum 183 days.
- `review_due_on` must be strictly later than `reviewed_on`.

## Evidence consistency

- `implementation_status: multiple-independent` requires at least two `source_urls`.
- `conformance_status: public-suite` or `public-validator` requires at least one `source_urls` entry pointing at the artifact or an authoritative page that identifies it.
- Prefer `unknown` / `none-known` over invented evidence.

## Cross-references

- `alternatives` and `related_resource_ids` reference other catalog IDs.
- Empty arrays are valid when the boundary note explains the absence of a close alternative.
- Self-references are rejected by `scripts/validate_catalog_v2.py`.

## Compatibility until cutover

1. Live validation remains `python scripts/validate_catalog.py` against `schema/catalog.schema.json` (v1).
2. v2 validation is `python scripts/validate_catalog_v2.py` (fixtures by default; `--live` only after migration).
3. `python scripts/validate_catalog.py --schema-version 2` delegates to the v2 fixture runner and does not require live shards to pass v2.
4. PR-07 replaces the v1 schema, renames fields in live shards, and removes compatibility shims.

## Fixture coverage

See `tests/fixtures/v2/` for valid pairs, emerging-agent intervals, and negative cases for missing stewardship/sources/dates, bad and self cross-references, contradictory implementation evidence, legacy fields, missing domains, and empty evidence types.
