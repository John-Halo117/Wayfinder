# ADR 0010: Consolidate Duplicate Forge Legacy With Compatibility Aliases

Status: Proposed

Date: 2026-07-05

## Context

Tracked duplicate analysis found 67 duplicate hash groups, dominated by
Forge-origin files preserved under both `engines/ark/legacy/` and
`engines/foundry/legacy/`.

Existing debt records already identify ARK historical source preservation and
Foundry compatibility shims as open debt. The duplicate files should not be
deleted casually because they preserve migration history and may anchor legacy
entry points.

## Decision

Consolidate duplicate Forge legacy only after one authoritative preserved
source-of-record and compatibility alias strategy are documented.

Foundry should own engineering workflow semantics. ARK should not remain the
long-term owner of Forge implementation behavior unless evidence shows a
preservation-specific responsibility.

## Alternatives Considered

- Delete one duplicate tree immediately. Rejected because history and entry
  point compatibility are not proven.
- Keep both duplicate trees indefinitely. Rejected because it creates review
  noise and ownership ambiguity.
- Rewrite Forge under Foundry. Rejected because migration should preserve
  capabilities and history.

## Tradeoffs

Compatibility aliases preserve behavior but temporarily keep an extra layer of
indirection. This is preferable to losing historical evidence or breaking
legacy workflows.

## Migration Plan

1. Generate a duplicate manifest for ARK/Foundry Forge-origin files.
2. Choose the authoritative preserved source location.
3. Add compatibility aliases for historical command paths.
4. Prove parity with legacy tests or smoke checks.
5. Remove duplicate copies only after review.
