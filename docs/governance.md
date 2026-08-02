# Governance

Humans govern Awesome Scientific Interoperability. Automation validates consistency; it never decides inclusion, removal, section placement, or taxonomy.

See also [conflicts of interest](conflicts-of-interest.md), [maintenance](maintenance.md), and [decision records](decision-records.md).

## Single-maintainer limitation

Until at least two non-lead humans accept named section-reviewer responsibility and appear in `.github/CODEOWNERS`, this repository operates under an explicit **single-maintainer limitation**:

- Lead maintainer [@fraware](https://github.com/fraware) currently fulfills lead, catalog-engineer, section-reviewer, and release-reviewer duties.
- CODEOWNERS lists only `@fraware`. Placeholder or invented reviewers are forbidden.
- Affiliated contributors still cannot sole-approve their own resources; when no second maintainer exists, affiliated changes wait for an invited independent reviewer or remain blocked.

## Roles

### Lead maintainer

- Owns scope and final editorial decisions.
- Approves schema migrations and taxonomy changes.
- Resolves disagreements after documented review.
- Confirms any central Awesome submission statements.
- Signs releases.
- Cannot approve an affiliated resource alone.

Current holder: [@fraware](https://github.com/fraware).

### Catalog engineer

- Maintains schemas, loaders, validators, query tools, tests, and manifests.
- Ensures migrations are deterministic and reversible.
- Does not decide inclusion based on automated scores or validator output alone.

### Section reviewer

- Inspects primary technical sources for one catalog section.
- Verifies descriptions, mechanisms, stewardship, alternatives, and evidence.
- Records review dates and limitations in `docs/reviews/`.
- May request removal, deferral, or watchlist placement.

Section reviewers are named in `.github/CODEOWNERS` on their shard and matching `docs/reviews/` file only after they explicitly accept. Until then, the lead maintainer acts as section reviewer for every section under the single-maintainer limitation above.

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

## What section reviewers do

- Inspect primary technical sources for their section shard and matching `docs/reviews/` notes.
- Verify mechanisms, stewardship, evidence types, typed relations, and boundary notes.
- Do **not** sole-approve resources with which they are affiliated.
- Prefer public review comments on pull requests.

Expected time commitment for an active section: roughly one focused review pass per quarter plus ad-hoc PR review when that section changes.

## Recruitment

Open recruitment tracks live in GitHub issues titled for domain reviewer recruiting. Target sections include systems biology and models, neuroscience, astronomy / Virtual Observatory, bioimaging, genomics, ecology, proteomics, clinical research data, preservation and packaging, workflows and provenance, and agents and controlled access.

Acceptance is explicit: a person comments that they accept the section, conflict-of-interest rules, and CODEOWNERS responsibility. Only then may a pull request add their GitHub handle to CODEOWNERS for the relevant paths.

## How to propose corrections or challenges

- Factual corrections: use the correction issue form.
- Challenge an evidence claim or guide recommendation: use the challenge issue form.
- New resources: use the add-resource issue form and [contributing.md](../contributing.md).

## Escalation

Escalate to the lead maintainer when:

- Two reviewers disagree whether a resource passes the sentence test.
- An affiliated contributor disputes a deferral or removal decision.
- A proposed change would alter admission rules documented in [editorial policy](editorial-policy.md) or [decision records](decision-records.md).
- Central Awesome requirements conflict with truthful disclosure.

Document the disagreement, sources inspected, and outcome in the pull request or an issue linked from it.

## Tools and automation

Validators, linters, link checkers, coverage audits, and manifest verification enforce consistency. They do not decide inclusion. A green CI run is necessary but never sufficient for editorial changes.
