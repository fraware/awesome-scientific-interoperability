# Maintenance

The list stays useful only when descriptions, URLs, standards status, and representative choices stay current. Roles and approvals are in [governance](governance.md). Recurring editorial decisions are in [decision records](decision-records.md).

## Review checklist

### Scope

- [ ] The entry enables a concrete relationship between independently developed scientific objects or systems.
- [ ] The documented mechanism can be named precisely.
- [ ] The proposed section is the single best primary location.

### Technical substance

- [ ] Primary technical documentation was inspected.
- [ ] A specification, implementation, schema, ontology, API, validator, mapping, or test suite is publicly available.
- [ ] The contribution is reusable beyond one private deployment.

### Quality

- [ ] The resource is among the strongest current examples for its function.
- [ ] A stronger included resource does not make it redundant.
- [ ] The `summary` states the actual interoperability contribution without promotional language and matches the README sentence.

### Maintenance signals

- [ ] Stewardship is credible and recorded via `steward_id`.
- [ ] The resource is not archived, deprecated, or materially undocumented.
- [ ] `reviewed_on` and `review_due_on` are recorded; `review_due_on` is later than `reviewed_on` and within the allowed interval for maturity and section.
- [ ] `primary_source_inspected` is true and `source_refs` list inspected primary technical sources.

### Integrity

- [ ] Contributor and reviewer affiliations are disclosed.
- [ ] An affiliated reviewer is not the sole approver.
- [ ] Limitations and boundary conditions are recorded.

## Every contribution

1. Inspect primary technical sources.
2. Apply the sentence test from the [project charter](project-charter.md).
3. Compare the candidate with the strongest existing alternative.
4. Update the README and the relevant catalog shard in the same change.
5. Record the decision basis, limitations, stewardship, `reviewed_on`, and `review_due_on`.
6. Run catalog validation, watchlist validation, review freshness, offline URL validation, unit tests, and Awesome lint.
7. Require independent approval when the contributor is affiliated with the resource ([conflicts of interest](conflicts-of-interest.md)).
8. Match the change type to the [approval matrix](governance.md#approval-matrix) before merge.

## Monthly

- Triage resource proposals and corrections.
- Resolve broken canonical URLs using the link-remediation rules below.
- Review resources reported as archived, deprecated, or superseded.
- Keep the watchlist separate from the main list and current in `catalog/watchlist.yaml` and `docs/watchlist.md`.

## Quarterly

- Run the network link workflow and download the JSON/Markdown artifacts.
- Remediate unresolved `permanent-failure`, `invalid-url`, and `tls-or-dns-failure` classifications before the next release.
- Run a full-scope offline reference audit (`python scripts/check_links.py --offline --scope all`) and refresh `docs/data-quality-baseline.md` / `docs/data-quality-baseline.json` from `python scripts/audit_data_quality.py --as-of <review-date> --write-baseline docs/data-quality-baseline.json`.
- Review section balance and duplicate functionality.
- Reassess fast-moving laboratory and agent interoperability resources.
- Confirm that validators and conformance suites still reflect current specifications.
- Treat unsupported `multiple-independent` and `documented-tests` depth regressions as merge-blocking. Do not weaken thresholds to clear queues.

## Link remediation

Network audits classify each main-list URL as one of: `ok`, `redirected`, `access-policy`, `transient-failure`, `permanent-failure`, `tls-or-dns-failure`, or `invalid-url` (`config/link-policy.yaml`, `scripts/check_links.py`).

1. Inspect the project’s official site, specification repository, and redirect destination before changing a URL.
2. Replace a URL only when the new target is more canonical or the old target is permanently broken or TLS/DNS-unusable.
3. Preserve a valid canonical URL that returns 401, 403, or 429 when the response is an access policy or rate limit.
4. Record persistent exceptions in `docs/link-audit-baseline.md` with rationale; do not add a silent allowlist without documented justification.
5. Update README and the relevant catalog shard together whenever a canonical URL changes.

## Annually

- Re-review every main-list entry.
- Move obsolete resources to `archive.md` with the date and reason.
- Recheck the taxonomy and admission rules against the North Star.
- Confirm that the catalog schema and contribution templates still support the editorial process.
- Reassess whether `config/catalog-taxonomy.yaml` domains should gain an optional hierarchy as a separate taxonomy change—do not mix ontology redesign with evidence edits.

## Invariants

The README remains manually authored and authoritative. Structured metadata and automated checks enforce consistency; they never decide inclusion or generate the list. Maintainers decide inclusion, removal, watchlist placement, taxonomy, and release timing.
