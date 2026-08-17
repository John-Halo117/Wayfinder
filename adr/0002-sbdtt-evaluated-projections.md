# ADR-0002 — Sparse Bipolar Dimensional Trend Tensor for Evaluated Projections

Status: Accepted for `0.1.0-alpha.19`

## Context

Polaris accumulated repeated cross-domain evaluation structures for magnitude, polarity, operating condition, epistemic state, trend, consequence, reach, and sparse material-change reporting. Weather/environmental work made the overlap explicit, but the semantics are not weather-specific.

The architecture must reuse one evaluated projection shape without turning that shape into universal canonical storage or collapsing unlike dimensions into a score.

## Decision

Adopt the Sparse Bipolar Dimensional Trend Tensor (SBDTT) as the default evaluated projection when several orthogonal evaluated dimensions materially change interpretation or action.

SBDTT is downstream of canonical evidence/state and upstream of Bearings/Decision/Projection.

Preserve these orthogonal dimensions:

- polarity;
- operational state;
- epistemic state;
- trend.

Use sparse material cells. Preserve raw units, provenance, scale definitions, objective, scope, time, and transformation version.

Use scalar, state machine, graph/DAG, or field instead when those are cheaper adequate representations.

## Consequences

- Weather Fabric and External Local Twin do not become independent truth owners.
- Environmental evaluation reuses the same cross-domain SBDTT semantics as finance, lifecycle, capability, attention, property, reliability, and other qualified domains.
- Operational Blue/Green/Yellow/Red remains distinct from epistemic White/Gray/Black and from positive/neutral/negative polarity.
- No unnamed universal goodness score is introduced.
- Implementations must be able to discard/recompute SBDTT projections without loss of canonical source state.

## Migration

1. Publish the SBDTT semantic contract in Wayfinder.
2. Update EWS and Bearings documentation to reference SBDTT as an evaluated projection, not storage.
3. Package shared types/schemas in Commons when that repository is available.
4. Implement conforming projection helpers in the appropriate runtime/application repositories.
5. Migrate domain-specific duplicate evaluation structures to SBDTT compatibility adapters only after parity tests.

## Rollback

If SBDTT proves too general or loses domain distinctions, domain projections may revert to their prior representations without changing canonical source state. The source state remains authoritative; SBDTT is derived and disposable.
