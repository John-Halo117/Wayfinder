# Human Interface — Ontology Self-Resolution v1

Status: canonical human-interface law for Model `0.1.0-alpha.21`.

## Objective

The human expresses intent, constraints, symptoms, examples, approximate descriptions, and preferences. Polaris resolves internal canonical concepts, owners, operators, standards, providers, diagnostics, and workflows without requiring the human to memorize them.

**A canonical name is a retrieval handle, not a prerequisite for use.**

## Default human surface

Normal interaction exposes at most two navigational levels. Default top-level projections are deliberately small and plain-language:

- **World** — what is happening outside/around the user and their systems?
- **Life** — what does the household/person need, want, or protect?
- **Things** — what resources, property, equipment, inventory, money, and capabilities exist?
- **Plans** — what should happen next, what is blocked, and what is reachable?
- **System** — is Polaris/Basecamp itself healthy, recoverable, synchronized, and trustworthy?

These are projections, not new canonical owners. Existing owners remain authoritative underneath.

## Resolution law

`natural language / approximate description / symptom / example`
`-> concept and alias resolution`
`-> relevant canonical owner/operator/standard/provider`
`-> state/evidence retrieval`
`-> decision/diagnostic/workflow composition`
`-> plain-language bearings/action`

The user MUST NOT need to know the internal name for this path to work.

## Disclosure policy

1. Default output uses plain language and consequences.
2. Internal handles may appear as optional secondary labels when useful for precision, provenance, engineering, debugging, or learning.
3. Deep ontology is progressive disclosure: reveal it on request or when a consequential choice cannot be understood safely without it.
4. Never require memorized commands, subsystem names, acronyms, taxonomies, providers, metrics, or canonical operators when intent can resolve them.
5. New internal concepts require a plain-language gloss and aliases/symptom/example hooks sufficient for retrieval.
6. Internal complexity may grow only when human-facing complexity does not grow proportionally.

## Human-facing completion test

A capability is not interface-complete until a user can invoke and understand its consequential result without knowing its canonical internal name.

Formally:

`CAN_USE_FROM_INTENT == true`

is required independently of:

`KNOWS_CANONICAL_NAME`.

## Naming policy

Cool/stable technical names may be retained. They support engineering, provenance, search, contracts, and precise discussion. They do not become human obligations.

Preferred rendering:

`Prove we can rebuild this.`

Optional technical detail:

`Mechanism: Reproduction Proof`

Not preferred:

`Run Reproduction Proof.`

unless the user deliberately uses that handle.

## Compatibility

This law composes with the existing owner graph, generated mission UI, Bearings, Concept Registry, aliases, standards-first resolution, SBDTT projections, and evidence service hatch. It creates no parallel truth store or authority surface.
