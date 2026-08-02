# Review notes: Workflows and Execution

**Review date:** 2026-08-01  
**Reviewer role:** Section reviewer (PR-05 catalog migration B)  
**Records migrated:** 10

## Sources inspected

| Resource | Primary sources |
|----------|-----------------|
| Common Workflow Language (CWL) | [commonwl.org](https://www.commonwl.org/); [cwl-v1.2 conformance tests](https://github.com/common-workflow-language/cwl-v1.2) |
| cwltool | [common-workflow-language/cwltool](https://github.com/common-workflow-language/cwltool); CWL conformance suite |
| GA4GH DRS | [GA4GH DRS product page](https://www.ga4gh.org/product/data-repository-service-drs/); [data-repository-service-schemas](https://github.com/ga4gh/data-repository-service-schemas) |
| GA4GH TES | [GA4GH TES product page](https://www.ga4gh.org/product/task-execution-service-tes/); [task-execution-schemas](https://github.com/ga4gh/task-execution-schemas) |
| GA4GH WES | [GA4GH WES product page](https://www.ga4gh.org/product/workflow-execution-service-wes/); [workflow-execution-service-schemas](https://github.com/ga4gh/workflow-execution-service-schemas) |
| LifeMonitor | [lifemonitor.eu](https://lifemonitor.eu/); [life-monitor/life-monitor](https://github.com/life-monitor/life-monitor) |
| Sapporo | [sapporo-wes/sapporo](https://github.com/sapporo-wes/sapporo); GA4GH WES specification |
| WfExS-backend | [inab/WfExS-backend](https://github.com/inab/WfExS-backend); Workflow Run RO-Crate specification |
| Workflow Description Language (WDL) | [openwdl.org](https://openwdl.org/); [openwdl/wdl](https://github.com/openwdl/wdl) |
| WorkflowHub | [workflowhub.eu](https://workflowhub.eu/); [Workflow RO-Crate profile](https://about.workflowhub.eu/Workflow-RO-Crate/) |

## Changes made

- Separated workflow languages (CWL, WDL) from execution APIs (WES, TES, DRS) in boundary notes and related_resource_ids.
- Linked GA4GH DRS, TES, and WES as a federated workflow stack; related Sapporo as reference WES implementation.
- Recorded CWL public-suite conformance with direct GitHub suite URL; mutual CWL/WDL alternatives.
- Connected LifeMonitor and WorkflowHub to Workflow Testing RO-Crate (group B data shard).
- WorkflowHub TRS integration noted in summary; TRS catalog ID deferred until PR-04/PR-07 (empty alternatives, boundary note).

## Unresolved questions

- Public GA4GH conformance test results for individual WES/DRS/TES deployments are not centrally published; status set to `documented-tests` from schema repositories rather than `public-suite`.
- Current WfExS-backend supported workflow engines should be re-verified on next review cycle from repository documentation.

## Conflicts

None.

## v2.1 provenance migration (2026-08-01)

- Migrated workflow records to claim-linked `source_refs`; retained CWL / cwltool `public-suite` via the ConformanceTests page artifact.
- Relationship graph unchanged for non-isolates; evidence-depth queues for GA4GH WES/TES/DRS and openEO remain for issue #30 Batch 1.
