# Link Audit Baseline

**Audit date:** 2026-08-01  
**Source run:** GitHub Actions Links workflow on `main` (`30720888543`) before PR-02 classification hardening, plus local classification against the remediated catalog.

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

## Post-remediation expectation

After PR-02 merges, a Links workflow run on the exact head should classify every main-list URL and report zero unresolved blocking failures. JSON and Markdown artifacts are uploaded from `.github/workflows/links.yml`.
