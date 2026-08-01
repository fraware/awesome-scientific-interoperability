# Controlled data access

Compare machine-readable authorization and data-use semantics for sensitive research data. Catalog entries: [resource:ga4gh-passports], [resource:ga4gh-data-use-ontology-duo].

**Primary sources inspected:** [GA4GH Passports](https://www.ga4gh.org/product/ga4gh-passports/), [Passports standard repository](https://github.com/ga4gh-duri/ga4gh-passport-standard), [GA4GH DUO](https://www.ga4gh.org/product/data-use-ontology-duo/), [DUO ontology repository](https://github.com/EBISPOT/DUO).

Watchlist candidates (not catalog entries): [Open Digital Rights Language (ODRL)](https://www.w3.org/TR/odrl-model/), [Five Safes RO-Crate](https://zenodo.org/records/10376350) — assessed **as of 2026-08-01** below.

## Separate layers

| Layer | Example in catalog | Responsibility |
|-------|-------------------|----------------|
| **Identity** | ORCID, institutional IdPs (see [Identifiers and discovery](identifiers-and-discovery.md)) | Who is requesting access |
| **Authorization transport** | [resource:ga4gh-passports] visas embedded in OAuth/OIDC flows | Machine-readable access assertions presented to services |
| **Data-use conditions** | [resource:ga4gh-data-use-ontology-duo] terms in dataset metadata | What uses are permitted or restricted |
| **Policy enforcement** | Repository DACs, TRE gates, contract law | Final human/legal decisions beyond ontology matching |

**Identity, authorization, and data-use policy are separate layers.** DUO terms do not authenticate users; Passports do not replace data-use committees; agent tools ([Scientific agents and tool interfaces](scientific-agents-and-tool-interfaces.md)) do not imply permitted data use.

## Comparison: Passports versus DUO

| Dimension | [resource:ga4gh-passports] | [resource:ga4gh-data-use-ontology-duo] |
|-----------|---------------------------|----------------------------------------|
| **Object represented** | Researcher visas / authorized roles for datasets | Dataset permission and restriction classes |
| **Mechanism** | Signed passport structures in federated auth flows | Ontology terms attached to dataset metadata |
| **Typical consumer** | Data access services validating tokens | Repositories, DAC matching tools, automated policy engines |
| **Maturity (2026-08-01)** | Maintained; genomics origin with broader lessons | Established; widely adopted in controlled-access genomics |
| **Strongest use case** | Federated access to controlled genomic datasets | Express and match data-use limitations computationally |
| **Inappropriate use case** | General license management for all software artifacts | Standalone user authentication without Passports or IdP |

Passports and DUO are **complementary**: datasets advertise DUO terms; authorized researchers present Passports that services match against those terms.

## Watchlist candidates (emerging, as of 2026-08-01)

| Candidate | Status | Assessment |
|-----------|--------|------------|
| [ODRL](https://www.w3.org/TR/odrl-model/) | W3C Recommendation for policy expressions | Potential foundation for machine-readable licenses and permissions; not catalogued as established scientific access layer; evaluate mapping to DUO/Passports before adoption |
| [Five Safes RO-Crate](https://zenodo.org/records/10376350) | Research-object profile proposal on Zenodo | Emerging pattern for Trusted Research Environment context; **as of 2026-08-01** implementation growth in TRE-FX/DARE UK/EOSC-ENTRUST still under watch—do not treat as production requirement |

Neither watchlist candidate replaces [resource:ga4gh-passports] or DUO in genomics-controlled access stacks today.

## Agent and workflow cautions

- Workflow APIs ([resource:ga4gh-data-repository-service-drs], [resource:ga4gh-workflow-execution-service-wes]) resolve **bytes** and **runs**; they do not inherit DUO compliance from caller identity unless enforcement is configured.
- MCP tool success does not prove an agent held a valid Passport or acceptable use role.
- Packaging ([Research object packaging](research-object-packaging.md)) may embed DUO terms in metadata but cannot enforce access without repository policy.

## Decision paths

- **Federated genomic controlled access:** Implement [resource:ga4gh-passports] with DUO-tagged datasets.
- **Automated DAC matching:** Encode dataset conditions with [resource:ga4gh-data-use-ontology-duo]; keep human appeal processes explicit.
- **Trusted Research Environment context packaging:** Monitor Five Safes RO-Crate implementations; pair with organizational Five Safes policies, not generic crates alone.
- **Cross-domain license automation:** Evaluate ODRL mappings to DUO-like terms; verify legal review workflows.

## Example architecture

A cohort repository registers DOIs with DUO terms describing health-data restrictions. Researchers authenticate via institutional OIDC; the access proxy validates [resource:ga4gh-passports] visas before DRS URLs resolve. Workflow engines log runs in [resource:workflow-run-ro-crate] without exposing passports in crates. An agent MCP server refuses tool calls unless the same visa validation succeeds, keeping authorization separate from tool invocation syntax.
