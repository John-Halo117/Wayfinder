# Space Efficiency Analysis

This analysis is directional. Exact savings depend on corpus repetition,
message length, document types, and storage backend.

## Strategies

| Strategy | Expected savings | Lookup cost | Maintenance cost | Rebuild cost |
| --- | ---: | --- | --- | --- |
| Raw text only | 0% | Low | Low | Low |
| Word interning | 10-30% on repeated corpora | Medium | Medium | Medium |
| Phrase interning | 20-45% on repeated domains | Medium | Medium-High | Medium |
| Statement interning | 25-60% when language repeats | Low-Medium | Medium | Medium |
| Hybrid statement + phrase + word | 35-70% on large repeated corpora | Medium | Medium-High | Medium-High |

## Recommendation

Use hybrid compression, but make Statement interning the primary layer.

Rationale:

- Statements are useful for compiler and future AI.
- Phrase and Word dictionaries improve retrieval and compression.
- Chunks should be derived windows, not primary storage.
- Raw text remains preserved by ARK, so derived compression can be rebuilt.

## Avoid

- Replacing raw text with dictionaries.
- Semantic compression that changes meaning.
- AI summarization as compression.
- Global mutable dictionary IDs.
- Chunk-only storage.
