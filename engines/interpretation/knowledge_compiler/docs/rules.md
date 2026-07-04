# Compiler Rule Families

## Concept Detection

Detects recurring canonical architectural terms and repeated title-case terms
not present in the supplied known-term baseline.

## Decision Detection

Detects decision language such as `decision`, `canonical`, `accepted`,
`promoted`, `boundary`, `shall`, and `must`.

## Principle Detection

Detects reusable principle language such as `always`, `never`, `prefer`,
`reality precedes`, `observe before`, and `preserve before`.

## ADR Candidates

Detects explicit `ADR` language or decision language paired with rationale or
tradeoff markers.

## Glossary Candidates

Detects definition, alias, deprecation, and terminology-change language. It can
also use a supplied deprecated-term baseline.

## Amendment Candidates

Detects constitutional, ownership, lifecycle, capability, and engine promotion
language.

## Capsule Candidates

Detects explicit capsule/continuity/handoff language and structural conversation
groups with multiple preserved observations.

## TODO Candidates

Detects future work, migration, validation, incomplete work, later phase, and
open-question language.

## Novelty Detection

Detects repeated terms absent from the supplied known-term baseline. Novelty is
relative to that baseline only.

## Duplicate Detection

Detects repeated normalized sentences and repeated explicit relationship shapes.

## Contradiction Detection

Detects conflict, rename, deprecation, and contradiction language. Single-source
signals are emitted as lower-confidence candidates to preserve uncertainty.
