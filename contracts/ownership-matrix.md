# Contract Ownership Matrix

Every contract has exactly one Producer. Producer means the canonical boundary
source for the artifact crossing engine or service boundaries; it does not
always mean ownership of the universal constitutional model.

| Contract | Producer | Consumers | Canonical Output |
| --- | --- | --- | --- |
| Observation Contract | Observation Source role | ARK, Evidence, Interpretation, Reasoning, Views, Jarvis, Capsules, MIDAS, Domains, Internal applications | Observation |
| Evidence Contract | ARK | Proof, Promotion, Interpretation, Reasoning, VALOR, MIDAS, Jarvis, MICE, Blackwall | Evidence item |
| Provenance Contract | ARK | Evidence, Proof, Promotion, Capsules, Views, Reasoning, VALOR, MICE, Domains, Operations | Provenance record |
| Identity Contract | Identity Service | ARK, Event Bus, Storage, Jarvis, Foundry, Capsules, MICE, Domains, Internal applications, Operations | RID / canonical identity reference |
| Event Contract | Event Bus | ARK, Jarvis, Foundry, Capsules, MICE, Domains, Internal applications, Operations, External integrations | Event envelope |
| Storage Contract | Storage Service | ARK, Capsules, Foundry, Jarvis, Event Bus, Identity Service, Policy Service, Domains, Internal applications, Operations | Persistence reference |
| Policy Contract | Policy Service | ARK, Jarvis, Foundry, MICE, Blackwall, VALOR, Event Bus, Storage, Domains, Internal applications, Operations | Policy decision |
| Permission Contract | Policy Service | Blackwall, MICE, Jarvis, Foundry, Domains, Internal applications, Operations, External integrations | Permission decision |
| Health Contract | VALOR | Jarvis, Foundry, Blackwall, NetWatch, Operations, Domains, Internal applications, MICE | Health state |
| Schema Contract | Build Bible | ARK, Event Bus, Storage, Identity Service, Policy Service, Foundry, Jarvis, Domains, Internal applications, Operations | Schema reference / validation result |
| Representation Contract | Views | Interpretation, Reasoning, Jarvis, Foundry, Capsules, Domains, Internal applications | Representation |
| Asset Contract | ARK | WEAVE, Interpretation, Reasoning, Views, Jarvis, ZWLib, Capsules, MIDAS, VALOR, MICE, Domains | Asset reference |
| Context Contract | ARK | Observation, Interpretation, Reasoning, Views, Jarvis, ZWLib, Capsules, MICE, VALOR, Blackwall, Domains | Context reference |
| Relationship Contract | WEAVE | Interpretation, Reasoning, Views, Jarvis, ZWLib, MICE, VALOR, Domains | Relationship |
| Capability Contract | NOMAD | Jarvis, ZWLib, Foundry, MICE, Domains, Services, Internal applications | Capability availability reference |
| Bearing Contract | Jarvis | MICE, Foundry, Domains, Internal applications, Capsules, VALOR | Bearing |
| Recommendation Contract | Jarvis | MICE, Foundry, Domains, Internal applications, Operators | Recommendation |
| Commitment Contract | MICE | Jarvis, Foundry, Domains, Operations, Internal applications, Capsules | Commitment |
| Transformation Contract | ZWLib | Jarvis, Foundry, Reasoning, VALOR, Domains, Sandbox | Transformation Path |
| Capsule Contract | Capsules | Jarvis, Foundry, MICE, Domains, Internal applications, Operators | Capsule |
| Specification Contract | Build Bible | Foundry, Domains, Internal applications, Operations, MICE | Specification |
| Proof Contract | ARK | Promotion, Build Bible, Foundry, Reasoning, MICE, Capsules, Domains | Proof |
| Promotion Contract | ARK | All engines, Services, Domains, Internal applications, Operations | Promotion record |
| View Contract | Views | Jarvis, Foundry, Domains, Internal applications, Operators, Capsules, MICE | View reference |

## Ownership Clarifications

- The Asset model is constitutionally owned by `constitution/assets.md` and `contracts/assets/`; ARK produces durable asset knowledge.
- Capability grammar is owned by `capabilities/`; NOMAD produces discovered capability availability.
- Context can frame Observation, but Context does not require Observation for identity.
- Identity Service owns reusable identity implementation; Event Bus owns subject/routing semantics.
- The Observation Source role produces observation-shaped records; ARK preserves them.
- ARK may preserve explicit Source Relationships as evidence; WEAVE owns durable relationship topology.
