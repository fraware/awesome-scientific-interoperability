# Link Audit Baseline

**Audit date:** 2026-08-01
**Latest source run:** GitHub Actions Links workflow on `main` (`30723706703`, 2026-08-01T23:38:21Z) after PR-16D and PR-18 merges.
**Initial source run:** `30720888543` before PR-02 classification hardening, plus local classification against the remediated catalog.

## Policy

Classification is governed by `config/link-policy.yaml`. The checker exits nonzero only for unresolved `invalid-url`, `permanent-failure`, and `tls-or-dns-failure` results. Access-policy responses (401/403) and exhausted transient failures (including 429 and 5xx) are reported but do not fail the audit by themselves.

## Initial live-audit findings on pre-remediation `main`

| URL | Observation | Disposition |
|-----|-------------|-------------|
| `https://autoprotocol.org/` | TLS failure: certificate outside validity period | Replaced canonical URL with `https://github.com/autoprotocol/autoprotocol-python` (maintained technical entry for the language and tooling). README and catalog updated together. |
| `https://www.scholix.org/` | TLS failure: unexpected EOF during handshake | Replaced canonical URL with `https://github.com/scholix/schema` (Scholix Link Information Package schema). Operational hub `https://scholexplorer.openaire.eu/` remains a related access point noted here for maintainers. |
| `https://www.iso.org/standard/87714.html` | HTTP 403 from automated clients | Kept. Canonical ISO catalogue page for ISO 23494-2:2026; classified `access-policy`. |

No 404/410 responses were observed for main-list URLs in the baseline run.

## Accepted exceptions

### ISO 23494-2 catalogue page (`access-policy`)

- **URL:** `https://www.iso.org/standard/87714.html`
- **Classification:** `access-policy` (HTTP 403 to the audit user agent)
- **Rationale:** The ISO store/catalogue URL remains the canonical public identifier for the standard. A 403 from automated fetching is an access-policy response, not evidence that the standard or URL is gone. Do not replace with a secondary summary page solely to obtain HTTP 200 for bots.
- **Review:** Revisit if ISO publishes a freely reachable normative HTML landing page that is more appropriate as the technical entry URL.

## Remediation rules applied

1. Inspect official site, specification repository, and redirect destination before changing a URL.
2. Replace a URL only when the new target is more canonical or the old target is permanently broken or TLS-unusable.
3. Preserve valid canonical URLs that return 401/403/429.
4. Record persistent exceptions here with rationale; do not add silent allowlist entries in code.

## v1.1.0 release audit (run `30723706703`)

| Classification | Count |
| --- | ---: |
| ok | 78 |
| redirected | 7 |
| access-policy | 2 |
| transient-failure | 0 |
| permanent-failure | 0 |
| tls-or-dns-failure | 0 |
| invalid-url | 0 |

**URLs checked:** 87 main-list canonical URLs. **Blocking failures:** 0.

Access-policy responses (unchanged from initial baseline):

- `https://www.iso.org/standard/87714.html` — ISO 23494-2 catalogue page.
- `https://www.iucr.org/resources/cif` — IUCr CIF landing page (added with PR-16B).

Seven URLs returned successful redirects (for example CDIF, COMBINE Archive, DDI Lifecycle, EDAM, EOSC Interoperability Framework, workflow-testing RO-Crate profile, ORKG). These are reported but do not fail the audit.

## Batch A offline scope (2026-08-02)

`python scripts/check_links.py --offline --scope all` validates the syntax of **362 unique HTTPS URLs** on the Batch A candidate tree. This is an offline structural check, not a replacement for the network audit. The historical network classifications below remain limited to the 87-entry v1.1.0 corpus until the Links workflow is run on the new exact head.

## Post-remediation expectation

After PR-02 merges, a Links workflow run on the exact head should classify every main-list URL and report zero unresolved blocking failures. JSON and Markdown artifacts are uploaded from `.github/workflows/links.yml`. Run `30723706703` satisfies this expectation for the v1.1.0 corpus.
