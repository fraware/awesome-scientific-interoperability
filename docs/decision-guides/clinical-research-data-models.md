# Clinical research data models

Use this guide when a program must distinguish operational healthcare exchange, clinical-study interchange, observational-data harmonization, and phenotype-centered genomic records.

## Decision table

| Need | Strongest starting point | Why | Boundary |
|---|---|---|---|
| Exchange healthcare resources and service operations | [resource:hl7-fhir] | Modular resources and APIs support clinical-system interoperability | FHIR does not define a shared observational analytics schema |
| Exchange and archive clinical-study data and metadata | [resource:cdisc-operational-data-model-odm] | Vendor-neutral model covers study setup, operation, audit, reference, and archival information | Deployed systems may implement earlier ODM versions or constrained subsets |
| Harmonize longitudinal observational data for federated analysis | [resource:omop-common-data-model] | Shared schema, vocabularies, conventions, and quality checks enable reusable network studies | OMOP requires ETL into a common analytical representation |
| Exchange phenotype and genomic interpretation context | [resource:ga4gh-phenopackets] | Phenotype-centered schema supports rare-disease and clinical-genomics workflows | It does not replace general EHR exchange or observational CDMs |

## Composition pattern

A health system exchanges operational records with [resource:hl7-fhir], captures clinical-trial structures and subject data with [resource:cdisc-operational-data-model-odm], transforms longitudinal source data into [resource:omop-common-data-model] for federated analyses, and uses [resource:ga4gh-phenopackets] where phenotype and genomic interpretation must be exchanged together.

## Evidence boundaries

- OMOP DataQualityDashboard checks structural, relational, plausibility, and completeness conditions; it does not prove that source-to-standard mappings are scientifically correct.
- ODM v2.0 is a maintained specification, but implementation and conformance evidence remains narrower than for FHIR or OMOP.
- Model conversion among FHIR, ODM, OMOP, and Phenopackets requires explicit mappings and loss analysis.
