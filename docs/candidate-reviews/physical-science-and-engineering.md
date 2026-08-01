# Candidate review: physical-science and engineering interoperability gaps

**Review date:** 2026-08-01  
**Specification:** PR-16B  
**Inclusion cap:** 4 main-list additions

## Candidate outcomes

| Candidate | Outcome | Rationale summary |
| --- | --- | --- |
| Functional Mock-up Interface (FMI) 3.0 | **include** | Normative model-exchange/co-simulation container with 170+ tool implementations and MAP FMI governance |
| Crystallographic Information Framework (CIF) | **include** | IUCr dictionaries, syntax, and checkCIF validation for structural-science exchange |
| NeXus | **include** | HDF5 scientific profile with NXDL application definitions and nxvalidate for scattering facilities |
| OPTIMADE | **include** | Federated materials-database REST API with public validator and multiple provider implementations |
| Generic HDF5 | **exclude** | Container format without domain contract; NeXus supplies the interoperability profile |
| HDF5 ES-NGS / other HDF5 profiles | **exclude** | Domain-specific but below corpus bar or subsumed by stronger domain entries in this review cycle |

## FMI — include

**Primary sources:** [FMI 3.0 specification](https://fmi-standard.org/docs/3.0/), [FMI about/governance](https://fmi-standard.org/about/), [modelica/fmi-standard](https://github.com/modelica/fmi-standard).

**Sentence test:** FMI enables simulation environments and supplier tools to exchange dynamic models through FMU ZIP containers and documented C APIs for model exchange and co-simulation.

## CIF — include

**Primary sources:** [IUCr CIF resources](https://www.iucr.org/resources/cif), [CIF specifications](https://www.iucr.org/resources/cif/spec), [COMCIFS policy](https://www.iucr.org/resources/cif/comcifs/policy).

**Sentence test:** CIF enables diffractometers, structure databases, and journals to exchange crystallographic data through STAR-derived syntax and machine-readable domain dictionaries.

## NeXus — include

**Primary sources:** [nexusformat.org](https://www.nexusformat.org/), [NeXus manual](https://manual.nexusformat.org/impatient/), [J. Appl. Cryst. 48, 301-305 (2015)](https://journals.iucr.org/j/issues/2015/01/00/po5029/po5029.pdf).

**Sentence test:** NeXus enables beamlines, analysis software, and archives to exchange neutron, X-ray, and muon data through HDF5 hierarchy rules and validated application definitions.

## OPTIMADE — include

**Primary sources:** [OPTIMADE specification 1.3](https://www.optimade.org/specification/latest/), [Materials-Consortia/OPTIMADE](https://github.com/Materials-Consortia/OPTIMADE), [optimade.org](https://optimade.org/).

**Sentence test:** OPTIMADE enables clients and meta-index services to query heterogeneous materials-structure databases through a JSON:API-based REST contract.

## Generic HDF5 — exclude

Recorded in `docs/source-notes.md`. HDF5 alone does not supply scientific semantics; NeXus is the included HDF5 profile for this domain gap.

## Conflict disclosure

None.
