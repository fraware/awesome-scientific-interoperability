# Review notes: Provenance and Evidence

**Review date:** 2026-08-01  
**Reviewer role:** Section reviewer (PR-05 catalog migration B)  
**Records migrated:** 5

## Sources inspected

| Resource | Primary sources |
|----------|-----------------|
| CWLProv | [cwltool CWLProv documentation](https://cwltool.readthedocs.io/en/latest/CWLProv.html); [cwltool repository](https://github.com/common-workflow-language/cwltool) |
| ISO 23494-2:2026 Common Provenance Model | [ISO 87714 standard page](https://www.iso.org/standard/87714.html) |
| P-Plan | [OPMW P-Plan model](https://www.opmw.org/model/p-plan/); [W3C PROV-O](https://www.w3.org/TR/prov-o/) |
| runcrate | [researchobject.org/runcrate](https://www.researchobject.org/runcrate/); [ResearchObject/runcrate](https://github.com/ResearchObject/runcrate) |
| W3C PROV | [PROV-O](https://www.w3.org/TR/prov-o/); [PROV-DM](https://www.w3.org/TR/prov-dm/) |

## Changes made

- Mapped provenance profile relationships among W3C PROV, P-Plan, CWLProv, Workflow Run RO-Crate, and runcrate via related_resource_ids.
- Listed CWLProv and Workflow Run RO-Crate as mutual alternatives with explicit boundary on profile evolution.
- ISO 23494-2 recorded as established normative standard with `implementation_status: unknown` and `conformance_status: none-known` pending uptake evidence.
- Distinguished provenance exchange (this section) from packaging profiles in Data and Digital Objects.

## Unresolved questions

- Full ISO 23494-2 text requires purchase; interoperability claims verified from ISO catalogue abstract only.
- P-Plan current independent implementation count is not documented on the canonical site; left as `unknown`.

## Conflicts

None.
