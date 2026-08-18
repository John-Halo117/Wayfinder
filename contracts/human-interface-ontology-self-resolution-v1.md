# Human Interface — Ontology Self-Resolution v1

Status: canonical human-interface law for Model `0.1.0-alpha.21`.

## Governing law

**Polaris remembers Polaris. The human states intent.**

A person MUST be able to invoke and correctly use an ordinary Polaris capability without knowing its canonical internal name. Canonical names are retrieval, engineering, provenance, testing, and debugging handles—not prerequisites, commands, or navigation requirements.

## Default human surface

Normal interaction exposes at most two navigational levels by default. The stable top-level projection is deliberately small:

- **World** — what is happening outside and around the user and their systems?
- **Life** — what does the person/household need, want, or protect?
- **Things** — what resources, property, equipment, inventory, money, and capabilities exist?
- **Plans** — what should happen next, what is blocked, and what is reachable?
- **System** — is Polaris/Basecamp healthy, recoverable, synchronized, current, and trustworthy?

These are projections only; they create no new semantic owners.

## Resolution law

`intent / approximate description / symptom / example / alias / remembered fragment`
`-> canonical concept + owner/operator/standard/provider resolution`
`-> state/evidence retrieval`
`-> decision/diagnostic/workflow composition`
`-> plain-language bearing/action`

Resolution SHOULD prefer consequence and intent over asking the user to choose ontology labels. Clarification is warranted only when unresolved ambiguity can materially change outcome, authority, safety, cost, privacy, or another protected constraint.

Historical/superseded names SHOULD remain retrieval aliases when safe, while the current canonical concept remains the semantic owner.

## Progressive disclosure

Default projection order:

1. plain-language state, consequence, recommendation, or action;
2. optional friendly explanation;
3. optional canonical technical handle;
4. evidence/service hatch to deeper ontology, provenance, transforms, assumptions, contracts, and implementation.

When an internal handle is shown, pair it with meaning. Example:

`Reproduction Proof — prove we can actually rebuild it.`

Do not require vocabulary such as EWS, SBDTT, Failure Drain, Tail-Cutter Capital, Germline/Phenotype, or future equivalents for ordinary operation.

## Retrieval requirements

Human-facing concepts SHOULD provide enough hooks to resolve from:

- plain-language meaning;
- aliases and old names;
- partial/approximate names;
- examples;
- symptoms;
- desired outcomes;
- provider-independent capability descriptions.

Friendly phrases may change without changing canonical identity or stored state.

## Completion gate

For every human-facing capability ask:

> Could the user successfully invoke, understand, and recover this capability without knowing its canonical internal name?

If no, the human interface is incomplete.

Formally, `CAN_USE_FROM_INTENT == true` is required independently of `KNOWS_CANONICAL_NAME`.

## Anti-bloat / anti-jargon invariants

- `new name != new required vocabulary`.
- `internal ontology complexity != required human memory`.
- `canonical name != command`.
- `technical precision available != technical precision always displayed`.
- No provider name is required when capability can be resolved independently.
- No architecture diagram is required for ordinary operation.
- Abbreviations are optional compression, never required knowledge.
- Cool/stable internal names may survive for engineering value without becoming human obligations.
- Natural-language resolution never grants authority; capability and authority remain separate.

## Compatibility

This law composes with the existing owner graph, Concept Registry, aliases, Generated Mission UI, Bearings, standards-first resolution, SBDTT projections, and evidence service hatch. It creates no parallel truth store, authority surface, or second ontology.
