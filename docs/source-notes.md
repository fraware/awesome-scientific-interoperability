# Source Notes

The seed corpus was selected from a 100-resource adversarial landscape review completed on August 1, 2026. The main list contains 75 resources that passed the initial scope and quality tests.

Version-sensitive corrections applied during repository construction include:

- RO-Crate 1.3, published June 22, 2026, as the current long-term release.
- Model Context Protocol specification revision 2026-07-28.
- Croissant format specification 1.1, published January 29, 2026.
- Workflow Run RO-Crate profile collection version 0.5.

A listed version or maintenance signal should be rechecked whenever an entry is materially edited.

## PR-16A exclusions (2026-08-01)

**RDF Data Cube Vocabulary** ([W3C Recommendation](https://www.w3.org/TR/vocab-data-cube/)) — excluded from the main list after PR-16A review. The cube model is compatible with SDMX; for operational statistical exchange SDMX is the stronger entry. RDF Data Cube remains appropriate for Linked Data publication portals already covered in part by [resource:w3c-data-catalog-vocabulary-dcat] and [resource:simple-knowledge-organization-system-skos]. Re-evaluate only if a distinct scientific profile supplies a contract not subsumed by SDMX.

## PR-16B exclusions (2026-08-01)

**Generic HDF5** ([HDF Group](https://www.hdfgroup.org/)) — excluded; container format without a domain interoperability contract. **NeXus** is the included HDF5 scientific profile for neutron, X-ray, and muon scattering data.

## PR-16C exclusions (2026-08-01)

**OGC API - Records** — excluded; federated catalog discovery is already addressed by [resource:w3c-data-catalog-vocabulary-dcat] and [resource:spatiotemporal-asset-catalog-stac].

**OGC API - Processes** — excluded for this corpus; generic geoprocessing is less decision-critical than **openEO** for EO cloud processing integrations.

## PR-16D exclusions (2026-08-01)

**Full DICOM** — excluded; **DICOMweb** is the included web integration profile.

**Additional RO/provenance profiles** — excluded; existing entries ([resource:ro-crate], Workflow Run RO-Crate, CWLProv, ISO 23494-2, P-Plan) already cover the packaging and provenance integration problems for this corpus.
