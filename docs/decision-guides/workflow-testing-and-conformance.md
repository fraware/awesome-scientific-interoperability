# Workflow testing and conformance

Compare language conformance suites, workflow test packaging, monitoring services, and what each layer can evidence. Catalog entries: [resource:cwl-conformance-tests], [resource:common-workflow-language-cwl], [resource:cwltool], [resource:workflow-testing-ro-crate], [resource:lifemonitor], [resource:workflowhub], [resource:workflow-ro-crate].

**Primary sources inspected:** [CWL v1.2 Conformance Tests](https://www.commonwl.org/v1.2/ConformanceTests.html), [cwl-v1.2 test repository](https://github.com/common-workflow-language/cwl-v1.2), [Workflow Testing RO-Crate](https://w3id.org/ro/wftest), [LifeMonitor documentation](https://lifemonitor.eu/), [WorkflowHub testing integration](https://workflowhub.eu/).

## What conformance can and cannot show

| Evidence type | Demonstrates | Does not demonstrate |
|---------------|--------------|----------------------|
| [resource:cwl-conformance-tests] runner results | Parser/runner behavior against normative CWL requirements for tested versions | Scientific correctness of domain workflows; equivalence across optional features not covered by tests |
| [resource:workflow-testing-ro-crate] structural validation | Portable test artifact packaging | That all registries or monitors implement every profile extension |
| [resource:lifemonitor] execution reports | Scheduled test runs for registered workflows in supported configurations | Universal workflow-language coverage; WES/TES API conformance |
| Registry integration tests ([resource:workflowhub]) | Publication and metadata exchange paths | Full stack reproducibility or authorization correctness |

Workflow language conformance, API interoperability, backend portability, and scientific-result equivalence remain distinct layers (see [Workflows and execution](workflows-and-execution.md)).

## Comparison

| Dimension | [resource:cwl-conformance-tests] | [resource:workflow-testing-ro-crate] | [resource:lifemonitor] |
|-----------|----------------------------------|--------------------------------------|------------------------|
| **Object under test** | CWL documents and runner behavior | Workflow test suites, inputs, expected outputs, services | Registered workflows' tests over time |
| **Scope** | Language and reference runner contract | Cross-registry portable test packaging | Operational monitoring of workflow tests |
| **Public suite / validator** | Public suite in catalog | Documented profile tests; no standalone public suite | No public conformance suite catalogued |
| **Typical consumer** | Engine maintainers, CI for CWL runners | Registry authors, CI authors, monitoring integrators | Workflow authors via [resource:workflowhub] |
| **Coupling to language** | CWL-specific | Workflow-language agnostic at packaging layer; tests embed engine-specific assets | Supports multiple languages via registered workflows |
| **Strongest use case** | Prove runner compatibility with CWL spec versions | Exchange test definitions between registries and monitors | Continuous regression detection for published workflows |
| **Inappropriate use case** | Substitute for domain scientific validation | Prove WES service conformance | Single source of truth for language specification compliance |

## Where public conformance evidence exists

| Area | Public evidence | Gap |
|------|-----------------|-----|
| CWL runner behavior | [resource:cwl-conformance-tests] with [resource:cwltool] reference path | Optional features and deployment-specific behavior may differ among runners |
| WDL cross-engine behavior | Not catalogued as public suite | Compare engine documentation and project-specific tests |
| WES/TES services | Documented tests on schemas; service-specific reports vary | No single catalogued cross-vendor WES certification program |
| Workflow test portability | [resource:workflow-testing-ro-crate] profile plus [resource:lifemonitor] demos | Full independent validator ecosystem still consolidating |
| Scientific outputs | Domain test suites (outside this guide's scope) | Language/API conformance alone |

## Architecture case: portable continuous workflow tests

1. Author workflow and tests; package with [resource:workflow-ro-crate] including a [resource:workflow-testing-ro-crate] profile.
2. Register in [resource:workflowhub] so TRS consumers and monitors discover the test definition.
3. Configure [resource:lifemonitor] to schedule test runs and surface failures to authors.
4. When changing runners, re-run [resource:cwl-conformance-tests] (for CWL) separately from LifeMonitor scientific tests.

**Category errors:**

- Passing CWL conformance while assuming untested workflow idioms (custom extensions, exotic containers) are portable.
- Treating LifeMonitor green status as authorization to access controlled workflow inputs.
- Using workflow test crates without specifying which engine and container environment the expected outputs assume.

## Decision paths

- **Validate a CWL runner before production:** Run [resource:cwl-conformance-tests]; publish results with engine version pins.
- **Share tests between registries:** Prefer [resource:workflow-testing-ro-crate] over ad hoc JSON or proprietary CI configs.
- **Monitor published workflows continuously:** Integrate [resource:lifemonitor] with [resource:workflowhub]; document language and resource requirements in the crate.
- **Compare WDL engines:** No catalogued public suite—document engine-specific test evidence explicitly rather than inferring from CWL results.

## Example architecture

A CWL workflow ships with conformance-tested [resource:cwltool] in CI ([resource:cwl-conformance-tests]). Authors embed regression tests in a [resource:workflow-testing-ro-crate], register on [resource:workflowhub], and enable [resource:lifemonitor] scheduling. Failures trigger investigation of runner upgrades separately from WES client changes, preserving separation between language conformance and operational monitoring.
