# Engineering Takeover Specification

**Repository:** `fraware/awesome-scientific-interoperability`  
**Specification status:** Final execution specification  
**Specification date:** 2026-08-01  
**Intended audience:** Maintainers, research engineers, technical editors, and junior contributors taking over implementation  
**Authority:** This document governs the remaining engineering and editorial program. It supersedes the shorter `docs/roadmap.md` whenever the two documents differ.

## 1. Mandate

The team shall turn the current public release into the definitive, actively maintained Awesome list for scientific interoperability. The repository must remain a selective human-curated list. Structured metadata, scripts, reports, and automated checks may strengthen review and discovery, but they must never generate the canonical README, decide whether a resource is included, or replace editorial judgment.

The work shall proceed through small, ordered pull requests. Each pull request must have one primary purpose, a bounded diff, reproducible validation, explicit acceptance criteria, and a rollback path. A pull request that mixes unrelated catalog additions, schema changes, repository settings, and prose restructuring must be split before review.

## 2. North Star

A technically competent user should be able to identify the strongest available interoperability mechanism for a concrete scientific integration problem without conducting a new landscape search.

Every design and editorial decision must be evaluated against this North Star. A change that adds volume without improving a concrete technical decision is outside scope.

## 3. Definition of the complete vision

The complete vision is achieved when all of the following are true.

1. The README remains a concise, manually authored, Awesome-compliant canonical list of exceptional resources.
2. Every main-list entry states what interoperates with what and through which documented mechanism.
3. Every entry has current primary sources, stewardship information, review dates, evidence types, implementation evidence, conformance evidence, domain tags, and explicitly recorded alternatives or boundary notes.
4. A user can navigate the corpus in two ways:
   - by technical layer and resource category through the README;
   - by concrete integration problem through a manually authored problem index and decision guides.
5. The repository distinguishes standards, profiles, implementations, registries, mappings, validators, conformance suites, and reference architectures without conflating popularity with interoperability value.
6. The watchlist is structured, time-bounded, and separate from the main list.
7. CI fails closed on schema violations, README/catalog drift, duplicate identities, stale review dates, invalid cross-references, malformed URLs, release-manifest drift, and Awesome formatting violations.
8. Network link audits produce actionable classifications instead of treating every non-200 response as equivalent.
9. Maintainer roles, conflicts, review requirements, and escalation paths are documented and enforceable.
10. The list has undergone a complete human re-review and at least one public maintenance cycle.
11. The repository has a tagged release with an accurate citation record and changelog.
12. Submission to the central Awesome index occurs only when every current requirement can be answered truthfully, including the human-curation and non-AI-generated requirements. If that statement cannot be made truthfully, the project remains a standalone Awesome list and the team requests clarification from the central maintainers instead of making a false certification.

## 4. Non-goals and immutable invariants

### 4.1 Non-goals

The project is not:

- a comprehensive scientific software directory;
- a certification authority;
- a vendor ranking;
- an automatically generated catalog;
- a general FAIR, reproducibility, or open-science bibliography;
- a benchmark of every implementation;
- a hosted interoperability testing service;
- a marketing channel for affiliated projects;
- an excuse to add every technically important general-purpose standard.

### 4.2 Immutable invariants

The following invariants apply to every pull request.

1. `README.md` is manually edited and authoritative.
2. The structured catalog validates and supports the README; it does not generate it.
3. Main-list inclusion is an editorial decision made by accountable humans.
4. A resource must pass the sentence test: **Resource enables X to exchange, interpret, execute, preserve, or compose with Y through documented mechanism Z.**
5. General importance, citation count, institutional prestige, and popularity are insufficient admission arguments.
6. Affiliated contributors cannot be the sole approvers of affected resources.
7. Deprecated, archived, superseded, inaccessible, or materially undocumented resources do not remain in the main list.
8. Every catalog change and every tracked-file change must be reflected in `MANIFEST.json` before merge.
9. CI must be green on the exact PR head. A previously green ancestor is insufficient.
10. No pull request may weaken validation merely to make a failing change pass.

## 5. Verified baseline at takeover

The starting state is the public `main` branch after merged PR #1, commit `572ded4420eeb66b0769b4235a8aa334365c9418`.

The verified baseline contains:

- 75 README entries;
- 75 structured catalog records;
- 11 section-scoped catalog shards;
- 44 tracked release files in the integrity manifest;
- JSON Schema validation;
- README/catalog parity checks;
- duplicate identifier, name, and URL checks;
- editorial description checks;
- offline HTTPS syntax checks;
- four unit tests;
- deterministic manifest generation and verification;
- Awesome lint with one temporary exclusion for repository metadata that cannot be written by the original publication connector;
- a weekly and manually dispatchable network-link workflow;
- issue forms, pull-request template, project charter, editorial policy, taxonomy, conflict policy, review checklist, maintenance protocol, watchlist, archive, CC0 license, and citation metadata.

Issue #2 records the unresolved settings-level work. Treat every checkbox in that issue as unresolved until independently verified in the GitHub interface.

## 6. Team roles and decision authority

A small team may fill multiple roles, but the responsibilities must remain distinct.

### 6.1 Lead maintainer

The lead maintainer:

- owns scope and final editorial decisions;
- approves schema migrations and taxonomy changes;
- resolves disagreements after documented review;
- confirms central Awesome submission statements;
- signs releases;
- cannot approve an affiliated resource alone.

### 6.2 Catalog engineer

The catalog engineer:

- maintains schemas, loaders, validators, query tools, tests, and manifests;
- ensures migrations are deterministic and reversible;
- does not decide inclusion based on automated scores.

### 6.3 Section reviewer

A section reviewer:

- inspects primary technical sources;
- verifies descriptions, mechanisms, stewardship, alternatives, and evidence;
- records review dates and limitations;
- has authority to request removal, deferral, or watchlist placement.

### 6.4 Release reviewer

The release reviewer:

- runs the complete validation matrix on the exact head commit;
- verifies manifest integrity;
- checks workflow results and network-audit classifications;
- confirms that release and citation metadata match.

### 6.5 Junior contributor

A junior contributor may research, propose, implement, and test changes. A junior contributor must not self-approve a resource addition, schema migration, removal, or taxonomy change.

