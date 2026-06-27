# Policy Contract

## Purpose

Defines shared language for rules, constraints, evaluation context, decisions, exceptions, and policy evidence.

## Producer

Policy Service

Exactly one service produces policy boundary language. Engines may apply policy results but do not own generic policy vocabulary.

## Consumers

ARK, Jarvis, Foundry, MICE, Blackwall, VALOR, Event Bus, Storage, Domains, Internal applications, Operations

## Inputs

Policy rule reference, actor identity, asset reference, capability reference, context, evidence, permission request, promotion request, event metadata, health signal.

## Outputs

Policy decision, rule reference, constraint, exception reference, escalation reference, audit reference, confidence reference.

## Invariants

- Policy evaluates constraints; it does not own the underlying asset, event, evidence, or capability.
- Policy decisions must identify their rule basis when known.
- Policy uncertainty must be explicit.
- Permission handling uses policy language without duplicating policy ownership.

## Failure Modes

Missing rule, conflicting rules, unknown actor, insufficient evidence, stale policy, unsupported context, or ambiguous exception remain explicit uncertainty.

## Promotion Rules

Policy decisions remain ephemeral unless promoted as durable policy evidence, audit record, or constitutional governance artifact by the relevant owner.

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
