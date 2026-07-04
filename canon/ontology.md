# Canonical Ontology

This file records canonical concept relationships. It is not runtime behavior,
schema definition, or implementation guidance. One Concept, One Home still
applies: the ontology summarizes ownership and points to canonical owners.

## First Contact Concepts

### Observation Source

Architectural Name: Observation Source

Technical Name: `IObservationSource`

Status: Canonical

Definition: A source-specific boundary that observes external source material
and emits canonical observation-shaped records before ARK preservation.

Responsibilities: Discover files or records; classify artifacts; parse
supported source structures; validate source shape; preserve provenance; emit
observations and explicit Source Relationships.

Non-responsibilities: Append-only reality preservation; identity ownership;
durable relationship topology; interpretation; reasoning; navigation;
summaries; embeddings; search.

Canonical Owner: `contracts/observations/`

Accepted Aliases: Oracle, integration producer.

Deprecated Aliases: importer as source-of-truth, parser as preservation owner.

Relationships: Produces Observation; produces Source Relationship; consumes
Import Profile; is preserved by ARK.

Lifecycle: discovered -> parsed or preserved -> observation-shaped record
emitted -> ARK validation -> ARK preservation or rejection.

Evidence: ChatGPT Oracle emitted 110,619 observations before ARK preservation
during First Contact.

### Source Relationship

Architectural Name: Source Relationship

Technical Name: `SourceRelationshipRecord`

Status: Canonical

Definition: An explicit relationship present in source data and preserved
before interpretation.

Responsibilities: Preserve source-provided containment, origin, reference,
reply, membership, and attachment relationships with provenance.

Non-responsibilities: Inferring topology; resolving meaning; creating a
knowledge graph; promoting durable relationship claims.

Canonical Owner: `contracts/relationships/`

Accepted Aliases: explicit source edge, preserved source edge.

Deprecated Aliases: relationship graph, inferred relationship.

Relationships: Produced by Observation Source; preserved by ARK; consumed by
WEAVE as evidence for later topology.

Lifecycle: explicit in source -> emitted by Observation Source -> preserved by
ARK -> optionally consumed by WEAVE after proof.

Evidence: First Contact preserved 217,994 explicit relationships while WEAVE
remained unimplemented.

### Import Profile

Architectural Name: Import Profile

Technical Name: `ImportProfile`

Status: Canonical

Definition: A bounded configuration posture for one import class.

Responsibilities: Declare file, observation, relationship, artifact, payload,
runtime, validation, and replay bounds.

Non-responsibilities: Repairing source data; encoding source-specific semantics;
selecting storage backends; changing observations.

Canonical Owner: `constitution/execution.md`

Accepted Aliases: validation profile, import limits profile.

Deprecated Aliases: unbounded import mode.

Relationships: Consumed by Observation Sources and ARK; referenced by
validation reports.

Lifecycle: selected before import -> enforced during discovery and preservation
-> recorded in validation report -> reviewed before reuse.

Evidence: First Contact required explicit ARK caps of 150,000 observations,
300,000 relationships, and 10,000 artifacts.

### Candidate Page

Architectural Name: Candidate Page

Technical Name: `CandidatePage`

Status: Proposed

Definition: A bounded slice of compiler candidates prepared for governance
review.

Responsibilities: Preserve reviewability when candidate volume exceeds one
repository batch; retain candidate provenance; support deterministic replay of
review intake.

Non-responsibilities: Changing candidate meaning; promoting knowledge;
summarizing private source content; bypassing human review.

Canonical Owner: `engines/interpretation/knowledge_governance/`

Accepted Aliases: review page, candidate batch page.

Deprecated Aliases: unbounded review batch.

Relationships: Produced from Knowledge Compiler output; consumed by Knowledge
Governance; projected by Knowledge Views.

Lifecycle: compiler emits candidates -> candidates grouped into pages ->
governance stores or rejects each page -> review views expose bounded queues.

Evidence: First Contact compiler reached a 250,000 candidate cap and governance
rejected intake at its 100,000 candidate cap.

### Opaque Attachment

Architectural Name: Opaque Attachment

Technical Name: `OpaqueAttachmentArtifact`

Status: Canonical

Definition: A preserved attachment artifact whose bytes are retained with
provenance but not parsed by the current Observation Source.

Responsibilities: Preserve attachment bytes, identity, classification, hash,
source location, and provenance.

Non-responsibilities: OCR; transcription; embeddings; semantic extraction;
file-type inference beyond safe classification.

Canonical Owner: `contracts/assets/` and source-specific Oracle docs.

Accepted Aliases: preserved blob, unparsed attachment.

Deprecated Aliases: unknown artifact when source evidence identifies it as an
attachment.

Relationships: Is an artifact; may be referenced by Observations; may be linked
by Source Relationships.

Lifecycle: discovered -> classified as attachment -> preserved with hash ->
referenced by observations or relationships -> optionally parsed by a future
evidence-backed parser.

Evidence: First Contact classified and preserved 250 `.dat` files as attachment
source files and normalized 700 attachment artifacts.