## 7. Standard pull-request protocol

Every pull request must follow this protocol.

### 7.1 Branch names

Use lowercase, hyphenated names with the specification PR identifier:

```text
pr-01-native-awesome-compliance
pr-04-catalog-migration-a
pr-12-laboratory-agent-guides
```

### 7.2 Commit discipline

- Keep commits logically separable.
- Do not commit generated caches, virtual environments, `node_modules`, or temporary reports.
- Regenerate `MANIFEST.json` as the final content commit.
- Do not amend or force-push after review has started unless the reviewer explicitly requests history cleanup.

### 7.3 Required PR body

Every PR body must contain:

1. **Objective** — one sentence stating the primary purpose.
2. **North-Star effect** — the concrete user decision improved by the change.
3. **Files changed** — grouped by function.
4. **Primary sources inspected** — required for editorial or resource changes.
5. **Migration and compatibility** — required for schema, file-layout, or CLI changes.
6. **Validation evidence** — exact commands and CI results.
7. **Conflict disclosure** — “None” is acceptable.
8. **Rollback** — how to revert without corrupting the catalog.
9. **Out-of-scope items** — explicit work deferred to later PRs.

### 7.4 Mandatory local commands

Run from the repository root:

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_catalog.py
python scripts/check_links.py --offline
python -m unittest discover -s tests -v
python scripts/generate_manifest.py
python scripts/verify_manifest.py
```

After PR-01, also run the unmodified standard linter:

```bash
npx --yes awesome-lint
```

Before committing, rerun `python scripts/generate_manifest.py` after every tracked-file modification, then rerun `python scripts/verify_manifest.py`.

### 7.5 Merge requirements

A PR may merge only when:

- all required CI jobs pass on the exact head SHA;
- README/catalog parity remains exact when applicable;
- manifest verification passes;
- no unresolved review thread concerns correctness, scope, conflict, or evidence;
- an independent approver has reviewed any affiliated resource;
- the PR contains no unexplained generated output;
- the lead maintainer confirms that the change advances the North Star.

Use squash merge unless preserving a multi-commit migration history materially improves auditability. The squash title must describe the completed result, not the implementation activity.

## 8. Ordered PR execution program

The PRs below are the authoritative sequence. A later PR may start in parallel only when its prerequisites are satisfied and it does not edit the same files as an earlier open PR.

---

## PR-01 — Close repository-settings debt and restore native Awesome lint

### Objective

Complete the settings work in issue #2 and remove the temporary Awesome-lint metadata-rule exception.

### Preconditions

- Confirm the live `main` branch is at or ahead of the takeover baseline.
- Inspect issue #2 in the GitHub interface.
- Confirm no unrelated PR edits `.github/workflows/quality.yml`, `Makefile`, or `scripts/run_awesome_lint.mjs`.

### Manual GitHub settings

1. Set the repository description exactly to:

   ```text
   Standards and tools that make scientific data, software, workflows, instruments, knowledge systems, and agents work together.
   ```

2. Add topics:

   ```text
   awesome
   awesome-list
   scientific-interoperability
   research-infrastructure
   open-science
   ```

3. Create optional triage labels `candidate` and `correction` only after confirming the issue forms work without them.
4. Delete the merged `agent/launch-hardening` branch.
5. Configure branch protection after the required checks appear on `main`:
   - require pull requests;
   - require `catalog` and `awesome-lint` status checks;
   - dismiss stale approvals when new commits are pushed;
   - require conversation resolution;
   - prohibit force pushes and branch deletion;
   - allow administrators to bypass only for repository recovery.

### Code changes

- Delete `scripts/run_awesome_lint.mjs`.
- Change `.github/workflows/quality.yml` to run `npx --yes awesome-lint` directly.
- Change `Makefile` to run `npx --yes awesome-lint` directly.
- Update `docs/publishing.md` and `docs/validation-report.md` to remove the temporary exception.
- Regenerate `MANIFEST.json`.

### Tests

Run all mandatory commands. Confirm the standard linter passes with the live repository metadata.

### Acceptance criteria

- No custom Awesome-lint rule filter remains.
- The live repository description and topics satisfy the current central Awesome requirement.
- Branch protection is visible and requires both CI jobs.
- CI is green on the exact PR head.
- Issue #2 is updated or closed only after every completed item is checked.

### Rollback

Revert only the code commit if standard lint unexpectedly regresses. Do not remove correct repository metadata or branch protection.

---

## PR-02 — Execute the first network audit and harden link classification

### Objective

Convert the network-link workflow from a binary URL probe into an auditable classification system that distinguishes genuine breakage from access-policy and transient failures.

### Preconditions

- PR-01 merged.
- Run **Actions → Links → Run workflow** on `main` and download or copy the complete log.

### Required design

Create `config/link-policy.yaml` with explicit policy fields:

```yaml
version: 1
accepted_redirect_hops: 5
transient_statuses: [408, 425, 429, 500, 502, 503, 504]
access_policy_statuses: [401, 403]
permanent_failure_statuses: [404, 410]
user_agent: awesome-scientific-interoperability-link-audit/1.0
retries: 2
backoff_seconds: 2
```

The checker must classify each result as one of:

- `ok`;
- `redirected`;
- `access-policy`;
- `transient-failure`;
- `permanent-failure`;
- `tls-or-dns-failure`;
- `invalid-url`.

### Files

- Add `config/link-policy.yaml`.
- Refactor `scripts/check_links.py` to:
  - load the policy;
  - preserve final URL and redirect chain;
  - record HTTP status or transport error;
  - retry only transient failures;
  - exit nonzero only for invalid URLs and unresolved permanent failures;
  - support `--json-report PATH` and `--markdown-report PATH`;
  - keep `--offline` deterministic and network-free.
- Add `tests/test_links.py` using mocks; tests must not access the public network.
- Add `docs/link-audit-baseline.md` summarizing the first live audit and every accepted exception.
- Update `.github/workflows/links.yml` to upload JSON and Markdown reports as workflow artifacts.
- Update `docs/maintenance-protocol.md` with remediation rules.
- Regenerate the manifest.

### Editorial remediation

For each failed URL:

1. Inspect the project’s official site, specification repository, and redirect destination.
2. Replace a URL only when the new target is more canonical or the old target is permanently broken.
3. Preserve a valid canonical URL that returns 401, 403, or 429 when the response is an access policy or rate limit.
4. Record persistent exceptions in the baseline document; do not add a silent allowlist entry without rationale.

### Acceptance criteria

- Every current main-list URL has a recorded classification.
- No unresolved 404, 410, invalid URL, or TLS/DNS failure remains.
- Tests cover redirects, 403, 429, 404, retry exhaustion, and malformed URLs.
- Workflow artifacts are downloadable.
- Offline validation remains deterministic.

---

## PR-03 — Specify catalog model v2 and staged migration rules

### Objective

Define a more rigorous catalog model that separates maturity from evidence and records the information required for defensible human curation.

### Rationale

The current `evidence_level` values are underspecified and mix standards maturity, implementation status, and testing evidence. The next model must represent those dimensions independently.

### Files

- Add `schema/catalog.schema.v2.json`.
- Add `docs/catalog-model-v2.md`.
- Add `scripts/validate_catalog_v2.py` or extend the existing validator with `--schema-version 2`.
- Add v2 fixtures under `tests/fixtures/`.
- Add unit tests for valid and invalid records.
- Do not modify the 75 live records in this PR.

### Final v2 resource fields

Every resource must ultimately contain:

```yaml
id: stable-lowercase-slug
name: Canonical name
url: https://canonical-technical-url
section: Existing taxonomy section
resource_type: Human-readable resource class
interoperability_layers:
  - Syntactic
