# Publishing and Repository Operations

The public repository is:

```text
https://github.com/fraware/awesome-scientific-interoperability
```

## Publication Checklist

1. Confirm the `Quality` workflow passes, including catalog validation, unit tests, and native `awesome-lint`.
2. Run the `Links` workflow manually after publication or URL changes.
3. Keep the GitHub description and topics current (required for the Awesome GitHub metadata rule).
4. Keep branch protection on `main` requiring the `catalog` and `awesome-lint` jobs and pull requests for changes.
5. Keep the README manually authored; do not add an automatic README renderer.
6. Review every contribution against `docs/editorial-policy.md` and record limitations in the relevant catalog shard.

## Repository Metadata

Description:

```text
Standards and tools that make scientific data, software, workflows, instruments, knowledge systems, and agents work together.
```

Topics: `awesome`, `awesome-list`, `scientific-interoperability`, `research-infrastructure`, `open-science`.

Run the unmodified linter locally and in CI:

```bash
npx --yes awesome-lint
```

## Central Awesome Submission

Maintain the repository publicly for at least 30 days, recheck the current central Awesome requirements, review the required peer submissions, and submit only after the repository has demonstrated responsive human maintenance. Do not certify non-AI-generated content unless that statement can be made truthfully; see `docs/engineering-takeover-specification.md` PR-20.
