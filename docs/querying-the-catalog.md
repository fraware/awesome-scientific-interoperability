# Querying the catalog

The structured catalog supports read-only queries for concrete integration questions. The query tool never modifies the README or catalog files, performs no network access, and does not rank resources automatically. Multiple filters combine with logical **AND**.

The live catalog currently holds **113** resources (as of 2026-08-02). Example result counts below were recomputed against that corpus; they will drift as admissions land—treat them as shape checks, not frozen inventory.

## Quick start

```bash
python scripts/query_catalog.py --section "Workflows and Execution"
python scripts/query_catalog.py --layer Operational
python scripts/query_catalog.py --domain genomics
python scripts/query_catalog.py --connects "workflow registry"
python scripts/query_catalog.py --evidence conformance-suite
python scripts/query_catalog.py --evidence public-validator
python scripts/query_catalog.py --review-type author
python scripts/query_catalog.py --id ro-crate
python scripts/query_catalog.py --format json
```

Make targets:

```bash
make query SECTION="Workflows and Execution"
make query-json LAYER=Operational
make query REVIEW_TYPE=author
make query-json EVIDENCE=public-validator
```

## Filters

| Flag | Matches |
|------|---------|
| `--section` | Exact section name (for example `Workflows and Execution`) |
| `--layer` | One of `Syntactic`, `Semantic`, `Operational`, `Evidentiary`, `Organizational` |
| `--domain` | Domain tag, case-insensitive (for example `genomics`) |
| `--connects` | All query tokens must appear in `connects`, `mechanism`, or `summary` |
| `--evidence` | Evidence type enum (for example `conformance-suite`, `public-validator`) |
| `--review-type` | Review provenance: `author`, `maintainer`, or `independent` |
| `--id` | Exact resource identifier |
| `--format` | `markdown` (default) or `json` |

Results are ordered by section (README order), then canonical name. Markdown output includes **boundary notes** and typed **relations** (`type→resource_id`). `--domain` matches any taxonomy dimension tag (`scientific_domains`, `integration_functions`, `infrastructure_contexts`, or `artifact_classes`).

Valid `--evidence` values: `normative-specification`, `reference-implementation`, `independent-implementation`, `institutional-adoption`, `conformance-suite`, `public-validator`, `interoperability-demonstration`, `documented-tests`.

## Typed relations

Catalog records store edges in a `relations` array of `{type, resource_id}` objects (see [catalog model v2.2](catalog-model-v2.2.md)). Legacy `alternatives` and `related_resource_ids` fields are retired.

JSON query output includes:

- `relations` — full typed edge list
- derived convenience arrays: `alternatives` (from `alternative-to`), `profiles_of` (from `profile-of`), `implements`, `validates`
- `review_type` — from the nested `review` object

The CLI does not expand related IDs into full records; follow up with `--id`.

## Integration query examples

Each example below was run against the live 113-resource catalog on 2026-08-02.

### 1. Which workflow standards support operational portability?

```bash
python scripts/query_catalog.py --section "Workflows and Execution" --layer Operational --format json
```

Returns thirteen resources including CWL, WDL, Nextflow-adjacent runners and registries, and GA4GH WES/TES/DRS APIs. Use this when choosing a workflow language or execution API rather than a packaging profile.

### 2. What genomics infrastructure identifiers and APIs exist?

```bash
python scripts/query_catalog.py --domain genomics --format json
```

Returns sixteen resources spanning GA4GH Service Info, Service Registry, TRS, DRS, Passports, refget, VRS, Phenopackets, and related discovery or representation mechanisms. Narrow further with `--section "Identifiers and Discovery"`.

### 3. Where can I register and discover portable workflows?

```bash
python scripts/query_catalog.py --connects "workflow registry" --format json
```

Returns **WorkflowHub**, which connects workflow definitions, metadata, and registries. The `--connects` flag tokenizes your phrase and requires every token to appear somewhere in the connects list, mechanism, or summary.

### 4. Which resources ship public conformance suites?

```bash
python scripts/query_catalog.py --evidence conformance-suite --format json
```

Returns thirteen resources including CWL, cwltool, GA4GH WES/TES/DRS, SBML, FMI, OGC APIs, and dedicated test-suite entries. Pair with `--layer Operational` to focus on execution-facing standards.