connects:
  - First object or system class
  - Second object or system class
mechanism: Precise documented contract
summary: Objective README-compatible sentence
maturity: established | maintained | emerging
evidence_types:
  - normative-specification
  - reference-implementation
  - independent-implementation
  - institutional-adoption
  - conformance-suite
  - public-validator
  - interoperability-demonstration
implementation_status: multiple-independent | reference-and-others | single-known | not-applicable | unknown
conformance_status: public-suite | public-validator | documented-tests | none-known | not-applicable
stewardship:
  name: Stewarding body
  type: standards-body | consortium | foundation | institution | community | vendor-led
  url: https://stewardship-source
domains:
  - cross-domain
source_urls:
  - https://primary-specification-or-official-source
alternatives:
  - existing-resource-id
related_resource_ids:
  - existing-resource-id
decision_basis: Why this belongs among the strongest current options
boundary_note: Limitation, scope edge, or closest alternative
reviewed_on: YYYY-MM-DD
review_due_on: YYYY-MM-DD
primary_source_inspected: true
```

### Model rules

- `summary` must exactly equal the README description for a main-list entry.
- `source_urls` must contain at least one official specification, standards-body page, maintained repository, or authoritative project documentation page.
- `alternatives` and `related_resource_ids` reference catalog IDs and may be empty arrays.
- `review_due_on` must be later than `reviewed_on`.
- Established and maintained resources have a maximum review interval of 365 days.
- Emerging laboratory and agent resources have a maximum review interval of 183 days.
- `implementation_status: multiple-independent` requires at least two independent implementations documented in `source_urls` or a later review record.
- `conformance_status: public-suite` or `public-validator` requires a source URL for the relevant artifact.
- `maturity` is not a quality score. It records lifecycle state.
- `evidence_types` are factual signals, not an automated inclusion score.

### Compatibility

The v2 validator must coexist with the live v1 validator until PR-07. No live record may fail because v2 is introduced.

### Acceptance criteria

- The v2 schema rejects missing stewardship, sources, review dates, invalid cross-reference formats, and contradictory evidence states.
- At least twelve fixture cases cover positive and negative behavior.
- Documentation includes a field-by-field migration guide.
- The README and live catalog remain unchanged.

---

## PR-04 — Migrate catalog group A to v2-compatible records

### Objective

Human-review and migrate the first 28 entries: Foundations, Identifiers and Discovery, and Metadata and Semantics.

### Required sections and expected counts

- Foundations: 4
- Identifiers and Discovery: 10
- Metadata and Semantics: 14

### Work per resource

For every entry:

1. Open the canonical URL.
2. Inspect at least one primary technical source.
3. Confirm the current canonical name and URL.
4. Identify the steward and governance type.
5. Record at least one domain.
6. Record implementation and conformance status without inference beyond sources.
7. Record evidence types.
8. Identify the strongest existing alternative or leave an empty array with a boundary explanation.
9. Rewrite `decision_basis` and `boundary_note` where they are generic.
10. Set `reviewed_on` to the actual review date and calculate `review_due_on` under the v2 rules.
11. Preserve the README description unless a factual or editorial correction is necessary; any correction must be made in README and catalog together.

### Files

- Update the three relevant catalog shards.
- Add section review notes under:
  - `docs/reviews/foundations.md`
  - `docs/reviews/identifiers-and-discovery.md`
  - `docs/reviews/metadata-and-semantics.md`
- Review notes must list sources inspected, changes made, unresolved questions, and conflicts.
- Extend tests as necessary.
- Regenerate the manifest.

### Acceptance criteria

- All 28 records pass the v2 validator.
- No source is a search-results page, AI summary, promotional landing page without technical documentation, or unsourced secondary list.
- At least one independent reviewer samples five records from each section and confirms the fields against sources.
- README/catalog parity remains exact.

---

## PR-05 — Migrate catalog group B to v2-compatible records

### Objective

Human-review and migrate 27 entries: Data and Digital Objects, Research Software and Environments, Workflows and Execution, and Provenance and Evidence.

### Expected counts

- Data and Digital Objects: 7
- Research Software and Environments: 5
- Workflows and Execution: 10
- Provenance and Evidence: 5

### Special review requirements

- Distinguish packaging from provenance.
- Distinguish workflow languages from execution APIs and reference implementations.
- Confirm whether implementations are genuinely independent.
- Confirm conformance claims through public suites, validators, or official results.
- Record relationships among RO-Crate profiles, CWLProv, W3C PROV, WES, TES, DRS, TRS, and representative implementations through catalog IDs.
- Do not imply that passing syntactic conformance establishes semantic equivalence or end-to-end interoperability.

### Files

Update the four shards and add four section review notes under `docs/reviews/`.

### Acceptance criteria

- All 27 records pass v2 validation.
- Every claimed public validator or conformance suite has a direct source.
- The review explicitly checks representative-implementation limits.
- README/catalog parity remains exact.

---

## PR-06 — Migrate catalog group C to v2-compatible records

### Objective

Human-review and migrate 20 entries: Knowledge Systems and Publications, Instruments and Laboratories, Agents, Access, and Policy, and Validation and Conformance.

### Expected counts

- Knowledge Systems and Publications: 5
- Instruments and Laboratories: 7
- Agents, Access, and Policy: 4
- Validation and Conformance: 4

### Special review requirements

- Recheck every fast-moving agent specification against the current published version.
- Distinguish laboratory procedure languages, device communication, analytical-data exchange, terminologies, and clinical exchange.
- Record vendor or consortium access conditions accurately.
- Confirm that validation resources test a documented contract and do not merely score general FAIRness or software quality.
- Apply a six-month review interval to emerging agent and laboratory resources.

### Files

Update the four shards and add four section review notes.

### Acceptance criteria

- All 20 records pass v2 validation.
- Agent and laboratory claims have current primary sources.
- Conflicts are disclosed for any reviewer affiliated with a listed project.
- README/catalog parity remains exact.

---

## PR-07 — Cut over to catalog v2 and enforce review freshness

### Objective

Make v2 the only supported catalog model and fail CI on stale or incomplete records.

### Files

- Replace `schema/catalog.schema.json` with the final v2 schema.
- Remove `schema/catalog.schema.v2.json` after copying its finalized content.
- Update `catalog/resources.yaml` to `catalog_version: 2.0.0`.
- Remove legacy fields:
  - `evidence_level`;
  - `maintenance_signal`;
  - `north_star_utility`.
- Rename `description` to `summary` throughout shards and validator code.
- Update `scripts/validate_catalog.py` to:
  - enforce v2 schema;
  - validate all catalog ID cross-references;
  - reject self-references;
  - reject unknown domains only if a controlled-domain registry is later adopted; initially domains remain normalized lowercase strings;
  - fail when `review_due_on` precedes the current date;
  - validate review-interval limits;
  - require evidence-source consistency.
- Add `scripts/check_review_freshness.py` with `--as-of YYYY-MM-DD` for deterministic tests.
- Update tests, contributing guide, issue form, PR template, editorial policy, review checklist, and maintenance protocol.
- Remove temporary v2 migration code.
- Regenerate the manifest.

### Acceptance criteria

- All 75 records pass the v2 schema.
- A fixture with an expired review date fails.
- Every `alternatives` and `related_resource_ids` value resolves.
- No legacy field remains in any shard.
- CI has no compatibility mode.

---

## PR-08 — Add a catalog query tool for concrete integration questions

### Objective

Allow maintainers and users to interrogate the structured catalog without changing the README’s canonical role.

### Files

- Add `scripts/query_catalog.py`.
- Add `tests/test_query_catalog.py`.
- Add `docs/querying-the-catalog.md`.
- Add Make targets `query` and `query-json`.
- Regenerate the manifest.

### Required CLI

```bash
python scripts/query_catalog.py --section "Workflows and Execution"
python scripts/query_catalog.py --layer Operational
python scripts/query_catalog.py --domain genomics
python scripts/query_catalog.py --connects workflow repository
python scripts/query_catalog.py --evidence conformance-suite
python scripts/query_catalog.py --id ro-crate
python scripts/query_catalog.py --format json
```

### Behavior

- Multiple filters use logical AND.
- `--connects` performs normalized token matching over `connects`, `mechanism`, and `summary`.
- Default output is stable Markdown ordered by section then canonical name.
- JSON output is deterministic and machine-readable.
- The command never ranks resources automatically.
- The command never writes to README or catalog files.
- No network access is required.

### Acceptance criteria

- Tests cover every filter, combined filters, no-result behavior, JSON stability, and invalid inputs.
- Output includes boundary notes and alternatives so users understand scope.
- Documentation includes at least eight real integration queries.

---

## PR-09 — Publish the integration-problem index

### Objective

Create the primary problem-oriented navigation layer required by the North Star.

### Files

- Add `docs/integration-problems.md`.
- Add `scripts/validate_problem_index.py`.
- Add `tests/test_problem_index.py`.
- Link the document from the README Footnotes section and `docs/project-charter.md`.
- Regenerate the manifest.

### Required problem classes

The document must include, at minimum:

1. Identify researchers, organizations, samples, software, and research objects.
2. Discover datasets, tools, workflows, and services.
3. Align metadata, terminology, quantities, and units.
4. Package data, software, workflows, and contextual entities.
5. Describe and cite research software and environments.
6. Exchange and execute workflows across engines and backends.
7. Capture provenance, execution evidence, and traceability.
8. Exchange publications, claims, and scholarly links.
9. Integrate instruments, analytical data, and laboratory automation.
10. Expose scientific tools and capabilities to AI agents.
11. Express controlled-data authorization and data-use conditions.
12. Validate conformance and compare independent implementations.

### Required structure per problem

Each problem entry must state:

- the concrete integration situation;
- the recommended starting resource or standard family;
- conditions under which an alternative is stronger;
- limitations and common category errors;
- links by catalog ID to relevant entries;
- a short example architecture.

### Validation

Use explicit resource-ID markers, for example:

```text
[resource:ro-crate]
```

The validator must fail on unknown IDs and duplicate problem identifiers. It must not generate the document.

### Acceptance criteria

- Every main section appears in at least one problem class.
- Every recommendation is traceable to catalog evidence and boundary notes.
- The document does not claim universal winners.
- Two engineers unfamiliar with the repository can answer a supplied set of ten integration questions using the index without performing a new general web search; record the exercise in the PR.

---

## PR-10 — Decision guides for research objects and provenance

### Objective

Provide precise comparison guidance for overlapping packaging and provenance mechanisms.

### Files

Add:

- `docs/decision-guides/research-object-packaging.md`
- `docs/decision-guides/provenance-and-execution-evidence.md`
- `docs/decision-guides/README.md`

### Required comparisons

Research-object packaging guide:

- RO-Crate;
- Workflow RO-Crate;
- Workflow Run RO-Crate;
- Workflow Testing RO-Crate;
- BagIt;
- COMBINE/OMEX Archive;
- FAIR Signposting.

Provenance guide:

- W3C PROV;
- P-Plan;
- CWLProv;
- Workflow Run RO-Crate;
- ISO 23494-2;
- runcrate.

### Required comparison dimensions

- object represented;
- prospective versus retrospective information;
- packaging versus graph model;
- serialization;
- profile or extension relationship;
- implementation support;
- validator or conformance support;
- portability assumptions;
- limitations;
- strongest use case;
- inappropriate use case.

### Acceptance criteria

- Every technical claim cites a primary source through Markdown links.
- No table cell uses unqualified “yes/no” where scope matters.
- The guide states explicitly that packaging conformance does not prove reproducibility or semantic equivalence.
- Catalog IDs are validated.

---

## PR-11 — Decision guides for workflows, execution, and testing

### Objective

Clarify how workflow languages, registries, execution APIs, runners, test descriptions, and monitoring services compose.

### Files

Add:

- `docs/decision-guides/workflows-and-execution.md`
- `docs/decision-guides/workflow-testing-and-conformance.md`

### Required resources

- CWL;
- WDL;
- TRS;
- WES;
- TES;
- DRS;
- WorkflowHub;
- Sapporo;
- cwltool;
- WfExS-backend;
- LifeMonitor;
- CWL Conformance Tests.

### Required architecture cases

1. Publish a workflow and make it discoverable.
2. Submit the same workflow through a standard execution API.
3. Separate orchestration from task execution.
4. Resolve data across repositories.
5. Package a workflow run and provenance.
6. Define and continuously execute portable workflow tests.

### Acceptance criteria

- The guide separates language portability, API interoperability, backend portability, and scientific-result equivalence.
- It does not imply that all WDL or CWL engines support identical features.
- It identifies where public conformance evidence exists and where it does not.

---

## PR-12 — Decision guides for identifiers, semantics, and discovery

### Objective

Help users choose identity, catalog, vocabulary, unit, and semantic-profile mechanisms.

### Files

Add:

- `docs/decision-guides/identifiers-and-discovery.md`
- `docs/decision-guides/metadata-semantics-and-units.md`

### Required comparisons

- ORCID, ROR, IGSN, DOI/DataCite, Crossref, Identifiers.org;
- Service Info, Service Registry, TRS, FAIRsharing;
- Schema.org, Bioschemas, DCAT, SKOS, OBO Foundry, EDAM, SOSA/SSN;
- QUDT and UCUM;
- STAC, CF Conventions, Darwin Core, DDI Lifecycle, Croissant.

### Acceptance criteria

- Identifier scope and object type are explicit.
- QUDT and UCUM are described as complementary where appropriate.
- General vocabularies are connected to their scientific profiles.
- Discovery registries are distinguished from identifiers and metadata standards.

---

## PR-13 — Decision guides for laboratories, agents, and controlled access

### Objective

Clarify rapidly evolving operational interfaces at the physical and agentic boundaries.

### Files

Add:

- `docs/decision-guides/laboratory-interoperability.md`
- `docs/decision-guides/scientific-agents-and-tool-interfaces.md`
- `docs/decision-guides/controlled-data-access.md`

### Required comparisons

Laboratories:

- SiLA 2;
- OPC UA LADS;
- Autoprotocol;
- AnIML;
- Allotrope Data Format;
- FHIR;
- LOINC.

Agents:

- MCP;
- ToolUniverse;
- current watchlist candidates including A2A, IEEE P3971, Science Context Protocol, and SciToolAgent.

Access:

- GA4GH Passports;
- Data Use Ontology;
- watchlist candidates ODRL and Five Safes RO-Crate.

### Required cautions

- Device communication does not standardize experimental semantics.
- Procedure representation does not establish device compatibility.
- Agent-tool invocation does not establish scientific validity, authorization, provenance, or safe physical execution.
- Identity, authorization, and data-use policy are separate layers.
- Emerging resources must be identified as emerging and reviewed against current versions.

### Acceptance criteria

- Every emerging-resource statement includes an as-of date.
- The guide does not promote an unimplemented standards project as a production choice.
- Physical-world approval, authority, reversibility, evidence, and point-of-no-return concerns are explicitly identified as integration requirements outside generic tool invocation.

---

## PR-14 — Structure the watchlist and candidate lifecycle

### Objective

Turn the prose watchlist into a disciplined, reviewable queue without converting it into a second main list.

### Files

- Add `catalog/watchlist.yaml`.
- Add `schema/watchlist.schema.json`.
- Add `scripts/validate_watchlist.py`.
- Add tests.
- Update `docs/watchlist.md` manually to match the structured records.
- Update issue forms and contribution guidance.
- Regenerate the manifest.

### Required watchlist fields

```yaml
id: stable-slug
name: Canonical name
url: https://canonical-url
candidate_section: Existing or conditional section
status: monitor | needs-evidence | needs-boundary-decision | superseded | rejected
reason: Why the main-list bar is not yet met
missing_evidence:
  - concrete missing signal
