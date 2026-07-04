# Retrieval Strategy

## Retrieval Units

| Unit | Use |
| --- | --- |
| Word | Exact lexical lookup and frequency. |
| Phrase | Repeated phrase lookup and autocomplete. |
| Statement | Primary precise retrieval and compiler support. |
| Chunk | Context window retrieval and future AI prompt input. |
| Paragraph | Display expansion. |
| Message / Section | Source navigation. |
| Conversation / Document | Full source reconstruction. |

## Ranking

Ranking should combine:

- exact statement match
- phrase overlap
- word/token relevance
- source recency when requested
- source type filters
- provenance quality
- governance promotion status
- relationship proximity

Do not rank by AI interpretation in Canonical Language. AI-derived ranking may
exist later as a separate rebuildable view.

## Expandability

Retrieval should expand in both directions:

```text
Word -> Phrase -> Statement -> Chunk -> Paragraph -> Message/Section -> Source Artifact
```

And trace back:

```text
Result -> Statement occurrence -> Observation -> ARK preserved source -> Raw artifact
```

## Replay

Given the same source observations, algorithm version, dictionary version, and
chunk profile, retrieval indexes must rebuild deterministically.
