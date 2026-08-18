# Human Interface Ontology Resolution v1

Status: canonical interface law for Model 0.1.0-alpha.21.

## Law

A human MUST NOT need to remember canonical architecture names, taxonomies, operators, doctrines, providers, commands, metrics, or dependency structure in order to use a capability correctly.

Canonical names are retrieval and engineering handles, not prerequisites for use.

## Default interaction

Natural intent, approximate descriptions, examples, symptoms, constraints, and ordinary language are resolved internally to canonical concepts and mechanisms.

Human-facing navigation SHOULD expose no more than two architectural levels by default. Deeper structure is progressive disclosure and appears only when requested or when it materially changes a consequential decision.

## Friendly projection

Every internal concept that can surface to a human SHOULD provide:

- `canonical_handle`: stable engineering/retrieval identity;
- `plain_meaning`: short ordinary-language meaning;
- `when_it_matters`: the condition under which it changes action or interpretation;
- `friendly_phrase`: language suitable for normal interaction;
- optional `technical_detail`: progressive disclosure, never required memorization.

Example:

`reproduction_proof` -> "prove we can actually rebuild it".

The system may use the canonical handle internally while saying the friendly phrase externally.

## Resolution

Human utterance -> intent/constraints -> concept resolution -> canonical owner/operator -> evidence/decision/execution.

Resolution MUST tolerate aliases, forgotten names, approximate descriptions, examples, and symptom-first requests. If multiple canonical concepts remain materially plausible, discriminate using the cheapest adequate question or evidence probe.

## Anti-jargon gate

A newly admitted internal name is not automatically a UI term. Before promotion to default human-facing vocabulary, it must demonstrate that the name itself improves navigation enough to justify memorization burden.

If the capability can be used correctly without knowing its name, default UI should prefer plain language.

## Invariants

1. Ontology complexity is paid by the system, not transferred to the human.
2. `canonical_handle != required_user_vocabulary`.
3. A friendly projection MUST NOT create a second semantic truth.
4. Renaming a friendly phrase MUST NOT change canonical identity or stored state.
5. Internal aliases collapse to the same canonical concept.
6. Natural-language resolution does not grant authority; capability and authority remain separate.
7. Technical terminology remains available for engineering, audit, provenance, and explicit deep dives.

Human-facing summary: **Polaris remembers Polaris; the human states what they want.**
