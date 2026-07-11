# Generation Contract

Generated artifacts are outputs, not sources of truth.

## Generated Artifact Requirements

Each generated artifact must record:

- source scope IDs
- source document revisions
- generator name
- generator version
- generation timestamp
- validation status
- output format

## Regeneration Rule

Generated outputs must be disposable. If a generated file cannot be recreated
from canonical source plus generator configuration, it is not generated; it is
canonical and must move to an owning source directory.

## Human Edits

Human edits to generated outputs are temporary inspection notes unless promoted
back into canonical source documents.

