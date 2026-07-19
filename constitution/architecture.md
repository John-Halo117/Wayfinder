# Architecture

Repository organization follows responsibility.

```text
Reality
  |
Observation Sources
  |
CivPhys
  |
Constitution
  |
Objectives
  |
Capability Grammar
  |
Capabilities
  |
Contracts
  |
Services
  |
Engines
  |
Domains
  |
Internal Applications
  |
External Systems
  |
Operations
```

Dependencies only point downward. When a dependency would point upward, the
concept must be reclassified or expressed as a contract.

## Observation Sources

Observation Sources are first-class constitutional producers of
observation-shaped records.

An Observation Source owns discovery, source-specific parsing, artifact
classification, source validation, provenance capture, and emission of canonical
observation-shaped records. An Oracle is an Observation Source with a
source-specific deterministic parser.

Observation Sources do not own reality preservation, identity, relationship
topology, interpretation, reasoning, navigation, promotion, search, embeddings,
or durable knowledge.

## ARK Preservation Boundary

ARK is the reality preservation authority. ARK owns append-only preservation,
provenance preservation, replay, and Last Verified Reality (LVR). ARK accepts
canonical observation-shaped records from Observation Sources and preserves
them when they satisfy the Observation Contract.

ARK does not own observation discovery, source parsing, identity, durable
relationship topology, interpretation, reasoning, navigation, or knowledge
promotion outside its preservation boundary.

## Source Relationships

Source Relationships are explicit relationships present in source data, such
as containment, reply, reference, origin, or membership edges. ARK may preserve
Source Relationships as source evidence. WEAVE owns later durable relationship
topology and may consume Source Relationships, but ARK preservation does not
make topology claims.

## Import Profiles

An Import Profile is a bounded configuration posture for one import class. It
declares limits, validation expectations, runtime expectations, and replay
behavior. Import Profiles do not repair source data or introduce
source-specific semantics beyond explicit limits and validation posture.

## Progressive Discovery

Progressive Discovery constrains every retrieval, indexing, import,
repository, and future domain workflow. Wayfinder should start from reality and
root inventories, then use metadata, structure, summaries, relationships,
candidate selection, and targeted retrieval before loading full content.

This discipline applies across ARK, conversation memory, repositories,
containers, OSINT, home systems, media, Build Bible records, and future
capability domains. It is not a separate engine; it is a resource, latency,
privacy, and confidence invariant applied by the owner of each workflow.



## Repository And Execution

Repository organization follows responsibility. Execution semantics are defined separately in [execution.md](execution.md).

The repository stack is not an execution pipeline. When a concept appears to belong to multiple layers, classify it by canonical ownership and express cross-layer communication through contracts.
