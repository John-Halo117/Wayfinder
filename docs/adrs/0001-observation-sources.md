# ADR-0001: Observation Sources Produce Observations

Status: Accepted

Date: 2026-07-03

## Context

First Contact proved that the ChatGPT Export Oracle emitted 110,619
observation-shaped records before ARK preservation. Several producer tables
still implied that ARK creates observations.

## Decision

Observation Sources produce canonical observation-shaped records. ARK preserves
those records into append-only reality when they satisfy the Observation
Contract.

## Consequences

- Future Oracles must remain source-specific producers, not preservation
  engines.
- ARK must not own source discovery or parsing.
- Contract producer tables must name Observation Sources for observations.

## Evidence

- `docs/first-contact/chatgpt-export-validation.md`
- `docs/first-contact/evidence-assimilation.md`
- ChatGPT Oracle First Contact output: 110,619 observations.

## Rollback

Rollback by reverting contract and glossary language if a later proof shows ARK
must produce observations directly. No current evidence supports rollback.
