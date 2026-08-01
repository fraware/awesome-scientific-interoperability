# Validation Report

**Release:** 1.1.0  
**Validation date:** 2026-08-01  
**Catalog version:** 2.0.0  
**Commit baseline:** PR-20 Awesome submission prep on `main`

## Corpus counts

| Item | Count |
| --- | ---: |
| Main-list catalog entries | 87 |
| README list entries (parity) | 87 |
| Section-scoped resource shards | 11 |
| Watchlist items | 17 |
| Decision guides (excluding README) | 9 |
| Integration problems in problem index | 12 |
| Unit tests (`python -m unittest discover -s tests`) | 64 |

## Completed checks

- JSON Schema validation passed for all **87** catalog entries loaded from **11** section-scoped shards.
- Catalog-index and shard loading passed.
- README and catalog parity passed for name, URL, section, and summary text.
- Duplicate identifier, name, and URL checks passed.
- Summary capitalization, terminal punctuation, length, and promotional-language checks passed.
- Every catalog entry identifies at least two connected objects or systems.
- No legacy v1 catalog fields remain in live shards.
- Contents is the first level-two README section; Contributing and Footnotes are excluded from Contents.
- All **87** canonical URLs passed offline HTTPS syntax validation.
- Problem index, decision guide, and watchlist validation passed.
- Review freshness passed for all **87** resources as of 2026-08-01.
- All **64** repository unit tests passed.
- Manifest covers every tracked file except the manifest itself and verifies SHA-256 digests and byte counts.
- PR-20/21 governance artifacts present: `docs/human-review-log.md`, updated `docs/publishing.md` (standalone mode; central path closed pending gates).

## Awesome lint

- Native `npx --yes awesome-lint` runs in `.github/workflows/quality.yml` and the Makefile. No custom rule filter remains.
- Repository description and topics satisfy the Awesome GitHub metadata rule.

## Checks delegated to GitHub Actions

- Network link validation is configured as a weekly and manually dispatchable workflow in `.github/workflows/links.yml`.

## Release constraints

- This report does **not** claim completeness, certification, or exhaustive landscape coverage.
- Central Awesome submission is **closed pending gates** (PR-21): earliest eligible date **2026-09-01**, and the non-AI-generated requirement cannot be certified truthfully today. See `docs/publishing.md` and `docs/human-review-log.md`.
- The list operates as a standalone Awesome list until maintainers can answer every central template checkbox truthfully or receive clarification from central maintainers.
- No pull request has been opened against `sindresorhus/awesome`.
