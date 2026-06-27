# Observation Contracts

Observation contracts define shared language for recording what was observed
before interpretation.

They contain no implementation.

## Ownership

Canonical owner: `contracts/observations/`

Owned concepts:

- Observation
- Observation source
- Observation subject reference
- Observation time
- Observed payload reference
- Observation metadata
- Observation integrity reference
- Observation status

## Constitutional Rule

Observation precedes interpretation.

An observation records that something was seen, received, measured, fetched, or
reported. It does not decide what the observation means.

## Contract Surfaces

### Observation

An observation is a bounded record of source-facing reality.

Required language:

- `observation_id`
- `source_ref`
- `subject_ref`
- `observed_at`
- `received_at`
- `payload_ref`
- `schema_ref`
- `integrity_ref`
- `metadata`
- `status`

### Observation Source

An observation source identifies where an observation came from without binding
Wayfinder to a specific integration implementation.

Required language:

- `source_id`
- `source_type`
- `source_uri`
- `source_owner_ref`
- `trust_ref`

### Payload Reference

A payload reference points to observed data without requiring the observation
contract to own storage.

Required language:

- `payload_uri`
- `content_type`
- `content_length`
- `content_hash`
- `storage_ref`

### Integrity Reference

An integrity reference names how the observation can be checked.

Required language:

- `hash_algorithm`
- `hash_value`
- `signature_ref`
- `verification_status`

### Observation Status

Observation status is about intake validity, not truth.

Allowed language:

- `received`
- `accepted`
- `rejected`
- `quarantined`

## Dependencies

Observation contracts may reference:

- `contracts/identities/`
- `contracts/events/`
- `contracts/storage/`
- `contracts/schemas/`

Observation contracts must not depend on:

- `engines/`
- `services/`
- `domains/`
- `internal/`
- `external/`
- `operations/`

## Invalid Ownership

Observation contracts do not own:

- Evidence weighting
- Interpretation
- Claims
- Promotion criteria
- Reality graph algorithms
- Storage implementation
- Event transport
- External integration adapters

Those concepts must be owned by their canonical contracts, services, or engines.

## Failure Model

Observation contract validation failures use the standard failure shape:

```json
{
  "status": "error",
  "error_code": "INVALID_OBSERVATION_CONTRACT",
  "reason": "Observation contract input is missing a required language field.",
  "context": {},
  "recoverable": true
}
```
