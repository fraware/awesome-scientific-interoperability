# Maintenance Protocol

The project remains useful only when its descriptions, URLs, standards status, and representative choices stay current.

## Every Contribution

1. Inspect primary technical sources.
2. Apply the sentence test from the project charter.
3. Compare the candidate with the strongest existing alternative.
4. Update the README and the relevant catalog shard in the same change.
5. Record the decision basis, limitations, stewardship, `reviewed_on`, and `review_due_on`.
6. Run catalog validation, review freshness, offline URL validation, unit tests, and Awesome lint.
7. Require independent approval when the contributor is affiliated with the resource.

## Monthly

- Triage resource proposals and corrections.
- Resolve broken canonical URLs using the link-classification remediation rules below.
- Review resources reported as archived, deprecated, or superseded.
- Keep the watchlist separate from the main list.

## Quarterly

- Run the network link workflow and download the JSON/Markdown artifacts.
- Remediate unresolved `permanent-failure`, `invalid-url`, and `tls-or-dns-failure` classifications before the next release.
- Review section balance and duplicate functionality.
- Reassess fast-moving laboratory and agent interoperability resources.
- Confirm that validators and conformance suites still reflect current specifications.

## Link Remediation Rules

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

## Release Invariant

The README remains manually authored and authoritative. Structured metadata and automated checks enforce consistency; they never decide inclusion or generate the list.
