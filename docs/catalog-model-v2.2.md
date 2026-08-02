# Catalog Model v2.2

**Status:** Live catalog model (`catalog_version: 2.2.0`).  
**Authority:** `docs/engineering-takeover-specification.md` supersedes this document on conflict.  
**Builds on:** [catalog-model-v2.1.md](catalog-model-v2.1.md).

## Why v2.2

v2.1 made provenance claim-addressable, but `implementation_status: multiple-independent` still meant “enough typed reference objects,” not independent operators. Official monorepos under one steward (for example MCP) could satisfy the old count rule while failing independence.

## What changed

| Concern | v2.1 | v2.2 |
|---|---|---|
| Independence unit | Typed `source_refs` count | `catalog/implementations.yaml` objects |
| MI validator | `len(source_refs) >= 2` | ≥2 `independent-implementation` operators with distinct `operator_steward_id`, neither equal to the resource `steward_id` (unless `multi_org_steward_exception`) |
| Audit MI queue | Same weak count | Same independence rule as the validator |

References remain provenance URLs. Implementations are the independence unit.

## Implementation registry

Each implementation object records:

- `id`, `name`, `url`
- `implements_resource_id`
- `operator_steward_id` → `catalog/stewards.yaml`
- `relationship`: `reference-implementation` | `independent-implementation` | `official-implementation` | `validator` | `conformance-suite`
- `evidence_ref_ids` → `catalog/references.yaml`
- optional `supported_versions`, `multi_org_steward_exception`, `notes`

Only `relationship: independent-implementation` counts toward MI, and steward-operated repos do not count by default.

## Integrity rules (blocking additions)

- Unknown implementation IDs are rejected via schema uniqueness of the registry document.
- Unresolved `implements_resource_id`, `operator_steward_id`, or `evidence_ref_ids` fail validation.
- Live `multiple-independent` claims that lack two qualifying independent operators fail validation.
- Live `documented-tests` claims without a direct conformance artifact reference (validator / conformance-suite / interoperability-result with conformance or interoperability-testing role) fail validation.
- Quality CI runs `audit_data_quality.py --fail-on warning` so depth-queue regressions cannot merge silently.

## Typed relations

Resources use a `relations` array of `{type, resource_id}` edges. Controlled types live in `config/catalog-taxonomy.yaml` under `relation_types`. Legacy `alternatives` and `related_resource_ids` arrays are removed; `alternative-to` replaces alternatives sugar.

Unknown relation types, self-edges, and empty relation sets (isolates) fail validation.

## Re-adjudication (2026-08-02)

All 28 former MI claims were re-reviewed. Six retained MI with registry evidence; twenty-two were downgraded to `reference-and-others`, including mandatory MCP same-steward failure. Decision record: [reviews/implementation-independence-pr38.md](reviews/implementation-independence-pr38.md).

## Validation

```bash
python scripts/validate_catalog.py
python scripts/audit_data_quality.py --as-of 2026-08-01 --check-baseline docs/data-quality-baseline.json
python -m unittest discover -s tests -v
```
