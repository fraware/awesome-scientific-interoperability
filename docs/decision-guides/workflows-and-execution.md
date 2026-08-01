# Workflows and execution

Compare workflow languages, GA4GH execution APIs, registries, and reference backends. Catalog entries: [resource:common-workflow-language-cwl], [resource:workflow-description-language-wdl], [resource:ga4gh-tool-registry-service-trs], [resource:ga4gh-workflow-execution-service-wes], [resource:ga4gh-task-execution-service-tes], [resource:ga4gh-data-repository-service-drs], [resource:workflowhub], [resource:sapporo], [resource:cwltool], [resource:wfexs-backend], [resource:lifemonitor].

**Primary sources inspected:** [Common Workflow Language](https://www.commonwl.org/), [OpenWDL](https://openwdl.org/), [GA4GH TRS](https://www.ga4gh.org/product/tool-registry-service-trs/), [GA4GH WES](https://www.ga4gh.org/product/workflow-execution-service-wes/), [GA4GH TES](https://www.ga4gh.org/product/task-execution-service-tes/), [GA4GH DRS](https://www.ga4gh.org/product/data-repository-service-drs/), [WorkflowHub](https://workflowhub.eu/), [Sapporo](https://github.com/sapporo-wes/sapporo), [cwltool](https://github.com/common-workflow-language/cwltool), [WfExS-backend](https://github.com/inab/WfExS-backend), [LifeMonitor](https://lifemonitor.eu/).

## Separation of concerns

| Layer | What it standardizes | What it does not guarantee |
|-------|---------------------|----------------------------|
| **Language portability** ([resource:common-workflow-language-cwl], [resource:workflow-description-language-wdl]) | Syntax and semantics of workflow definitions across engines | Identical feature support on every engine; bitwise-identical outputs |
| **API interoperability** ([resource:ga4gh-workflow-execution-service-wes], [resource:ga4gh-task-execution-service-tes], [resource:ga4gh-data-repository-service-drs]) | Client/service contracts for runs, tasks, and data access | Scientific equivalence of results; full engine conformance |
| **Backend portability** ([resource:sapporo], [resource:wfexs-backend], [resource:cwltool]) | Concrete execution paths and reference behaviors | Universal coverage of all workflow languages or profiles |
| **Scientific-result equivalence** | Out of scope for any single standard | Requires domain validation, test suites, and explicit assumptions |

Not all WDL or CWL engines support identical language features, container backends, or provenance profiles. WES/TES conformance documented on one service does not transfer to another without evidence.

## Component roles

| Resource | Role | Conformance evidence in catalog |
|----------|------|--------------------------------|
| [resource:common-workflow-language-cwl] | Portable workflow language with public suite | Public suite ([resource:cwl-conformance-tests]) |
| [resource:workflow-description-language-wdl] | Portable workflow language; multiple engines | No public suite catalogued |
| [resource:ga4gh-tool-registry-service-trs] | Discover and fetch workflow/tool descriptors | Documented tests |
| [resource:ga4gh-workflow-execution-service-wes] | Submit and monitor workflow runs via API | Documented tests |
| [resource:ga4gh-task-execution-service-tes] | Execute individual tasks decoupled from orchestration | Documented tests |
| [resource:ga4gh-data-repository-service-drs] | Resolve data objects across repositories | Documented tests |
| [resource:workflowhub] | FAIR workflow registry (RO-Crate, TRS, Bioschemas) | Documented tests |
| [resource:sapporo] | Reference WES across CWL, WDL, Nextflow, Snakemake | Documented tests; single-known implementation |
| [resource:cwltool] | Reference CWL runner linked to conformance suite | Public suite |
| [resource:wfexs-backend] | Multi-engine backend with RO-Crate run packaging | Interoperability demo; no public suite |
| [resource:lifemonitor] | Continuous workflow test monitoring | Reference service; no public suite |

## Architecture cases

### 1. Publish a workflow and make it discoverable

Package the definition with [resource:workflow-ro-crate] and register in [resource:workflowhub]. Expose discovery through [resource:ga4gh-tool-registry-service-trs] and Bioschemas metadata. **Category error:** treating registry metadata as proof that any WES service can execute the workflow without engine-specific validation.

### 2. Submit the same workflow through a standard execution API

Clients call [resource:ga4gh-workflow-execution-service-wes] (for example via [resource:sapporo]). The service maps WES requests to [resource:common-workflow-language-cwl] or [resource:workflow-description-language-wdl] runners. **Category error:** assuming WES endpoint availability implies language feature parity across backends.

### 3. Separate orchestration from task execution

Workflow engines orchestrate steps; [resource:ga4gh-task-execution-service-tes] executes individual containerized tasks on diverse compute. WES covers workflow-run lifecycle; TES covers task dispatch. **Category error:** using TES alone without a workflow orchestration layer when multi-step control flow is required.

### 4. Resolve data across repositories

Workflow inputs reference [resource:ga4gh-data-repository-service-drs] objects so engines fetch bytes consistently across clouds and repositories. Authorization for controlled data remains outside DRS (see [Controlled data access](controlled-data-access.md)). **Category error:** treating DRS URIs as semantic metadata or license grants.

### 5. Package a workflow run and provenance

After execution, export [resource:workflow-run-ro-crate] or [resource:cwlprov] via backends such as [resource:wfexs-backend] or [resource:cwltool]. Packaging conformance does not prove reproducibility (see [Provenance and execution evidence](provenance-and-execution-evidence.md)). **Category error:** equating a valid run crate with identical scientific outputs on rerun.

### 6. Define and continuously execute portable workflow tests

Describe tests with [resource:workflow-testing-ro-crate]; monitor through [resource:lifemonitor] integrated with [resource:workflowhub]. **Category error:** conflating LifeMonitor monitoring with general workflow registry or WES execution responsibilities.

## Language comparison (selected dimensions)

| Dimension | [resource:common-workflow-language-cwl] | [resource:workflow-description-language-wdl] |
|-----------|----------------------------------------|---------------------------------------------|
| **Primary artifact** | Command-line tool and workflow descriptions | Task and workflow definitions for data pipelines |
| **Conformance infrastructure** | Public [resource:cwl-conformance-tests] tied to spec versions | No catalogued public cross-engine suite |
| **Typical execution path** | [resource:cwltool] and other runners; WES via adapters | Cromwell, miniwdl, etc.; WES via [resource:sapporo] among others |
| **Strongest use case** | Cross-institution portable tools/workflows with test evidence | Genomics and cloud pipeline communities with WDL tooling |
| **Inappropriate assumption** | Every runner passes all optional CWL v1.2 features | WDL portability implies identical behavior across all engines |

## Decision paths

- **Need tested cross-engine CWL portability:** Start with [resource:common-workflow-language-cwl] and validate runners against [resource:cwl-conformance-tests].
- **Need a standard client/server execution contract:** Implement [resource:ga4gh-workflow-execution-service-wes]; evaluate [resource:sapporo] as a reference multi-language service.
- **Need compute-backend independence for tasks:** Introduce [resource:ga4gh-task-execution-service-tes] behind the orchestrator.
- **Need federated data access:** Use [resource:ga4gh-data-repository-service-drs] for object resolution; keep authorization separate.
- **Need publication plus community discovery:** Prefer [resource:workflowhub] with Workflow RO-Crate over ad hoc file shares.

## Example architecture

Authors publish a [resource:workflow-ro-crate] to [resource:workflowhub], exposed via TRS. A portal submits runs to a WES endpoint ([resource:sapporo]) that dispatches CWL tasks to a TES backend on cloud VMs. Input BAM files resolve through DRS. The backend emits [resource:workflow-run-ro-crate] to archival storage. [resource:lifemonitor] executes [resource:workflow-testing-ro-crate] tests nightly and reports regressions.
