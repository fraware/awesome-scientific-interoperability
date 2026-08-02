# Publishing and release operations

**Public repository:** https://github.com/fraware/awesome-scientific-interoperability

Community recruitment and the single-maintainer limitation are documented in [governance](../governance.md). Utility evaluation lives in [evaluation](evaluation.md).

## Operating mode

This project operates as a **high-quality standalone Awesome list**. It follows Awesome list conventions (badge, `Contents` section, CC0 license, contribution guidelines, native `awesome-lint`) but is **not** submitted to the central [sindresorhus/awesome](https://github.com/sindresorhus/awesome) index at this time.

Central submission stays closed until maintainers can truthfully answer every central checklist item, including the non-AI-generated requirement, and the repository meets the current public-maturity rule. If those conditions cannot both be satisfied, the standalone path remains permanent.

## AI assistance disclosure

The repository was materially assisted by AI during initial construction, migration tooling, and documentation drafting. Human maintainers inspect primary sources, accept or edit entries, and record review notes. The central Awesome template currently asks submitters to confirm the list **is not AI-generated**. That checkbox cannot be answered truthfully today. Never conceal AI assistance when directly asked.

## Honesty gate

Before any central Awesome submission:

1. Every main-list entry has a documented human primary-source review under `docs/reviews/` or `docs/candidate-reviews/`.
2. Human maintainers independently accept, edit, or remove each entry and take responsibility for selection and wording.
3. The README represents human editorial judgment.
4. If the team cannot truthfully check “Is not AI-generated,” do not submit. Ask central maintainers for clarification or continue standalone.

## Open gaps before any central submission

As of 2026-08-01:

1. **Public maturity** — repository became public on 2026-08-01; earliest eligibility under a 30-day rule is **2026-09-01** (recheck the live rule before submitting).
2. **Non-AI-generated certification** — blocked; see disclosure above.
3. **Independent cross-section sampling** — second-maintainer sampling of section reviews not yet documented.
4. **Peer reviews of other central Awesome PRs** — not started; do not invent reviews.
5. **Duplicate search** — search the central repository and GitHub immediately before submission.
6. **Optional README illustration** — decision not yet recorded.
7. **Sustained responsive maintenance** — ongoing.

## Publication checklist (standalone)

1. Confirm the Quality workflow passes, including catalog validation, unit tests, and native `awesome-lint`.
2. Run the Links workflow manually after publication or URL changes.
3. Keep the GitHub description and topics current.
4. Keep branch protection on `main` requiring the `catalog` and `awesome-lint` jobs and pull requests for changes.
5. Keep the README manually authored; do not add an automatic README renderer.
6. Review every contribution against [editorial policy](../editorial-policy.md) and record limitations in the relevant catalog shard.
7. Regenerate and verify `MANIFEST.json` whenever tracked files change.

## Repository metadata

Description:

```text
Standards and tools that make scientific data, software, workflows, instruments, knowledge systems, and agents work together.
```

Topics: `awesome`, `awesome-list`, `scientific-interoperability`, `research-infrastructure`, `open-science`.

```bash
npx --yes awesome-lint
```

## Release validation matrix

Run against the exact commit to release:

| Check | Command / workflow |
| --- | --- |
| Catalog schema and semantics | `python scripts/validate_catalog.py` |
| Watchlist | `python scripts/validate_watchlist.py` |
| Review freshness | `python scripts/check_review_freshness.py` |
| Unit tests | `python -m unittest discover -s tests -v` |
| Awesome lint | `npx --yes awesome-lint` |
| Offline URL syntax | `python scripts/check_links.py --offline --scope all` |
| Data-quality baseline | `python scripts/audit_data_quality.py --as-of <date> --check-baseline docs/data-quality-baseline.json` |
| Coverage baseline | coverage audit scripts / Quality workflow |
| Manifest integrity | `python scripts/generate_manifest.py` then `python scripts/verify_manifest.py` |
| Network links | Links workflow (manual or scheduled) |

Section and gap review artifacts under `docs/reviews/` and `docs/candidate-reviews/` are the durable human-review record. Do not maintain a parallel batch-coded review diary for merged work.
