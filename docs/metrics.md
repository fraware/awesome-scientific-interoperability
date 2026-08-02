# Metrics That Matter

Track maintenance and utility—not promotion. Star counts, raw list size, social engagement, and automated quality scores are explicitly out of scope ([editorial policy](editorial-policy.md), [engineering takeover specification](engineering-takeover-specification.md) §14).

## Maintenance metrics

| Metric | Intent |
|--------|--------|
| Percentage of entries reviewed within their required interval | Freshness of human stewardship |
| Unresolved permanent link failures | Integrity of outbound references |
| Median time to triage correction issues | Responsiveness |
| Percentage of entries with independent-implementation evidence | Strength of interoperability claims |
| Percentage with public conformance or validation evidence (`conformance-suite` / `public-validator`) | Verifiability |
| Section and domain concentration | Avoid silent over-representation |
| Watchlist items past due | Boundary hygiene |
| Resource additions, removals, and corrections per release | Change transparency |
| Integration questions answerable through the problem index | Decision coverage |
| PRs with complete source and conflict disclosures | Process integrity |

## Utility evaluation metrics

From [utility-evaluation.md](utility-evaluation.md):

- Task success rate (candidate named that matches guide/catalog intent)
- Median time-to-first-candidate
- Rate of primary-source opens
- Rate of avoided category errors attributed to boundary notes
- Structured satisfaction scores
- Number of steward challenge findings that produce corrections

## Forbidden vanity metrics

Do not optimize or report as success:

- GitHub stars / forks as quality proxies
- Social impressions
- Maximizing main-list size
- Opaque automated “awesome scores”

## Instrumentation notes

Prefer metrics that can be recomputed from repository state, CI artifacts, issue timestamps, and evaluation worksheets. When a metric cannot yet be measured (for example cohort not filled), leave it blank rather than inventing numbers.
