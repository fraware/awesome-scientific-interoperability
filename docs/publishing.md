# Publishing and Repository Operations

The public repository is:

```text
https://github.com/fraware/awesome-scientific-interoperability
```

## Operating mode: standalone Awesome list

**Decision (2026-08-01):** This project operates as a **high-quality standalone Awesome list**. It follows Awesome list conventions (badge, `Contents` section, CC0 license, contribution guidelines, native `awesome-lint`) but is **not** submitted to the central [sindresorhus/awesome](https://github.com/sindresorhus/awesome) index at this time.

Central submission is **deferred** until both conditions below are satisfied. If they cannot both be satisfied, the standalone path remains permanent—not a failure of list quality.

## Central submission path — closed pending gates (PR-21)

**Status:** Closed (not rejected—never opened).

**Reason:** On 2026-08-01 the repository became public. The central Awesome template requires at least 30 days of public existence and asks submitters to confirm the list is not AI-generated. This repository was materially AI-assisted during construction; maintainers cannot truthfully certify non-AI-generated content today. Opening a central PR would require false certification.

**Actions taken:**

- No pull request opened against `sindresorhus/awesome`.
- No incubation comment posted under a false non-AI claim.
- Human review path documented in [human-review-log.md](human-review-log.md).
- Native `awesome-lint` restored and enforced in CI (see below).

**If maintainers later pursue central inclusion:** Re-read the live [pull-request template](https://github.com/sindresorhus/awesome/blob/main/pull_request_template.md) and [create-list.md](https://github.com/sindresorhus/awesome/blob/main/create-list.md), complete the gaps in `human-review-log.md`, and open a submission PR only when every checkbox can be answered truthfully—including requesting clarification from central maintainers on the AI-assistance policy if needed.

## Earliest submission date

| Milestone | Date |
| --- | --- |
| Repository public / first real commit | 2026-08-01 |
| Earliest eligible under 30-day rule | **2026-09-01** (recheck immediately before any submission) |

Do **not** open a central Awesome PR before 2026-09-01 unless a later substantial re-publication event resets the clock and the current rule is rechecked.

## Readiness checklist vs central Awesome template

Rechecked against the live [sindresorhus/awesome pull-request template](https://github.com/sindresorhus/awesome/blob/main/pull_request_template.md) on **2026-08-01**.

### Pull-request requirements

| Requirement | Status | Notes |
| --- | --- | --- |
| Not a fully AI-generated PR | **Blocked** | Repo was AI-assisted; human curation documented but non-AI checkbox not truthfully answerable |
| Complete PR when opened (no draft) | N/A | No PR opened |
| Review ≥4 other open central Awesome PRs substantively | **Not done** | See `human-review-log.md`; do not invent reviews |
| Read [create-list.md](https://github.com/sindresorhus/awesome/blob/main/create-list.md) | Done | Incorporated into this checklist |
| Title format `Add Name of List` | Planned | Proposed: `Add Scientific Interoperability` |
| Entry describes the field, not the list; uppercase start, period end | Planned | Draft: interoperability standards and tools for scientific data, software, workflows, instruments, knowledge systems, and agents. |
| Entry at bottom of appropriate category | Pending | Recheck category before submission |
| Entry title title-cased; URL ends in `#readme` | Ready | `https://github.com/fraware/awesome-scientific-interoperability#readme` |
| No blockchain-related list | Ready | — |
| List complies with Awesome list requirements below | Partial | See list table |
| Comment `unicorn` on submission PR | Pending | Only after truthful completion |

### Awesome list requirements

| Requirement | Status | Notes |
| --- | --- | --- |
| Public ≥30 days | **Not yet** | Public since 2026-08-01; eligible ≥2026-09-01 |
| Not AI-generated | **Blocked** | AI-assisted construction; see honesty gate |
| `awesome-lint` passes | **Ready** | Native `npx --yes awesome-lint` in CI and Makefile; no custom rule filter |
| Default branch `main` | Ready | — |
| Succinct project/theme description at top of README | Ready | Blockquote under title |
| Hard work / best possible produce | Ongoing | Human review log tracks section reviews |
| Repo name lowercase slug | Ready | `awesome-scientific-interoperability` |
| Heading title case | Ready | `# Awesome Scientific Interoperability` |
| Non-generated Markdown in GitHub repo | Ready | Manually authored README |
| Topics `awesome` and `awesome-list` | Ready | Plus domain topics |
| Not a duplicate | **Recheck before submit** | Search central repo and GitHub |
| Only awesome items; no unmaintained main-list entries | Ongoing | Editorial policy + review dates |
| Logo/illustration when possible | **Optional / undecided** | Document decision before submit |
| Entries have descriptions | Ready | 100 entries with dash descriptions |
| Awesome badge on heading | Ready | Links to awesome.re |
| `Contents` first section; no Contributing/Footnotes inside | Ready | Verified in validation report |
| CC0 or Creative Commons license file | Ready | CC0 in `license` |
| `contributing.md` with guidelines | Ready | Root `contributing.md` |
| Footnotes section for non-TOC extras | Ready | README Footnotes |
| Consistent formatting; no hard wrapping | Ready | — |
| No CI badge in README | Ready | — |
| No “Inspired by awesome-foo” link | Ready | Badge only |

## Honesty gate (non-negotiable)

From `docs/engineering-takeover-specification.md` PR-20:

1. Every main-list entry must have a documented human primary-source review (section and gap reviews under `docs/reviews/` and `docs/candidate-reviews/`).
2. Human maintainers must independently accept, edit, or remove each entry and take responsibility for selection and wording.
3. The README must represent human editorial judgment.
4. **If the team cannot truthfully check “Is not AI-generated,” do not submit.** Ask central maintainers for clarification or continue standalone.
5. Never conceal AI assistance when directly asked.

## Publication checklist (standalone operations)

1. Confirm the `Quality` workflow passes, including catalog validation, unit tests, and native `awesome-lint`.
2. Run the `Links` workflow manually after publication or URL changes.
3. Keep the GitHub description and topics current.
4. Keep branch protection on `main` requiring the `catalog` and `awesome-lint` jobs and pull requests for changes.
5. Keep the README manually authored; do not add an automatic README renderer.
6. Review every contribution against `docs/editorial-policy.md` and record limitations in the relevant catalog shard.

## Repository metadata

Description:

```text
Standards and tools that make scientific data, software, workflows, instruments, knowledge systems, and agents work together.
```

Topics: `awesome`, `awesome-list`, `scientific-interoperability`, `research-infrastructure`, `open-science`.

Run the unmodified linter locally and in CI:

```bash
npx --yes awesome-lint
```

## Related documents

- [Human review log](human-review-log.md) — PR-04–06 migrations, PR-16A–D gap reviews, and submission gaps
- [Validation report](validation-report.md) — release checks
- [Engineering takeover specification](engineering-takeover-specification.md) — PR-20, PR-21