reviewed_on: YYYY-MM-DD
review_due_on: YYYY-MM-DD
promotion_conditions:
  - objective condition
rejection_conditions:
  - objective condition
source_urls:
  - https://primary-source
```

### Lifecycle rules

- Watchlist status is neither endorsement nor rejection.
- Every item has a review deadline.
- An expired item must be reviewed, removed, or explicitly renewed with new evidence.
- Promotion requires a dedicated resource-addition PR.
- Rejection requires a reason and may be retained in source notes to prevent repeated work.
- The watchlist does not appear in the README Contents.

### Acceptance criteria

- Every current prose watchlist item is represented.
- Prose and YAML parity are validated.
- No watchlist item is counted in the 75 main-list records.
- CI fails on expired review dates and unknown candidate sections.

---

## PR-15 — Add coverage and concentration auditing

### Objective

Measure corpus balance and reveal gaps without using metrics to automate inclusion.

### Files

- Add `scripts/audit_coverage.py`.
- Add `tests/test_coverage_audit.py`.
- Add `docs/coverage-baseline.md`.
- Add a non-blocking CI artifact initially; make only invariant breaches blocking.
- Regenerate the manifest.

### Required metrics

- entries per section;
- domains per entry and entries per domain;
- interoperability layers;
- resource types;
- maturity states;
- evidence types;
- implementation and conformance status;
- stewardship types;
- review dates and upcoming deadlines;
- number of implementations per standard family;
- proportion of general-purpose substrates;
- proportion of entries from any single scientific domain.

### Guardrails

The audit must flag, but not automatically reject:

- a section with fewer than three main-list entries;
- a single domain exceeding 30 percent of entries;
- general-purpose substrates exceeding 10 percent;
- more than two implementation entries for one standard family without documented justification;
- entries with no alternatives or related-resource links after v2 migration;
- evidence claims with no source URL.

Only hard data-integrity failures block CI. Editorial concentration warnings appear in the report and require maintainer acknowledgment.

### Acceptance criteria

- Baseline metrics are reproducible from the catalog.
- The report identifies concrete underserved domains and mechanisms.
- No automatic score is described as “quality” or used to add/remove entries.

---

## PR-16A — Evaluate statistical and social-science interoperability gaps

### Objective

Review high-value candidates for statistical and social-science data exchange.

### Mandatory candidate set

At minimum evaluate:

- SDMX;
- DDI Cross Domain Integration where technically mature and publicly specified;
- relevant controlled vocabulary or data-cube profiles not already subsumed by stronger entries.

### Process

- Produce `docs/candidate-reviews/statistical-and-social-science.md`.
- For each candidate, complete the sentence test, compare with DDI Lifecycle and DCAT, inspect primary sources, assess governance and implementations, and return `include`, `watchlist`, or `exclude`.
- Add no more than three resources in this PR.
- Every inclusion updates README, the relevant shard, problem index, relevant decision guide, coverage baseline, tests, and manifest.
- Every non-inclusion updates the structured watchlist or source notes with a precise reason.

### Acceptance criteria

The PR is complete even if zero resources qualify, provided the review is rigorous and reusable.

---

## PR-16B — Evaluate physical-science and engineering interoperability gaps

### Objective

Address the current underrepresentation of physical-science and engineering exchange mechanisms.

### Mandatory candidate set

At minimum evaluate:

- Functional Mock-up Interface (FMI) for model exchange and co-simulation;
- Crystallographic Information Framework (CIF);
- NeXus for neutron, X-ray, and muon data;
- a current materials-data interoperability standard or profile with public technical documentation;
- scientific HDF5 profiles only when the profile, not generic HDF5, supplies the interoperability contract.

### Process and acceptance

Use the same rules as PR-16A. Add no more than four resources. Explicitly distinguish general data containers from scientific profiles.

---

## PR-16C — Evaluate geospatial and environmental interoperability gaps

### Objective

Review operational geospatial and environmental interfaces beyond metadata-only exchange.

### Mandatory candidate set

At minimum evaluate:

- current OGC API standards relevant to features, records, coverages, or processes;
- OGC SensorThings API;
- relevant Earth-observation or environmental profiles that complement STAC, SOSA/SSN, and CF Conventions.

### Acceptance criteria

- Avoid listing an umbrella family when one or two specific standards answer the integration question more clearly.
- Record the relationship to STAC, DCAT, SOSA/SSN, and CF.
- Add no more than four resources.

---

## PR-16D — Evaluate experimental and biomedical research-object gaps

### Objective

Review mechanisms for describing experiments, analyses, and regulated computational records.

### Mandatory candidate set

At minimum evaluate:

- ISA-Tab/ISA-JSON or the current ISA model specifications;
- BioCompute Objects;
- DICOM or a narrower imaging-interoperability profile when justified;
- current research-object or provenance profiles not already subsumed by RO-Crate and existing entries.

### Acceptance criteria

- Clinical exchange standards must be included only when their scientific or laboratory integration role is explicit.
- Avoid duplicate coverage of FHIR, LOINC, RO-Crate, and provenance profiles.
- Add no more than four resources.

---

## PR-17 — Reassess taxonomy and conditionally split combined sections

### Objective

Determine whether the corpus now supports separate `Scientific Agents and Automation` and `Identity, Access, and Policy` sections.

### Decision rule

Split `Agents, Access, and Policy` only when both proposed sections contain at least three strong main-list entries and each section answers a distinct recurring integration problem. Do not add weak entries merely to satisfy the threshold.

### If the split qualifies

- Update README headings and Contents.
- Update `docs/taxonomy.md`.
- Update catalog index and split the shard.
- Update schema section enums.
- Update issue forms, problem index, decision guides, tests, coverage baseline, and manifest.
- Preserve stable resource IDs.

### If the split does not qualify

- Add a dated decision record to `docs/taxonomy.md` explaining why the combined section remains.
- Identify the evidence required for future reassessment.

### Additional taxonomy review

Evaluate whether `Foundations` remains sufficiently selective and whether any broad platform entry belongs under `Reference Architectures`. Create a new section only if it contains at least three exceptional entries and improves user decisions.

### Acceptance criteria

The PR must contain a reasoned taxonomy decision, not a cosmetic reorganization.

---

## PR-18 — Formalize maintainer governance and review ownership

### Objective

Make the repository maintainable by a team without diluting accountability.

### Files

- Add `.github/CODEOWNERS`.
- Add `docs/reviewer-roles.md`.
- Add `docs/decision-records.md` or a `docs/decisions/` directory with an index.
- Update conflict policy, contributing guide, PR template, and maintenance protocol.
- Add issue templates for removal and taxonomy change.
- Regenerate the manifest.

### Required approval matrix

- Typographic correction: one maintainer approval.
- Canonical URL correction with no identity change: one maintainer approval plus green CI.
- Resource addition, removal, or section move: two approvals, including one section reviewer.
- Affiliated resource change: two approvals; neither may rely solely on the affiliated contributor’s assessment.
- Schema or validator change: catalog engineer plus lead maintainer.
- Taxonomy change: lead maintainer plus two section reviewers.
- Release: lead maintainer plus release reviewer.

### Decision records

Record decisions that are likely to recur, including:

- why generic HDF5 and NetCDF are represented through scientific profiles;
- why popular workflow engines are not automatically included;
- how general agent protocols qualify;
- why validation is distinct from interoperability;
- when a broad platform qualifies as a reference architecture.

### Acceptance criteria

- CODEOWNERS paths match actual files.
- The approval matrix is reflected in branch-protection and review practice.
- No governance document grants automated tools authority over inclusion.

---

## PR-19 — Release 1.1 and complete maintenance-cycle audit

### Objective

Publish the first fully re-reviewed, decision-oriented release after the v2 migration and coverage work.

### Preconditions

- PR-01 through PR-18 complete or explicitly waived by a written lead-maintainer decision.
- All main-list records are within review dates.
- No unresolved permanent link failure.
- No unresolved high-severity catalog or governance issue.

### Files and actions

- Add `changelog.md` with entries since v1.0.0.
- Update `CITATION.cff` version and release date.
- Update `docs/validation-report.md` with exact counts and checks.
- Update `archive.md` for any removals.
- Run full network audit and commit the dated baseline report.
- Regenerate and verify the manifest.
- Create signed or annotated tag `v1.1.0` after merge.
- Create a GitHub release whose notes summarize editorial changes, schema v2, decision guides, additions, removals, and known limitations.

### Acceptance criteria

- CI passes on the release commit.
- Tag points to the audited commit.
- Citation metadata matches the tag.
- Changelog counts match actual diffs.
- Release notes do not claim completeness or certification.

---

## PR-20 — Prepare central Awesome incubation and submission

### Objective

Prepare a truthful, standards-compliant submission to the central Awesome index after sustained public maintenance.

### Timing

The repository became public on 2026-08-01. Use **2026-09-01** as the earliest safe submission date, subject to the current central rule and any later substantial re-publication event. Recheck the rule immediately before submission.

### Current official requirements that must be rechecked

The central project currently requires, among other items:

- at least 30 days of public existence;
- human editorial ownership and a list that is not AI-generated;
- standard `awesome-lint` compliance;
- default branch `main`;
- lowercase slug repository name;
- title-case README heading;
- repository topics `awesome` and `awesome-list`;
- a selective maintained list without deprecated main-list items;
- an Awesome badge;
- a `Contents` section as the first section;
- a Creative Commons license, with CC0 strongly recommended;
- contribution guidelines;
- no hard wrapping or CI badge;
- substantive review of at least four other open central Awesome PRs;
- a submission PR that is complete when opened;
- the verification comment `unicorn` under the current template.

The authoritative source is the current `sindresorhus/awesome` pull-request template and list-creation documentation. Never rely solely on this specification for the final submission checklist.

### Human-curation gate

This repository was materially assisted by AI during its initial construction. The team must not falsely certify that the list is “not AI-generated.” Before submission:

1. Every main-list entry must have a documented human primary-source review.
2. Human maintainers must independently accept, edit, or remove each entry and take responsibility for the final selection and wording.
3. The README must represent human editorial judgment, not an unreviewed model output.
4. If the team cannot truthfully check the central template’s non-AI-generated requirement, do not submit. Ask the central maintainers for clarification or continue as an independent Awesome list.
5. Never conceal AI assistance when directly asked.

### Incubation work

- Use the current central incubation mechanism referenced by the template, presently issue #2242, if still applicable.
- Maintain responsive issue and PR activity for at least 30 days.
- Record substantial human reviews in `docs/human-review-log.md`.
- Review at least four open central Awesome PRs thoroughly. Record links and substantive comments; lint-only comments do not count.
- Search the central repository and GitHub for duplicates immediately before submission.
- Add an original, high-DPI, accessible illustration if it improves the README and complies with the current design rule. Do not delay submission solely for decorative artwork when the maintainers judge it inappropriate, but document the decision.

### Submission PR preparation

- Recheck the appropriate central category.
- Proposed title: `Add Scientific Interoperability`.
- Proposed entry title: `Scientific Interoperability`.
- The URL must end in `#readme`.
- The description must describe the field, not the list, begin with an uppercase character, and end with a period.
- Add the entry at the bottom of the appropriate category.
- Open the PR only when every checkbox can be answered truthfully.
- Respond quickly and precisely to maintainer feedback.

