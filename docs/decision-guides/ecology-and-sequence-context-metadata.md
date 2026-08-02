# Ecology and sequence-context metadata

Use this guide when scientific data must retain ecological dataset context, biodiversity observations, persistent sample identity, or sequence-associated environmental metadata.

## Decision table

| Need | Strongest starting point | Why | Boundary |
|---|---|---|---|
| Describe contextual metadata for sequenced samples | [resource:minimum-information-about-any-sequence-mixs] | Versioned checklists and environmental extensions connect sequence records to samples, environments, and processing methods | MIxS does not assign persistent sample identifiers |
| Describe complete ecological datasets, methods, coverage, tables, and provenance | [resource:ecological-metadata-language-eml] | Modular schemas capture dataset structure and interpretation context | EML is broader than biodiversity occurrence exchange |
| Exchange biodiversity occurrences and taxonomic records | [resource:darwin-core] | Shared terms support observations, collections, taxonomy, events, and locations | Darwin Core does not describe complete dataset methods or table structures |
| Identify physical samples persistently | [resource:igsn-id] | Persistent identifiers connect samples with datasets and publications | IGSN does not supply the full contextual metadata model |
| Describe investigation, study, and assay structure | [resource:isa-json] | Multi-assay experimental model connects studies, samples, assays, and pipelines | ISA-JSON is not a domain-specific sequence or ecology profile |

## Composition pattern

A sequencing project assigns [resource:igsn-id] identifiers to samples, records sequence and environmental context with [resource:minimum-information-about-any-sequence-mixs], describes the broader experiment with [resource:isa-json], and publishes ecological dataset methods and table structures with [resource:ecological-metadata-language-eml]. [resource:darwin-core] remains appropriate for occurrence and taxonomic records.

## Evidence boundaries

- MIxS valid and invalid examples support documented tests, not independent certification.
- EML validation combines XML Schema checks with document-wide identifier and reference constraints.
- Passing either validator establishes structural conformance, not scientific completeness or semantic correctness of entered values.
