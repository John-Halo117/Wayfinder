# ADR-0001: Canonical External World State

- **Status:** Accepted for `0.1.0-alpha.18`
- **Date:** 2026-08-16
- **Semantic owner:** Wayfinder
- **Related contract:** `contracts/world-state/README.md`
- **Related ontology:** `ontology/external-world-state.md`

## Context

Earlier Polaris-family artifacts used overlapping names and ownership shapes for the qualified state used by navigation and execution, including `External World State`, `Operative State`, and `Current Head`. Packaging history also encouraged a monolithic `System/Model/App` interpretation that does not match the live repository constitution.

The current Wayfinder skeleton already separates Observation, ARK evidence preservation, Interpretation, Reasoning, Bearings/Recommendations, commitments, and views. Any migration must preserve those boundaries and must not introduce runtime/schema implementation into Wayfinder merely to mirror an older package layout.

## Decision

1. **External World State (EWS)** is the canonical semantic name for the qualified derived world/operative state consumed by downstream navigation, planning, comparison, and execution systems.
2. **Wayfinder owns the EWS semantic model and compatibility rules.**
3. **Reasoning is the producer of EWS boundary artifacts** because it owns inference, contradiction handling, confidence posture, and reasoned conclusions.
4. **ARK remains owner of durable evidence/provenance.** EWS references evidence and never replaces the reality record.
5. **Interpretation remains candidate-meaning ownership.** It does not own final state inference.
6. **Jarvis consumes EWS** to generate Bearings and Recommendations; it does not redefine canonical state.
7. `Operative State` is retained as a compatibility alias. `Current Head` is deprecated and accepted only when historical context proves it refers to EWS.
8. Baseline, Successor, Reachability, and Twin are relations/concepts attached to state semantics rather than separate competing world models.
9. Executable storage, synchronization, invalidation, projection, and API mechanisms must be implemented in implementing repositories/components and tested there; Wayfinder does not select those mechanisms.

## Consequences

- The old monolithic package ownership shape is not reproduced in the live repositories.
- Consumers gain one canonical state concept while historical names remain resolvable during migration.
- Evidence, inference, recommendation, commitment, capability, authority, and presentation remain distinct.
- Runtime implementations can vary without semantic drift so long as they conform to the EWS contract.

## Compatibility and migration

Existing consumers using `Operative State` may continue to read/write that alias during the alpha migration window but should emit `External World State` when updated. Consumers using `Current Head` must first establish that the old field means qualified world state; branch/ledger/evidence-head uses are not compatible aliases.

No destructive rewrite of durable evidence is required. Migration occurs at the semantic boundary and consumer adapters.

## Rollback

Rollback consists of removing the new EWS contract/ontology/ownership entries and retaining the prior contract vocabulary. No durable evidence transformation is performed by this ADR, so rollback does not require evidence mutation.
