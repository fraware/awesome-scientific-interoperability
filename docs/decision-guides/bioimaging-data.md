# Bioimaging data exchange

**Decision question:** Which mechanism should a bioimaging system use for installed-base microscopy files, cloud-native multidimensional arrays, clinical imaging services, facility data, or publication packaging?

**Primary sources inspected:** [OME-TIFF 6.2.2](https://docs.openmicroscopy.org/ome-model/6.2.2/ome-tiff/specification.html), [Bio-Formats OME-TIFF support](https://docs.openmicroscopy.org/bio-formats/latest/formats/ome-tiff.html), [OME-XML validation](https://docs.openmicroscopy.org/bio-formats/latest/users/comlinetools/xml-validation.html), [OME-Zarr 0.5](https://ngff.openmicroscopy.org/0.5/), [DICOMweb](https://www.dicomstandard.org/using/dicomweb), [NeXus](https://www.nexusformat.org/), and [RO-Crate 1.3](https://www.researchobject.org/ro-crate/specification/1.3/).

## Choose by integration job

| Integration job | Strong starting point | Why | Boundary |
|---|---|---|---|
| Exchange mature single-file or multi-file microscopy datasets across installed readers and writers | [resource:ome-data-model-and-ome-tiff] | TIFF or BigTIFF pixel storage with embedded OME-XML and broad Bio-Formats compatibility | Less suitable for object-store-native chunk access and very large distributed pyramids |
| Exchange cloud-native multidimensional images, pyramids, labels, plates, wells, and coordinates | [resource:ome-ngff] | Versioned OME semantics over Zarr for chunked arrays and object stores | Version and optional-feature support must be declared by producers and consumers |
| Retrieve clinical imaging objects through standardized services | [resource:dicomweb] | Preserves DICOM identity, information model, and service operations | Clinical exchange contract, not a general microscopy replacement |
| Exchange neutron, X-ray, and muon facility data | [resource:nexus] | HDF5 application definitions and field dictionaries | Facility-scoped scientific profile |
| Publish images with software, instruments, workflows, and provenance | [resource:ro-crate] | Contextual research-object package | Does not replace the image representation |

## OME-TIFF and OME-NGFF are complementary

OME-TIFF remains the strongest installed-base exchange format where producers and consumers require TIFF compatibility, portable files, and embedded OME-XML. OME-NGFF is stronger for cloud storage, partial reads, multiscale arrays, and distributed analysis. Migration should record the source format, OME schema or OME-Zarr version, conversion software, and any metadata that could not be preserved.

## Evidence and conformance

Bio-Formats is the official OME-TIFF reader and writer, and BioIO supplies a separately operated reader and writer. The implementation claim therefore remains `reference-and-others`, because the catalog has verified one independent operator beyond the official ecosystem. Bio-Formats can validate OME-XML extracted from OME-TIFF. That check does not establish TIFF layout consistency, pixel correctness, lossless conversion, or scientific completeness.

The OME-NGFF public validator checks represented schema and hierarchy constraints. It does not establish reader support for every optional feature or scientific validity of coordinate transformations.

## Common category errors

- Treating generic TIFF compatibility as OME-TIFF support.
- Treating generic Zarr compatibility as OME-NGFF conformance.
- Assuming XML or hierarchy validation proves lossless conversion.
- Replacing DICOMweb in clinical workflows without preserving DICOM identity and metadata.
- Treating RO-Crate as an image format.

## Relevant catalog entries

[resource:ome-data-model-and-ome-tiff] [resource:ome-ngff] [resource:dicomweb] [resource:nexus] [resource:ro-crate]
