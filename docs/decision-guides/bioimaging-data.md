# Bioimaging data exchange

**Decision question:** Which mechanism should a bioimaging system use for cloud-native multidimensional arrays, clinical imaging services, facility data, or publication packaging?

**Primary sources inspected:** [OME-Zarr 0.5](https://ngff.openmicroscopy.org/0.5/), [OME-Zarr tools](https://ngff.openmicroscopy.org/tools/), [OME-NGFF Validator](https://ome.github.io/ome-ngff-validator/), [DICOMweb](https://www.dicomstandard.org/using/dicomweb), [NeXus](https://www.nexusformat.org/), and [RO-Crate 1.3](https://www.researchobject.org/ro-crate/specification/1.3/).

## Choose by integration job

| Integration job | Strong starting point | Why |
|---|---|---|
| Store and exchange cloud-native multidimensional microscopy images, pyramids, labels, plates, wells, and coordinate metadata | [resource:ome-ngff] | OME-Zarr defines bioimaging metadata and hierarchy rules over Zarr v3 for object stores and distributed analysis. |
| Retrieve and manage clinical imaging studies, series, instances, and rendered objects through standardized web services | [resource:dicomweb] | DICOMweb preserves the clinical DICOM service and information model. |
| Exchange neutron, X-ray, and muon facility data through HDF5 application definitions | [resource:nexus] | NeXus carries facility-specific application definitions and field dictionaries. |
| Publish a broader research object connecting images with software, people, instruments, workflows, and provenance | [resource:ro-crate] | RO-Crate packages context around the image data without replacing the image representation. |

## OME-Zarr boundary

OME-Zarr 0.5 is the current released cloud-oriented specification and uses Zarr v3. The release still contains transitional metadata and the ecosystem is actively moving toward later specifications. Producers must record the OME-Zarr metadata version and the Zarr version they write; consumers must declare the versions and optional features they support.

OME-TIFF remains a strong installed-base choice for mature single-file exchange and broad Bio-Formats compatibility. Zarr alone supplies chunked-array storage but lacks the bioimaging semantics required for axes, multiscales, labels, plates, wells, and rendering metadata. Neither substrate should be treated as equivalent to the OME-Zarr profile.

## Evidence and conformance

The OME project publishes the normative specification, an implementation registry, and a public OME-NGFF Validator. `ome-zarr-py` is an official implementation and `bioformats2raw` is separately operated. The catalog therefore records `reference-and-others`, not `multiple-independent`, because one independently operated converter plus official tools does not meet the two-independent-operator threshold.

The public validator checks represented schema and hierarchy constraints. It does not establish pixel correctness, lossless conversion from proprietary formats, coordinate-transform validity for a specific experiment, or reader support for every optional feature.

## Common category errors

- Equating generic Zarr compatibility with OME-Zarr conformance.
- Assuming every OME-Zarr reader supports every released version and transitional feature.
- Replacing DICOMweb with OME-Zarr in regulated clinical workflows without preserving DICOM identity and metadata.
- Treating RO-Crate as an image format.
- Assuming a successfully converted pyramid preserves all source metadata and scientific meaning.

## Relevant catalog entries

[resource:ome-ngff] [resource:dicomweb] [resource:nexus] [resource:ro-crate]
