# Transformation Contract

## Purpose

Defines how assets may change state, form, context, or affordance.

## Producer

ZWLib

Exactly one engine produces this contract across engine boundaries.

## Consumers

Jarvis, Foundry, Reasoning, VALOR, Domains, Sandbox

## Inputs

Asset in Context, Capability, CivPhys Profile, constraints, objective, evidence, relationship, context.

## Outputs

Transformation Path, transformation opportunity, byproduct, transformed asset reference, affordance map.

## Invariants

- Transformation does not erase source identity without proof.
- Transformation paths must preserve provenance.
- Byproducts and waste remain potential transformation opportunities when useful.
- Transformation proposals do not execute themselves.

## Failure Modes

Impossible path, missing capability, insufficient potential, blocking membrane, excessive pressure, unknown byproduct, or uncertain outcome remain explicit uncertainty.

## Promotion Rules

Transformation paths remain ephemeral until proven. Durable transformation knowledge requires evidence of feasibility or completed action observation.

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
