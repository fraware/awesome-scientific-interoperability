# Conflicts of Interest

A conflict exists when a contributor or reviewer created, maintains, funds, advises, employs, competes with, or has a close professional relationship with the submitted resource or its responsible organization.

## Contributor obligations

Affiliated people may propose resources, provide technical information, and correct factual errors. They may not serve as the sole approving reviewer. The pull request or issue must disclose the relationship, and a non-affiliated maintainer must make the final inclusion decision.

Commercial status, institutional reputation, funding, citation count, and GitHub stars do not substitute for the inclusion standard.

## Reviewer obligations

- Disclose affiliation before reviewing a resource you helped build, fund, or govern.
- Do not approve an affiliated resource change when you are the only maintainer-level reviewer on the pull request.
- Do not rely solely on an affiliated contributor's assessment when recording conformance, maintenance, or adoption claims; inspect primary sources independently.
- Recuse from the final merge decision when the conflict is material and no independent reviewer is available; escalate to the lead maintainer.

## Approval requirements for affiliated changes

| Change type | Minimum approvals |
| --- | --- |
| Affiliated resource addition or substantive edit | Two approvals; neither may rely solely on the affiliated contributor's assessment |
| Affiliated resource removal or downgrade | Two approvals; at least one section reviewer for the affected section |
| Affiliated correction (URL, typo, maintenance date) with no scope change | One non-affiliated maintainer plus green CI |

See the full matrix in [reviewer roles](reviewer-roles.md).

## Tools and automation

Automated checks do not resolve conflicts of interest. A green validator or linter run does not waive independent human review for affiliated contributions.

## Escalation

When reviewers disagree about whether a conflict affects impartiality, or when an affiliated contributor disputes a deferral or removal:

1. Document affiliations and the disputed claim in the pull request or linked issue.
2. Request review from a maintainer without the disclosed conflict.
3. If disagreement persists, escalate to the lead maintainer ([@fraware](https://github.com/fraware)) with primary sources cited by each party.

The lead maintainer records the outcome in the pull request. Taxonomy or policy implications belong in [decision records](decision-records.md).
