# Recovery Procedures

Recovery procedures define how a capability returns to acceptable service after
fault, failure, maintenance, emergency, or outage.

## Required Fields

- affected scope or capability class
- trigger
- safety isolation
- immediate stabilization
- repair or bypass
- fallback mode
- recovery steps
- verification after recovery
- documentation update
- digital twin update

## Rule

Recovery is complete only after the capability is verified, documentation is
updated, and any degraded fallback state is visible.

## Relationships

- Parent reliability: [Reliability](README.md)
- Related ontology: [Operational State Model](../../registries/ontologies/operational-state-model.md)
- Related operations: [BUILD_OPERATIONS](../../../BUILD_OPERATIONS/README.md)
- Generated artifacts: emergency guides, recovery checklists, operating-mode
  transitions

