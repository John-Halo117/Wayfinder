# Capabilities

Capabilities are architectural verbs. They remain stable while implementations evolve.

This directory owns the canonical capability grammar: the universal verb language Wayfinder uses to describe outcomes. Engines and services may provide, discover, route, execute, or evaluate capabilities, but they do not redefine the verbs themselves.

Canonical examples include acquire, observe, represent, interpret, reason, predict, navigate, plan, execute, learn, reflect, remember, compress, preserve, retrieve, protect, verify, recover, transform, transfer, communicate, measure, and optimize.

Brain-inspired capabilities such as attention, working memory, episodic memory, semantic memory, procedural memory, pattern completion, novelty detection, hierarchical control, and prediction are cross-cutting capabilities, not architectural layers.

## Capability Grammar and Availability

- `capabilities/` owns the stable verb language.
- `contracts/capabilities/` defines what crosses boundaries when capability language or availability is referenced.
- NOMAD owns discovery of available providers, resources, and opportunities.
- Jarvis owns navigation among available capabilities.
- Foundry, ZWLib, domains, services, and external integrations may implement or expose capabilities without owning the grammar.
