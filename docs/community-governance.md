# Community Governance

This document explains how humans govern Awesome Scientific Interoperability. Automation validates consistency; it never decides inclusion.

## Single-maintainer limitation (current)

Until at least two non-lead humans accept named section-reviewer responsibility and appear in `.github/CODEOWNERS`, this repository operates under an explicit **single-maintainer limitation**:

- Lead maintainer [@fraware](https://github.com/fraware) currently fulfills lead, catalog-engineer, section-reviewer, and release-reviewer duties described in [reviewer-roles.md](reviewer-roles.md).
- CODEOWNERS lists only `@fraware`. Placeholder or invented reviewers are forbidden.
- Affiliated contributors still cannot sole-approve their own resources; when no second maintainer exists, affiliated changes wait for an invited independent reviewer or remain blocked.

This limitation is honesty, not theater. The browser About page and reviewer-roles document the same fact.

## What reviewers do

Domain section reviewers:

- Inspect primary technical sources for their section shard and matching `docs/reviews/` notes.
- Verify mechanisms, stewardship, evidence types, typed relations, and boundary notes.
- Do **not** sole-approve resources with which they are affiliated ([conflicts-of-interest.md](conflicts-of-interest.md)).
- Prefer public review comments on pull requests; durable disagreements can be summarized in [human-review-log.md](human-review-log.md) or short records under `docs/decisions/` when that directory is used.

Expected time commitment for an active section: roughly one focused review pass per quarter plus ad-hoc PR review when that section changes.

## Recruitment

Open recruitment tracks live in GitHub issues titled for domain reviewer recruiting. Target sections include:

- Systems biology and models
- Neuroscience
- Astronomy / Virtual Observatory
- Bioimaging
- Genomics
- Ecology
- Proteomics
- Clinical research data
- Preservation and packaging
- Workflows and provenance
- Agents and controlled access

Acceptance is explicit: a person comments that they accept the section, COI rules, and CODEOWNERS responsibility. Only then may a PR add their GitHub handle to CODEOWNERS for the relevant paths.

## How to propose corrections or challenges

- Factual corrections: use the correction issue form.
- Challenge an evidence claim or guide recommendation: use the challenge issue form.
- New resources: use the add-resource issue form and [contributing.md](../contributing.md).

## Related documents

- [Reviewer roles](reviewer-roles.md)
- [Conflicts of interest](conflicts-of-interest.md)
- [Editorial policy](editorial-policy.md)
- [Project charter](project-charter.md)
- [Publishing](publishing.md)
- [Utility evaluation](utility-evaluation.md)
- [Metrics](metrics.md)
