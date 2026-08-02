# Computational models and simulation experiments

Choose among model languages, simulation-experiment descriptions, archive packaging, and conformance suites. Catalog entries: [resource:systems-biology-markup-language-sbml], [resource:cellml], [resource:simulation-experiment-description-markup-language-sed-ml], [resource:combine-omex-archive], [resource:sbml-test-suite], [resource:biosimulators-test-suite].

**Primary sources inspected:** [SBML Level 3 Version 2 Core Release 2](https://sbml.org/documents/specifications/level-3/version-2/core/release-2/), [SED-ML Level 1 Version 5](https://sed-ml.org/specifications.html), [CellML 2.0](https://www.cellml.org/specifications/cellml_2.0/), [COMBINE Archive](https://combinearchive.org/), [SBML Test Suite](https://sbml.org/software/sbml-test-suite/), and [BioSimulators Test Suite](https://docs.biosimulators.org/Biosimulators_test_suite/).

## Decision table

| Integration problem | Strongest starting point | Why | Boundary |
|---|---|---|---|
| Exchange biochemical reaction-network models | [resource:systems-biology-markup-language-sbml] | Normative mathematical semantics, Level 3 package system, independent simulators, and public conformance tests | Does not describe a complete simulation experiment or bundle external files |
| Exchange modular equation-based physiological models | [resource:cellml] | Explicit components, variables, units, imports, resets, and model composition | Biochemical pathway packages and broad reaction-network semantics are stronger in SBML |
| Exchange what simulation to run and what outputs to produce | [resource:simulation-experiment-description-markup-language-sed-ml] | Software-independent models, changes, simulations, tasks, data generators, and outputs | Prospective experiment description is distinct from execution traces and workflow provenance |
| Transfer a complete modeling study | [resource:combine-omex-archive] | Packages models, SED-ML, data, metadata, and manifests as one portable archive | Packaging does not prove that every contained artifact is executable by every tool |
| Test SBML parser and simulator behavior | [resource:sbml-test-suite] | Public cross-implementation suite tied to SBML semantics | Passing tests does not prove scientific validity of a model |
| Test SED-ML and COMBINE execution across simulators | [resource:biosimulators-test-suite] | Executes curated and synthetic archives against supported simulator capabilities | Current public coverage concentrates on established SED-ML feature subsets |

## Composition pattern

A portable computational study commonly uses [resource:systems-biology-markup-language-sbml] or [resource:cellml] for the model, [resource:simulation-experiment-description-markup-language-sed-ml] for the simulation procedure and requested outputs, and [resource:combine-omex-archive] to package the model, experiment, data, and metadata. Conformance is evaluated separately through [resource:sbml-test-suite] and [resource:biosimulators-test-suite].

## Category errors

- Treating SBML or CellML as a workflow language for arbitrary data-processing pipelines.
- Treating SED-ML as an execution trace; it describes intended experiments and requested results.
- Assuming COMBINE Archive packaging guarantees that every simulator supports every model package or SED-ML feature.
- Inferring scientific correctness from conformance-suite success.
- Converting between SBML and CellML without checking whether modular structure, events, units, or package-specific semantics are preserved.

## Example architecture

A physiological modeling group publishes a CellML model, specifies parameter changes and repeated simulations in SED-ML, and distributes both in a COMBINE Archive. A biochemical model uses SBML Level 3 packages instead. Continuous integration runs the SBML Test Suite for the model engine and BioSimulators tests for archive execution, keeping model semantics, experiment intent, packaging, and conformance as separate layers.
