# Physical Scope Contract

A physical scope is any bounded physical thing that can own identity,
interfaces, capabilities, constraints, maintenance, history, or generated
artifacts.

The Physical Scope Contract inherits from the
[Universal Scope Contract](universal-scope-contract.md). This contract adds
physical-world specificity to the universal fields.

## Required Fields

- stable ID
- human name
- purpose
- parent scope
- child scopes
- boundary
- spatial identity
- lifecycle state
- operational state
- capabilities
- interfaces
- dependencies
- resources
- constraints
- reserve capacity
- health
- reliability
- service paths
- inspection paths
- upgrade paths
- replacement paths
- maintenance obligations
- history links
- verification state
- documentation
- digital twin metadata

## Invariants

- A scope has one parent except for cross-cutting registries.
- Interfaces are explicit.
- Critical service paths are documented.
- Verification state is visible.
- Generated artifacts reference the scope; the scope does not depend on a
  generated artifact as canonical truth.
