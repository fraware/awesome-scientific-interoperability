# Maintainer sign-off: MIAPPE, BrAPI, SBOL

**Prepared:** 2026-08-03  
**Catalog IDs:** `minimum-information-about-plant-phenotyping-experiments-miappe`, `breeding-api-brapi`, `synthetic-biology-open-language-sbol`  
**Admission PR:** [#64](https://github.com/fraware/awesome-scientific-interoperability/pull/64)  
**Live Links run (main-list):** [30789533912](https://github.com/fraware/awesome-scientific-interoperability/actions/runs/30789533912)  
**Evidence class today:** AI-assisted **author** review only. Do **not** set `review_type: independent` unless a distinct human completes review.  
**Human action required:** Lead maintainer [@fraware](https://github.com/fraware) (or designated section reviewer) must execute the checklist below and record the outcome in the linked GitHub issue.

This dossier is a reproducible packet, not a fabricated approval. Rows are `Pass` / `Fail` / `Needs-judgment` based on primary-source inspection on 2026-08-03.

---

## Shared prerequisites

| Check | Result | Notes |
| --- | --- | --- |
| Main-list Links workflow zero blocking failures | Pass | Run `30789533912`: ok=106, redirected=8, access-policy=2, permanent/tls/invalid=0 |
| Admission-related permanent URL failures remediated | Pass (pending merge) | Cassavabase → `/brapi/v2/serverinfo`; IPK → `/brapi/v1/`; PlantBreeding repo → `plantbreeding/BrAPI` (see [link-audit-baseline](../link-audit-baseline.md)) |
| `review_type` remains `author` until human signs | Pass | All three records still declare author review + pending maintainer approval |
| Optional peer review not claimed complete | Pass | Recruitment / invitation issues only; no invented reviewers |

---

## 1. MIAPPE (`minimum-information-about-plant-phenotyping-experiments-miappe`)

### Normative identity

| Field | Catalog claim | Primary source | Result |
| --- | --- | --- | --- |
| Canonical URL | `https://www.miappe.org/` | MIAPPE homepage (EMBL-EBI hosted) describes checklist + data model for plant phenotyping | Pass |
| Normative version | Not pinned in resource name; releases page is technical-definition | [Releases](https://www.miappe.org/releases/): **v1.2 (October 2024)** current; v1.1 (2019) still documented | Needs-judgment |
| Steward | `miappe-community` → `https://www.miappe.org/` | Community-driven standard; contributions via mailing list / GitHub | Pass |
| Section | Metadata and Semantics | Fits minimum-information / metadata-standard role beside MIxS, EML, ISA-JSON | Pass |

### Sentence test and placement

| Check | Result | Notes |
| --- | --- | --- |
| Sentence test | Pass | README/summary names plant phenotyping experiment metadata (environments, treatments, observation units, phenotypes) |
| Strongest-example vs neighbors | Pass | Distinct from EML (ecology datasets), MIxS (sequence-context), BrAPI (breeding API transport) |
| Decision guide / integration problems | Pass | Listed in [ecology-and-sequence-context-metadata.md](../decision-guides/ecology-and-sequence-context-metadata.md) and [integration-problems.md](../integration-problems.md) |

### Claim-level URL support

| Claim / role | URL | Supports exact claim? | Result |
| --- | --- | --- | --- |
| stewardship | `https://www.miappe.org/` | Project hub and community entry | Pass |
| technical-definition | `https://www.miappe.org/releases/` | Versioned releases including v1.2 | Pass |
| technical-definition | `https://github.com/MIAPPE/MIAPPE` | Spec/checklist repository | Pass |
| implementation | `https://github.com/MIAPPE/ISA-Tab-for-plant-phenotyping` | ISA-Tab configurations for plant phenotyping | Pass |
| conformance | `https://ipk-bit.github.io/isa4j/miappe-validation.html` | Documents **MIAPPE v1.1** field validation via isa4j | Pass (bounded) |

### Implementation independence and conformance boundary

| Check | Result | Notes |
| --- | --- | --- |
| `implementation_status: reference-and-others` | Pass | ISA-Tab configs share MIAPPE stewardship; isa4j is IPK (`ipk-gatersleben`) — not inflated to MI |
| `conformance_status: public-validator` | Pass with residual risk | Validator is real and public; bound to **v1.1 configuration checks** while current release is **v1.2** (compatible per MIAPPE release notes, but not a v1.2-specific suite) |
| Boundary note honesty | Pass | Explicitly limits validator evidence to configured ISA/MIAPPE field checks |

### Relations

| Edge | Result | Notes |
| --- | --- | --- |
| complements BrAPI, ISA-JSON, EML, MIxS | Pass | Matches MIAPPE site mapping note (ISA-Tools, BrAPI) and catalog decision guides |

### Residual risks / recommended downgrades

- Consider pinning `supported` normative version text in `boundary_note` to “current release v1.2; public validator evidence inspected for v1.1 configurations” if maintainers want zero ambiguity (optional clarity, not a Fail).
- Do **not** upgrade to `multiple-independent` without a second non-steward implementation registered with distinct `operator_steward_id`.

---

## 2. BrAPI (`breeding-api-brapi`)

### Normative identity

| Field | Catalog claim | Primary source | Result |
| --- | --- | --- | --- |
| Canonical URL | `https://brapi.org/specification` | Spec index; **V2.1** marked Latest Stable Release (2022-07-01) | Pass |
| Steward | `brapi-community` → `https://brapi.org/` | Community project / plantbreeding org | Pass |
| Section | Workflows and Execution | API transport among breeding systems; peers GA4GH DRS/WES-style operational contracts | Needs-judgment |
| Spec repo | `https://github.com/plantbreeding/BrAPI` | Canonical renamed repo (was `/API`) | Pass |

### Sentence test and placement

| Check | Result | Notes |
| --- | --- | --- |
| Sentence test | Pass | REST API for germplasm, trials, phenotypes, genotypes across independently operated databases |
| Complementary to MIAPPE | Pass | MIAPPE site and catalog both treat BrAPI as exchange/API layer vs metadata completeness |
| Decision guide pointer | Pass | Ecology/sequence-context guide + integration-problems plant phenotyping/breeding row |

### Claim-level URL support

| Claim / role | URL | Supports exact claim? | Result |
| --- | --- | --- | --- |
| technical-definition | `https://brapi.org/specification` | Versioned module specs (Core, Phenotyping, Genotyping, Germplasm) | Pass |
| stewardship | `https://brapi.org/` | Project hub | Pass |
| technical-definition | `https://github.com/plantbreeding/BrAPI` | OpenAPI/source repo | Pass |
| implementation | `https://cassavabase.org/brapi/v2/serverinfo` | Live V2 discovery; **401** without credentials (access-policy) | Pass |
| implementation | `https://webapps.ipk-gatersleben.de/brapi/v1/` | Live V1 base; **200** (and `/calls` **200**) | Pass |
| adoption | `https://brapi.org/servers` | Public servers directory listing Cassavabase (BTI) and IPK among others | Pass |

### Implementation independence and conformance boundary

| Check | Result | Notes |
| --- | --- | --- |
| `implementation_status: multiple-independent` | Pass | Operators `boyce-thompson-institute` (Cassavabase) and `ipk-gatersleben` are distinct from each other and from `brapi-community` |
| Operators not same steward family | Pass | BrAPI servers directory: Cassavabase hosted by Boyce Thompson Institute; IPK by IPK-Gatersleben |
| `conformance_status: none-known` | Pass | No cataloged public BrAPI conformance suite claimed; BRAVA exists as tooling but is not asserted as catalog conformance evidence |
| Boundary note honesty | Pass | States no public suite claimed; cites Cassavabase + IPK for independence |

### Relations

| Edge | Result | Notes |
| --- | --- | --- |
| complements MIAPPE, ISA-JSON | Pass | Correct layering (API vs metadata checklist / multi-assay model) |

### Residual risks / recommended downgrades

- Cassavabase module root 404 is expected; discovery URL returns 401 — document, do not substitute homepage.
- BrAPI servers directory may still advertise the obsolete IPK `/api/brapi/v1/` path; catalog uses the live `/brapi/v1/` path verified 2026-08-03.
- Section placement in Workflows vs Data remains a maintainer judgment call; do not block on it unless a reviewer prefers relocation.
- If either operator endpoint becomes permanently unreachable outside access-policy responses, **downgrade** to `reference-and-others` rather than retaining MI.

---

## 3. SBOL (`synthetic-biology-open-language-sbol`)

### Normative identity

| Field | Catalog claim | Primary source | Result |
| --- | --- | --- | --- |
| Canonical URL | `https://sbolstandard.org/datamodel-specification/version-3.1.0/` | SBOL Data Model **Version 3.1.0** (2022-10-26), includes complete validation rules | Pass |
| Steward | `sbol-community` / SynBioDex | `https://sbolstandard.org/` + SynBioDex org | Pass |
| Section | Data and Digital Objects | Design-exchange format beside SBML/CellML/COMBINE | Pass |

### Sentence test and placement

| Check | Result | Notes |
| --- | --- | --- |
| Sentence test | Pass | Genetic design exchange (components, sequences, interactions, constraints, provenance) |
| Distinct from SBML/CellML | Pass | Decision guide and integration-problems treat SBOL as design intent, not executable math models |
| Decision guide pointer | Pass | [systems-biology-models.md](../decision-guides/systems-biology-models.md) |

### Claim-level URL support

| Claim / role | URL | Supports exact claim? | Result |
| --- | --- | --- | --- |
| technical-definition | version 3.1.0 page | Normative data model + validation rules | Pass |
| stewardship | `https://sbolstandard.org/` | Project hub | Pass |
| technical-definition | `https://github.com/SynBioDex/SBOL-specification` | Spec source | Pass |
| implementation | `https://github.com/SynBioDex/pySBOL3` | Python SBOL 3 library | Pass |
| conformance | `https://pysbol3.readthedocs.io/en/stable/validation.html` | Validation docs (live probe saw transient **429**; keep URL) | Pass (transient) |
| implementation | `https://github.com/SynBioDex/libSBOLj3` | Java SBOL 3 library | Pass |

### Implementation independence and conformance boundary

| Check | Result | Notes |
| --- | --- | --- |
| `implementation_status: reference-and-others` | Pass | pySBOL3 and libSBOLj3 both `operator_steward_id: sbol-community` — correctly **not** MI |
| `conformance_status: public-validator` | Pass | Library validation reports / rules; does not prove biological correctness |
| Boundary note honesty | Pass | States validation ≠ biological correctness; same-steward dual libs not counted independent |

### Relations

| Edge | Pre-fix | Post-fix | Result |
| --- | --- | --- | --- |
| complements SBML | complements | complements | Pass |
| complements COMBINE Archive | complements | complements | Pass |
| relation to CellML | **alternative-to** (incorrect: different integration job) | **complements** | Pass after fix |

`alternative-to` means competing mechanism for a similar integration job (`config/catalog-taxonomy.yaml`). SBOL design exchange is not an alternative to CellML physiological models; the admission incorrectly mirrored SBML↔CellML. Fixed in the accompanying remediation PR.

### Residual risks / recommended downgrades

- Keep `reference-and-others`; do not promote MI without two non-SynBioDex operators.
- pySBOL3 docs may rate-limit (`429`); treat as transient, not a URL replacement trigger.

---

## Maintainer Sign-off Checklist (executable)

Copy this block into the GitHub issue and check boxes only after **human** inspection of primary sources.

### Process gates

- [ ] I inspected primary sources for all three catalog IDs (not README alone).
- [ ] I reviewed Links run [30789533912](https://github.com/fraware/awesome-scientific-interoperability/actions/runs/30789533912) and the related-URL remediations in `docs/link-audit-baseline.md`.
- [ ] I confirm no `review_type: independent` claim is being recorded by this sign-off alone.
- [ ] Affiliated conflicts (if any) are disclosed per `docs/conflicts-of-interest.md`.

### MIAPPE

- [ ] Pass — admit / retain as cataloged
- [ ] Needs-judgment — specify (version pinning / validator v1.1 vs release v1.2): _______________
- [ ] Fail — action (downgrade / defer / remove): _______________

### BrAPI

- [ ] Pass — admit / retain including `multiple-independent` with Cassavabase + IPK operators
- [ ] Needs-judgment — specify (section placement or operator URL): _______________
- [ ] Fail — action (downgrade MI / replace operator / remove): _______________

### SBOL

- [ ] Pass — admit / retain with `reference-and-others` and CellML `complements` relation
- [ ] Needs-judgment — specify: _______________
- [ ] Fail — action: _______________

### Signature

- **Reviewer GitHub handle:** @fraware (or: _______________)
- **Role:** lead maintainer / section reviewer (circle one)
- **Date:** YYYY-MM-DD
- **Commit reviewed:** _______________
- **Decision record:** (issue comment or `docs/decision-records.md` entry) _______________

---

## What still requires human action

1. Execute the checklist above in the GitHub issue (this file alone is not approval).
2. Merge the remediation PR for BrAPI URL fixes + SBOL relation correction if not already on `main`.
3. Optionally recruit domain peer reviewers using the peer-review invitation brief; optional gate stays open until a distinct human responds.
4. Only after human sign-off, update each resource `review.review_type` to `maintainer` (never to `independent` unless a separate independent reviewer actually reviewed).
