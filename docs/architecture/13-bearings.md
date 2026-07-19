# 13 Bearings

Bearings orient Wayfinder before recommendations or navigation. A Bearing is
not an action; it is a directionally useful orientation.

## Owns

- Orientation.
- Route posture.
- Tradeoff-ready direction.
- Inputs for recommendations.

## Does Not Own

- Capability discovery.
- Commitment.
- Direct action.

## Canonical Owner

- `contracts/bearings/`
- Jarvis as future producer.

## Current State

Bearing contracts exist, but no full Jarvis bearing engine proof is active.

## Migration Path

Do not build navigation directly from raw views. Use Mission -> Bearing ->
Reasoning/Navigation contracts so Jarvis remains explainable.

