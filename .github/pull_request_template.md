## Change type

Select one (see [governance](docs/governance.md) for required approvals):

- [ ] Typographic correction (one maintainer)
- [ ] Canonical URL correction, no identity change (one maintainer + green CI)
- [ ] Resource addition, removal, or section move (two approvals, one section reviewer)
- [ ] Affiliated resource change (two independent approvals)
- [ ] Schema or validator change (catalog engineer + lead maintainer)
- [ ] Taxonomy change (lead maintainer + two section reviewers)
- [ ] Other editorial or documentation change

## Change

Describe the resource addition, correction, removal, or editorial change.

## Interoperability relationship

What interoperates with what, and through which documented mechanism?

## Primary sources inspected

List the specification, documentation, repository, validator, implementation report, or other primary technical sources.

## Conflict of interest

Disclose any affiliation with affected resources or organizations.

## Required reviewers

List the roles that must approve before merge (maintainer, section reviewer, catalog engineer, release reviewer). Confirm approvals are independent for affiliated changes.

## Checklist

- [ ] I read `contributing.md`, `docs/editorial-policy.md`, and `docs/governance.md`.
- [ ] I inspected primary technical sources.
- [ ] The README and catalog contain the same name, URL, section, and `summary`.
- [ ] The `summary` is objective, specific, and ends with a period.
- [ ] Current catalog fields are complete (`steward_id`, `review_due_on`, `source_refs`, evidence statuses, taxonomy dimensions, and typed relations).
- [ ] I recorded limitations and the closest alternative in the catalog.
- [ ] I ran `python scripts/validate_catalog.py`.
- [ ] I ran `python scripts/validate_watchlist.py` when watchlist records changed.
- [ ] I ran `python scripts/check_review_freshness.py`.
- [ ] I ran `python -m unittest discover -s tests -v`.
- [ ] I ran `python scripts/generate_manifest.py` and `python scripts/verify_manifest.py` when tracked files changed.
- [ ] I understand that CI and validators enforce consistency but do not decide inclusion.
- [ ] I accept responsibility for the factual accuracy of this contribution.
