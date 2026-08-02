# Evaluation and metrics

North Star under test: a technically competent user can identify the strongest available interoperability mechanism for a concrete scientific integration problem without conducting a new landscape search.

This protocol treats that claim as empirical. It does **not** optimize star counts, social engagement, or list size.

## Metrics that matter

| Metric | Intent |
| --- | --- |
| Percentage of entries reviewed within their required interval | Freshness of human stewardship |
| Unresolved permanent link failures | Integrity of outbound references |
| Median time to triage correction issues | Responsiveness |
| Percentage of entries with independent-implementation evidence | Strength of interoperability claims |
| Percentage with public conformance or validation evidence | Verifiability |
| Section and domain concentration | Avoid silent over-representation |
| Watchlist items past due | Boundary hygiene |
| Resource additions, removals, and corrections per release | Change transparency |
| Integration questions answerable through the problem index | Decision coverage |
| PRs with complete source and conflict disclosures | Process integrity |

### Utility evaluation measures

- Task success rate (candidate named that matches guide/catalog intent)
- Median time-to-first-candidate
- Rate of primary-source opens
- Rate of avoided category errors attributed to boundary notes
- Structured satisfaction scores
- Number of steward challenge findings that produce corrections

### Forbidden vanity metrics

Do not optimize or report as success: GitHub stars or forks as quality proxies, social impressions, maximizing main-list size, or opaque automated “awesome scores.” Prefer metrics recomputed from repository state, CI artifacts, issue timestamps, and evaluation worksheets. Leave unmeasurable metrics blank rather than inventing numbers.

## Utility evaluation protocol

### Status

| Element | Status |
| --- | --- |
| Written protocol | Ready |
| Task battery (10 problems) | Ready |
| Practitioner cohort (≥5 external) | Not yet filled |
| Steward entry challenge week | Process ready; dates TBD when cohort opens |
| Downstream `catalog.json` consumer example | Ready (`examples/catalog_json_consumer.py`) |
| Evaluation report with outcomes | Pending first cohort |

### Task battery

Draw ten tasks from the [integration problem index](../integration-problems.md). Default battery:

1. Identify researchers/organizations/samples/software objects.
2. Package heterogeneous research objects for transfer.
3. Choose among RO-Crate, BagIt, OCFL, and Data Package.
4. Exchange neurophysiology data (NWB/BIDS path).
5. Choose astronomy file/table/query mechanisms (FITS/VOTable/TAP/ObsCore).
6. Find public validators for a packaging or workflow family.
7. Discover portable workflows and execution APIs.
8. Harmonize clinical/observational health data models.
9. Exchange mass-spectrometry spectra.
10. Preserve repository objects with fixity and layout guarantees.

Facilitators may substitute an equal number of problem-index tasks for a domain-focused cohort; record substitutions.

### Participants and measures

Recruit at least five external practitioners (not the lead maintainer). For each task, record time-to-first-candidate, whether primary sources were opened, whether boundary notes prevented a category error, structured satisfaction (1–5), and free-text blockers.

Allowed surfaces: README, decision guides, integration problems, local query CLI, published explorer/downloads. Do not require private tooling.

### Entry challenge week

Invite standards stewards to comment on their entries. Goal: catch stale URLs, overstated evidence, or missing boundaries. File corrections as ordinary issues/PRs.

### Downstream smoke test

Run or review `examples/catalog_json_consumer.py` against a downloaded `catalog.json` (release asset, Pages `/data/catalog.json`, or local `dist/catalog.json`). Success means a third party can consume joined steward/implementation fields without cloning the YAML shards.

### Reporting

Record methods, participant count (no unnecessary personal data), aggregate outcomes, and catalog/guide fixes filed as issues/PRs. Do not report GitHub stars as a success metric.
