# Review notes: Identifiers and Discovery

**Review date:** 2026-08-01  
**Reviewer role:** Section reviewer (PR-04 catalog migration A)  
**Records migrated:** 10

## Sources inspected

| Resource | Primary sources |
|----------|-----------------|
| Crossref REST API and Metadata | [Crossref REST API documentation](https://www.crossref.org/documentation/retrieve-metadata/rest-api/); [api.crossref.org](https://api.crossref.org/) |
| DataCite Metadata Schema and REST API | [DataCite REST API guide](https://support.datacite.org/docs/api); [DataCite metadata schema](https://schema.datacite.org/) |
| FAIRsharing | [fairsharing.org](https://fairsharing.org/); [FAIRsharing API documentation](https://fairsharing.github.io/FAIRsharing-API/) |
| GA4GH Service Info | [GA4GH Service Info product page](https://www.ga4gh.org/product/service-info/); [ga4gh-discovery/ga4gh-service-info](https://github.com/ga4gh-discovery/ga4gh-service-info) |
| GA4GH Service Registry | [GA4GH Service Registry product page](https://www.ga4gh.org/product/service-registry/); [ga4gh-discovery/ga4gh-service-registry](https://github.com/ga4gh-discovery/ga4gh-service-registry) |
| GA4GH Tool Registry Service (TRS) | [GA4GH TRS product page](https://www.ga4gh.org/product/tool-registry-service-trs/); [ga4gh/tool-registry-service-schemas](https://github.com/ga4gh/tool-registry-service-schemas) |
| Identifiers.org | [identifiers.org](https://identifiers.org/); [docs.identifiers.org](https://docs.identifiers.org/) |
| IGSN ID | [IGSN e.V. about page](https://ev.igsn.org/about-igsns); [DataCite IGSN partnership documentation](https://support.datacite.org/docs/igsn-ids) |
| ORCID | [ORCID about page](https://info.orcid.org/what-is-orcid/); [ORCID public API v3.0](https://pub.orcid.org/v3.0/) |
| Research Organization Registry (ROR) | [ror.org/about](https://ror.org/about/); [ror-community/ror-api](https://github.com/ror-community/ror-api) |

## Changes made

- Renamed `description` to `summary` (exact README parity preserved).
- Removed v1 scoring fields (`evidence_level`, `maintenance_signal`, `north_star_utility`).
- Added v2 maturity, evidence_types, implementation_status, conformance_status, stewardship, domains, source_urls, alternatives, related_resource_ids, and review_due_on (2027-08-01).
- Crossref and DataCite listed as mutual alternatives; ORCID and ROR cross-linked.
- Crossref related to Scholix (group C); GA4GH TRS related to CWL (group B); IGSN related to DataCite for registration partnership.
- GA4GH discovery trio (Service Info, Service Registry, TRS) linked through `related_resource_ids`.

## Unresolved questions

- GA4GH Service Registry versus Planet implementation registry distinction remains editorial; boundary notes preserved from v1.
- Identifiers.org resolution API timed out during automated fetch; stewardship confirmed via docs.identifiers.org and ELIXIR infrastructure statements.

## Conflicts

None.
