# Validation Report

**Release:** 1.1.0  
**Validation date:** 2026-08-01  
**Catalog version:** 2.0.0  
**Commit baseline:** post PR-18 merge on `main` (includes PR-20 publishing prep)

## Corpus counts

| Item | Count |
| --- | ---: |
| Main-list catalog entries | 87 |
| README list entries (parity) | 87 |
| Section-scoped resource shards | 11 |
| Watchlist items | 17 |
| Decision guides (excluding README) | 9 |
| Integration problems in problem index | 12 |
| v2 schema validation fixtures | 14+ |
| Watchlist validation fixtures | 3 |
| Unit tests (`python -m unittest discover -s tests`) | 64 |

## Completed checks

- JSON Schema validation passed for all **87** catalog entries loaded from **11** section-scoped shards.
- Catalog-index and shard loading passed (`catalog/resources.yaml` lists 11 files; each shard present).
- README and catalog parity passed for name, URL, section, and summary text.
- Duplicate identifier, name, and URL checks passed.
- Summary capitalization, terminal punctuation, length, and promotional-language checks passed.
- Every catalog entry identifies at least two connected objects or systems.
- No legacy v1 catalog fields remain in live shards.
- Contents is the first level-two README section; Contributing and Footnotes are excluded from Contents.
- All **87** canonical URLs passed offline HTTPS syntax validation.
- Problem index validation passed (`docs/integration-problems.md`).
- Decision guide validation passed (nine guides under `docs/decision-guides/`).
- Watchlist schema and README parity passed (**17** items).
- Review freshness passed for all **87** resources as of 2026-08-01.
- Coverage audit integrity checks passed; editorial warnings only (CWL implementation-family concentration; **18** isolated entries).
- All **64** repository unit tests passed on Python 3.13.
- Manifest covers every tracked file except the manifest itself and verifies SHA-256 digests and byte counts.
- Governance files present: `docs/reviewer-roles.md`, `.github/CODEOWNERS`, `docs/decision-records.md`, `docs/human-review-log.md`.
- PR-20/21 publishing prep recorded in `docs/publishing.md` (standalone mode; central path closed pending gates).

## Network link audit

- **Workflow:** `.github/workflows/links.yml` (manual dispatch on `main`).
- **Run ID:** `30723706703` (2026-08-01T23:38:21Z).
- **URLs checked:** 87.
- **Blocking failures:** 0 (`permanent-failure`, `tls-or-dns-failure`, `invalid-url`).
- **Classifications:** 78 ok, 7 redirected, 2 access-policy (ISO 23494-2 catalogue page; IUCr CIF page), 0 transient-failure.
- Baseline recorded in `docs/link-audit-baseline.md`.

## Awesome lint

- Native `npx --yes awesome-lint` runs in `.github/workflows/quality.yml` and the Makefile. No custom rule filter remains.
- Repository description and topics satisfy the Awesome GitHub metadata rule.

## Quality CI alignment (§13 intent)

The Quality workflow implements these logically separate checks:

| §13 step | Implementation |
| --- | --- |
| Catalog and schema validation | `scripts/validate_catalog.py` |
| Unit tests | `python -m unittest discover -s tests` |
| Offline URL validation | `scripts/check_links.py --offline` |
| Problem-index and decision-guide reference validation | `validate_problem_index.py`, `validate_decision_guides.py` |
| Watchlist validation | `scripts/validate_watchlist.py` |
| Review freshness | `scripts/check_review_freshness.py` |
| Coverage invariant checks | `scripts/audit_coverage.py` |
| Manifest verification | `scripts/verify_manifest.py` |
| Standard Awesome lint | separate `awesome-lint` job |

Network link validation is delegated to the scheduled Links workflow; it does not mutate the repository.

## Test architecture (§12)

| Required module | Status |
| --- | --- |
| Catalog loading and shard integrity | `tests/test_catalog.py` |
| JSON Schema validation | `tests/test_catalog.py` (fixtures + live catalog) |
| README parsing and parity | `tests/test_catalog.py` |
| Duplicate IDs, names, URLs | `tests/test_catalog.py` (`test_repository_invariants`) |
| Cross-reference resolution | `tests/test_catalog.py` (fixtures) |
| Review-date freshness | `tests/test_catalog.py` (`ReviewFreshnessTests`) |
| Evidence/source consistency | Partial — `tests/test_coverage_audit.py` fixture `evidence-without-source`; no dedicated standalone module |
| Link-policy classification | `tests/test_links.py` |
| Problem-index resource references | `tests/test_problem_index.py` |
| Decision-guide resource references | `tests/test_decision_guides.py` |
| Watchlist schema and parity | `tests/test_watchlist.py` |
| Coverage-audit determinism | `tests/test_coverage_audit.py` |
| Manifest generation and verification | CI scripts only (`generate_manifest.py`, `verify_manifest.py`); **no dedicated test module** |
| Query CLI behavior | `tests/test_query_catalog.py` |

## Archive

No main-list resources were removed in this release cycle. See `archive.md`.

## Release constraints

- This report does **not** claim completeness, certification, or exhaustive landscape coverage.
- Central Awesome submission is **closed pending gates** (PR-21): earliest eligible date **2026-09-01**, and the non-AI-generated requirement cannot be certified truthfully today. See `docs/publishing.md` and `docs/human-review-log.md`.
- The list operates as a standalone Awesome list until maintainers can answer every central template checkbox truthfully or receive clarification from central maintainers.
- No pull request has been opened against `sindresorhus/awesome`.