### 5. Which resources expose a public validator?

```bash
python scripts/query_catalog.py --evidence public-validator --format json
```

Returns twenty-three resources with a recorded `public-validator` evidence type. Combine with `--section` or `--domain` to narrow by family.

### 6. How do I package heterogeneous research objects?

```bash
python scripts/query_catalog.py --id ro-crate --format markdown
```

Returns a single record for **RO-Crate** with summary, mechanism, connects, typed relations (including `alternative-to→bagit` and profile complements), and a boundary note distinguishing packaging profiles from execution provenance profiles.

### 7. Which provenance mechanisms cover workflow runs?

```bash
python scripts/query_catalog.py --section "Provenance and Evidence" --layer Evidentiary --format json
```

Returns seven resources including CWLProv, ISO 23494-2, P-Plan, W3C PROV, RunCrate, BioCompute Objects, and SED-ML. Compare boundary notes to see whether you need workflow-plan provenance or run-level RO-Crate profiles.

### 8. Which cross-domain semantic layers apply broadly?

```bash
python scripts/query_catalog.py --layer Semantic --domain cross-domain --format json
```

Returns twenty-two resources including RO-Crate, Schema.org, DCAT, and FAIR Signposting. Useful when the integration problem spans repositories rather than a single domain silo.

### 9. What validators exist for research-object packaging?

```bash
python scripts/query_catalog.py --section "Validation and Conformance" --connects "ro-crate" --format json
```

Returns **RO-Crate Validator**. Combine section and connects filters to stay within validation resources while matching packaging vocabulary.

### 10. Filter by review provenance

```bash
python scripts/query_catalog.py --review-type author --format json
```

Returns resources whose nested `review.review_type` is `author` (currently the full migration-era corpus). Use `maintainer` or `independent` as those provenance classes appear.

### 11. Which metadata bridges help machines navigate repository landing pages?

```bash
python scripts/query_catalog.py --connects "metadata repository" --format json
```

Returns **FAIR Signposting** and **CITATION.cff**—lightweight discovery/citation bridges rather than full packaging standards.

### 12. Which workflow provenance resources mention both provenance and workflow vocabulary?

```bash
python scripts/query_catalog.py --connects "provenance workflow" --format json
```

Returns six resources including Workflow Run RO-Crate, CWLProv, P-Plan, RunCrate, cwltool, and WfExS. Read each boundary note to decide between plan-level, run-level, and language-native provenance.

## JSON output

JSON output is deterministic: resources appear in section/name order with stable field ordering. Pipe to `jq` or other tools for further filtering. The command exits `0` even when no resources match (empty array). Invalid section, evidence, or review-type values exit `2`.

## Downloads

Published catalog dumps are built by `python scripts/export_catalog.py` (or `make export`) into a local `dist/` directory (gitignored). Quality CI runs the same export on every pull request and every push to `main`, then uploads the `catalog-exports` workflow artifact containing:

| Artifact | Purpose |
|----------|---------|
| `catalog.json` | Full joined resources with resolved steward and implementation summaries |
| `catalog.csv` | Flat spreadsheet table |
| `relations.json` | Typed relation edge list for graph tools |
| `catalog.jsonld` | Minimal JSON-LD context over resources and edges |
| `problems.json` | Navigation index parsed from `docs/integration-problems.md` |
| `guides-index.json` | Index parsed from `docs/decision-guides/` |

**Browser / curl path (tagged releases):** after a GitHub Release is published, the same files are attached as release assets. Download without cloning:

```bash
curl -fsSL -O https://github.com/fraware/awesome-scientific-interoperability/releases/latest/download/catalog.json
```

Replace `catalog.json` with any artifact name above. On GitHub, open the latest release page and use the Assets list.

**CI artifact path (every main/PR run):** open the Quality workflow run → Artifacts → `catalog-exports`.

Exports are deterministic for a fixed catalog snapshot (`export_generated_on` appears once under `meta`). They never decide catalog inclusion; the manually curated README and catalog remain authoritative.

## Limitations

- Queries reflect catalog editorial scope only; absence from results does not mean no external tool exists.
- `--connects` is token substring matching, not full-text search ranking.
- The tool does not resolve typed `relations` targets to full records; use `--id` for follow-up lookups.
- For offline bulk use without the query CLI, download the published dumps described under Downloads above.
