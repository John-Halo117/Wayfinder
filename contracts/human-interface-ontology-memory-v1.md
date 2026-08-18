# Human Interface: Ontology Memory v1

Status: canonical human-interface law for Model `0.1.0-alpha.21`.

## Law

**The ontology remembers itself. The human states intent.**

Canonical names, operators, owners, doctrines, providers, metrics, standards, commands, and internal architecture are retrieval handles for the system; they are not prerequisites for use.

A human-facing capability is incomplete if correct ordinary use requires the user to remember its canonical internal name.

## Default interaction contract

1. Accept natural language intent, approximate descriptions, examples, symptoms, aliases, and remembered fragments.
2. Resolve them internally to canonical concepts, evidence, capabilities, diagnostics, operators, standards, safeguards, and owners.
3. Present the result in ordinary language first.
4. Show at most two navigational levels below the top by default.
5. Reveal canonical/internal names only when they materially improve precision, retrieval, debugging, provenance, engineering, or a consequential decision.
6. Deeper structure is progressive disclosure, never a memorization requirement.

## Human-facing top level

Default projections SHOULD organize around a small stable vocabulary such as:

- **World** — what is happening outside the user/system?
- **Life** — what does the user/household need or want?
- **Things** — what is owned/available and what can it do?
- **Plans** — what should happen next?
- **System** — is Polaris itself healthy/capable?

These are projections, not new semantic owners.

## Friendly explanation contract

When an internal handle must be surfaced, pair it with a short meaning. Example:

`Reproduction Proof — prove we can actually rebuild it.`

The friendly meaning is primary in ordinary UI. The canonical handle remains searchable/inspectable metadata.

## Retrieval behavior

Resolution SHOULD tolerate:

- aliases and old names;
- partial/approximate names;
- examples instead of taxonomy terms;
- symptoms instead of diagnostic names;
- user language instead of provider/API vocabulary;
- historical names that have since collapsed into successors.

Resolution MUST prefer the current canonical concept while retaining provenance to superseded aliases.

## Anti-bloat / anti-jargon invariants

- `new name != new required vocabulary`.
- `internal precision != human memorization burden`.
- No command vocabulary is required when intent can be safely inferred.
- No provider name is required when capability can be resolved independently.
- No architecture diagram is required for ordinary operation.
- Abbreviations are optional display compression, not required knowledge.
- A cool internal name may survive for engineering value without appearing in normal interaction.

## Completion test

For every human-facing capability ask:

> Could the user successfully invoke, understand, and recover this capability without knowing its canonical internal name?

If no, the human interface is not complete.
