# Validation Report

**Release candidate:** 1.0.0  
**Validation date:** 2026-08-01

## Completed Checks

- JSON Schema validation passed for all 75 catalog entries loaded from 11 section-scoped shards.
- Catalog-index and shard loading passed.
- README and catalog parity passed for name, URL, section, and description.
- Duplicate identifier, name, and URL checks passed.
- Description capitalization, terminal punctuation, length, and promotional-language checks passed.
- Every catalog entry identifies at least two connected objects or systems.
- Contents is the first level-two README section.
- Contributing and Footnotes are excluded from Contents.
- All 75 canonical URLs passed offline HTTPS syntax validation.
- All four repository unit tests passed.
- The release manifest covers every tracked file except the manifest itself and verifies SHA-256 digests and byte counts in CI.
- The repository was initialized on `main` and committed as a clean Git working tree.

## Checks Delegated to GitHub Actions

- `awesome-lint` is configured in `.github/workflows/quality.yml`. The local execution environment could not retrieve the npm package from its internal registry, so this check must run in GitHub Actions after publication.
- Network link validation is configured as a weekly and manually dispatchable workflow in `.github/workflows/links.yml`. The local execution environment has no external DNS access.

## Release Constraint

The repository should not be submitted to the central Awesome index until it has been public and actively maintained for at least 30 days and the current central submission requirements have been rechecked.
