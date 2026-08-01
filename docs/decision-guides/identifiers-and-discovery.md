# Identifiers and discovery

Compare persistent identifier systems, resolver registries, and discovery services. Explicitly separate **what is identified**, **how it is resolved**, and **where metadata is catalogued**. Catalog entries: [resource:orcid], [resource:research-organization-registry-ror], [resource:igsn-id], [resource:datacite-metadata-schema-and-rest-api], [resource:crossref-rest-api-and-metadata], [resource:identifiers-org], [resource:optimade], [resource:ga4gh-service-info], [resource:ga4gh-service-registry], [resource:ga4gh-tool-registry-service-trs], [resource:fairsharing].

**Primary sources inspected:** [ORCID](https://info.orcid.org/what-is-orcid/), [ROR](https://ror.org/about/), [IGSN ID](https://ev.igsn.org/about-igsns), [DataCite API](https://support.datacite.org/docs/api), [Crossref REST API](https://www.crossref.org/documentation/retrieve-metadata/rest-api/), [Identifiers.org](https://identifiers.org/), [GA4GH Service Info](https://www.ga4gh.org/product/service-info/), [GA4GH Service Registry](https://www.ga4gh.org/product/service-registry/), [GA4GH TRS](https://www.ga4gh.org/product/tool-registry-service-trs/), [FAIRsharing](https://fairsharing.org/).

## Identifier scope and object type

| Resource | Object type identified | Scope | Not an identifier for |
|----------|------------------------|-------|------------------------|
| [resource:orcid] | Individual researchers | Global scholarly identity | Organizations, samples, datasets, workflows |
| [resource:research-organization-registry-ror] | Research organizations | Global open org IDs | People, instruments, granular departments unless mapped |
| [resource:igsn-id] | Material samples | Physical specimens and derived digital records | Software, workflows, organizations |
| [resource:datacite-metadata-schema-and-rest-api] | Research entities via DOI registration | Data, software, samples, and other registrable objects | People (use ORCID); orgs (use ROR) |
| [resource:crossref-rest-api-and-metadata] | Scholarly works via DOI | Publications and related scholarly metadata | Primary sample IDs; executable workflows |
| [resource:identifiers-org] | Namespace resolution for compact IDs | Life-science compact identifiers (CHEBI, UniProt, etc.) | Creating new identifier schemes; policy registry |

**Category error:** using a DOI as a person identifier, or ORCID as a dataset PID without a separate object registration.

## Discovery registries versus identifiers versus metadata standards

| Mechanism | Provides | Does not provide |
|-----------|----------|------------------|
| **PID systems** (ORCID, ROR, IGSN, DOI registrars) | Persistent identity and landing metadata | Full semantic alignment of dataset fields |
| **Resolver registry** ([resource:identifiers-org]) | Compact ID → resolver URL patterns | Curated descriptions of standards relationships |
| **Service discovery APIs** ([resource:ga4gh-service-info], [resource:ga4gh-service-registry]) | Live service endpoints, versions, types | Persistent IDs for research objects |
| **Tool/workflow discovery** ([resource:ga4gh-tool-registry-service-trs]) | Fetchable tool/workflow descriptors | Semantic harmonization of dataset variables |
| **Standards registry** ([resource:fairsharing]) | Curated records linking standards, databases, policies | Operational resolution of compact IDs |

[resource:fairsharing] complements PID and API layers: use it to **find** which metadata standard or repository policy applies; use PIDs and resolvers to **cite** and **retrieve** objects.

## Comparison: scholarly and research-object discovery

| Dimension | [resource:crossref-rest-api-and-metadata] | [resource:datacite-metadata-schema-and-rest-api] | [resource:fairsharing] |
|-----------|------------------------------------------|--------------------------------------------------|------------------------|
| **Primary artifact** | Publication DOI metadata graph | Research-object DOI metadata and relations | Curated standard/database/policy records |
| **API role** | Retrieve/update scholarly metadata | Register and discover research entities | Search relationships among standards |
| **Strongest use case** | Link publications, funders, citations | Repository DOI registration for data/software | Discover applicable standards and databases |
| **Inappropriate use case** | Register primary experimental samples | Replace Crossref for journal articles | Resolve UniProt accessions (use [resource:identifiers-org]) |

## Comparison: operational service discovery (GA4GH)

| Dimension | [resource:ga4gh-service-info] | [resource:ga4gh-service-registry] | [resource:ga4gh-tool-registry-service-trs] |
|-----------|------------------------------|-----------------------------------|-------------------------------------------|
| **Granularity** | Single service self-description | Index of services | Versioned tools/workflows |
| **Typical consumer** | Clients probing one endpoint | Federated discovery portals | Workflow engines and registries |
| **Relation to PIDs** | Operational URLs and versions | Aggregates Service Info records | Retrieves executable descriptors, not DOIs for people |
| **Strongest use case** | Health/version checks before calls | Build service catalogs in genomics clouds | Connect [resource:workflowhub] to execution clients |

Genomics-originated but illustrates separable **service metadata** ([resource:ga4gh-service-info]) from **registry aggregation** ([resource:ga4gh-service-registry]) from **tool retrieval** ([resource:ga4gh-tool-registry-service-trs]).

## Decision paths

- **Attribute a paper to people and organizations:** ORCID + ROR in Crossref/DataCite metadata, resolved via public APIs.
- **Link a physical sample to datasets and publications:** [resource:igsn-id] with DataCite relations where registrars support them.
- **Resolve life-science compact IDs in pipelines:** [resource:identifiers-org] registry entries; do not conflate with FAIRsharing curation.
- **Discover which standard applies to a domain dataset:** Start at [resource:fairsharing]; then implement the cited metadata standard (see [Metadata semantics and units](metadata-semantics-and-units.md)).
- **Find and fetch a workflow for execution:** [resource:ga4gh-tool-registry-service-trs] via [resource:workflowhub]; separate from DOI registration of results.

## Example architecture

A repository mints DOIs through [resource:datacite-metadata-schema-and-rest-api], embedding ORCID and ROR in metadata. Sample IDs use [resource:igsn-id]. Pipeline code resolves enzyme IDs via [resource:identifiers-org]. Authors locate applicable field standards through [resource:fairsharing]. A workflow portal discovers services via [resource:ga4gh-service-registry], reads [resource:ga4gh-service-info] from each candidate, and fetches workflow bundles through TRS.