### Acceptance criteria

- The submission is factually honest.
- Four substantive peer reviews are documented.
- Native Awesome lint passes without exclusions.
- Repository description, topics, license detection, branch name, README structure, and maintenance history satisfy the current template.
- No unresolved duplicate or collision exists.

---

## PR-21 — Respond to central review or close the submission path cleanly

### Objective

Handle the central Awesome outcome without compromising project quality.

### If maintainers request changes

- Create one local PR per coherent requested change.
- Cite the central review comment in the PR body.
- Do not make unreviewed direct edits to `main`.
- Rerun all checks and refresh the manifest.
- Reply to central maintainers only after the local change is merged and visible.

### If the submission is accepted

- Record the central PR and merge date in `docs/publishing.md`.
- Update the README Footnotes only if the central rules permit and the information is useful.
- Tag a patch release if repository content changed.
- Continue the maintenance protocol; central inclusion is not completion of maintenance.

### If the submission is rejected or cannot be truthfully made

- Record the exact reason in `docs/publishing.md`.
- Close the submission issue without framing rejection as a technical failure of the list.
- Continue as a standalone Awesome list.
- Do not weaken editorial standards to obtain central inclusion.

---

## 9. Resource-addition specification

Every resource addition after takeover must be a dedicated PR or part of a tightly related set of no more than four entries.

