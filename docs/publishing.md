# Publishing and Repository Operations

The public repository is:

```text
https://github.com/fraware/awesome-scientific-interoperability
```

## Publication Checklist

1. Confirm the `Quality` workflow passes, including catalog validation, unit tests, and `awesome-lint`.
2. Run the `Links` workflow manually after the initial publication commit.
3. Add the GitHub topics `awesome`, `awesome-list`, `scientific-interoperability`, `research-infrastructure`, and `open-science`.
4. Enable branch protection after the first successful workflow run, requiring the catalog and Awesome lint jobs.
5. Keep the README manually authored; do not add an automatic README renderer.
6. Review every contribution against `docs/editorial-policy.md` and record limitations in the relevant catalog shard.

## Central Awesome Submission

Maintain the repository publicly for at least 30 days, recheck the current central Awesome requirements, review the required peer submissions, and submit only after the repository has demonstrated responsive human maintenance.

## Repository Metadata Required for Awesome Lint

The GitHub repository description and topics cannot be set through the publication connector used for the initial release. Until a maintainer sets them in repository settings, `scripts/run_awesome_lint.mjs` excludes only the `awesome-github` metadata rule while retaining every content and structure rule.

Set the description to:

```text
Standards and tools that make scientific data, software, workflows, instruments, knowledge systems, and agents work together.
```

Add the topics `awesome`, `awesome-list`, `scientific-interoperability`, `research-infrastructure`, and `open-science`. Then remove the single-rule filter from `scripts/run_awesome_lint.mjs`, run the standard `npx --yes awesome-lint`, and rerun the Quality workflow.
