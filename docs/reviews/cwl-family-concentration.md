# CWL family concentration adjudication

**Date:** 2026-08-02  
**Policy:** `config/coverage-policy.yaml` role buckets (`runner`, `conformance`, `multi-engine-service`) with `max_per_family_role_bucket: 2`.

## Why these entries remain top-level

| Resource | Kind | Role bucket | Why retain as main-list entry |
|---|---|---|---|
| `common-workflow-language-cwl` | workflow-language | (standard, not counted) | Normative language users must discover first |
| `cwltool` | implementation | runner | Reference runner with decision value distinct from the language |
| `cwl-conformance-tests` | conformance-artifact | conformance | Public suite users need without collapsing into language prose |
| `cwlprov` | provenance-model | (not implementation-like) | Provenance profile spanning W3C PROV + CWL |
| `lifemonitor` | execution-service | multi-engine-service | Monitoring/test orchestration service, not a CWL runner |
| `sapporo` | implementation | runner | WES-oriented multi-engine service with CWL execution path |

Typed relations already connect runners/validators/services (`implements`, `validates`, `executes`) without requiring collapse into a single README slot.

## Concentration outcome

Under undifferentiated counting, CWL had four implementation-like kinds (threshold 2). Under role-sensitive buckets, no single bucket exceeds threshold 2, so the prior `implementation-family-concentration` warning is cleared by policy alignment rather than corpus deletion.
