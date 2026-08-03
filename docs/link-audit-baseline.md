# Link Audit Baseline

**Audit date:** 2026-08-03
**Latest source run:** GitHub Actions Links workflow on `main` ([run 30789533912](https://github.com/fraware/awesome-scientific-interoperability/actions/runs/30789533912), 2026-08-03T06:14:25Z) after MIAPPE / BrAPI / SBOL admission (#64) and ORKG exception documentation (#65).
**Prior v1.1.0 source run:** `30723706703` (2026-08-01T23:38:21Z).
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

### IUCr CIF landing page (`access-policy`)

- **URL:** `https://www.iucr.org/resources/cif`
- **Classification:** `access-policy` (HTTP 403 to the audit user agent)
- **Rationale:** Canonical IUCr CIF entry; bot 403 is access policy, not disappearance.
- **Review:** Revisit if IUCr publishes a freely reachable normative HTML landing that better serves as the technical entry URL.

### ORKG homepage TLS instability in GitHub Actions (`tls-or-dns-failure`, intermittent)

- **URL:** `https://www.orkg.org/`
- **Classification:** `tls-or-dns-failure` observed in Links run `30760295612` (Connection reset by peer). Subsequent run `30789533912` classifies the same URL as `redirected` (200 → `https://orkg.org/`).
- **Rationale:** The ORKG homepage remains the canonical stewardship/product entry. Do not replace with a secondary DOI or article landing page solely to obtain a bot HTTP 200 under intermittent Actions networking.
- **Review:** Revisit on the next full Links workflow run; replace only if the homepage becomes permanently unreachable outside CI as well.

## Remediation rules applied

1. Inspect official site, specification repository, and redirect destination before changing a URL.
2. Replace a URL only when the new target is more canonical or the old target is permanently broken or TLS-unusable.
3. Preserve valid canonical URLs that return 401/403/429.
4. Record persistent exceptions here with rationale; do not add silent allowlist entries in code.
5. For BrAPI-style API bases that 404 on the module root, prefer a documented discovery path (`serverinfo` / `calls`) that still supports the same operator/implementation claim rather than substituting a homepage.

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

## Post-admission main-list audit (run `30789533912`)

| Classification | Count |
| --- | ---: |
| ok | 106 |
| redirected | 8 |
| access-policy | 2 |
| transient-failure | 0 |
| permanent-failure | 0 |
| tls-or-dns-failure | 0 |
| invalid-url | 0 |

**URLs checked:** 116 main-list canonical URLs (includes MIAPPE, BrAPI, SBOL and other post-v1.1.0 admissions). **Blocking failures:** 0.

Admission canonical URLs in this run:

| URL | Classification |
| --- | --- |
| `https://www.miappe.org/` | ok (200) |
| `https://brapi.org/specification` | ok (200) |
| `https://sbolstandard.org/datamodel-specification/version-3.1.0/` | ok (200) |
| `https://www.orkg.org/` | redirected (200 → `https://orkg.org/`) |

Access-policy responses unchanged: ISO 23494-2 and IUCr CIF.

## MIAPPE / BrAPI / SBOL related-URL live probe (2026-08-03)

Offline expansion scope previously validated syntax only. A focused live probe of **19** admission-related URLs (resource, steward, reference, and implementation URLs for MIAPPE / BrAPI / SBOL) was executed locally with `scripts/check_links.py` classification policy on 2026-08-03.

| Classification | Count | Notes |
| --- | ---: | --- |
| ok | 15 | Includes GitHub repos, MIAPPE/SBOL hubs, BrAPI org pages, isa4j docs, IPK institute homepage |
| redirected | 1 | `https://github.com/plantbreeding/API` → `https://github.com/plantbreeding/BrAPI` (remediated to canonical repo) |
| access-policy | 0* | Cassavabase discovery remapped to `.../brapi/v2/serverinfo` (401) after probe |
| transient-failure | 1 | `https://pysbol3.readthedocs.io/en/stable/validation.html` HTTP 429 — kept; rate limit is not disappearance |
| permanent-failure | 2 (pre-remediation) | Remediated as below |

\* After remediation, Cassavabase classifies as `access-policy` (401) on the discovery URL.

### Permanent failures remediated (same claim preserved)

| Old URL | Observation | Replacement | Claim preserved |
| --- | --- | --- | --- |
| `https://cassavabase.org/brapi/v2/` | HTTP 404 on module root | `https://cassavabase.org/brapi/v2/serverinfo` | Live Cassavabase BrAPI V2 operator endpoint (401 without credentials) |
| `https://webapps.ipk-gatersleben.de/api/brapi/v1/` | HTTP 404; FAIR-IPK Swagger still names `/api` host root but live traffic serves `/brapi/v1/` | `https://webapps.ipk-gatersleben.de/brapi/v1/` | IPK-operated BrAPI V1 germplasm/phenotype service (`/brapi/v1/` and `/brapi/v1/calls` return 200) |
| `https://github.com/plantbreeding/API` | Permanent redirect to renamed repo | `https://github.com/plantbreeding/BrAPI` | Same OpenAPI/spec repository under Plant Breeding API org |

Do **not** replace these API/validator URLs with project homepages solely to obtain HTTP 200.

## Stacked expansion offline scope (2026-08-02)

`python scripts/check_links.py --offline --scope all` validates the syntax of unique HTTPS URLs across canonical + registries. This is an offline structural check, not a replacement for the network audit. Network classifications for the post-admission main list are recorded under run `30789533912` above.

## Post-remediation expectation

A Links workflow run on the exact head should classify every main-list URL and report zero unresolved blocking failures. JSON and Markdown artifacts are uploaded from `.github/workflows/links.yml`. Run `30789533912` satisfies this expectation for the post-admission main-list corpus on `main` at dispatch time; related-URL remediations for BrAPI implementations are tracked in the focused probe section and must land via PR before the next release gate treats those registry URLs as clean.
