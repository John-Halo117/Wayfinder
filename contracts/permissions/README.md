# Permission Contract

## Purpose

Defines shared language for whether an actor may exercise a capability on an asset in context.

## Producer

Policy Service

Exactly one service produces permission decision language. Permissions are evaluated through policy; engines do not own independent permission vocabularies.

## Consumers

Blackwall, MICE, Jarvis, Foundry, Domains, Internal applications, Operations, External integrations

## Inputs

Actor identity, asset reference, capability reference, action intent, context, policy reference, evidence, delegation reference, commitment reference.

## Outputs

Permission decision, permission scope, denial reason, delegation boundary, audit reference, uncertainty reference.

## Invariants

- Permission is contextual and revocable.
- Permission does not imply capability availability.
- Denial and uncertainty must remain visible.
- Permission language depends on policy but does not duplicate policy rules.

## Failure Modes

Unknown actor, missing policy, conflicting delegation, insufficient evidence, expired scope, ambiguous context, or denied capability remain explicit outcomes.

## Promotion Rules

Permission decisions remain ephemeral unless promoted as audit evidence, commitment evidence, or durable policy knowledge by the canonical owner.

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
