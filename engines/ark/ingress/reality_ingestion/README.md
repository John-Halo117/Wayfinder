# ARK Reality Ingestion

ARK reality ingestion is the canonical boundary between Observation Sources and
ARK preservation.

Observation Sources produce canonical observations. ARK accepts those records,
validates the Observation Contract, asks the Identity Service to resolve known
identity references, preserves observations and explicit relationships through a
replaceable Storage Service abstraction, and publishes transport-neutral events
through the Event Bus.

Explicit relationships from source data are Source Relationships. ARK preserves
them as evidence; WEAVE owns later durable relationship topology.

This package contains no ChatGPT-specific logic. The ChatGPT Export Oracle is
only the first producer of canonical observation streams.

## Pipeline

```text
Observation Source
  -> Canonical Observation Contract
  -> ARK validation
  -> Identity Service lookup
  -> Append-only reality preservation
  -> Explicit relationship preservation
  -> Event Bus publication
  -> Last Verified Reality update
```

## Non-Goals

- AI interpretation
- summarization
- embeddings
- search
- ranking
- recommendations
- navigation
- knowledge graph construction
- inferred relationships

## Storage Boundary

`RealityStorage` is the only persistence interface consumed by the pipeline.
`InMemoryRealityStorage` is a bounded proof implementation for tests and local
verification. It is not a durable backend selection.

## LVR

Last Verified Reality updates only when an observation preservation write
succeeds. Relationship preservation does not move the LVR cursor.

## Import Profiles

Large local imports must use an Import Profile that declares observation,
relationship, artifact, payload, runtime, and replay bounds. The profile keeps
execution deterministic without repairing source data.

## Events

The pipeline emits:

- `ObservationPreserved`
- `ObservationRejected`
- `RelationshipPreserved`
- `IdentityResolved`
- `IdentityConflict`
- `ImportCompleted`
- `ValidationFailed`

Events are published through an `EventSink`. `EventBusEventSink` adapts this
boundary to the Event Bus service without importing a concrete broker or backend.

First Contact emitted 328,614 event publication records. Larger imports should
use streamable event publication or bounded event reporting before expanding
import scale.