### 9.1 Required evidence packet

The PR must include:

- canonical name and technical URL;
- sentence-test statement;
- resource class;
- interoperability layers;
- connected objects or systems;
- mechanism;
- stewardship and governance;
- domains;
- implementation evidence;
- conformance evidence;
- primary sources;
- closest alternatives already in the catalog;
- decision basis;
- limitation or boundary note;
- review and review-due dates;
- conflict disclosure.

### 9.2 Required comparative question

The contributor must answer:

> What technical decision becomes easier or more accurate because this resource is present, and why is that decision not already adequately supported by a stronger existing entry?

### 9.3 Addition outcomes

An evaluated candidate must result in one of:

- main-list inclusion;
- watchlist placement with objective promotion conditions;
- exclusion with reusable rationale;
- deferral because primary sources or stewardship cannot be verified.

Silence or “interesting project” is not a valid outcome.

### 9.4 Prohibited addition arguments

Do not use these as sufficient justification:

- high star count;
- famous institution;
- “widely used” without evidence;
- “state of the art”;
- “comprehensive”;
- a single integration demo presented as broad interoperability;
- the existence of an API without a reusable contract;
- the existence of a file format without scientific semantics;
- vendor claims without inspectable technical material.

## 10. Removal and archival specification

Open a removal PR when any of these conditions holds:

