# Provenance and execution evidence

Compare mechanisms for describing what happened during scientific activities, linking plans to executions, and packaging workflow-run evidence. Catalog entries: [resource:w3c-prov], [resource:p-plan], [resource:cwlprov], [resource:workflow-run-ro-crate], [resource:iso-23494-2-2026-common-provenance-model], [resource:runcrate].

**Primary sources inspected:** [PROV-O](https://www.w3.org/TR/prov-o/), [PROV-DM](https://www.w3.org/TR/prov-dm/), [P-Plan](https://www.opmw.org/model/p-plan/), [CWLProv documentation](https://cwltool.readthedocs.io/en/latest/CWLProv.html), [Workflow Run RO-Crate profile](https://www.researchobject.org/workflow-run-crate/profiles/workflow_run_crate/), [ISO 23494-2:2026 catalogue entry](https://www.iso.org/standard/87714.html), [runcrate](https://www.researchobject.org/runcrate/).

## Scope boundary

Provenance graphs and portable run crates document **what was asserted to have occurred** and **which entities participated**. They do not, by themselves, establish scientific validity, authorization to access underlying data, or safe repetition of laboratory or instrument actions. Packaging or profile conformance also **does not prove reproducibility or semantic equivalence** across engines, environments, or implementations.

## Comparison dimensions

| Dimension | [resource:w3c-prov] | [resource:p-plan] | [resource:cwlprov] | [resource:workflow-run-ro-crate] | [resource:iso-23494-2-2026-common-provenance-model] | [resource:runcrate] |
|-----------|---------------------|-------------------|--------------------|----------------------------------|-------------------------------------------------------|---------------------|
| **Object represented** | Entities, activities, agents, and relations in any domain | Prospective plans, steps, variables linked to executions | CWL workflow execution records in PROV-oriented research objects | Workflow run inputs, outputs, software, execution records as RO-Crate | Biological materials, derived data, laboratory/biobank traceability | Tooling layer for inspecting/replaying/converting run crates and CWLProv |
| **Prospective vs retrospective** | Retrospective assertions (can describe plans if modeled) | Prospective plan structures bridged to execution | Retrospective execution-focused | Retrospective run packaging | Both traceability directions in biotech materials chain | Operates on retrospective artifacts |
| **Packaging vs graph model** | Graph model with multiple serializations (PROV-O, PROV-N, etc.) | OWL ontology extending PROV | PROV graph packaged in research-object layout | JSON-LD RO-Crate graph plus files | Standardized model and serialization requirements (ISO) | Implementation toolkit, not a graph standard |
| **Serialization** | RDF/JSON-LD (PROV-O), XML, PROV-N | OWL/RDF | PROV serializations within RO-style bundles | JSON-LD (RO-Crate) | ISO-defined serializations (see standard text) | CLI/notebook-oriented over crate and CWLProv files |
| **Profile / extension relationship** | Foundation for scientific profiles | Extension of PROV for plans | CWL + PROV + research-object packaging profile | RO-Crate profile specializing PROV for workflow runs | Domain international standard; related conceptually to PROV | Consumes [resource:workflow-run-ro-crate] and [resource:cwlprov] |
| **Implementation support** | Multiple independent PROV libraries and exporters | Documented ontology; implementation uptake not fully catalogued | Reference path via [resource:cwltool] | Multiple implementations listed on profile site | Published 2026; implementation uptake not yet catalogued | Reference toolkit with documented conversions |
| **Validator / conformance support** | General PROV validators exist; no single scientific suite in catalog | No public conformance suite in catalog | Documented tests with cwltool path | Documented profile tests; public validator ecosystem evolving | Normative ISO text; conformance infrastructure not catalogued | No standalone conformance suite |
| **Portability assumptions** | Consumers understand PROV roles and chosen serialization | Consumers understand plan/workflow abstractions | Consumers run or interpret CWL executions | Consumers align on workflow engine semantics and crate profile | Biotech laboratories, biobanks, and software reporting chains | Users have compatible crate or CWLProv inputs |
| **Limitations** | Does not define domain semantics or workflow-specific step models | Adoption evidence limited in catalog | Tied to CWL execution ecosystem | Profile conformance ≠ identical rerun across engines | Standard text may require purchase; uptake emerging | Tool coverage varies by profile version |
| **Strongest use case** | Cross-domain provenance interchange among independent producers | Linking intended workflow plans to observed executions | CWL-centric portable execution provenance | Cross-engine workflow run exchange with research-object packaging | Regulated biotech traceability for materials and derived data | Operational inspection, replay, and conversion of run evidence |
| **Inappropriate use case** | Substituting for workflow-specific run packaging without a profile | General data packaging without execution context | Non-CWL workflow stacks without translation | Domain-only biobank traceability without workflow angle | Arbitrary workflow provenance outside biotech scope | Defining a new provenance model (use PROV or ISO instead) |

## Relationship to packaging

[resource:workflow-run-ro-crate] lives at the boundary of packaging and provenance: it packages files **and** encodes execution graphs. [resource:cwlprov] pursues a similar goal for CWL via PROV directly. [resource:w3c-prov] and [resource:p-plan] supply graph semantics; [resource:runcrate] supplies operational tooling atop packaged profiles.

## Decision paths

### Capture CWL execution provenance today

Evaluate [resource:cwlprov] on [resource:cwltool] paths and compare with [resource:workflow-run-ro-crate] for cross-system exchange requirements.

### Exchange workflow runs across engines and archives

Prefer [resource:workflow-run-ro-crate] when consumers expect RO-Crate tooling; validate engine feature support separately via [resource:cwl-conformance-tests] or engine-specific evidence.

### Model planned steps linked to executed steps

Use [resource:p-plan] concepts atop [resource:w3c-prov] when prospective workflow structure must link to retrospective records.

### Biotech materials traceability across labs and biobanks

Monitor [resource:iso-23494-2-2026-common-provenance-model] where ISO normative requirements apply; map concepts to existing PROV tooling where profiles exist.

### Inspect or replay packaged run evidence

Use [resource:runcrate] after selecting [resource:workflow-run-ro-crate] or [resource:cwlprov] as the interchange format.

## Common category errors

- Asserting that a valid Workflow Run RO-Crate guarantees bitwise-identical outputs on another engine.
- Using [resource:w3c-prov] alone without a domain or workflow profile when consumers expect bundled files and licenses.
- Treating [resource:runcrate] as authorization or validation of scientific conclusions.
- Ignoring prospective plan linkage when only entity-activity graphs are exported.

## Example architecture

A CWL runner emits [resource:cwlprov] bundles during execution. A converter produces [resource:workflow-run-ro-crate] for archival storage. Researchers use [resource:runcrate] to inspect step timings and replay on a compatible runner. Planned workflow structure is documented with [resource:p-plan] terms embedded in the PROV graph. A biobank integration pilot maps sample lineage fields to [resource:iso-23494-2-2026-common-provenance-model] where required by policy.
