# Repository preservation and data packaging

Compare mechanisms for durable repository storage, bounded transfer packages, semantic research objects, and lightweight dataset descriptors. Catalog entries: [resource:oxford-common-file-layout-ocfl], [resource:bagit], [resource:ro-crate], [resource:data-package-standard], [resource:croissant], [resource:combine-omex-archive], [resource:fair-signposting].

**Primary sources inspected:** [OCFL Specification v1.1](https://ocfl.io/1.1/spec/), [OCFL Validation Codes v1.1](https://ocfl.io/1.1/spec/validation-codes.html), [RFC 8493 (BagIt)](https://datatracker.ietf.org/doc/html/rfc8493), [RO-Crate 1.1/1.3](https://www.researchobject.org/ro-crate/specification/1.3/), [Data Package Standard](https://datapackage.org/standard/data-package/), [Data Package v2 release notes](https://datapackage.org/blog/2024-06-26-v2-release/), [Croissant 1.1](https://docs.mlcommons.org/croissant/docs/croissant-spec-1.1.html), [COMBINE Archive](https://combinearchive.org/), [FAIR Signposting](https://signposting.org/).

## Scope boundary

**Layout, packaging, or descriptor conformance does not prove scientific correctness, semantic equivalence, dataset availability, or lossless interpretation of referenced content.** OCFL validation proves storage-layout and digest rules. BagIt proves transfer completeness and fixity. RO-Crate and Data Package validators prove declared metadata structure. Separate provenance, execution, and domain-schema layers remain required for research claims.

## Comparison dimensions

| Dimension | [resource:oxford-common-file-layout-ocfl] | [resource:bagit] | [resource:ro-crate] | [resource:data-package-standard] | [resource:croissant] | [resource:combine-omex-archive] |
|-----------|-------------------------------------------|------------------|---------------------|----------------------------------|----------------------|---------------------------------|
| **Object represented** | Versioned repository objects with inventories and content addressing | Opaque content set with manifests and fixity | Heterogeneous research objects with JSON-LD context | Dataset/resource descriptors, schemas, dialects, licenses | ML dataset metadata on Schema.org | Computational biology models, simulations, related files |
| **Primary job** | Durable repository storage layout and rebuildability | Bounded transfer with integrity checks | Semantic packaging of files and contextual entities | Lightweight dataset packaging and tabular description | ML-ready dataset descriptions | Domain study archive exchange |
| **Serialization** | Directory/object-store layout + inventory JSON | Directory tree + text manifests | JSON-LD metadata plus payload files | `datapackage.json` plus resources | JSON-LD Croissant descriptor | OMEX ZIP with manifest |
| **Validator / conformance** | Named OCFL validation codes; ocfl-py validator | Structural bag checks; no semantic suite in catalog | Public RO-Crate validator | Frictionless Framework `validate` for descriptors/schemas | Public Croissant validator path | Toolkit archive-structure checks |
| **Strongest use case** | Repository preservation stores that must remain rebuildable across software generations | Moving packages between systems with checksum evidence | Cross-domain exchange of data, software, people, and provenance | Publishing tabular/open datasets with portable descriptors | Training/evaluation dataset handoff into ML tooling | Bundling SED-ML/SBML and related COMBINE assets |
| **Inappropriate use case** | Substituting for semantic research-object graphs or transfer-only bags | Semantic entity graphs or repository versioning layouts | Fixity-only bulk transfer without need for context | Claiming scientific correctness of remote data from descriptor validation alone | General research-object packaging outside ML datasets | General cross-domain packaging outside COMBINE models |

## Decision paths

### Preserve repository objects for long-term rebuildability

Prefer [resource:oxford-common-file-layout-ocfl]. Pair with [resource:ro-crate] or [resource:fair-signposting] when semantic context or landing-page discovery must accompany stored objects.

### Transfer files with integrity checks only

Prefer [resource:bagit]. Combine with [resource:oxford-common-file-layout-ocfl] when the destination is a durable repository store rather than a one-shot transfer.

### Package a heterogeneous study for reuse

Start with [resource:ro-crate]. Use [resource:data-package-standard] when the primary need is a lightweight dataset/resource descriptor rather than a full research-object graph. Use [resource:croissant] for ML-dataset consumers. Use [resource:combine-omex-archive] for COMBINE modeling archives.

### Publish tabular datasets with schemas and dialects

Prefer [resource:data-package-standard]. Treat Frictionless validation as descriptor-scoped evidence. Do not treat validator success as proof that every remote resource is available or scientifically correct. Surrounding software is still migrating unevenly to Data Package v2.

## Common category errors

- Treating OCFL layout validation as proof of semantic packaging completeness.
- Using BagIt where consumers need typed entities, people, software versions, and license graphs.
- Treating Data Package descriptor validation as proof of dataset scientific correctness or lossless interpretation.
- Conflating RO-Crate, Data Package, and Croissant as interchangeable packaging contracts.
- Expecting COMBINE/OMEX to serve as a general cross-domain packaging standard.

## Example architecture

A repository stores versioned payloads under [resource:oxford-common-file-layout-ocfl], exposes landing-page discovery with [resource:fair-signposting], and publishes a [resource:ro-crate] for study context. Tabular releases additionally ship a [resource:data-package-standard] descriptor for portal and analytics consumers. Bulk migration between sites uses [resource:bagit] for transfer integrity before re-ingest into OCFL storage roots.
