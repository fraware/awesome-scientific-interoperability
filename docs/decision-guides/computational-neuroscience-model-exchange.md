# Computational-neuroscience model exchange

Choose between declarative model semantics and performance-oriented large-network representation. Catalog entries: [resource:neuroml], [resource:sonata], [resource:neurodata-without-borders-nwb], [resource:brain-imaging-data-structure-bids].

**Primary sources inspected:** [NeuroML 2.3 specification](https://docs.neuroml.org/Userdocs/Specification.html), [NeuroML validation](https://docs.neuroml.org/Userdocs/ValidatingNeuroMLModels.html), [NeuroML supporting tools](https://docs.neuroml.org/Userdocs/Software/SupportingTools.html), [SONATA specification repository](https://github.com/AllenInstitute/sonata), [SONATA developer guide](https://github.com/AllenInstitute/sonata/blob/master/docs/SONATA_DEVELOPER_GUIDE.md), [SONATA paper](https://doi.org/10.1371/journal.pcbi.1007696), and [NetPyNE conversion documentation](https://doc.netpyne.org/netpyne.conversion.html).

## Decision table

| Integration problem | Strongest starting point | Why | Boundary |
|---|---|---|---|
| Exchange reusable neuronal cell, channel, morphology, network, input, and simulation semantics | [resource:neuroml] | Governed XML and LEMS contracts, explicit units and component definitions, official schema validation, and conversion to multiple simulation environments | Individual tools may implement different language subsets; schema validity does not establish equivalent numerical behavior |
| Exchange very large instantiated neuronal circuits and high-volume simulation products efficiently | [resource:sonata] | HDF5-backed node, edge, spike, and report structures with CSV type tables and JSON configuration designed for high-performance simulation, analysis, and visualization | Flexible extensions and implementation-specific namespaces require explicit profile and version agreements; no public format-wide conformance suite is claimed |
| Exchange experimental neurophysiology acquisition and analysis data | [resource:neurodata-without-borders-nwb] | Typed experimental data structures, extensions, cross-language APIs, and validation | NWB is an experimental-data contract, not a computational model-definition language |
| Organize subjects, sessions, modalities, sidecars, and derivatives across a study | [resource:brain-imaging-data-structure-bids] | Dataset-level naming, organization, metadata, and pipeline conventions | BIDS does not define neural model semantics or scalable circuit representation |

## NeuroML and SONATA are complementary

[resource:neuroml] is strongest when model meaning must remain explicit and reusable across simulators. It represents biological and mathematical components declaratively and supports structural validation before conversion or execution. [resource:sonata] is strongest when a network has been instantiated at scale and producers and consumers need efficient exchange of nodes, edges, configuration, inputs, spikes, and time-series reports.

The SONATA developer guide explicitly positions the format as a performance representation that should coexist with declarative approaches such as NeuroML. A defensible architecture can retain NeuroML as the canonical semantic model, generate or exchange a SONATA representation for large-scale execution, and record the exact conversion tool, source commit, format versions, extension profile, and simulator configuration.

## Evidence and validation boundaries

NeuroML's public validators check schema names, types, values, required elements, cardinality, and hierarchy. Cross-simulator testing remains a separate requirement because valid documents can exercise unsupported subsets or yield divergent dynamics through numerical methods and simulator semantics.

SONATA has published specifications, reference APIs, examples, and support in independently governed tools such as NetPyNE. The current evidence does not justify a public-suite or public-validator claim for the complete format. BMTK unit tests and successful exchange demonstrations support implementation quality and adoption, though they do not constitute universal format conformance.

## Category errors

- Treating a valid NeuroML document as proof of simulator support or numerical equivalence.
- Treating SONATA as a complete declarative semantics language for every cellular and synaptic model.
- Counting BMTK and other same-origin repositories as independent SONATA implementations.
- Using NWB simulation-output extensions as a replacement for model-definition and network-configuration contracts.
- Treating HDF5 readability as SONATA or NWB conformance.
- Publishing a converted representation without recording source format, converter, versions, parameter mappings, and unsupported constructs.

## Example architecture

A model repository stores canonical cells, channels, and networks in NeuroML, validates each release, and runs representative cross-simulator tests. A versioned conversion pipeline produces SONATA network and configuration artifacts for large-scale execution in BMTK or NetPyNE. Simulation outputs are retained in SONATA reports or mapped into NWB where experimental and simulated neurophysiology must be compared. BIDS or RO-Crate supplies study-level organization and contextual packaging, and Workflow Run RO-Crate records conversion and execution provenance.
