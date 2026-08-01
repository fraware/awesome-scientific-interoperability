# Contributing

Contributions should improve the list's ability to answer concrete scientific integration questions. Link-only proposals are rejected.

## Propose a Resource

Use the resource-proposal issue form or open a pull request that updates `README.md` and the relevant file under `catalog/resources/`. Update `catalog/resources.yaml` only when adding, removing, or renaming a catalog shard.

Resources that do not yet satisfy the main-list bar belong on the structured watchlist (`catalog/watchlist.yaml` and `docs/watchlist.md`), not in the README or main catalog. Watchlist items do not count toward the 75 main-list records.

A proposal must state:

1. What scientific objects or systems interoperate.
2. Which documented mechanism enables the relationship.
3. Which primary technical sources were inspected.
4. Why the resource is among the strongest available examples.
5. How the resource differs from existing entries.
6. Current maintenance or stewardship evidence.
7. Known limitations.
8. Any contributor affiliation or conflict of interest.

## Editorial Requirements

- Use the canonical project or specification URL.
- Place the entry in one primary section.
- Write one concise, objective sentence ending with a period.
- Avoid taglines, marketing adjectives, star counts, funding claims, and unsupported adoption claims.
- Update the relevant catalog shard with the same name, URL, section, and `summary` (README parity).
- Populate v2 catalog fields: `maturity`, `evidence_types`, `implementation_status`, `conformance_status`, `stewardship`, `domains`, `source_urls`, `alternatives`, `related_resource_ids`, `reviewed_on`, and `review_due_on`.
- For watchlist placement instead of main-list inclusion, update `catalog/watchlist.yaml` and `docs/watchlist.md` together with `candidate_section`, `status`, `reason`, review dates, promotion conditions, and rejection conditions.
- Run the repository checks before submitting.

## Human Responsibility

Fully automated or unreviewed AI-generated submissions are rejected. Assistive tools may support discovery, comparison, or drafting, but the contributor must inspect the primary sources, verify every factual claim, and accept responsibility for the final text.

## Local Checks

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_catalog.py
python scripts/validate_watchlist.py
python scripts/check_review_freshness.py
python -m unittest discover -s tests -v
npx --yes awesome-lint
```

The link checker can be run separately:

```bash
python scripts/check_links.py
```
