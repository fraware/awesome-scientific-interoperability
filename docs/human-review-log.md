# Human Review Log

This document records the human editorial review path for the catalog and main list. It exists to support truthful central Awesome submission decisions (see `docs/publishing.md` and `docs/engineering-takeover-specification.md` PR-20). It does **not** certify that the list is free of AI assistance.

## AI assistance disclosure

The repository was materially assisted by AI during initial construction, migration tooling, and documentation drafting. Human maintainers inspected primary sources, accepted or edited entries, and recorded review notes—but the central Awesome template currently asks submitters to confirm the list **is not AI-generated**. That checkbox cannot be answered truthfully today. See `docs/publishing.md` for the operating decision.

## Review process

Human review follows these documents, in order:

1. [Project charter](project-charter.md) — sentence test and scope.
2. [Editorial policy](editorial-policy.md) — inclusion and exclusion rules.
3. [Review checklist](review-checklist.md) — per-entry inspection steps.
4. [Maintenance protocol](maintenance-protocol.md) — contribution and recurring review cadence.
5. [Reviewer roles and approval matrix](reviewer-roles.md) — who may approve what.

For each catalog migration or addition:

- Open the canonical URL and at least one primary technical source.
- Confirm name, URL, stewardship, domains, implementation and conformance status, evidence types, alternatives, and boundary notes against sources—not inference.
- Preserve README/catalog parity; any correction applies to both.
- Record `reviewed_on`, `review_due_on`, sources inspected, changes, unresolved questions, and conflicts in the section review file under `docs/reviews/` or a candidate review under `docs/candidate-reviews/`.
- Run catalog validation, tests, offline link checks, and native `awesome-lint` before merge.

