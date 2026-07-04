# Observation Contract

## Purpose

Defines what crosses the boundary when reality is observed before interpretation. Observations may reference Context as a situational frame.

## Producer

Observation Source role

An Observation Source produces canonical observation-shaped records. ARK
consumes and preserves those records into append-only reality when they satisfy
this contract.

## Consumers

Evidence, Interpretation, Reasoning, Views, Jarvis, Capsules, MIDAS, Domains, Internal applications

## Inputs

Reality, Observation Source, Asset or RID, Context reference or situational conditions, time, location, actor, capability, constraints.

## Outputs

Observation, source reference, subject reference, payload reference, integrity reference, observation metadata.

## Invariants

- Observation precedes interpretation.
- Observation does not decide meaning.
- Observation is append-only once promoted.
- Observation references representations without becoming a representation.
- Observation may reference Context, but Context does not depend on Observation for identity.

## Failure Modes

Missing source, uncertain subject, incomplete context, conflicting observation, untrusted source, or insufficient provenance are represented as uncertainty and evidence gaps.

## Promotion Rules

Observation remains ephemeral until ARK preserves it with sufficient source,
integrity, and provenance. Preserved observations become durable reality
references. ARK preserves observations; it does not discover or parse source
exports.

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
