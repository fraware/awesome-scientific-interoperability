# Reviewer Roles and Approval Matrix

This document formalizes maintainer responsibilities and the approvals required before merge. A small team may hold multiple roles, but the duties stay distinct. See also [conflicts of interest](conflicts-of-interest.md), [maintenance protocol](maintenance-protocol.md), and [decision records](decision-records.md).

## Roles

### Lead maintainer

- Owns scope and final editorial decisions.
- Approves schema migrations and taxonomy changes.
- Resolves disagreements after documented review.
- Confirms central Awesome submission statements.
- Signs releases.
- Cannot approve an affiliated resource alone.

Current holder: [@fraware](https://github.com/fraware) (repository owner).

### Catalog engineer

- Maintains schemas, loaders, validators, query tools, tests, and manifests.
- Ensures migrations are deterministic and reversible.
- Does not decide inclusion based on automated scores or validator output alone.

### Section reviewer

- Inspects primary technical sources for one catalog section.
- Verifies descriptions, mechanisms, stewardship, alternatives, and evidence.
- Records review dates and limitations in `docs/reviews/`.
- May request removal, deferral, or watchlist placement.

Section reviewers will be named in `.github/CODEOWNERS` on their shard and matching `docs/reviews/` file as the team grows. Until then, the lead maintainer acts as section reviewer for every section.

### Release reviewer

- Runs the complete validation matrix on the exact head commit.
- Verifies manifest integrity.
- Checks workflow results and network-audit classifications.
- Confirms that release and citation metadata match.

### Junior contributor

May research, propose, implement, and test changes. Must not self-approve a resource addition, schema migration, removal, or taxonomy change.

## Approval matrix

| Change type | Required approvals | CI |
| --- | --- | --- |
| Typographic correction (no factual change) | One maintainer | Optional |
| Canonical URL correction with no identity change | One maintainer | Required green |
| Resource addition, removal, or section move | Two approvals, including one section reviewer for the affected section | Required green |
| Affiliated resource change | Two approvals; neither may rely solely on the affiliated contributor's assessment | Required green |
| Schema or validator change | Catalog engineer plus lead maintainer | Required green |
| Taxonomy change (section split, merge, rename, or new section) | Lead maintainer plus two section reviewers | Required green |
| Release (`v*` tag and GitHub release) | Lead maintainer plus release reviewer | Required green on release commit |

When a dedicated section reviewer has not yet been appointed, the lead maintainer may not count twice toward the two-approval minimum for resource or taxonomy changes; a second independent maintainer or invited reviewer must provide the second approval.

## Tools and automation

Validators, linters, link checkers, coverage audits, and manifest verification enforce consistency. They do not decide inclusion, removal, section placement, or taxonomy. A green CI run is necessary but never sufficient for editorial changes.

## Escalation

Escalate to the lead maintainer when:

- Two reviewers disagree whether a resource passes the sentence test.
- An affiliated contributor disputes a deferral or removal decision.
- A proposed change would alter admission rules documented in [editorial policy](editorial-policy.md) or [decision records](decision-records.md).
- Central Awesome requirements conflict with truthful disclosure.

Document the disagreement, sources inspected, and outcome in the pull request or an issue linked from it.

## Related documents

- [Contributing](../contributing.md) — proposal requirements and local checks.
- [Review checklist](review-checklist.md) — per-entry inspection steps.
- [Conflicts of interest](conflicts-of-interest.md) — affiliation rules.
- [Maintenance protocol](maintenance-protocol.md) — recurring review cadence.
