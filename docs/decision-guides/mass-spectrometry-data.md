# Mass-spectrometry data exchange

Use this guide when instrument output, spectra, chromatograms, acquisition settings, and processing metadata must move among vendor converters, analysis tools, repositories, and archives.

## Decision table

| Need | Strongest starting point | Why | Boundary |
|---|---|---|---|
| Exchange mass-spectrometry primary data and metadata | [resource:hupo-psi-mzml] | Controlled-vocabulary-backed XML captures spectra, chromatograms, binary arrays, instruments, acquisition, and processing | Identification and quantification results use separate PSI formats |
| Exchange heterogeneous analytical-instrument data | [resource:analytical-information-markup-language-animl] | Broader analytical schema covers multiple technique families | Less specialized for proteomics mass spectrometry |
| Use a cross-vendor analytical data ecosystem with ontologies | [resource:allotrope-data-format] | Common data format and semantic models cover broad analytical workflows | Some specification and tooling access is consortium-governed |

## Composition pattern

A laboratory converts proprietary files to [resource:hupo-psi-mzml], validates controlled-vocabulary placement and binary-array semantics, and deposits the resulting files in a repository. Broader laboratory systems may map selected metadata to [resource:analytical-information-markup-language-animl] or [resource:allotrope-data-format] without replacing mzML as the mass-spectrometry exchange contract.

## Evidence boundaries

- Independent readers and writers demonstrate practical interoperability but do not guarantee lossless vendor conversion.
- The OpenMS semantic validator checks schema and controlled-vocabulary rules; it does not certify instrument calibration, peak picking, or scientific interpretation.
- mzIdentML and mzTab remain separate result-exchange decisions.
