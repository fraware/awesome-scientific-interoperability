# Review notes: Metadata and Semantics

**Review date:** 2026-08-01  
**Reviewer role:** Section reviewer (PR-04 catalog migration A)  
**Records migrated:** 14

## Sources inspected

| Resource | Primary sources |
|----------|-----------------|
| Bioschemas | [bioschemas.org/profiles](https://bioschemas.org/profiles/); [Bioschemas/bioschemas.github.io](https://github.com/Bioschemas/bioschemas.github.io) |
| Climate and Forecast (CF) Metadata Conventions | [cfconventions.org](https://cfconventions.org/); [CF Conventions 1.10 specification](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.10/cf-conventions.html) |
| Croissant | [Croissant 1.1 specification](https://docs.mlcommons.org/croissant/docs/croissant-spec-1.1.html); [mlcommons/croissant](https://github.com/mlcommons/croissant) |
| Darwin Core | [dwc.tdwg.org](https://dwc.tdwg.org/); [tdwg/dwc](https://github.com/tdwg/dwc) |
| DDI Lifecycle | [DDI Alliance DDI-Lifecycle specification](https://ddialliance.org/Specification/DDI-Lifecycle/); [ddialliance/Specification-DDI-Lifecycle](https://github.com/ddialliance/Specification-DDI-Lifecycle) |
| EDAM Ontology | [edamontology.org](https://edamontology.org/); [edamontology/edamontology](https://github.com/edamontology/edamontology) |
| OBO Foundry | [obofoundry.org](https://obofoundry.org/); [OBOFoundry/OBOFoundry.github.io](https://github.com/OBOFoundry/OBOFoundry.github.io) |
| QUDT | [qudt.org](https://www.qudt.org/); [qudt/qudt-public-repo](https://github.com/qudt/qudt-public-repo) |
| Schema.org | [schema.org](https://schema.org/); [schemaorg/schemaorg](https://github.com/schemaorg/schemaorg) |
| Simple Knowledge Organization System (SKOS) | [W3C SKOS Reference](https://www.w3.org/TR/skos-reference/); [W3C SKOS Primer](https://www.w3.org/2009/08/skos-reference/skos.html) |
| SOSA/SSN | [W3C/OGC SSN specification](https://www.w3.org/TR/vocab-ssn/); [OGC SSN standard page](https://www.ogc.org/standards/ssn/) |
| SpatioTemporal Asset Catalog (STAC) | [stacspec.org](https://stacspec.org/); [radiantearth/stac-spec](https://github.com/radiantearth/stac-spec) |
| Unified Code for Units of Measure (UCUM) | [ucum.org](https://ucum.org/); [UnifiedCodeUnits4UnitsOfMeasure/ucum](https://github.com/UnifiedCodeUnits4UnitsOfMeasure/ucum) |
| W3C Data Catalog Vocabulary (DCAT) | [W3C DCAT 3 Recommendation](https://www.w3.org/TR/vocab-dcat-3/); [w3c/dxwg](https://github.com/w3c/dxwg) |

## Changes made

- Renamed `description` to `summary` (exact README parity preserved).
- Removed v1 scoring fields (`evidence_level`, `maintenance_signal`, `north_star_utility`).
- Added v2 maturity, evidence_types, implementation_status, conformance_status, stewardship, domains, source_urls, alternatives, related_resource_ids, and review_due_on (2027-08-01).
- Schema.org hub linked to Bioschemas, Croissant, and DCAT; QUDT and UCUM listed as mutual alternatives.
- Croissant conformance_status set to `public-validator` based on mlcommons/croissant verifier tooling.
- EDAM linked to OBO Foundry and GA4GH TRS; STAC linked to DCAT as complementary catalog vocabulary.

## Unresolved questions

- EDAM stewardship spans ELIXIR Norway and EMBL-EBI contributors; recorded as community maintainers without naming individual governance bodies beyond edamontology.org.
- CF Conventions formal standards-body affiliation is community-led; no separate incorporated body documented on cfconventions.org.

## Conflicts

None.

## v2.1 provenance migration (2026-08-01)

- Closed isolates: Darwin Core, DDI Lifecycle, and SOSA/SSN via related links to Bioschemas/Schema.org, SDMX, and SensorThings respectively.

## Issue #30 Batch 4a metadata evidence (2026-08-01)

- Enriched Bioschemas, CF, Croissant, Darwin Core, DDI, EDAM, ISA-JSON, OBO Foundry; upgraded Croissant/ISA validators where primary artifacts exist.


## Issue #30 Batch 4b/5 metadata residual (2026-08-01)

- Completed Schema.org, SDMX, SKOS, SOSA/SSN, STAC, UCUM, DCAT evidence dispositions; STAC upgraded to public-validator then MI claim adjusted to reference-and-others where independence evidence remained thin.
| GA4GH Variation Representation Specification (VRS) | [VRS specification](https://vrs.ga4gh.org/en/stable/); [VRS-Python](https://github.com/ga4gh/vrs-python); [validation tests](https://github.com/ga4gh/vrs-python/tree/main/tests/validation) |
| GA4GH Phenopackets | [GA4GH product page](https://www.ga4gh.org/product/phenopackets/); [schema documentation](https://phenopacket-schema.readthedocs.io/en/latest/); [validator tools](https://github.com/phenopackets/phenopacket-tools) |
