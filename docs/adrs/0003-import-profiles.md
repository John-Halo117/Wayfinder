# ADR-0003: Require Import Profiles For Large Private Imports

Status: Accepted

Date: 2026-07-03

## Architecture Sections

- [02 Perception](../architecture/02-perception.md)
- [03 Observations](../architecture/03-observations.md)
- [18 Cross-Cutting Systems](../architecture/18-cross-cutting.md)

## Context

The default ARK observation cap of 100,000 rejected the First Contact export,
which contained 110,619 observations. Validation succeeded with explicit
bounded caps.

## Decision

Large private imports require an Import Profile declaring limits, validation
posture, runtime expectations, and replay behavior before execution.

## Consequences

- Import scale remains bounded and deterministic.
- Profiles document expectations without repairing source data.
- Configuration implementation can remain deferred until reuse requires it.

## Evidence

- First Contact ARK validation profile: 150,000 observations, 300,000
  relationships, 10,000 artifacts.
- `docs/first-contact/chatgpt-export-validation.md`.

## Rollback

Rollback by returning to engine-local limits only if later evidence shows
profiles add ambiguity without improving validation.
