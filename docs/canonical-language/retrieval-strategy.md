# Retrieval Strategy

Retrieval follows Progressive Discovery: load only the smallest sufficient
representation needed for the current objective, then escalate depth only when
confidence is insufficient.

Canonical progression:

```text
Reality -> Root Inventory -> Metadata -> Structure -> Summary -> Relationships -> Candidate Selection -> Targeted Retrieval -> Full Content
```

Full content retrieval is allowed only when smaller representations cannot
satisfy the objective with adequate confidence.

## Retrieval Principles

- Never load more information than necessary.
- Traverse information incrementally.
- Prefer indexes over full scans.
- Prefer metadata over content.
- Prefer summaries over complete documents.
- Prefer relationships over exhaustive traversal.
- Prefer deltas over rescans.
- Prefer hashes over byte comparisons.
- Prefer references over duplication.
- Stop traversal as soon as confidence is adequate for the objective.

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

## Escalation

Retrieval begins at the shallowest representation that can answer the current
question. It escalates one step at a time and records why deeper access was
required when full content is loaded.

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
Root Inventory -> Metadata -> Structure -> Summary -> Relationships -> Candidate Selection -> Targeted Retrieval -> Full Content
```

And trace back:

```text
Result -> Statement occurrence -> Observation -> ARK preserved source -> Raw artifact
```

Lexical expansion remains available inside targeted retrieval:

```text
Word -> Phrase -> Statement -> Chunk -> Paragraph -> Message/Section -> Source Artifact
```

## Replay

Given the same source observations, algorithm version, dictionary version, and
chunk profile, retrieval indexes must rebuild deterministically.

## Cross-Domain Rule

The same progression applies to ARK, conversation memory, repositories,
containers, OSINT, home systems, media, Build Bible records, and future
capability domains. Domain owners may add stricter limits, but must not bypass
the shallow-to-deep retrieval order without recording a reason.
