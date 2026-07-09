# Traceability Model

Every future engineering decision must trace through:

```text
Implementation
-> Capability
-> Runtime
-> Protocol
-> Architecture
-> Constitution
-> Eisengarten
```

## Required Trace Fields

| Field | Meaning |
| --- | --- |
| Implementation artifact | Concrete file, module, adapter, service, engine, app, or operation. |
| Capability | Stable outcome the implementation serves. |
| Runtime role | Ingress, Reality, Ephemeral, Proof, Promotion, Core, or Egress role. |
| Protocol surface | Contract, schema, event, import profile, compatibility alias, or CLI/API boundary. |
| Architecture layer | Evidence pipeline layer and repository ownership layer. |
| Constitutional law | Law or invariant that authorizes the work. |
| Eisengarten purpose | Continuity, reality preservation, attention, capability, or maneuverability purpose. |
| Evidence source | Source document, ADR, validation result, or preserved artifact that supports the claim. |
| Uncertainty | Ambiguity or missing source that blocks full confidence. |

## Promotion Trace

Ephemeral or generated material becomes durable only when it records:

```text
source evidence
-> provenance
-> validation/proof
-> promotion reason
-> durable owner
```

## Compatibility Trace

Legacy names and providers must record:

```text
legacy name
-> canonical concept
-> canonical owner
-> compatibility boundary
-> deprecation or alias rule
```

Forge therefore traces to Foundry rather than creating a parallel canonical
owner.

## Minimal Template

```text
Artifact:
Capability:
Runtime role:
Protocol surface:
Architecture layer:
Constitutional law:
Eisengarten purpose:
Evidence:
Uncertainty:
```