Until additional section reviewers are named in `.github/CODEOWNERS`, the lead maintainer ([@fraware](https://github.com/fraware)) acts as section reviewer for every section (`docs/reviewer-roles.md`).

## PR-04 — Catalog migration group A (2026-08-01)

**Scope:** 28 main-list entries across Foundations (4), Identifiers and Discovery (10), and Metadata and Semantics (14).

**Review artifacts:**

| Section | Records | Review notes |
| --- | ---: | --- |
| Foundations | 4 | [foundations.md](reviews/foundations.md) |
| Identifiers and Discovery | 10 | [identifiers-and-discovery.md](reviews/identifiers-and-discovery.md) |
| Metadata and Semantics | 14 | [metadata-and-semantics.md](reviews/metadata-and-semantics.md) |

**What was reviewed:** Canonical URLs; primary specification or stewardship pages; v2 field migration (summary, maturity, evidence, stewardship, domains, sources, alternatives, review dates); README parity; boundary notes for emerging conformance tooling (e.g. CDIF, FDO revision cycle).

**Sampling:** Engineering specification PR-04 requires an independent reviewer to sample five records per section. That cross-section sampling has **not** been recorded as a separate artifact; second-maintainer sampling remains a gap before any central submission.

## PR-05 — Catalog migration group B (2026-08-01)

**Scope:** 27 main-list entries across Data and Digital Objects (7), Research Software and Environments (5), Workflows and Execution (10), and Provenance and Evidence (5).

**Review artifacts:**

| Section | Records | Review notes |
| --- | ---: | --- |
| Data and Digital Objects | 7 | [data-and-digital-objects.md](reviews/data-and-digital-objects.md) |
| Research Software and Environments | 5 | [research-software-and-environments.md](reviews/research-software-and-environments.md) |
| Workflows and Execution | 10 | [workflows-and-execution.md](reviews/workflows-and-execution.md) |
| Provenance and Evidence | 5 | [provenance-and-evidence.md](reviews/provenance-and-evidence.md) |

**What was reviewed:** Packaging vs. provenance boundaries; workflow languages vs. execution APIs; representative-implementation limits; RO-Crate profile relationships; conformance claims tied to public validators or official suites; cross-shard references (e.g. CWLProv, TRS deferrals).

## PR-06 — Catalog migration group C (2026-08-01)

**Scope:** 20 main-list entries across Knowledge Systems and Publications (5), Instruments and Laboratories (7), Agents, Access, and Policy (4), and Validation and Conformance (4).

**Review artifacts:**

| Section | Records | Review notes |
| --- | ---: | --- |
| Knowledge Systems and Publications | 5 | [knowledge-systems-and-publications.md](reviews/knowledge-systems-and-publications.md) |
| Instruments and Laboratories | 7 | [instruments-and-laboratories.md](reviews/instruments-and-laboratories.md) |
| Agents, Access, and Policy | 4 | [agents-access-and-policy.md](reviews/agents-access-and-policy.md) |
| Validation and Conformance | 4 | [validation-and-conformance.md](reviews/validation-and-conformance.md) |

**What was reviewed:** Fast-moving agent specifications against current published versions; laboratory procedure vs. device vs. analytical-data vs. clinical exchange boundaries; vendor and consortium access conditions; validation resources that test documented contracts (not generic FAIRness scoring); six-month review intervals for emerging agent and laboratory resources.

## PR-16A–D — Domain gap reviews (2026-08-01)

Structured candidate reviews evaluated whether additional main-list entries were warranted without duplicating existing coverage. Each review applied the sentence test, inspected primary sources, compared overlap with the corpus, and recorded include/exclude/watchlist outcomes.

| Review | Specification | Artifact | Main-list additions |
| --- | --- | --- | ---: |
| Statistical and social-science gaps | PR-16A | [statistical-and-social-science.md](candidate-reviews/statistical-and-social-science.md) | 1 (SDMX) |
| Physical-science and engineering gaps | PR-16B | [physical-science-and-engineering.md](candidate-reviews/physical-science-and-engineering.md) | 4 (FMI, CIF, NeXus, OPTIMADE) |
| Geospatial and environmental gaps | PR-16C | [geospatial-and-environmental.md](candidate-reviews/geospatial-and-environmental.md) | 4 (OGC API Features, Coverages, SensorThings, openEO) |
| Experimental and biomedical gaps | PR-16D | [experimental-and-biomedical.md](candidate-reviews/experimental-and-biomedical.md) | 3 (ISA-JSON, BioCompute Objects, DICOMweb) |

Exclusions and watchlist placements are recorded in the candidate review files and [source-notes.md](source-notes.md).

## Current corpus status (2026-08-02)

- **Main-list entries:** 96 on the stacked Issue #44 Batch B candidate tree (README and catalog parity enforced by CI).
- **Section review files:** 11 under `docs/reviews/`.
- **Gap review files:** 4 under `docs/candidate-reviews/`.
- **Review freshness:** Enforced by `scripts/check_review_freshness.py` in CI.

## Central Awesome peer reviews — not completed

The central Awesome pull-request template requires substantive review of at least four other open Awesome list submissions, with documented links and comments. **No such peer reviews have been performed or recorded.** This log intentionally does not invent peer reviews that did not occur.

If the project later pursues central submission, maintainers must complete and document those reviews before opening a PR to [sindresorhus/awesome](https://github.com/sindresorhus/awesome).

## Gaps before any central submission

The following remain open as of 2026-08-01:

1. **30-day public maturity** — repository became public on 2026-08-01; earliest eligible date is **2026-09-01** (recheck the current rule immediately before submission).
2. **Non-AI-generated certification** — cannot be answered truthfully; request clarification from central maintainers or continue as a standalone list.
3. **Independent cross-section sampling** — PR-04 sampling by a second reviewer not yet documented.
4. **Four substantive central Awesome PR reviews** — not started.
5. **Duplicate search** — search the central repository and GitHub immediately before submission.
6. **Incubation visibility** — use the current central incubation issue (template references [#2242](https://github.com/sindresorhus/awesome/issues/2242)) if still applicable, after timing and honesty gates clear.
7. **README illustration** — optional high-DPI illustration decision not yet recorded.
8. **Sustained responsive maintenance** — ongoing; not yet demonstrated for 30 days.

## Related documents

- [Publishing and repository operations](publishing.md)
- [Validation report](validation-report.md)
- [Engineering takeover specification](engineering-takeover-specification.md) — PR-20, PR-21

## Issue #44 Batch A — pending human maintainer review (2026-08-02)

**Scope:** Proposed admission of SBML, SED-ML, CellML, BIDS, and NWB.

The records were prepared through AI-assisted primary-source review and remain marked `review_type: author` with a conflict disclosure stating that human maintainer approval is required before merge. The PR must not be represented as independently reviewed until a maintainer records that approval.

Review artifacts:

- [Data and Digital Objects](reviews/data-and-digital-objects.md)
- [Provenance and Evidence](reviews/provenance-and-evidence.md)
- [Computational models decision guide](decision-guides/systems-biology-models.md)
- [Neuroscience data decision guide](decision-guides/neuroscience-data-standards.md)
## Issue #44 Batch B — pending human maintainer review (2026-08-02)

**Scope:** Proposed admission of OME-NGFF, FITS, IVOA TAP, and IVOA VOTable on top of Batch A.

Evidence was classified through AI-assisted primary-source review. The records remain `review_type: author`; no independent human review is claimed. Human review must check implementation-operator separation, validator scope, IVOA family boundaries, OME-Zarr version caveats, and decision-guide recommendations.

Review artifacts:

- [Data and Digital Objects](reviews/data-and-digital-objects.md)
- [Identifiers and Discovery](reviews/identifiers-and-discovery.md)
- [Astronomy decision guide](decision-guides/astronomy-data-and-services.md)
- [Bioimaging decision guide](decision-guides/bioimaging-data.md)
