# Implementation independence re-adjudication (PR #38)

**Date:** 2026-08-02  
**Catalog version:** 2.2.0  
**Rule:** `multiple-independent` requires ≥2 `independent-implementation` registry rows with distinct `operator_steward_id` values that are not the resource `steward_id` (unless an explicit multi-org steward exception is recorded).

## Summary

| Outcome | Count |
|---|---:|
| Retained `multiple-independent` | 6 |
| Downgraded to `reference-and-others` | 22 |
| Former MI claims reviewed | 28 |

## Retained MI (with registry operators)

| Resource | Independent operators |
|---|---|
| `bagit` | Library of Congress (`loc-bagit-python`); Artefactual Systems (`archivematica-bagit`) |
| `common-workflow-language-cwl` | Data Biosphere / Toil; Arvados Foundation |
| `dicomweb` | dcm4che; OHIF |
| `ga4gh-tool-registry-service-trs` | Dockstore Consortium; WorkflowHub |
| `optimade` | FAIRmat / NOMAD; Materials Project |
| `workflow-description-language-wdl` | Broad Institute / Cromwell; Chan Zuckerberg Initiative / miniwdl |

## Downgraded

| Resource | Reason |
|---|---|
| `apptainer-singularity-image-format` | Resource steward operates Apptainer; only one clear non-steward SIF runtime (Sylabs) at primary-source threshold |
| `biocompute-objects` | Cited repos under BioCompute community stewardship |
| `bioschemas` | Profile/community tooling, not two independent operators |
| `citation-file-format-citation-cff` | Tooling cluster under one project org |
| `codemeta` | Steward-maintained vocabulary without second non-steward operator |
| `cwl-conformance-tests` | Conformance artifact; independence belongs on CWL language entry |
| `edam-ontology` | Single ontology artifact plus adoption, not two EDAM implementations |
| `ga4gh-data-repository-service-drs` | Could not verify two non-GA4GH operators with primary URLs |
| `ga4gh-data-use-ontology-duo` | Maintainer overlap under GA4GH umbrella |
| `ga4gh-task-execution-service-tes` | Only one verified non-steward TES backend |
| `ga4gh-workflow-execution-service-wes` | Only one verified non-steward WES service |
| `journal-article-tag-suite-jats` | NLM stewardship family tooling |
| `model-context-protocol-mcp` | **Mandatory fail:** official repos under `modelcontextprotocol` / same steward |
| `nanopublications` | Same-community library cluster |
| `obo-foundry` | Governance/registry coordination, not multi-implemented format |
| `openeo-api` | Consortium-hosted backends; institution backends not registered as independent operators here |
| `orcid` | Central registry; consumers are not ORCID implementations |
| `research-organization-registry-ror` | Central registry pattern (same as ORCID) |
| `schema-org` | Vocabulary standard; consumer adoption is not Schema.org implementation |
| `sila-2` | Consortium reference stacks; vendor SDKs not evidenced to threshold |
| `unified-code-for-units-of-measure-ucum` | Same-maintainer community repos |
| `w3c-data-catalog-vocabulary-dcat` | Vocabulary consumers are not DCAT implementations |

## MCP fixture note

`catalog/implementations.yaml` records MCP specification and servers repos as `official-implementation` under `model-context-protocol-project`. Those rows deliberately do not satisfy MI. Same-steward dual-repo claims fail validator and audit under the v2.2 rule.
