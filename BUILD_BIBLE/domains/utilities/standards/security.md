# Security Utility Standard

Security systems protect people, assets, access, boundaries, and continuity
through physical design first and automation second.

## Required Standard

- identify secure boundaries
- identify access points
- define lock, gate, camera, alarm, lighting, and sensor interfaces where used
- preserve emergency access
- document manual fallback
- keep service access from becoming a security weakness

## Expansion Rule

Security infrastructure should reserve power, data, mounting, sightline, and
control interfaces for future sensing without committing to a specific
technology.

## Relationships

- Parent doctrine: [Optionality](../../../doctrine/optionality.md)
- Contracts: [Interface Contract](../../../contracts/interface-contract.md),
  [Capability Contract](../../../contracts/capability-contract.md)
- Schemas: [interface.schema.json](../../../schemas/interface.schema.json)
- Dependent patterns: [Security Domain](../../security/README.md),
  [Lighting Standard](lighting.md)
- Generated artifacts: access-control maps, camera coverage maps, emergency
  access guides
- Reality records: lock records, sensor observations, and inspections
  instantiate this standard.

