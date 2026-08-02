# Catalog Model

**Status:** Live catalog model (`catalog_version: 2.2.0`).

The structured catalog validates the manually authored README and supports queries. It does not generate the list or decide inclusion. For local queries, see [querying the catalog](querying-the-catalog.md).

## Current model (v2.2)

v2.2 makes implementation independence operator-based. `implementation_status: multiple-independent` requires distinct operators recorded in `catalog/implementations.yaml`, not merely multiple typed reference URLs under one steward.

| Concern | Rule |
| --- | --- |
| Independence unit | `catalog/implementations.yaml` objects |
| Multiple-independent claim | At least two `independent-implementation` operators with distinct `operator_steward_id`, neither equal to the resource `steward_id` (unless `multi_org_steward_exception`) |
| Provenance URLs | Remain in `catalog/references.yaml` via `source_refs` |

### Implementation registry

Each implementation object records:

- `id`, `name`, `url`
- `implements_resource_id`
- `operator_steward_id` → `catalog/stewards.yaml`
- `relationship`: `reference-implementation` \| `independent-implementation` \| `official-implementation` \| `validator` \| `conformance-suite`
- `evidence_ref_ids` → `catalog/references.yaml`
- optional `supported_versions`, `multi_org_steward_exception`, `notes`

Only `relationship: independent-implementation` counts toward multiple-independent status. Steward-operated repositories do not count by default.

### Registries and controlled vocabularies

- `catalog/references.yaml` — deduplicated technical references with stable IDs
- `catalog/stewards.yaml` — normalized steward identities
- `catalog/implementations.yaml` — implementation and validator identities
- `config/catalog-taxonomy.yaml` — resource kinds, taxonomy dimensions, claim roles, reference types, relation types

### Resource fields (summary)

Every main-list resource carries identity (`id`, `name`, `url`, `section`, `resource_kind`), interoperability description (`interoperability_layers`, `connects`, `mechanism`, `summary`), evidence dimensions (`maturity`, `evidence_types`, `implementation_status`, `conformance_status`), stewardship (`steward_id`), claim-level provenance (`source_refs`), taxonomy dimensions (`scientific_domains`, `integration_functions`, `infrastructure_contexts`, `artifact_classes`), typed `relations`, review provenance (`review`, `reviewed_on`, `review_due_on`), and editorial notes (`decision_basis`, `boundary_note`, `primary_source_inspected`).

`summary` must exactly equal the README sentence.

### Review provenance

Each resource includes a `review` object with `reviewed_by`, `review_type` (`author` \| `maintainer` \| `independent`), `reviewed_on` (must match top-level `reviewed_on`), `conflict_disclosure`, and optional `reviewed_commit` / `decision_record`. Author-level reviews must not be described as independent reviews.

### Typed relations

Resources use a `relations` array of `{type, resource_id}` edges. Unknown relation types, self-edges, and empty relation sets fail validation.

### Integrity rules (blocking)

- Unknown implementation IDs, unresolved registry references, and schema violations fail validation.
- Live `multiple-independent` claims that lack two qualifying independent operators fail validation.
- Live `documented-tests`, `public-suite`, and `public-validator` claims require direct conformance artifact evidence.
- README/catalog parity, review-interval rules, and isolate prevention remain enforced.
- Quality CI runs `audit_data_quality.py --fail-on warning` so depth-queue regressions cannot merge silently.

### Validation

```bash
python scripts/validate_catalog.py
python scripts/audit_data_quality.py --as-of 2026-08-01 --check-baseline docs/data-quality-baseline.json
python -m unittest discover -s tests -v
```

## Model history

| Version | What it introduced |
| --- | --- |
| v2.0 | Separated maturity, implementation, and conformance from opaque scores |
| v2.1 | Claim-level `source_refs`, `steward_id`, controlled `resource_kind`, and domain taxonomy |
| v2.2 | Implementation registry and operator-based independence |

Earlier field names such as `resource_type`, free-text `stewardship`, `source_urls`, `alternatives`, and `related_resource_ids` are not live fields. See [implementation-independence review notes](reviews/implementation-independence-pr38.md) for the v2.2 re-adjudication of multiple-independent claims.
