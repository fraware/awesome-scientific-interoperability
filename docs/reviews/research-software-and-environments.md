# Review notes: Research Software and Environments

**Review date:** 2026-08-01  
**Reviewer role:** Section reviewer (PR-05 catalog migration B)  
**Records migrated:** 5

## Sources inspected

| Resource | Primary sources |
|----------|-----------------|
| Apptainer / Singularity Image Format | [Apptainer user guide](https://apptainer.org/docs/user/latest/introduction.html); [apptainer/apptainer](https://github.com/apptainer/apptainer) |
| Citation File Format (CITATION.cff) | [citation-file-format.github.io](https://citation-file-format.github.io/); [cffconvert](https://github.com/citation-file-format/cffconvert) |
| CodeMeta | [codemeta.github.io](https://codemeta.github.io/); [codemeta/codemeta](https://github.com/codemeta/codemeta) |
| ReproZip | [reprozip.org](https://www.reprozip.org/); [ViDA-NYU/reprozip](https://github.com/ViDA-NYU/reprozip) |
| Software Hash Identifiers (SWHIDs) | [swhid.org](https://www.swhid.org/); [Software Heritage](https://www.softwareheritage.org/) |

## Changes made

- Migrated all five records to v2 with README-identical summaries.
- Recorded mutual alternatives between CITATION.cff and CodeMeta with complementary boundary notes.
- Classified Apptainer as operational HPC container interoperability; left OCI alternatives empty with boundary note (OCI not in this shard).
- Set ReproZip as reference-and-others packaging/capture tool, distinct from provenance standards.
- SWHIDs stewardship attributed to Software Heritage with institutional-adoption evidence.

## Unresolved questions

- Apptainer Linux Foundation affiliation and exact governance page were not verified beyond apptainer.org project documentation; stewardship type recorded as foundation based on public project branding.
- No public conformance suite identified for CodeMeta or SWHIDs (`none-known`).

## Conflicts

None.
