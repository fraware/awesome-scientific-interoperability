# Peer-review invitation brief: MIAPPE, BrAPI, SBOL

Pasteable invitation for domain experts. This does **not** close the optional peer-review gate. Do not invent acceptances.

## Suggested message

Subject: Optional peer review — plant phenotyping metadata, breeding APIs, and synthetic-biology design exchange

We maintain [Awesome Scientific Interoperability](https://github.com/fraware/awesome-scientific-interoperability), a curated catalog of scientific interoperability mechanisms (not a general awesome list of tools). Three recently admitted entries need optional domain peer review:

1. **MIAPPE** — plant phenotyping experiment metadata  
   Catalog ID: `minimum-information-about-plant-phenotyping-experiments-miappe`  
   Record: `catalog/resources/metadata-and-semantics.yaml`  
   Hub: https://www.miappe.org/

2. **BrAPI** — plant breeding database REST API  
   Catalog ID: `breeding-api-brapi`  
   Record: `catalog/resources/workflows-and-execution.yaml`  
   Spec index: https://brapi.org/specification

3. **SBOL** — synthetic-biology design exchange  
   Catalog ID: `synthetic-biology-open-language-sbol`  
   Record: `catalog/resources/data-and-digital-objects.yaml`  
   Spec: https://sbolstandard.org/datamodel-specification/version-3.1.0/

### Scope (what we ask)

Please review whether each entry’s **summary, mechanism, boundary note, implementation/conformance claims, and typed relations** are accurate and non-inflated relative to primary sources. Disagreement is welcome and valuable.

### Time estimate

45–90 minutes for all three, or ~20–30 minutes per resource if you prefer to take only one domain.

### Conflicts of interest

If you help build, fund, govern, or commercially depend on a resource, disclose that before reviewing and do not serve as the sole approving reviewer for that resource ([conflicts of interest](https://github.com/fraware/awesome-scientific-interoperability/blob/main/docs/conflicts-of-interest.md)).

### Exact files to review

- Resource shards linked above  
- Supporting registries as needed: `catalog/implementations.yaml`, `catalog/references.yaml`, `catalog/stewards.yaml`  
- Decision guides:  
  - `docs/decision-guides/ecology-and-sequence-context-metadata.md` (MIAPPE, BrAPI)  
  - `docs/decision-guides/systems-biology-models.md` (SBOL)  
- Sign-off dossier (author packet, not approval): `docs/reviews/maintainer-signoff-miappe-brapi-sbol.md`

### Questions to answer (comment on the GitHub issue)

For each resource you review:

1. Does the summary pass a strict sentence test (what interoperates with what, via what mechanism)?
2. Is section placement appropriate?
3. Does every cited URL support the **exact** claim role (stewardship / technical-definition / implementation / conformance / adoption)?
4. Are independence or validator claims bounded correctly?
5. Are typed relations to neighbors correct (`complements` vs `alternative-to`)?
6. What would you downgrade, clarify, or remove?

### How to respond

Comment on the recruitment / peer-review GitHub issue with: domain covered, COI disclosure, answers to the questions above, and your GitHub handle. We will not mark peer review complete until a distinct human responds.

Thank you for considering this. Declining is fine; a short “no capacity” reply still helps us track outreach.
