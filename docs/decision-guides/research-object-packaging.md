# Research object packaging

Compare mechanisms for bundling data, software, workflows, and contextual metadata into exchangeable units. Catalog entries: [resource:ro-crate], [resource:workflow-ro-crate], [resource:workflow-run-ro-crate], [resource:workflow-testing-ro-crate], [resource:bagit], [resource:combine-omex-archive], [resource:fair-signposting], [resource:oxford-common-file-layout-ocfl], [resource:data-package-standard].

For durable repository storage layouts versus lightweight dataset descriptors, see also [Repository preservation and data packaging](repository-preservation-and-data-packaging.md).

**Primary sources inspected:** [RO-Crate 1.3](https://www.researchobject.org/ro-crate/specification/1.3/), [Workflow RO-Crate](https://about.workflowhub.eu/Workflow-RO-Crate/), [Workflow Run RO-Crate profile](https://www.researchobject.org/workflow-run-crate/profiles/workflow_run_crate/), [Workflow Testing RO-Crate](https://w3id.org/ro/wftest), [RFC 8493 (BagIt)](https://datatracker.ietf.org/doc/html/rfc8493), [COMBINE Archive](https://combinearchive.org/), [FAIR Signposting](https://signposting.org/), [OCFL Specification v1.1](https://ocfl.io/1.1/spec/), [Data Package Standard](https://datapackage.org/standard/data-package/).

## Scope boundary

**Packaging conformance does not prove reproducibility, semantic equivalence, or that two systems will interpret bundled entities identically.** A valid crate or bag demonstrates structural and declared metadata conformance; rerunning workflows, verifying scientific claims, or matching environment semantics requires separate execution, provenance, and software-description layers (see [Provenance and execution evidence](provenance-and-execution-evidence.md) and workflow guides).

## Comparison dimensions

| Dimension | [resource:ro-crate] | [resource:workflow-ro-crate] | [resource:workflow-run-ro-crate] | [resource:workflow-testing-ro-crate] | [resource:bagit] | [resource:combine-omex-archive] | [resource:fair-signposting] |
|-----------|---------------------|------------------------------|----------------------------------|--------------------------------------|------------------|---------------------------------|-----------------------------|
| **Object represented** | General research object: files, people, software, instruments, contextual entities | Portable workflow definition, metadata, diagrams, examples, tests | Workflow execution record: inputs, outputs, software, provenance | Workflow test suite: inputs, expected outputs, test services | Opaque digital content set with manifests and fixity | Computational models, simulations, metadata, related files in systems biology | HTTP landing-page relations to identifiers, metadata, licenses, files |
| **Prospective vs retrospective** | Both; base profile is neutral | Prospective (definition before run) | Retrospective (evidence after run) | Prospective test specification | Neither; transfer container only | Primarily prospective study packaging | Neither; discovery navigation only |
| **Packaging vs graph model** | JSON-LD graph in `ro-crate-metadata.json` plus files | RO-Crate profile extending base graph | RO-Crate profile for run graph | RO-Crate profile for test artifacts | Directory tree + manifest files; no semantic graph | ZIP archive with manifest and typed entries | HTTP Link headers/relations; not a file package |
| **Serialization** | JSON-LD (Schema.org / RO terms) | JSON-LD under RO-Crate | JSON-LD under RO-Crate | JSON-LD under RO-Crate | Text manifests (`bagit.txt`, `manifest-*.txt`) | OMEX ZIP with manifest | Typed HTTP relations per Signposting spec |
| **Profile / extension relationship** | Base specification; other rows are profiles or alternatives | Profile of [resource:ro-crate] | Profile of [resource:ro-crate]; overlaps provenance domain | Profile of [resource:ro-crate]; links to [resource:lifemonitor] | Independent IETF packaging standard | Domain archive format; not an RO-Crate profile | Independent web convention; complements repositories |
| **Implementation support** | Multiple independent libraries and exporters (see [ro-crate-py](https://github.com/ResearchObject/ro-crate-py)) | Reference path through WorkflowHub and ELIXIR tooling | Reference implementations including [resource:runcrate] consumers | Documented with LifeMonitor and WorkflowHub paths | Widespread library support (e.g. LoC bagit-python) | Reference CombineArchive toolkit and community adopters | Multiple repository plugins and clients |
| **Validator / conformance support** | Public validator ([resource:ro-crate-validator]) | Documented tests; no standalone public suite in catalog | Documented tests; profile validation tooling emerging | Documented tests via profile and LifeMonitor integration | Structural checks via bag tools; no semantic validator | Toolkit validation of archive structure | Documented conformance patterns on signposting.org |
| **Portability assumptions** | Consumers understand JSON-LD and declared profiles | Consumers understand CWL/WDL or cited workflow languages in crate | Consumers align on workflow engine and provenance profile semantics | Consumers align on workflow language and test harness | Any system that can verify checksums and read manifests | COMBINE ecosystem (SED-ML, SBML, etc.) | HTTP clients and resolvable landing pages |
| **Limitations** | Profile choice required for specialized use; graph complexity can grow | Does not by itself capture execution provenance | Does not replace workflow definition packaging; profile ≠ rerun guarantee | Adoption still consolidating with monitoring services | No embedded semantic metadata graph | Domain-specific to computational biology archives | Does not package files or assert fixity |
| **Strongest use case** | Cross-domain exchange of heterogeneous research objects with rich context | Publishing workflows to registries for discovery and reuse | Archiving or exchanging a specific workflow run and its outputs | Portable workflow test definitions across registries and CI | Durable transfer with fixity between storage systems | Bundling multi-file computational biology studies | Machine discovery of related resources from a landing page |
| **Inappropriate use case** | Fixity-only bulk transfer where semantics are unnecessary | Representing completed execution evidence without run profile | Shipping workflow definitions without execution context | General data packaging unrelated to workflow tests | Semantic research-object graphs or workflow metadata | General cross-domain packaging outside COMBINE models | Substituting for RO-Crate, BagIt, or repository access APIs |

## Decision paths

### Package a heterogeneous study for reuse

Start with [resource:ro-crate]. Add [resource:workflow-ro-crate] when the primary artifact is a workflow definition; add [resource:workflow-run-ro-crate] only when the goal is execution evidence, not prospective definition.

### Transfer files with integrity checks only

Prefer [resource:bagit]. Combine with [resource:ro-crate] when semantic context must travel with the bits. Prefer [resource:oxford-common-file-layout-ocfl] when the destination must remain a durable, rebuildable repository store rather than a transfer package.

### Describe lightweight datasets for portals and analytics

Prefer [resource:data-package-standard] when consumers need resource, schema, dialect, and license descriptors without a full research-object graph. See [Repository preservation and data packaging](repository-preservation-and-data-packaging.md).

### Publish a systems-biology model archive

[resource:combine-omex-archive] fits when SED-ML/SBML and related COMBINE assets are the core. For broader cross-domain packaging, evaluate [resource:ro-crate] instead.

### Help clients discover related metadata from a repository URL

Use [resource:fair-signposting] at the HTTP layer. It does not replace packaging; pair with repository APIs and crates as needed.

## Common category errors

- Treating any RO-Crate profile validation as proof that a workflow rerun will reproduce published results.
- Using [resource:bagit] when consumers need typed entities, people, software versions, and license graphs.
- Expecting [resource:fair-signposting] to bundle or sign content; it only advertises typed links.
- Conflating [resource:workflow-ro-crate] (definition) with [resource:workflow-run-ro-crate] (execution evidence).

## Example architecture

A workflow author publishes a [resource:workflow-ro-crate] to [resource:workflowhub]. After execution on a CWL runner, the site exports a [resource:workflow-run-ro-crate] alongside outputs. A repository stores the run crate and exposes [resource:fair-signposting] links from the landing page to metadata, license, and content resources. Bulk archival transfer to a tape site uses [resource:bagit] for fixity; semantic context remains in the crate metadata.
