# Event Bus Service Migration Plan

## Minimal Promotion Completed

1. Establish `services/event-bus/` as canonical service home.
2. Reference existing contract language rather than inventing new schemas.
3. Record evidence, consumers, dependency boundaries, verification, and rollback.
4. Leave all engine implementations untouched.

## Later Implementation Migration

1. Build contract tests against legacy behavior.
2. Extract reusable implementation behind service interfaces.
3. Add compatibility adapters for ARK, Jarvis, and Foundry consumers.
4. Run engine verification before removing any duplicate local implementation.