- canonical source is permanently unavailable;
- resource is deprecated or archived;
- stewardship has ceased and no stable standard remains;
- documentation no longer supports the catalog claims;
- a successor clearly supersedes the entry;
- the entry duplicates a stronger resource;
- the resource fails the sentence test after clarification;
- the resource is no longer among the strongest current options.

A removal PR must:

1. update README and catalog;
2. add an `archive.md` record with date and reason when historically useful;
3. update alternatives and cross-references;
4. update problem index and decision guides;
5. update coverage reports;
6. regenerate the manifest;
7. explain migration guidance for users when applicable.

## 11. Source and citation standard

Preferred sources, in order:

1. published normative specification;
2. official standards-body or consortium documentation;
3. maintained canonical repository;
4. official validator, conformance suite, or implementation report;
5. peer-reviewed paper describing the technical artifact;
6. authoritative institutional documentation.

Avoid relying on:

- search snippets;
- AI-generated summaries;
- unaffiliated blog posts;
- press releases;
- marketing pages without technical details;
- copied Awesome lists as evidence of technical claims.

A secondary source may explain context but cannot be the sole basis for a mechanism, governance, implementation, or conformance claim.

## 12. Test architecture target

By PR-19, the test suite must include separate modules for:

- catalog loading and shard integrity;
- JSON Schema validation;
- README parsing and parity;
- duplicate IDs, names, and URLs;
- cross-reference resolution;
- review-date freshness;
- evidence/source consistency;
- link-policy classification;
- problem-index resource references;
- decision-guide resource references;
- watchlist schema and parity;
- coverage-audit determinism;
- manifest generation and verification;
- query CLI behavior.

