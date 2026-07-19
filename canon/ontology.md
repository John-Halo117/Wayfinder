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

## Canonical Language Concepts

### Canonical Language

Architectural Name: Canonical Language

Technical Name: `CanonicalLanguageArtifact`

Status: Proposed

Definition: A deterministic, rebuildable, source-agnostic language
normalization and compression substrate derived from ARK-preserved reality.

Responsibilities: Normalize source language; segment blocks, paragraphs,
Statements, Phrases, and Words; build dictionaries; create Chunk windows;
preserve traceability to observations and raw artifacts.

Non-responsibilities: Preserving reality; evaluating truth; creating durable
knowledge; reasoning; navigation; summarization; embedding generation.

Canonical Owner: Proposed `docs/canonical-language/` until implementation
owner is selected.

Accepted Aliases: CL, language substrate.

Deprecated Aliases: knowledge, reality, summary layer.

Relationships: Consumes ARK-preserved observations; produces Statements,
Chunks, dictionaries, and structural relationships; feeds Knowledge Compiler
and Retrieval.

Lifecycle: preserved observation -> deterministic extraction -> Canonical
English normalization -> dictionary lookup or append -> Statement and Chunk
emission -> validation -> rebuildable indexes.

Evidence: Phase 8D design requirement that future Oracles normalize into one
substrate before compiler and future AI consumption.

### Canonical English

Architectural Name: Canonical English

Technical Name: `CanonicalEnglishV1`

Status: Proposed

Definition: The deterministic normalized English surface used for deduplication
and language IDs.

Responsibilities: Normalize whitespace, punctuation variants, structural
boundaries, and safe lexical forms while preserving raw source by reference.

Non-responsibilities: Translation, summarization, meaning repair, fact
extraction, or AI correction.

Canonical Owner: Proposed Canonical Language subsystem.

Accepted Aliases: normalized English surface.

Deprecated Aliases: cleaned truth, summary text.

Relationships: Produces Word, Phrase, Statement, and Chunk content IDs.

Lifecycle: raw source text reference -> deterministic normalization ->
versioned normalized surface -> content-addressed IDs.

Evidence: Phase 8D requirement that AI never own normalization.

### Statement

Architectural Name: Statement

Technical Name: `CanonicalStatement`

Status: Proposed

Definition: The primary reusable language unit, smaller than a Chunk and more
useful than a Phrase for compiler and retrieval inputs.

Responsibilities: Represent a deterministic surface unit such as sentence,
heading, bullet item, table cell, transcript utterance, or metadata field.

Non-responsibilities: Asserting truth, resolving claims, promoting knowledge,
or summarizing source content.

Canonical Owner: Proposed Canonical Language subsystem.

Accepted Aliases: canonical statement.

Deprecated Aliases: claim when truth has not been evaluated.

Relationships: Contains Phrases and Words; belongs to Paragraphs, Blocks, and
Chunks; traces to Observations.

Lifecycle: segmented from source language -> normalized -> content ID assigned
-> occurrence ID linked to observation -> consumed by compiler/retrieval.

Evidence: Phase 8D selected Statement as the primary reusable unit.

### Chunk

Architectural Name: Chunk

Technical Name: `CanonicalChunk`

Status: Proposed

Definition: A bounded ordered window of Statements used for retrieval, context
expansion, and future AI input.

Responsibilities: Preserve source-near context windows, stable numbering under
a chunk profile, and traceability to statement occurrences.

Non-responsibilities: Primary meaning, truth, source preservation, or summary.

Canonical Owner: Proposed Canonical Language subsystem.

Accepted Aliases: context window.

Deprecated Aliases: summary chunk.

Relationships: Contains Statement occurrences; expands to Paragraph, Message,
Section, Conversation, or Document.

Lifecycle: statements emitted -> chunk profile selected -> boundaries applied
-> content and occurrence IDs assigned -> retrieval indexes rebuilt.

Evidence: Phase 8D chunk architecture.

### Canonical Dictionary

Architectural Name: Canonical Dictionary

Technical Name: `CanonicalDictionary`

Status: Proposed

Definition: A versioned, content-addressed, rebuildable dictionary for Words,
Phrases, Statements, and Chunks.

Responsibilities: Deduplicate language units, track occurrences, rebuild
frequencies, and support compression/retrieval.

Non-responsibilities: Owning raw text, mutating content IDs, or promoting
knowledge.

Canonical Owner: Proposed Canonical Language subsystem.

Accepted Aliases: language dictionary.

Deprecated Aliases: memory store, knowledge base.

Relationships: Contains Word Dictionary, Phrase Dictionary, Statement
Dictionary, and Chunk Dictionary.

Lifecycle: normalize unit -> content-address lookup -> append immutable entry
if absent -> rebuild frequency indexes.

Evidence: Phase 8D dictionary architecture.
