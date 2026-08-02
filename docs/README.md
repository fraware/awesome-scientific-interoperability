# Documentation

Human-oriented documentation for Awesome Scientific Interoperability. Start with the [project charter](project-charter.md) (North Star and sentence test), then use the paths below.

## Decide and explore

| Document | Purpose |
| --- | --- |
| [Integration problems](integration-problems.md) | Concrete scientific integration questions mapped to catalog resources |
| [Decision guides](decision-guides/README.md) | Side-by-side comparisons for packaging, workflows, domains, and access |
| [Querying the catalog](querying-the-catalog.md) | Local read-only queries over the structured catalog |
| [Watchlist](watchlist.md) | Near-miss and emerging resources kept out of the main list |

## Contribute and govern

| Document | Purpose |
| --- | --- |
| [Contributing](../contributing.md) | How to propose resources and run local checks |
| [Editorial policy](editorial-policy.md) | Admission, exclusion, and summary rules |
| [Governance](governance.md) | Roles, approvals, recruitment, and the single-maintainer limitation |
| [Conflicts of interest](conflicts-of-interest.md) | Affiliation disclosure and review rules |
| [Decision records](decision-records.md) | Recurring editorial decisions and notable exclusions |
| [Maintenance](maintenance.md) | Review checklist and recurring maintenance cadence |
| [Taxonomy](taxonomy.md) | Main-list sections and when to reassess them |

## Catalog model

| Document | Purpose |
| --- | --- |
| [Catalog model](catalog-model.md) | Live structured catalog fields, registries, and integrity rules |

## Editorial evidence

Section reviews live under [`reviews/`](reviews/). Gap and expansion reviews live under [`candidate-reviews/`](candidate-reviews/). These are working notes that support inclusion decisions; they are not a second public catalog.

## Maintainers

Release operations, central Awesome submission gates, and evaluation protocol live under [`maintainers/`](maintainers/README.md).

## Baselines

Machine-checked baselines stay in this directory (`data-quality-baseline.*`, `coverage-baseline.*`, `link-audit-baseline.md`). Do not hand-edit the generated JSON without regenerating from the audit scripts.
