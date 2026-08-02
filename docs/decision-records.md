# Decision Records

Maintainer decisions that are likely to recur. Each record states the decision, rationale, and evidence that would trigger reassessment. These records supplement [editorial policy](editorial-policy.md) and [taxonomy](taxonomy.md); they do not override the project charter or North Star.

| ID | Title | Status | Date |
| --- | --- | --- | --- |
| [DR-001](#dr-001-hdf5-and-netcdf-via-scientific-profiles) | HDF5 and NetCDF via scientific profiles | Accepted | 2026-08-01 |
| [DR-002](#dr-002-workflow-engines-not-automatically-included) | Workflow engines not automatically included | Accepted | 2026-08-01 |
| [DR-003](#dr-003-general-agent-protocol-qualification) | General agent protocol qualification | Accepted | 2026-08-01 |
| [DR-004](#dr-004-validation-is-distinct-from-interoperability) | Validation is distinct from interoperability | Accepted | 2026-08-01 |
| [DR-005](#dr-005-reference-architecture-criteria) | Reference architecture criteria | Accepted | 2026-08-01 |

---

## DR-001: HDF5 and NetCDF via scientific profiles

**Decision:** List generic [HDF5](https://www.hdfgroup.org/) and generic NetCDF as container formats only through scientific profiles that supply an interoperability contract. Do not add standalone entries for the base formats.

**Rationale:** HDF5 and NetCDF are storage containers. Scientific interoperability requires agreed variable semantics, coordinates, units, application definitions, or validation rules that independent systems can implement without private conventions. Generic containers fail the sentence test on their own.

**Included examples:**

- [NeXus](https://www.nexusformat.org/) — HDF5 application definitions and nxvalidate for scattering-facility data (`catalog/resources/data-and-digital-objects.yaml`).
- [Climate and Forecast (CF) Metadata Conventions](https://cfconventions.org/) — semantic layer for NetCDF climate and forecast arrays (`catalog/resources/metadata-and-semantics.yaml`).

**Excluded:** Generic HDF5 (see [notable exclusions](#notable-exclusions)). Generic NetCDF without a profile that supplies cross-system semantics.

**Reassess when:** A new scientific profile over HDF5 or NetCDF passes the admission tests, is maintained by multiple institutions, and is not subsumed by an existing entry.

---

## DR-002: Workflow engines not automatically included

**Decision:** Popular workflow engines (Nextflow, Snakemake, Cromwell, Galaxy, and similar) are not automatically included because they are widely deployed. Include a workflow engine only when it exposes a documented cross-system interoperability mechanism that is among the strongest available examples for that mechanism.

**Rationale:** Most workflow engines are primarily execution environments for a single language or platform. The list curates interchange contracts—workflow languages (CWL, WDL), execution APIs (GA4GH WES, TES), registries (WorkflowHub, TRS), portable test systems (Sapporo), and backends that connect heterogeneous engines (WfExS-backend)—not every runner implementation.

**Watchlist:** Nextflow, Snakemake, Cromwell, and Galaxy remain on the [watchlist](watchlist.md) with explicit promotion conditions in `catalog/watchlist.yaml`.

**Reassess when:** An engine documents normative cross-backend contracts, conformance tests, or registry interchange beyond what existing main-list entries already cover, and boundary analysis shows distinct decision value.

---

## DR-003: General agent protocol qualification

**Decision:** General agent-tool protocols (for example, Model Context Protocol) may enter the main list when they define a reusable public contract for scientific tool discovery and invocation, even though they are domain-agnostic. They must not be treated as authorization, provenance, validation, or laboratory safety layers.

**Rationale:** Agent protocols qualify as interoperability contributions when independently maintained clients and servers exchange capabilities through a documented wire format. Scientific use still requires domain profiles, access control, and evidence packaging elsewhere in the corpus. Preprint-only or draft-only protocols belong on the watchlist until a normative specification and independent implementations exist.

**Included:** [Model Context Protocol](https://modelcontextprotocol.io/), [ToolUniverse](https://zitniklab.hms.harvard.edu/ToolUniverse/en/) (see [scientific agents decision guide](decision-guides/scientific-agents-and-tool-interfaces.md)).

**Watchlist:** Agent2Agent, IEEE P3971, Science Context Protocol, SciToolAgent.

**Reassess when:** A draft protocol publishes a stable normative specification with multiple independent scientific implementations, or [taxonomy reassessment](taxonomy.md) supports splitting agent and access sections.

---

## DR-004: Validation is distinct from interoperability

**Decision:** Validation, conformance testing, and schema checking are listed under **Validation and Conformance** only when they test interoperability across independently developed systems. Passing a validator does not by itself establish that two systems can exchange or interpret scientific content in production.

**Rationale:** A JSON Schema or SHACL shape can verify syntax without guaranteeing semantic agreement between producers and consumers. Interoperability requires documented exchange semantics—what objects connect, through which mechanism, and with what stewardship. Validators support adoption; they do not replace the mechanism.

**Examples:** Profile validators (RO-Crate, CF checker), cross-implementation test suites (Sapporo), and conformance suites tied to normative specifications belong in Validation and Conformance when they test multi-party exchange.

**Not sufficient alone:** Internal QA tools, single-vendor linters, or popularity metrics without a public interoperability contract.

**Reassess when:** A validator becomes the authoritative normative specification for cross-system exchange (rare); treat as a specification change, not a validation-only addition.

---

## DR-005: Reference architecture criteria

**Decision:** Broad platforms qualify as **reference architectures** only when they (1) integrate multiple listed interoperability mechanisms across independently maintained components, (2) expose documented boundaries so readers can extract reusable patterns, and (3) meet the exceptional-quality bar relative to mechanism-specific entries already on the main list. Do not create a dedicated **Reference Architectures** section until at least three such entries exist (see [taxonomy reassessment](taxonomy.md)).

**Rationale:** End-to-end platforms (Galaxy, SciToolAgent, all-in-one laboratory stacks) are valuable but often duplicate decision paths already covered by workflow languages, packaging profiles, and device standards. Listing them as generic platforms dilutes the North Star. Watchlist placement with explicit promotion conditions preserves visibility without lowering the bar.

**Current status (2026-08-01):** No main-list entry is classified as a reference architecture. Galaxy, SciToolAgent, Cromwell, and related candidates remain on the watchlist.

**Reassess when:** At least three watchlist or new candidates pass promotion conditions with explicit comparison to existing main-list entries, or taxonomy reassessment documents a new section threshold met.

---

## Notable exclusions

These exclusions prevent repeated re-evaluation of candidates already decided against the North Star. Full gap reviews remain under [`candidate-reviews/`](candidate-reviews/).

| Resource | Decision | Rationale |
| --- | --- | --- |
| RDF Data Cube Vocabulary | Excluded | Compatible with SDMX; for operational statistical exchange SDMX is the stronger entry. RDF-native portals are partly covered by DCAT and SKOS. |
| Generic HDF5 | Excluded | Container format without a domain interoperability contract. NeXus is the included HDF5 scientific profile for scattering data. |
| OGC API - Records | Excluded | Federated catalog discovery is already addressed by DCAT and STAC. |
| OGC API - Processes | Excluded for this corpus | Generic geoprocessing is less decision-critical than openEO for Earth-observation cloud processing. |
| Full DICOM | Excluded | DICOMweb is the included web integration profile. |
| Additional RO/provenance profiles | Excluded | Existing RO-Crate, Workflow Run RO-Crate, CWLProv, ISO 23494-2, and P-Plan entries already cover the packaging and provenance problems for this corpus. |

Re-evaluate an exclusion only when a distinct scientific profile or contract appears that is not subsumed by an existing main-list entry.
