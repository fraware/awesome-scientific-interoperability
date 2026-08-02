# Astronomy data files, tables, and query services

**Decision question:** Which mechanism should an astronomy archive or client use for durable files, table serialization, or federated remote queries?

**Primary sources inspected:** [FITS Standard 4.0](https://fits.gsfc.nasa.gov/fits_standard.html), [IAU FITS Working Group rules](https://fits.gsfc.nasa.gov/iaufwg/iaufwg_rules.html), [IVOA VOTable 1.5](https://www.ivoa.net/documents/VOTable/), [IVOA TAP 1.1](https://ivoa.net/documents/TAP/), [CFITSIO](https://heasarc.gsfc.nasa.gov/docs/software/fitsio/fitsio.html), [Astropy VOTable](https://docs.astropy.org/en/stable/io/votable/index.html), [STILTS taplint](https://www.star.bris.ac.uk/~mbt/stilts/sun256/taplint.html), and [STILTS votlint](https://www.star.bris.ac.uk/~mbt/stilts/sun256/votlint.html).

## Choose by integration job

| Integration job | Strong starting point | Why |
|---|---|---|
| Preserve or exchange astronomical images, spectra, cubes, and binary tables as files | [resource:flexible-image-transport-system-fits] | FITS supplies the durable header-data-unit contract used across instruments, missions, archives, and analysis libraries. |
| Exchange richly annotated table results between Virtual Observatory services and clients | [resource:ivoa-votable] | VOTable defines field metadata, arrays, links, parameters, and several table serializations. |
| Query relational astronomy holdings across independently operated data centers | [resource:ivoa-table-access-protocol-tap] | TAP defines metadata endpoints, synchronous and asynchronous queries, ADQL, uploads, and spatial cross-matching. |
| Discover geospatial or Earth-observation assets through object catalogs | [resource:spatiotemporal-asset-catalog-stac] | STAC addresses spatiotemporal asset catalogs rather than astronomy relational-table services. |

## Composition pattern

A TAP service usually exposes table and column metadata, accepts ADQL or another declared query language, and returns results in [resource:ivoa-votable]. The table rows may identify or link durable [resource:flexible-image-transport-system-fits] products. These are complementary layers: service behavior, response serialization, and file representation.

ObsCore/ObsTAP may profile TAP tables for uniform observation discovery. It is a data-model profile, not a replacement for TAP. SAMP addresses application-to-application messaging and is outside the remote query decision. ASDF may be stronger than FITS for some hierarchical, schema-rich data models, but its archive adoption and family role require a separate decision.

## Evidence and conformance

- FITS has independent CFITSIO and Astropy implementations. Astropy exposes direct standard-verification behavior.
- TAP has separately operated OpenCADC and GAVO DaCHS service implementations. STILTS `taplint` checks protocol endpoints, metadata consistency, job behavior, and returned VOTables, but explicitly does not claim comprehensive coverage.
- VOTable has independent Astropy and STILTS implementations. `votlint` checks XML validity and data-structure semantics beyond schema validation.

A successful validator result establishes conformity for the checks performed. It does not prove scientific correctness, complete metadata quality, or semantic equivalence between every producer and consumer.

## Common category errors

- Treating VOTable as a query protocol.
- Treating TAP as a durable file format.
- Treating FITS compliance as evidence that coordinate systems or scientific metadata are adequate for a particular analysis.
- Adding ObsCore, SAMP, and every IVOA companion as separate top-level entries without a distinct user decision.
- Treating ASDF as a universal replacement for the installed FITS ecosystem.

## Relevant catalog entries

[resource:flexible-image-transport-system-fits] [resource:ivoa-votable] [resource:ivoa-table-access-protocol-tap] [resource:spatiotemporal-asset-catalog-stac]
