# Compression Architecture

Canonical Language compression is structural and dictionary-based. It is not
semantic summarization.

## Hierarchy

```text
Raw Source Artifact
  -> Observation
  -> Block
  -> Paragraph
  -> Statement
  -> Phrase
  -> Word
```

Chunks cut across the hierarchy as bounded statement windows:

```text
Paragraph / Message / Section
  -> ordered Statements
  -> Chunk windows
```

## Compression Strategy

Use hybrid compression:

1. Preserve raw source artifacts through ARK.
2. Store statement occurrence records with provenance.
3. Intern repeated statement content.
4. Intern repeated phrases and words for indexes.
5. Build chunks from statement IDs.

Do not replace raw source text. Compression is an additional rebuildable view.

## Why Hybrid

| Strategy | Savings | Complexity | Risk |
| --- | --- | --- | --- |
| Raw text only | Low | Low | Duplicate compiler/retrieval work. |
| Word interning only | Medium | Medium | Loses useful statement boundaries. |
| Phrase interning | Medium-High | Medium-High | Phrase selection can overfit. |
| Statement interning | High for repeated language | Medium | Needs careful segmentation. |
| Hybrid | High with good retrieval utility | Medium-High | Best tradeoff if versioned and rebuildable. |

## Recommended Tradeoff

Use Statement interning as the primary compression layer, with Word and Phrase
dictionaries as supporting indexes. Use Chunk dictionaries for retrieval
windows, not as the core deduplication layer.

## Rebuild Cost

Expected rebuild cost is linear in extracted text length plus dictionary lookup
cost. Implementations should use bounded streaming inputs and avoid requiring
the full corpus in memory.

## Maintenance Cost

Maintenance cost is acceptable if:

- dictionary entries are immutable per version
- frequencies are rebuildable
- chunk profiles are explicit
- raw observations remain the authority
- migrations can run version-by-version
