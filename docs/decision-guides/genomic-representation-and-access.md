# Genomic representation and access

Use this guide when a workflow must distinguish variant semantics, phenotype exchange, regional genomic-data retrieval, and reference-sequence identity. These mechanisms solve adjacent integration problems and should not be substituted for one another.

## Decision table

| Need | Strongest starting point | Why | Boundary |
|---|---|---|---|
| Normalize and identify genomic variation independent of source notation | [resource:ga4gh-variation-representation-specification-vrs] | Defines variation objects, normalization conventions, digest serialization, and computed identifiers | VRS is not a file format or clinical record schema |
| Exchange phenotype, disease, biosample, pedigree, and interpretation data | [resource:ga4gh-phenopackets] | Provides a constrained, machine-readable phenotype-centered schema | FHIR covers broader healthcare exchange; the mappings are not direct equivalence |
| Retrieve reads or variants for a genomic interval | [resource:ga4gh-htsget] | Returns an ordered retrieval ticket for region-scoped HTS data | [resource:ga4gh-data-repository-service-drs] resolves whole objects instead of genomic regions |
| Identify and retrieve an exact reference sequence | [resource:ga4gh-refget-sequences] | Uses content-derived identifiers and a sequence/range API | [resource:identifiers-org] resolves registered namespaces; it does not establish sequence identity from content |

## Composition pattern

A federated variant-analysis system commonly uses [resource:ga4gh-refget-sequences] to identify the reference sequence, [resource:ga4gh-htsget] to retrieve region-scoped reads or variants, [resource:ga4gh-variation-representation-specification-vrs] to normalize and identify variation concepts, and [resource:ga4gh-phenopackets] to exchange phenotype and interpretation context. [resource:ga4gh-data-repository-service-drs] remains useful for resolving complete underlying objects.

## Evidence boundaries

- VRS-Python includes specification validation tests, which support a `documented-tests` claim without establishing independent certification.
- Phenopacket validation checks schema-specific required and recommended constraints; application-specific clinical validity remains outside the general validator.
- htsget currently has reference and independent implementation evidence without a cataloged public conformance suite.
- Refget has a public compliance suite and reports for separately operated services; historical report dates should be considered during maintenance review.

## Related candidate boundaries

Beacon v2 remains on the structured watchlist pending a GA4GH discovery-family budget and independent federation evidence. HTS file specifications are represented by htsget; Crypt4GH and RNAget are closed as out of scope for the current corpus. Their roles should not be inferred from the four mechanisms admitted here.
