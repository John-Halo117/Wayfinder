# Storage Contracts

Storage contracts define shared language for replaceable persistence. They
contain no implementation.

## Owned Concepts

- Storage address
- Storage backend capability
- Persistence operation
- Transaction
- Object
- Object metadata
- Version
- Version hook

## Contract Surfaces

### Storage Address

A storage address identifies a durable location without naming a required
backend technology.

Required language:

- `storage_uri`
- `namespace`
- `collection`
- `object_key`
- `version`

### Object Metadata

Object metadata describes a stored object without owning the object payload.

Required language:

- `object_key`
- `content_type`
- `content_length`
- `content_hash`
- `created_at`
- `updated_at`
- `owner_ref`
- `tags`

### Transaction

A transaction describes a bounded set of storage operations.

Required language:

- `transaction_id`
- `operations`
- `preconditions`
- `commit_policy`
- `rollback_policy`

### Backend Capability

Backend capability describes what a storage backend can safely provide.

Required language:

- `backend_id`
- `supports_transactions`
- `supports_versioning`
- `supports_object_metadata`
- `max_object_size_bytes`
- `health_ref`

## Invalid Ownership

These contracts do not define database vendors, engine-specific state machines,
backup operations, or event routing.
