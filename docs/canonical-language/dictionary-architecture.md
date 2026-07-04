# Dictionary Architecture

## Purpose

Dictionaries reduce duplicate language storage and make cross-Oracle language
reuse visible. They are derived, rebuildable indexes over ARK-preserved
observations and Canonical Language artifacts.

## Dictionary Types

| Dictionary | Unit | Identity | Mutability | Purpose |
| --- | --- | --- | --- | --- |
| Word Dictionary | Canonical word form | Content-addressed | Append-only per version | Compression, frequency, lexical retrieval. |
| Phrase Dictionary | Ordered word sequence | Content-addressed | Append-only per version | Repeated phrase reuse. |
| Statement Dictionary | Canonical statement surface | Content-addressed | Append-only per version | Primary compiler input reuse. |
| Chunk Dictionary | Ordered statement window | Content-addressed | Rebuildable | Retrieval windows and context expansion. |

## Append-Only Versus Rebuildable

Dictionary entries are append-only inside one algorithm version. Dictionary
indexes are rebuildable.

The durable source is still ARK-preserved reality. If a dictionary algorithm
changes, create a new dictionary version and rebuild derived entries.

## Content Addressing

Dictionary IDs use normalized content and versioned algorithm names:

```text
clw:v1:<sha256(canonical_word)>
clp:v1:<sha256(word_ids + phrase_surface)>
cls:v1:<sha256(canonical_statement)>
clc:v1:<sha256(statement_ids + chunk_profile)>
```

## Frequency Awareness

Frequency is not part of identity. It is an index property rebuilt from
occurrences.

Track frequency by:

- corpus
- Oracle/source type
- source artifact
- time window
- author/role when present
- Import Profile

## Required Provenance

Every dictionary occurrence links to:

- ARK observation ID
- source artifact ID
- source path/span when available
- Observation Source
- parser version
- Canonical Language algorithm version

## Mutable Fields

Mutable fields are limited to rebuildable index metadata:

- frequency counts
- first/last seen pointers
- source distribution
- validation issue counts

Dictionary content entries are immutable for their version.

## Validation

Validation must report:

- empty normalized entries
- unstable IDs across replay
- broken observation references
- missing source spans when expected
- dictionary version mismatch
- excessive phrase length
- excessive statement length
- excessive chunk size
