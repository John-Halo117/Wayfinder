# Compiler Validation Rules

The compiler validates without silently discarding uncertainty.

## Validation Issues

- missing observation ID
- missing provenance
- observation payload limit exceeded
- observation text truncated for bounded compilation
- candidate limit exceeded
- low-confidence candidate emitted

## Determinism

Compiler IDs are derived from canonical JSON payloads. Running the compiler over
the same preserved records with the same configuration produces the same
candidate IDs and ordering.

## Replayability

The compiler has no hidden state. Replay is achieved by re-running compilation
over ARK-preserved records.

## AI Fallback

AI fallback is intentionally not implemented in this phase. Any future fallback
must record prompt version, model identifier, confidence, and supporting
observations, and must still emit only proposed candidates.
