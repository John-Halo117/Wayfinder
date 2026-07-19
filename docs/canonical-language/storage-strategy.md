# Storage Strategy

## Durable

Durable:

- raw source artifacts preserved by ARK
- ARK preserved observations
- ARK preserved Source Relationships
- governance-promoted durable knowledge

Canonical Language artifacts are not durable knowledge by default.

## Rebuildable

Rebuildable:

- extracted blocks
- paragraphs
- statements
- phrases
- words
- chunks
- dictionaries
- frequency indexes
- compression indexes
- retrieval indexes

Rebuildable artifacts may be cached or materialized for performance, but their
authority comes from ARK-preserved reality and algorithm versions.

## Constitutional Ownership

| Artifact | Owner |
| --- | --- |
| Raw artifact | ARK preservation |
| Observation | ARK preservation |
| Source Relationship | ARK preservation |
| Canonical Language artifact | Canonical Language subsystem |
| Dictionary entry | Canonical Language subsystem |
| Frequency index | Canonical Language subsystem |
| Promoted knowledge | Knowledge Governance target |
| Retrieval index | Knowledge Retrieval |

## Storage Requirements

Canonical Language storage must support:

- content-addressed lookup
- occurrence lookup by observation
- replay by source artifact
- dictionary versioning
- chunk profile versioning
- validation issue storage
- deletion and rebuild of derived artifacts

## Migration

Migrations create new version namespaces. Do not mutate old content IDs in
place. Rebuild derived artifacts from ARK if a segmentation or normalization
algorithm changes.
