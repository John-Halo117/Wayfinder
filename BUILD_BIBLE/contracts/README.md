# Contracts

Contracts define the expected shape and semantics of Build Bible records.

Use these documents when creating or reviewing canonical records. Machine
validation lives in `schemas/`.

## Core Contracts

- [Universal Scope Contract](universal-scope-contract.md)
- [Physical Scope Contract](physical-scope-contract.md)
- [Resource Flow Contract](resource-flow-contract.md)
- [Dependency Contract](dependency-contract.md)
- [Reliability Contract](reliability-contract.md)
- [Operational State Contract](operational-state-contract.md)
- [Spine Contract](spine-contract.md)
- [Interface Contract](interface-contract.md)
- [Capability Contract](capability-contract.md)
- [Capacity Contract](capacity-contract.md)
- [Maintenance Contract](maintenance-contract.md)

## Inheritance Rule

Scope-specific contracts inherit from the Universal Scope Contract. They may
specialize fields, but common concepts should remain defined once at the
highest accurate level.
