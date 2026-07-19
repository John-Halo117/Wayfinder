# 07 Understanding

Understanding turns focused representations into candidate meanings while
preserving uncertainty. It precedes missions and reasoning.

## Owns

- Interpretive candidates.
- Candidate concepts, decisions, principles, glossary entries, contradictions,
  and TODOs.
- Ambiguity and uncertainty surfaces.

## Does Not Own

- Reality preservation.
- Final inference.
- Human promotion.
- Navigation.

## Current Implementations

- `engines/interpretation/knowledge_compiler/`
- `engines/interpretation/knowledge_governance/`
- `tooling/export_mining/compile_knowledge.py` as derived export compiler
  tooling, not canonical engine behavior.

## Seven Roots Audit

Current repository search found Seven Roots primarily in generated Knowledge
and CivPhys language, not as an implemented reusable semantic system.

Recommendation:

- Keep Seven Roots internal to semantic reasoning.
- Do not expose Seven Roots as a presentation abstraction.
- Reuse them later as specialist reasoning primitives only after Reasoning and
  Specialist boundaries are implemented.

