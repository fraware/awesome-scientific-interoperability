# Candidate review: statistical and social-science interoperability gaps

**Review date:** 2026-08-01  
**Specification:** PR-16A (`docs/engineering-takeover-specification.md`)  
**Reviewer scope:** Mandatory candidates for statistical and social-science data exchange  
**Inclusion cap:** 3 main-list additions

## Corpus context

The main list already includes [resource:ddi-lifecycle] for social-science lifecycle metadata, [resource:w3c-data-catalog-vocabulary-dcat] for federated catalog discovery, [resource:simple-knowledge-organization-system-skos] for vocabulary exchange, and [resource:croissant] for ML dataset descriptions. This review asks which additional mechanisms materially improve integration decisions for official statistics, survey microdata, and multidimensional statistical cubes.

## Evaluation method

For each candidate the review applied the sentence test (*Resource enables X to exchange, interpret, execute, preserve, or compose with Y through documented mechanism Z*), inspected primary stewardship and specification sources, compared overlap with existing entries, and recorded implementation and conformance evidence only where primary sources document it.

## Candidate outcomes

| Candidate | Outcome | Rationale summary |
| --- | --- | --- |
| SDMX (Statistical Data and Metadata eXchange) | **include** | ISO 17369 statistical exchange with REST/JSON, global DSD governance, distinct from DDI Lifecycle and DCAT |
| DDI Cross Domain Integration (DDI-CDI) 1.0 | **watchlist** | Published v1.0 model complements DDI Lifecycle but independent production adoption remains early |
| RDF Data Cube Vocabulary (W3C) | **exclude** | Linked-data cube serialization subsumed for integration decisions by SDMX operational exchange and existing DCAT/SKOS |
| SDMX-JSON / SDMX-ML profiles (as separate entries) | **exclude** | Transmission formats are part of the SDMX standard family, not separate interoperability mechanisms |
| CSVW (CSV on the Web) | **exclude** | General tabular metadata; does not meet the selective bar relative to DDI and SDMX for this corpus |

---

## SDMX — include

**Sentence test:** SDMX enables national statistical offices, international agencies, and downstream analysis systems to exchange aggregated statistical data and structural metadata through documented information-model, REST API, and transmission-format contracts.

**Primary sources inspected:**

- [SDMX standards page](https://sdmx.org/standards-2/) — SDMX 3.1 technical specifications released May 2025; ISO 17369 lineage documented
- [SDMX 3.1 Framework Section 1 (FINAL PDF)](https://sdmx.org/wp-content/uploads/SDMX_3-1-0_SECTION_1_FINAL.pdf) — information model, REST API, SDMX-JSON and SDMX-ML transmission formats
- [SDMX governance of artefacts (Ownership Group ToR)](https://sdmx.org/wp-content/uploads/SDMX-MES_OG_TermsOfReference.pdf) — global Data Structure Definition maintenance through domain Ownership Groups and the SDMX Global Registry

**Stewardship:** SDMX initiative with seven sponsor organizations (BIS, ECB, Eurostat, IMF, OECD, World Bank, UN); Technical Working Group and Statistical Working Group under a Sponsors Committee.

**Implementation evidence:** Multiple independent implementations documented on sdmx.org (reference tools, global registry, national statistical office deployments). `implementation_status: multiple-independent`.

**Conformance evidence:** SDMX conformance guidelines and executable tests are published for structure and REST API conformance classes; `conformance_status: documented-tests` (not a single public suite URL equivalent to CWL Conformance Tests).

**Comparison with existing entries:**

| Existing entry | Relationship |
| --- | --- |
| [resource:ddi-lifecycle] | DDI Lifecycle documents social-science study design, waves, and dissemination lifecycle; SDMX addresses operational exchange of statistical structures and time-series or cube data among producers and consumers |
| [resource:w3c-data-catalog-vocabulary-dcat] | DCAT describes catalog-level dataset and distribution metadata; SDMX supplies the structural metadata and payload contracts for statistical datasets themselves |
| [resource:simple-knowledge-organization-system-skos] | SKOS publishes concept schemes; SDMX uses coded classifications within DSDs but is not a general thesaurus standard |

**Decision basis:** SDMX is the strongest documented contract when integrating official statistics, macroeconomic indicators, or cross-national statistical feeds where producers and consumers must share Data Structure Definitions, constraints, and payload formats.

**Boundary note:** Not a survey-instrument or wave-level metadata standard; pair with [resource:ddi-lifecycle] when study documentation must travel with statistical payloads. Not a general-purpose research-object packaging mechanism.

---

## DDI Cross Domain Integration (DDI-CDI) 1.0 — watchlist

**Sentence test:** DDI-CDI enables systems describing research data across domains to exchange datum-level structure and process metadata through a UML-based model with XML and JSON serializations.

**Primary sources inspected:**

- [DDI-CDI product page](https://ddialliance.org/ddi-cdi) — v1.0 (2025), model-driven, domain-neutral datum and process description
- [DDI-CDI Model Specification 1.0 PDF](https://ddialliance.org/hubfs/Specification/DDI-CDI/1.0/DDI-CDI_Model_Specification.pdf) — complements DDI-Codebook and DDI-Lifecycle; integrates with CDIF Integration Profile
- [Publication announcement](https://ddialliance.org/news/announcing-the-publication-of-ddi-cdi-version-1.0) — January 2025 release after multi-year working-group process
- [GitHub specification repository](https://github.com/ddi-cdi/ddi-cdi)

**Stewardship:** DDI Alliance (consortium).

**Implementation evidence:** Reference schemas and documentation are public; independent production deployments beyond pilot integrations are not yet documented at the level required for main-list inclusion. `needs-evidence`.

**Comparison:** DDI-CDI explicitly complements [resource:ddi-lifecycle] rather than replacing it. CDIF already references DDI-CDI in its Integration Profile; adding DDI-CDI now would duplicate framing without new operational evidence.

**Watchlist record:** `ddi-cross-domain-integration-ddi-cdi` in `catalog/watchlist.yaml`.

**Promotion conditions:** Multiple independent archives or integration pipelines publish and consume DDI-CDI serializations in production; public validators or documented conformance tests beyond JSON Schema; boundary analysis showing distinct value from DDI Lifecycle for cross-domain datum integration.

**Rejection conditions:** Remains a specification without substantive adoption; absorbed entirely into DDI Lifecycle product suite updates without a distinct mechanism.

---

## RDF Data Cube Vocabulary — exclude

**Primary sources inspected:**

- [W3C RDF Data Cube Recommendation](https://www.w3.org/TR/vocab-data-cube/) — cube model compatible with SDMX
- [Data Cube use cases](https://www.w3.org/TR/vocab-data-cube-use-cases/)

**Rationale:** The vocabulary publishes multidimensional statistical observations as Linked Data. For the integration problems this list prioritizes—operational exchange among statistical producers and consumers—SDMX provides the stronger, ISO-backed contract including REST APIs and global DSD governance. RDF Data Cube remains valuable for RDF-native open-data portals but does not add a decision the corpus lacks once SDMX is present alongside [resource:w3c-data-catalog-vocabulary-dcat] and [resource:simple-knowledge-organization-system-skos]. Recorded in `docs/source-notes.md` to prevent repeated evaluation.

---

## North-Star effect

Including SDMX lets integrators choose between DDI Lifecycle (study lifecycle documentation), DCAT (catalog discovery), and SDMX (statistical structure and payload exchange) without conflating them. Watchlisting DDI-CDI preserves a timed reassessment path for cross-domain datum integration as implementations mature.

## Conflict disclosure

None.
