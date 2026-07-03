# Forge Classification and Ownership

This map classifies Forge-labeled ARK source that has been folded into
Foundry. Forge is a legacy name; Foundry is the canonical owner for engineering
workflow behavior.

## Contract

Inputs:

- Folded source evidence under `engines/ark/legacy/`
- Preserved compatibility copy under `engines/foundry/legacy/`
- Wayfinder repository ownership rules
- Canonical glossary alias from Forge to Foundry

Outputs:

- Canonical ownership decisions for Forge app, runtime, and planner surfaces
- Extraction destinations for future proof-backed work
- Compatibility rules for legacy names

Constraints:

- Runtime: documentation-only classification; expected review runtime under 5
  minutes.
- Memory: less than 64 MiB above editor and shell baseline.
- Environment: no runtime entrypoint rename in this phase.
- State: source artifacts remain local to `engines/foundry/legacy/` until a
  proof-backed extraction promotes them.

Edge cases:

- A file named Forge may still own Foundry behavior until compatibility aliases
  are proven.
- A UI shell can move to `internal/` later while Foundry keeps behavior
  ownership.
- Provider adapters may move to `external/` while Foundry keeps workflow
  orchestration.
- Shared persistence, policy, configuration, and eventing must move through
  services or contracts, not directly into Foundry core.

Invariants:

- Forge does not become a second engine.
- ARK remains owner of reality preservation.
- Foundry owns engineering workflow behavior.
- Compatibility names stay valid until an explicit migration proves equivalent
  canonical names.

## ARK Check

- Loop bounds defined? yes
- Resource caps defined? yes
- State localized? yes
- Interfaces strict? yes
- Failure paths explicit? yes

## Classification Map

| Surface | Preserved evidence | Classification | Canonical owner | Future extraction target | Boundary notes |
| --- | --- | --- | --- | --- | --- |
| Launcher entrypoints | `legacy/forge`, `legacy/forge.cmd`, `legacy/forge.ps1`, `legacy/forge-app`, `legacy/Forge App.*`, `legacy/install-forge-arch.sh` | Compatibility app surface | Foundry compatibility | `internal/desktop/` or `internal/cli/` for shell; Foundry for workflow behavior | Preserve names. Do not rename without compatibility tests. |
| Linux app packaging | `legacy/packaging/linux/forge-app.desktop.in`, `legacy/packaging/linux/forge-app.svg` | Compatibility app packaging | Foundry compatibility with Operations as deployment consumer | `operations/` for install/deployment flow after proof | Packaging evidence is preserved because it binds app identity and launcher behavior. |
| Developer UI modules | `legacy/ark-core/forge/ui/` | Internal app/controller surface | Foundry behavior owner | `internal/web/` or `internal/desktop/` for app shell; `engines/foundry/core/` for orchestration | UI must not become canonical engine authority. |
| Runtime configuration and guards | `legacy/ark-core/forge/runtime/`, `legacy/ark-core/forge/exec/` | Engine runtime surface | Foundry | `engines/foundry/core/` with future dependencies on configuration, policy, and runtime services | Keep bounded execution and explicit health checks. |
| Planner facade | `legacy/ark/forge_planner.py` | Planner ingress/API facade | Foundry | `engines/foundry/ingress/` | Planner publishes plans; it must not own ARK reality semantics. |
| Proposal generation | `legacy/ark-core/forge/transform/propose.py`, `legacy/scripts/ai/forge.py`, `legacy/scripts/ai/local_codegen_loop.py` | Ephemeral engineering workflow | Foundry | `engines/foundry/ephemeral/` and `engines/foundry/core/` | Candidate patches remain disposable until proof. |
| Patch application | `legacy/ark-core/forge/transform/apply.py`, `legacy/scripts/ai/apply_proposal.sh` | Core engineering mutation | Foundry | `engines/foundry/core/` | Requires rollback evidence and verification gates. |
| Verification and red-team checks | `legacy/ark-core/forge/verify/`, `legacy/ark-core/tests/test_forge_*.py` | Proof surface | Foundry | `engines/foundry/proofs/` | Shared verification primitives may later become services, but engineering checks stay Foundry-owned. |
| Workspace context | `legacy/ark-core/forge/context/` | Ingress and ephemeral context assembly | Foundry | `engines/foundry/ingress/` and `engines/foundry/ephemeral/` | Context is evidence for engineering work, not durable reality. |
| Model use | `legacy/ark-core/forge/models/` | Provider-consuming workflow | Foundry consumes; external provider owns adapter boundary | `external/ollama/` or provider-specific external folders plus Foundry core caller | Foundry owns model-use policy and orchestration, not provider identity. |
| MCP tooling | `legacy/ark-core/forge/mcp/` | Tool routing and policy surface | Foundry consumer with shared contract/policy extraction | `contracts/tools/`, `services/policy/`, `external/mcp/` after proof | Avoid duplicating policy or contract language inside Foundry core. |
| Local engineering memory | `legacy/ark-core/forge/memory/` | Ephemeral state and safety memory | Foundry for working memory; Storage/Policy for shared durable concerns | `engines/foundry/ephemeral/`, `services/storage/`, `services/policy/` | `.forge` state is not canonical storage by itself. |
| Artifacts and logs | `legacy/ark-core/forge/runtime/artifacts.py`, `legacy/ark-core/forge/runtime/logs.py`, `.forge` references in docs | Egress evidence surface | Foundry | `engines/foundry/egress/` with `services/storage/` persistence dependency | Generated artifacts require structured proof and rollback references. |
| Native agent bridge | `legacy/agents/forge_native/` | Foundry integration surface | Foundry | `engines/foundry/ingress/` or internal agent bridge after proof | Agent bridge may consume capabilities but must not redefine them. |
| Compatibility scripts | `legacy/ark-core/scripts/ai/forge.py`, `legacy/ark-core/scripts/ai/orchestrator.py`, `legacy/scripts/ai/*` | Developer workflow tooling | Foundry | `engines/foundry/legacy/` until canonical CLI/workflow extraction | Preserve until tests prove canonical replacement parity. |

