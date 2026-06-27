# Schema Contract

## Purpose

Defines shared structural language for schema identity, version, validation result, compatibility, and structured failure reporting.

## Producer

Build Bible

Exactly one engine produces canonical specification and schema language. Services and engines consume schema references without redefining schema vocabulary.

## Consumers

ARK, Event Bus, Storage, Identity Service, Policy Service, Foundry, Jarvis, Domains, Internal applications, Operations

## Inputs

Schema identifier, version reference, contract reference, asset reference, event reference, validation evidence, compatibility claim, failure context.

## Outputs

Schema reference, schema version, compatibility reference, validation result, structured failure model, conformance claim.

## Invariants

- Schemas describe structure; they do not own runtime behavior.
- Validation results must identify the schema basis when known.
- Compatibility and conformance are explicit claims.
- Structured failure language remains stable across implementations.

## Failure Modes

Unknown schema, incompatible version, missing required structure, invalid reference, ambiguous validation result, or unsupported contract remain explicit failure states.

## Promotion Rules

Schema language is durable as contract vocabulary. Specific schema versions become durable when promoted by Build Bible or the canonical specification owner.

## Constitutional Basis

- [Asset Model](../../constitution/assets.md)
- [Execution Semantics](../../constitution/execution.md)
- [Repository Responsibilities](../../constitution/repository.md)
- [Engine Boundaries](../../engines/README.md)

## Non-Goals

- Runtime behavior.
- Implementation APIs.
- Storage formats.
- Domain-specific schemas.
- Engine internals.
