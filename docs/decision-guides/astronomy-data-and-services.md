# Astronomy data files, discovery, queries, and application messaging

**Decision question:** Which mechanism should an astronomy archive or application use for durable data, hierarchical models, observation discovery, tabular exchange, remote queries, or interactive tool composition?

**Primary sources inspected:** [FITS Standard 4.0](https://fits.gsfc.nasa.gov/fits_standard.html), [ASDF Standard](https://asdf-standard.readthedocs.io/en/latest/), [IVOA VOTable 1.5](https://www.ivoa.net/documents/VOTable/), [IVOA TAP 1.1](https://ivoa.net/documents/TAP/), [IVOA ObsCore 1.1](https://ivoa.net/documents/ObsCore/), [IVOA SAMP 1.3](https://www.ivoa.net/documents/SAMP/), [STILTS taplint](https://www.star.bris.ac.uk/~mbt/stilts/sun256/taplint.html), and [STILTS ObsTAP validation](https://www.star.bris.ac.uk/~mbt/stilts/sun256/ObsTapStage.html).

## Choose by integration job

| Integration job | Strong starting point | Why | Boundary |
|---|---|---|---|
| Preserve or exchange installed-base astronomical images, spectra, cubes, and tables | [resource:flexible-image-transport-system-fits] | Durable header-data-unit contract across instruments, missions, archives, and libraries | Header validity does not establish complete or scientifically adequate metadata |
| Exchange complex hierarchical data with schemas, references, and versioned extensions | [resource:advanced-scientific-data-format-asdf] | YAML metadata trees, binary blocks, schema validation, and explicit extensions | Consumers need compatible extension manifests and schemas; adoption remains narrower than FITS |
| Exchange richly annotated table results | [resource:ivoa-votable] | Field metadata, arrays, links, parameters, and multiple table serializations | Serialization is distinct from service behavior and archive discovery semantics |
| Query relational holdings across independent data centers | [resource:ivoa-table-access-protocol-tap] | Synchronous and asynchronous queries, ADQL, uploads, metadata endpoints, and spatial operations | TAP does not impose one scientific table model |
| Issue one observation-discovery query across archives | [resource:ivoa-observation-core-obscore] | Minimal common `ivoa.obscore` metadata profile implemented through TAP | Discovery view only; it does not replace complete archive metadata or data-access protocols |
| Send data, selections, coordinates, and commands between running applications | [resource:ivoa-simple-application-messaging-protocol-samp] | Mature hub-mediated desktop and browser interoperability | Messaging does not provide persistence, provenance, authorization, or scientific validation |

## Composition pattern

An archive may store products as FITS or ASDF, expose its relational holdings through TAP, implement ObsCore for uniform observation discovery, and serialize query results as VOTable. A scientist may then use SAMP to move a selected result, sky position, or file reference among TOPCAT, Aladin, DS9, and Python clients. Each layer has a separate conformance boundary.

## Evidence and conformance

FITS, VOTable, TAP, ObsCore, and SAMP have separately operated implementations. ASDF currently retains the narrower `single-known` classification because this catalog models one confidently verified full implementation. STILTS validates TAP, VOTable, and ObsCore-specific behaviors. ASDF validation checks core and installed extension schemas. SAMP has no public protocol-wide conformance suite recorded.

Successful validation establishes only the checks performed. It does not prove scientific metadata completeness, archive calibration quality, cross-implementation numerical equivalence, or availability of every ASDF extension.

## Common category errors

- Treating VOTable as a query protocol or TAP as a durable file format.
- Treating ObsCore as a complete archive schema or a substitute for TAP.
- Treating SAMP messages as persistent workflow evidence.
- Treating ASDF as a universal FITS replacement.
- Inferring scientific validity from syntactic or schema conformance.

## Relevant catalog entries

[resource:flexible-image-transport-system-fits] [resource:advanced-scientific-data-format-asdf] [resource:ivoa-votable] [resource:ivoa-table-access-protocol-tap] [resource:ivoa-observation-core-obscore] [resource:ivoa-simple-application-messaging-protocol-samp]
