# Metadata semantics and units

Compare general vocabularies, scientific profiles, domain conventions, and unit systems. Connect broad web semantics to domain profiles where the catalog lists both. Catalog entries: [resource:schema-org], [resource:bioschemas], [resource:w3c-data-catalog-vocabulary-dcat], [resource:simple-knowledge-organization-system-skos], [resource:obo-foundry], [resource:edam-ontology], [resource:sosa-ssn], [resource:qudt], [resource:unified-code-for-units-of-measure-ucum], [resource:spatiotemporal-asset-catalog-stac], [resource:climate-and-forecast-cf-metadata-conventions], [resource:darwin-core], [resource:ddi-lifecycle], [resource:croissant].

**Primary sources inspected:** [Schema.org](https://schema.org/), [Bioschemas profiles](https://bioschemas.org/profiles/), [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/), [SKOS](https://www.w3.org/TR/skos-reference/), [OBO Foundry](http://obofoundry.org/), [EDAM](http://edamontology.org/), [SOSA/SSN](https://www.w3.org/TR/vocab-ssn/), [QUDT](https://www.qudt.org/), [UCUM](https://ucum.org/), [STAC specification](https://github.com/radiantearth/stac-spec), [CF Conventions](https://cfconventions.org/), [Darwin Core](https://dwc.tdwg.org/), [DDI Lifecycle](https://ddialliance.org/Specification/DDI-Lifecycle), [Croissant 1.1](https://docs.mlcommons.org/croissant/docs/croissant-spec-1.1.html).

## General vocabularies and scientific profiles

| Base vocabulary | Scientific profile or extension | Relationship |
|-----------------|--------------------------------|--------------|
| [resource:schema-org] | [resource:bioschemas] | Bioschemas constrains Schema.org types for life-science resources (datasets, tools, workflows) |
| [resource:schema-org] | [resource:croissant] | Croissant expresses ML dataset metadata as Schema.org-compatible JSON-LD |
| [resource:schema-org] | RO-Crate (see packaging guide) | RO-Crate uses Schema.org as a core JSON-LD layer |
| [resource:simple-knowledge-organization-system-skos] | Terminology services in [resource:obo-foundry], [resource:edam-ontology] | SKOS patterns often publish ontology term hierarchies |
| [resource:w3c-data-catalog-vocabulary-dcat] | Repository and catalog exports | DCAT describes catalog-level dataset distributions, not bench-level assay semantics |

**Category error:** publishing only generic Schema.org when a domain profile ([resource:bioschemas], [resource:darwin-core], [resource:climate-and-forecast-cf-metadata-conventions]) is required for interoperability.

## Domain metadata conventions (selected)

| Resource | Domain | Object described | Distinct from |
|----------|--------|------------------|---------------|
| [resource:spatiotemporal-asset-catalog-stac] | Geospatial/raster stacks | Spatiotemporal assets and catalogs | CF inside NetCDF files; general DCAT catalog only |
| [resource:climate-and-forecast-cf-metadata-conventions] | Climate/forecast NetCDF | Variables, coordinates, units in arrays | STAC catalog JSON; BagIt packaging |
| [resource:darwin-core] | Biodiversity occurrence | Taxa, occurrences, events | EDAM workflow semantics |
| [resource:ddi-lifecycle] | Social science surveys | Study, variable, and lifecycle metadata | Croissant ML dataset layout |
| [resource:croissant] | ML datasets | Fields, splits, files for training pipelines | DDI survey wave definitions |

## Ontologies and terminologies

| Resource | Style | Strongest use case | Limitations |
|----------|-------|-------------------|-------------|
| [resource:obo-foundry] | Open biomedical ontologies with shared principles | Gene, phenotype, anatomy semantics across resources | Domain-specific; not a unit system |
| [resource:edam-ontology] | Bioinformatics operations, types, formats | Describe tools, workflows, and file types in registries | Complements—not replaces—domain assay ontologies |
| [resource:sosa-ssn] | Sensors, observations, actuations | Link instruments to observations in semantic graphs | Does not replace instrument control protocols (see laboratory guide) |
| [resource:simple-knowledge-organization-system-skos] | Concept schemes and mappings | Publish vocabulary mappings and hierarchies | Not a measurement unit or dataset layout standard |

## QUDT and UCUM: complementary roles

| Dimension | [resource:qudt] | [resource:unified-code-for-units-of-measure-ucum] |
|-----------|-----------------|---------------------------------------------------|
| **Primary artifact** | Quantity kinds, units, dimensions as linked data | Unit expression syntax for unambiguous strings |
| **Typical use** | Semantic web descriptions of measurable quantities | Clinical, lab, and metadata fields requiring UCUM strings (e.g., with [resource:climate-and-forecast-cf-metadata-conventions]) |
| **Complementarity** | Rich ontology of units and quantity classes | Lightweight interchange syntax validated by registries |
| **Category error** | Treating QUDT URIs as automatically supported in every UCUM-only validator | Assuming UCUM strings alone encode full quantity-kind semantics without context |

Use UCUM where APIs and conventions require standard unit strings; use QUDT where linked-data semantics and dimensional analysis across resources matter. Many systems use **both**: UCUM in payload fields, QUDT in semantic graphs.

## Decision paths

- **Expose life-science tools/datasets to search and registries:** [resource:bioschemas] profiles atop [resource:schema-org].
- **Publish a data catalog portal:** [resource:w3c-data-catalog-vocabulary-dcat] for catalog-level metadata; pair with domain profiles for dataset contents.
- **Harmonize geospatial asset collections:** [resource:spatiotemporal-asset-catalog-stac]; use CF inside NetCDF assets when climate semantics apply.
- **Document biodiversity surveys:** [resource:darwin-core]; map terms via SKOS where integrating foreign vocabularies.
- **Describe social science study waves:** [resource:ddi-lifecycle].
- **Ship ML dataset metadata to training frameworks:** [resource:croissant].
- **Align bioinformatics service descriptions:** [resource:edam-ontology] in tool and workflow metadata ([resource:workflowhub] uses Bioschemas/EDAM patterns).

## Example architecture

A climate repository serves NetCDF with [resource:climate-and-forecast-cf-metadata-conventions] variables using UCUM unit strings. A STAC catalog ([resource:spatiotemporal-asset-catalog-stac]) indexes those assets for cloud workflows. A related biodiversity dataset exports Darwin Core terms. The repository DCAT feed ([resource:w3c-data-catalog-vocabulary-dcat]) advertises both collections. Workflow metadata in [resource:edam-ontology] links analysis steps to file formats, while observation graphs use [resource:sosa-ssn] to connect samples to derived data.
