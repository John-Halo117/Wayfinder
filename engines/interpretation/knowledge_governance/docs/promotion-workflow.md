# Promotion Workflow

Promotion creates durable knowledge records. It does not edit compiler
candidates, ARK observations, provenance, or constitutional files.

## Requirements

- candidate exists
- candidate is `approved`
- candidate has review history
- candidate has supporting observation provenance
- reviewer is supplied
- rationale is supplied
- rollback is supplied
- target is valid

## Targets

- glossary
- constitution
- adr_repository
- capsule_repository
- execution_backlog
- knowledge_repository

## Versioning

Every promotion creates a new `PromotionRecord` with version `1` for that
artifact. Future replacement or deprecation should create additional records
rather than mutating history.

## Rollback

Rollback is required as human-authored governance context. The engine records the
rollback text but does not execute rollback actions.
