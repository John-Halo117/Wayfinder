# Ontology Remembers Itself v1

Status: canonical human-interface contract for Model `0.1.0-alpha.21`.

## Human-interface law

A person MUST be able to use a Polaris capability correctly without knowing its canonical internal name.

Canonical names are retrieval, engineering, provenance, testing, and debugging handles. They are not prerequisites for use.

Polaris resolves natural language, intent, symptoms, examples, approximate descriptions, aliases, and desired outcomes into canonical concepts and mechanisms internally.

## Depth budget

Default human-facing navigation MUST expose no more than two conceptual levels below the top-level view unless deeper structure is necessary for a consequential decision or explicitly requested.

Default top-level projection:

- **World** — what is happening outside and around me?
- **Life** — what do I/we need, want, or need to protect?
- **Things** — what do we have, where is it, and what can it do?
- **Plans** — what should happen next and what is blocking it?
- **System** — is Polaris itself healthy, trustworthy, recoverable, and current?

These are projections/navigation surfaces, not new sovereign owners.

## Progressive disclosure

Default projection order:

1. plain-language state / consequence / action;
2. optional friendly explanation;
3. optional canonical technical handle;
4. evidence service hatch to deeper ontology, provenance, transforms, assumptions, contracts, and implementation.

Internal names such as EWS, SBDTT, Reproduction Proof, Failure Drain, Tail-Cutter Capital, Germline/Phenotype, Affordance Tensor, or future equivalents MUST NOT be required vocabulary.

## Naming test

For every new or renamed concept ask:

`Can the human invoke and use this capability correctly without knowing this name?`

If no, the human interface is incomplete.

## Alias / retrieval behavior

- Natural language and aliases map many-to-one into canonical concepts where semantics permit.
- Renaming a canonical concept MUST NOT invalidate old human language; prior names remain retrieval aliases unless actively dangerous or misleading.
- Friendly phrases may change without changing canonical identity.
- Approximate user language SHOULD be resolved by consequence and intent before asking the user to select ontology labels.
- The system SHOULD ask for clarification only when ambiguity can materially change outcome, authority, safety, cost, or another protected constraint.

## Output behavior

Normal output SHOULD lead with consequence, state, recommendation, or action rather than architecture names.

Prefer:

`We can actually rebuild this from the retained material.`

Optional technical detail:

`Verified with Reproduction Proof.`

Avoid requiring:

`Run RP against the germline/phenotype boundary.`

## Architecture boundary

The ontology may grow internally when justified. Human-facing complexity does not inherit that growth automatically.

`internal ontology complexity != required human memory`

`canonical name != command`

`canonical name != navigation requirement`

`technical precision available != technical precision always displayed`

## Governing objective

Polaris remembers Polaris. The human supplies intent, preferences, corrections, and consequential judgment rather than memorizing system architecture.
