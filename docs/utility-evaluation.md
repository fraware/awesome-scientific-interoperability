# Utility Evaluation Protocol

North Star claim under test: a technically competent user can identify the strongest available interoperability mechanism for a concrete scientific integration problem without conducting a new landscape search.

This protocol treats that claim as empirical. It does **not** optimize star counts, social engagement, or list size ([metrics.md](metrics.md)).

## Status

| Element | Status |
|---------|--------|
| Written protocol | Ready |
| Task battery (10 problems) | Ready |
| Practitioner cohort (≥5 external) | Not yet filled — recruit via issues/social/domain lists |
| Steward entry challenge week | Scheduled process ready; dates TBD when cohort opens |
| Downstream `catalog.json` consumer example | Ready (`examples/catalog_json_consumer.py`) |
| Evaluation report with outcomes | Pending first cohort |

## 1. Task battery

Draw ten tasks from the [integration problem index](integration-problems.md). Default battery:

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

Facilitators may substitute an equal number of problem-index tasks if a cohort has a domain focus; record substitutions.

## 2. Participants

Recruit at least five external practitioners (not the lead maintainer). Capture domain background, but no vanity metrics about followers or stars.

## 3. Measures

For each task, record:

- Time-to-first-candidate (minutes from start to first catalog/guide/README candidate named).
- Whether the participant opened primary sources (yes/no; which URLs).
- Whether guide boundary notes prevented a category error (yes/no/uncertain + note).
- Structured satisfaction items (1–5): clarity of next step, trust in evidence, willingness to reuse the corpus.
- Free-text blockers.

Allowed surfaces: README, decision guides, integration problems, local query CLI, published explorer/downloads. Do not require private tooling.

## 4. Entry challenge week

Invite standards stewards to comment on their entries (issue labels or discussion thread). Goal: catch stale URLs, overstated evidence, or missing boundaries. File corrections as ordinary issues/PRs.

## 5. Downstream smoke test

Run or review `examples/catalog_json_consumer.py` against a downloaded `catalog.json` (release asset, Pages `/data/catalog.json`, or local `dist/catalog.json`). Success means a third party can consume joined steward/implementation fields without cloning the YAML shards.

## 6. Reporting

Write results into [human-review-log.md](human-review-log.md) or an evaluation appendix linked from it:

- methods and battery used
- participant count (no unnecessary personal data)
- aggregate outcomes
- catalog/guide fixes filed as issues/PRs

Do not report GitHub stars as a success metric.

## 7. Acceptance for this program wave

The evaluation program is ready when this protocol, metrics policy, challenge issue path, and consumer example exist—even if the first cohort is still recruiting. A completed study report remains a follow-on deliverable once participants finish.
