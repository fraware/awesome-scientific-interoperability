# Querying the catalog

The structured catalog supports read-only queries for concrete integration questions. The query tool never modifies the README or catalog files, performs no network access, and does not rank resources automatically. Multiple filters combine with logical **AND**.

## Quick start

```bash
python scripts/query_catalog.py --section "Workflows and Execution"
python scripts/query_catalog.py --layer Operational
python scripts/query_catalog.py --domain genomics
python scripts/query_catalog.py --connects "workflow registry"
python scripts/query_catalog.py --evidence conformance-suite
python scripts/query_catalog.py --id ro-crate
python scripts/query_catalog.py --format json
```

Make targets:

```bash
make query SECTION="Workflows and Execution"
make query-json LAYER=Operational
```

## Filters

| Flag | Matches |
|------|---------|
| `--section` | Exact section name (for example `Workflows and Execution`) |
| `--layer` | One of `Syntactic`, `Semantic`, `Operational`, `Evidentiary`, `Organizational` |
| `--domain` | Domain tag, case-insensitive (for example `genomics`) |
| `--connects` | All query tokens must appear in `connects`, `mechanism`, or `summary` |
| `--evidence` | Evidence type enum (for example `conformance-suite`) |
| `--id` | Exact resource identifier |
| `--format` | `markdown` (default) or `json` |

Results are ordered by section (README order), then canonical name. Markdown output includes **boundary notes** and typed **relations** (`alternative-to`, `profile-of`, `implements`, `validates`, and related edge types).

## Integration query examples

Each example below was run against the live catalog on 2026-08-01.

### 1. Which workflow standards support operational portability?

```bash
python scripts/query_catalog.py --section "Workflows and Execution" --layer Operational --format json
```

Returns eight resources including CWL, WDL, Nextflow, Snakemake, and GA4GH WES/TES APIs. Use this when choosing a workflow language or execution API rather than a packaging profile.

### 2. What genomics infrastructure identifiers and APIs exist?

```bash
python scripts/query_catalog.py --domain genomics --format json
```

Returns ten resources spanning GA4GH Service Info, Service Registry, TRS, DRS, Passports, and related discovery mechanisms. Narrow further with `--section "Identifiers and Discovery"`.

### 3. Where can I register and discover portable workflows?

```bash
python scripts/query_catalog.py --connects "workflow registry" --format json
```

Returns **WorkflowHub**, which connects workflow definitions, metadata, and registries. The `--connects` flag tokenizes your phrase and requires every token to appear somewhere in the connects list, mechanism, or summary.

### 4. Which resources ship public conformance suites?

```bash
python scripts/query_catalog.py --evidence conformance-suite --format json
```

Returns five resources: CWL, cwltool, GA4GH WES, GA4GH TES, and the OpenAPI Specification. Pair with `--layer Operational` to focus on execution-facing standards.

### 5. How do I package heterogeneous research objects?

```bash
python scripts/query_catalog.py --id ro-crate --format markdown
```

Returns a single record for **RO-Crate** with summary, mechanism, connects, alternatives (`bagit`), and a boundary note distinguishing packaging profiles from execution provenance profiles.

### 6. Which provenance mechanisms cover workflow runs?

```bash
python scripts/query_catalog.py --section "Provenance and Evidence" --layer Evidentiary --format json
```

Returns five resources: CWLProv, ISO 23494-2, P-Plan, W3C PROV, and RunCrates. Compare boundary notes to see whether you need workflow-plan provenance or run-level RO-Crate profiles.

### 7. Which cross-domain semantic layers apply broadly?

```bash
python scripts/query_catalog.py --layer Semantic --domain cross-domain --format json
```

Returns seventeen resources including RO-Crate, schema.org, DCAT, and FAIR Signposting. Useful when the integration problem spans repositories rather than a single domain silo.

### 8. What validators exist for research-object packaging?

```bash
python scripts/query_catalog.py --section "Validation and Conformance" --connects "ro-crate" --format json
```

Returns **RO-Crate Validator** plus related conformance tooling in that section. Combine section and connects filters to stay within validation resources while matching packaging vocabulary.

### 9. Which metadata bridges help machines navigate repository landing pages?

```bash
python scripts/query_catalog.py --connects "metadata repository" --format json
```

Returns **FAIR Signposting** and **CITATION.cff**—lightweight discovery/citation bridges rather than full packaging standards.

### 10. Which workflow provenance resources mention both provenance and workflow vocabulary?

```bash
python scripts/query_catalog.py --connects "provenance workflow" --format json
```

Returns six resources including Workflow Run RO-Crate, CWLProv, P-Plan, and WfExS. Read each boundary note to decide between plan-level, run-level, and language-native provenance.

## JSON output

JSON output is deterministic: resources appear in section/name order with stable field ordering. Pipe to `jq` or other tools for further filtering. The command exits `0` even when no resources match (empty array). Invalid section or evidence values exit `2`.

## Limitations

- Queries reflect catalog editorial scope only; absence from results does not mean no external tool exists.
- `--connects` is token substring matching, not full-text search ranking.
- The tool does not resolve `alternatives` or `related_resource_ids` to full records; use `--id` for follow-up lookups.