## Ownership Decisions

| Legacy name or concept | Canonical owner | Compatibility owner | Notes |
| --- | --- | --- | --- |
| Forge | Foundry | `engines/foundry/legacy/` | Alias only; no separate engine identity. |
| Forge app | Foundry for workflow behavior; internal app surface later | `engines/foundry/legacy/` | App shell extraction must keep Foundry as behavior authority. |
| forge runtime | Foundry | `engines/foundry/legacy/` | Runtime extraction must preserve bounded execution and health signals. |
| forge planner | Foundry | `engines/foundry/legacy/ark/forge_planner.py` | Planner is Foundry ingress, not ARK reality preservation. |
| `.forge` artifacts | Foundry egress with Storage dependency | Legacy generated state name | Durable persistence requires Storage service boundary. |
| Forge tests | Foundry proofs | `engines/foundry/legacy/ark-core/tests/` | Tests are preservation evidence and future parity gates. |

## Extraction Order

1. Preserve legacy entrypoints and tests without renaming.
2. Extract planner ingress contracts and runtime health checks.
3. Extract proposal and patch application behind strict Foundry interfaces.
4. Promote verification/red-team gates into Foundry proofs.
5. Move app shell concerns to internal application folders while retaining
   Foundry behavior ownership.
6. Move provider, policy, storage, eventing, and configuration concerns only
   through their canonical external, service, or contract owners.

## Failure Modes

```json
{
  "status": "error",
  "error_code": "FOUNDRY_FORGE_AMBIGUOUS_OWNER",
  "reason": "A Forge-labeled artifact maps to more than one canonical owner.",
  "context": {
    "required_action": "Record ambiguity before extraction and do not promote runtime behavior."
  },
  "recoverable": true
}
```

```json
{
  "status": "error",
  "error_code": "FOUNDRY_FORGE_COMPATIBILITY_BREAK",
  "reason": "A canonical rename removed or changed a legacy Forge entrypoint without proof.",
  "context": {
    "required_action": "Restore compatibility alias or provide parity tests and migration notes."
  },
  "recoverable": true
}
```

```json
{
  "status": "error",
  "error_code": "FOUNDRY_BOUNDARY_VIOLATION",
  "reason": "Foundry extraction attempted to own shared service, contract, or ARK reality behavior.",
  "context": {
    "required_action": "Route the concern to the canonical owner before implementation."
  },
  "recoverable": true
}
```

## Complexity

- Time: O(n) over the finite preserved Forge artifact set.
- Space: O(n) documentation table entries; no runtime state allocation.
