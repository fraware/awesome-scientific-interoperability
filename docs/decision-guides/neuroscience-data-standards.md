# Neuroscience dataset and neurophysiology exchange

Choose among dataset organization, rich neurophysiology representation, clinical image transport, and facility-style experimental containers. Catalog entries: [resource:brain-imaging-data-structure-bids], [resource:neurodata-without-borders-nwb], [resource:dicomweb], [resource:nexus].

**Primary sources inspected:** [BIDS 1.11.1](https://bids-specification.readthedocs.io/en/stable/), [BIDS Validator](https://bids-validator.readthedocs.io/en/latest/user_guide/web.html), [NWB Schema](https://nwb.org/tools/core/nwb-schema/), [NWB Inspector](https://nwb.org/tools/core/nwbinspector/), [DICOMweb](https://www.dicomstandard.org/using/dicomweb), and [NeXus](https://www.nexusformat.org/).

## Decision table

| Integration problem | Strongest starting point | Why | Boundary |
|---|---|---|---|
| Organize a multi-subject neuroscience dataset for sharing and analysis | [resource:brain-imaging-data-structure-bids] | Standard paths, filenames, modality rules, JSON/TSV sidecars, derivatives, independent writers, and a public validator | Retains underlying modality file formats and does not define every internal signal structure |
| Exchange rich neurophysiology acquisition and analysis data | [resource:neurodata-without-borders-nwb] | Extensible typed schema, cross-language APIs, HDF5 storage, extensions, and best-practice validation | Dataset-level organization and many imaging workflows remain stronger in BIDS |
| Retrieve or store clinical imaging studies through healthcare infrastructure | [resource:dicomweb] | DICOM PS3.18 REST services for studies, series, instances, metadata, and rendered objects | Research dataset organization, experimental annotations, and derivatives require additional profiles |
| Exchange beamline and scattering-facility experimental data | [resource:nexus] | HDF5 application definitions, facility conventions, and field dictionaries | It is not a general neuroscience dataset convention despite sharing an HDF5 substrate with NWB |

## BIDS and NWB are complementary

Use [resource:brain-imaging-data-structure-bids] when the principal interoperability problem is dataset layout and cross-pipeline discovery. Use [resource:neurodata-without-borders-nwb] when the principal problem is representing continuous neurophysiology, stimulus, behavior, processing modules, and analysis results inside a typed extensible file. A project may place NWB files inside a BIDS-organized dataset when both contracts are needed, but each profile's current rules must be checked explicitly.

## Category errors

- Treating BIDS validation as proof that source measurements, coordinate systems, or scientific annotations are correct.
- Treating NWB's HDF5 storage as sufficient interoperability without the NWB schema and extension rules.
- Converting DICOM to BIDS while discarding acquisition metadata needed for traceability.
- Assuming BIDS and NWB are interchangeable because both support neuroscience data.
- Listing generic HDF5 or NIfTI as substitutes for the domain semantics supplied by BIDS or NWB.

## Example architecture

A neuroscience archive receives scanner studies through DICOMweb, converts deidentified acquisitions into BIDS with a separately operated converter, validates the dataset with BIDS Validator, and stores electrophysiology sessions as NWB files checked by NWB Inspector. Repository packaging and execution provenance remain separate layers.
