# Review: Instruments and Laboratories

**Review date:** 2026-08-01  
**Records migrated:** 7  
**Reviewer conflict of interest:** None

## Sources inspected

| ID | Primary sources |
|----|-----------------|
| allotrope-data-format | https://docs.allotrope.org/ ; https://www.allotrope.org/adf/ |
| analytical-information-markup-language-animl | https://www.animl.org/ ; https://www.astm.org/e13 |
| autoprotocol | https://github.com/autoprotocol/autoprotocol-python ; https://autoprotocol.org/ |
| hl7-fhir | https://hl7.org/fhir/ ; https://github.com/FHIR/fhir-test-cases |
| loinc | https://loinc.org/ ; https://loinc.org/kb/users-guide/ |
| opc-ua-laboratory-and-analytical-device-standard-lads | https://opcfoundation.org/markets-collaboration/lads/ ; https://reference.opcfoundation.org/ |
| sila-2 | https://sila2.gitlab.io/sila_base/ ; https://gitlab.com/sila2 |

## Category distinctions recorded

| Category | Resources |
|----------|-----------|
| Analytical-data exchange | Allotrope Data Format, AnIML |
| Laboratory procedure language | Autoprotocol |
| Clinical exchange | HL7 FHIR |
| Terminology | LOINC |
| Device communication | OPC UA LADS, SiLA 2 |

## Changes made

- Migrated all seven records to v2.
- Cross-linked ADF and AnIML as analytical-data alternatives within this shard.
- Cross-linked LADS and SiLA 2 as device-communication alternatives within this shard.
- Linked LOINC and FHIR as related clinical/laboratory exchange resources.
- Set Autoprotocol to `emerging` with 183-day review interval (review_due_on 2027-01-31).
- Documented Allotrope consortium access/licensing in `boundary_note`.
- Clarified `resource_type` labels to distinguish exchange, terminology, procedure, and device layers.

## Unresolved questions

- Autoprotocol ecosystem breadth after Strateos restructuring merits recheck at next 183-day review.
- Allotrope specification access conditions for non-members should be verified against current membership terms.

## Conflicts

None.

## v2.1 provenance migration (2026-08-01)

- Closed isolate: `autoprotocol` alternatives/related to SiLA 2.
