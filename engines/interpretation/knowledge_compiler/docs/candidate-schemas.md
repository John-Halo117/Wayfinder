# Candidate Artifact Schemas

The compiler schema lives in `models.py`.

## CandidateArtifact

- `candidate_id`
- `candidate_type`
- `title`
- `summary`
- `confidence`
- `uncertainty`
- `status`
- `provenance`
- `metadata`

`status` is always `proposed` in this phase.

## Candidate Types

- concept
- decision
- principle
- adr
- glossary
- amendment
- capsule
- todo
- novelty
- duplicate
- contradiction

## Provenance

Every candidate includes:

- compiler version
- rule set version
- compile timestamp
- supporting observation IDs
- supporting reality IDs
- supporting conversation IDs
- supporting message IDs
- supporting timestamps
- source Oracles
- evidence references

## Confidence

Confidence is deterministic and rule-derived. It is not proof, promotion, or
truth. Low-confidence candidates are retained with validation warnings rather
than hidden.
