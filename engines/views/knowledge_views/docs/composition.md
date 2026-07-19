# View Composition

Views compose by combining `ViewItem` references from existing `ViewResult`
objects.

Composition:

- preserves original item provenance
- deduplicates by item ID
- records source view IDs in filters
- does not copy or mutate promoted knowledge
- remains deterministic for identical input views

Examples:

- Timeline + Decisions
- Concept + Architecture
- Conversation + Capsule
- Objective + TODOs
