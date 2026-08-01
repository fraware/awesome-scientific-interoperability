# Laboratory interoperability

Compare device communication standards, procedure languages, analytical data formats, and clinical exchange layers at the physical-laboratory boundary. Catalog entries: [resource:sila-2], [resource:opc-ua-laboratory-and-analytical-device-standard-lads], [resource:autoprotocol], [resource:analytical-information-markup-language-animl], [resource:allotrope-data-format], [resource:hl7-fhir], [resource:loinc].

**Primary sources inspected:** [SiLA 2](https://sila2.gitlab.io/sila_base/), [OPC UA LADS](https://opcfoundation.org/markets-collaboration/lads/), [Autoprotocol](https://autoprotocol.org/), [AnIML](https://www.animl.org/), [Allotrope Data Format](https://docs.allotrope.org/), [HL7 FHIR](https://hl7.org/fhir/), [LOINC](https://loinc.org/).

## Layer separation

| Layer | Examples in catalog | Provides | Does not provide |
|-------|---------------------|----------|------------------|
| **Device communication** | [resource:sila-2], [resource:opc-ua-laboratory-and-analytical-device-standard-lads] | Control, status, features, operational data access | Experimental intent semantics, analytical file schemas, authorization |
| **Procedure representation** | [resource:autoprotocol] | Machine-readable steps for automation platforms | Guarantee that every device supports every step; safety interlocks |
| **Analytical data exchange** | [resource:analytical-information-markup-language-animl], [resource:allotrope-data-format] | Vendor-neutral analytical result files and metadata | Live instrument command/control |
| **Clinical observation exchange** | [resource:hl7-fhir] with [resource:loinc] | Orders, results, observations across health systems | Robotic wet-lab orchestration |

**Device communication does not standardize experimental semantics.** **Procedure representation does not establish device compatibility**—validate feature maps per instrument model.

## Comparison: device communication

| Dimension | [resource:sila-2] | [resource:opc-ua-laboratory-and-analytical-device-standard-lads] |
|-----------|-------------------|------------------------------------------------------------------|
| **Transport / style** | gRPC services with extensible SiLA features | OPC UA information model and services |
| **Typical ecosystem** | Life-science lab automation vendors adopting SiLA features | Industrial/analytical devices with OPC UA stacks |
| **Extensibility** | Feature definitions per device class | Companion specification atop OPC UA core |
| **Implementation support** | Multiple independent SiLA servers/clients catalogued | Reference OPC UA models; vendor adoption varies |
| **Strongest use case** | Greenfield lab automation with SiLA-native devices | Facilities standardized on OPC UA industrial stacks |
| **Inappropriate use case** | Substitute for analytical file exchange ([resource:allotrope-data-format]) | Assume LADS alone defines high-level experimental protocols |

## Comparison: analytical data versus clinical semantics

| Dimension | [resource:analytical-information-markup-language-animl] | [resource:allotrope-data-format] | [resource:hl7-fhir] + [resource:loinc] |
|-----------|--------------------------------------------------------|----------------------------------|----------------------------------------|
| **Primary artifact** | XML analytical results | HDF5-based ADF with ontologies | FHIR resources carrying coded observations |
| **Domain center** | Analytical chemistry instruments | Cross-vendor analytical R&D data | Clinical and diagnostic workflows |
| **Semantic layer** | Technique-specific XML modules | Allotrope ontologies and taxonomies | LOINC codes for tests/observations |
| **Strongest use case** | Exchange chromatography/mass-spec traces between software | Enterprise analytical data lakes | Hospital/lab results integration |
| **Inappropriate use case** | Clinical billing or orders | Real-time robot scheduling | Raw instrument method files without clinical mapping |

## Autoprotocol (emerging, reviewed 2026-08-01)

[resource:autoprotocol] expresses platform-independent liquid-handling and sample-processing steps. As of **2026-08-01**, it remains **emerging** in the catalog with `review_due_on: 2027-01-31`. Treat it as a procedure interchange candidate, not a production guarantee that all cloud labs accept every instruction without translation.

## Integration requirements outside device protocols

Physical-world integration must explicitly address:

- **Approval and authority** — who may arm instruments, start runs, or override interlocks
- **Reversibility** — whether a step can be undone safely
- **Evidence** — logs tying device actions to samples and personnel
- **Point-of-no-return** — irreversible operations (waste, synthesis, human subjects)

Generic device APIs ([resource:sila-2], OPC UA) do not encode these governance concerns; layer organizational policy and LIMS/clinical systems above them.

## Decision paths

- **Integrate heterogeneous lab robots today:** Evaluate [resource:sila-2] feature coverage per device; compare with [resource:opc-ua-laboratory-and-analytical-device-standard-lads] where OPC UA is already mandated.
- **Describe executable wet-lab methods:** Consider [resource:autoprotocol] with per-platform validation; do not skip compatibility matrices.
- **Exchange analytical files between software:** Choose [resource:allotrope-data-format] or [resource:analytical-information-markup-language-animl] based on vendor support and consortium access, not control protocols.
- **Integrate diagnostic results with EHRs:** [resource:hl7-fhir] transport with [resource:loinc] semantics.

## Example architecture

A automation layer speaks [resource:sila-2] to liquid handlers, translating [resource:autoprotocol] steps into device-specific feature calls after compatibility review. Analytical instruments export [resource:allotrope-data-format] files to a data lake. Diagnostic results flow to clinicians via [resource:hl7-fhir] Observation resources coded with [resource:loinc]. Authorization for controlled patient data stays in access layers ([Controlled data access](controlled-data-access.md)), not in SiLA feature calls.
