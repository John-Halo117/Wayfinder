# Index Types

## Full Text

Token index for keyword, phrase, and simple boolean retrieval.

## BM25

Deterministic lexical ranking using local document frequencies.

## Embedding

Deterministic token-vector projection for similarity retrieval. This phase does
not use AI models or vector databases.

## Hybrid

Combines full text, BM25, and deterministic vector scores with explicit weights.

## Timeline

Orders promoted knowledge chronologically by promotion timestamp and promotion
identity.

## RID

Looks up promotion IDs, promoted artifact IDs, supporting observation IDs, and
supporting reality IDs.

## Concept

Indexes concept-like terms from promoted artifact titles, summaries, targets,
and provenance.

## Capability

Indexes capability vocabulary such as capabilities, providers, services,
engines, contracts, storage, identity, events, policy, and configuration.

## Acronym

Indexes uppercase acronyms present in promoted knowledge text.

## Relationship

Provides index-based traversal from promotion IDs, promoted artifact IDs,
candidate IDs, observations, reality IDs, and conversations. It is not a graph
database.