Tests must be deterministic, network-free unless explicitly in the scheduled Links workflow, and runnable on Python 3.13.

## 13. CI target

The final Quality workflow should contain logically separate jobs or clearly separated steps for:

1. catalog and schema validation;
2. unit tests;
3. offline URL validation;
4. problem-index and decision-guide reference validation;
5. watchlist validation;
6. review freshness;
7. coverage invariant checks;
8. manifest verification;
9. standard Awesome lint.

The scheduled Links workflow performs network access and uploads reports. It must not mutate the repository automatically.

Pin third-party actions by major version at minimum. For high-assurance maintenance, evaluate pinning by full commit SHA in a dedicated dependency-hardening PR; do not mix that change into an editorial PR.

## 14. Metrics that matter

Track these metrics for maintenance, not promotion:

- percentage of entries reviewed within their required interval;
- unresolved permanent link failures;
- median time to triage correction issues;
- percentage of entries with independent implementation evidence;
- percentage with public conformance or validation evidence;
- section and domain concentration;
- watchlist items past due;
- number of resource additions, removals, and corrections per release;
- number of integration questions answerable through the problem index;
- number of PRs with complete source and conflict disclosures.

Do not optimize star count, raw list size, social engagement, or automated “quality scores.”

## 15. Stop and escalation conditions

Pause the relevant workstream and escalate to the lead maintainer when:

- a schema migration would require losing source information;
- two reviewers cannot agree whether a resource passes the sentence test;
- a contributor has an undisclosed affiliation;
- a taxonomy change is being used to make weak entries appear necessary;
- the same standard family begins to dominate a section through implementation entries;
- a network checker change would silently ignore permanent failures;
- central Awesome requirements conflict with truthful disclosure;
- a proposed automation would generate or select README content;
- a PR exceeds approximately 1,000 changed lines without a documented reason and review plan;
- primary sources are inaccessible or contradictory.

Record the decision in a durable issue or decision record. Do not resolve ambiguity through an undocumented private message.

## 16. Definition of done

The engineering takeover program is complete only when:

- PR-01 through PR-19 are merged or explicitly waived with written rationale;
- the live repository uses native, unfiltered Awesome lint;
- repository description, topics, branch protection, and labels are configured;
- the first network audit has no unresolved permanent failures;
- catalog v2 is the only catalog model;
- all main-list entries have complete v2 records and current human reviews;
- the query tool, problem index, and decision guides are published and validated;
- the watchlist is structured and current;
- coverage gaps have been reviewed through PR-16A–D;
- taxonomy has been reassessed under explicit thresholds;
- governance and CODEOWNERS are active;
- release `v1.1.0` is tagged and documented;
- a full maintenance cycle has been completed;
- central Awesome submission has either been made truthfully, accepted, or explicitly declined for a documented reason;
- there are no open high-severity correctness, integrity, or governance issues.

The project is never “finished” in the maintenance sense. Completion means the repository has reached the intended operating system: human-curated, evidence-backed, decision-oriented, reproducibly validated, and maintainable by the team without dependence on the original builder.

## 17. Immediate engineer start sequence

The first engineer taking over should perform these steps in order:

1. Read this specification completely.
2. Read `README.md`, `docs/project-charter.md`, `docs/editorial-policy.md`, `docs/maintenance-protocol.md`, and issue #2.
3. Confirm the current `main` SHA and compare it with the takeover baseline.
4. Verify repository description, topics, branches, branch protection, and Actions state in the GitHub interface.
5. Create branch `pr-01-native-awesome-compliance`.
6. Execute PR-01 exactly as specified.
7. Open the PR only after all local checks pass.
8. Merge only after both required GitHub Actions jobs pass on the exact head SHA.
9. Update issue #2.
10. Start PR-02 only after PR-01 is merged.

No engineer should start with speculative resource additions. The settings, native lint, network audit, and catalog model must be stabilized first.
