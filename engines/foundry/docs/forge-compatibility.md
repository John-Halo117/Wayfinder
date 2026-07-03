# Forge Compatibility

Forge is the legacy ARK name for Foundry engineering workflow behavior. This
document records compatibility rules for legacy names while future extraction
work moves behavior toward canonical Foundry ownership.

## Contract

Inputs:

- Legacy commands and module names under `engines/foundry/legacy/`
- Canonical owner `engines/foundry/`
- Alias rule in `canon/glossary.md`

Outputs:

- Stable compatibility expectations for legacy Forge entrypoints
- Canonical replacement names and ownership boundaries
- Failure model for compatibility breaks

Constraints:

- Runtime: documentation-only compatibility map; expected review runtime under
  5 minutes.
- Memory: less than 64 MiB above editor and shell baseline.
- Environment: no generated `.forge` state is promoted by this document.
- State: legacy names are preserved until proof-backed aliases or replacements
  exist.

## Name Map

| Legacy name | Canonical meaning | Canonical owner | Compatibility rule |
| --- | --- | --- | --- |
| Forge | Foundry engineering engine | Foundry | Treat as alias only. Do not create `engines/forge/`. |
| `forge` | Legacy terminal entrypoint | Foundry compatibility | Preserve until canonical CLI parity is proven. |
| `forge-app` | Legacy browser/app launcher | Foundry compatibility | Preserve until internal app shell parity is proven. |
| `forge.cmd` | Windows command prompt launcher | Foundry compatibility | Preserve while Windows users or scripts may call it. |
| `forge.ps1` | PowerShell launcher | Foundry compatibility | Preserve while Windows users or scripts may call it. |
| `Forge App.cmd` | Windows click launcher | Foundry compatibility | Preserve because file name is user-facing compatibility. |
| `Forge App.ps1` | PowerShell click launcher | Foundry compatibility | Preserve because file name is user-facing compatibility. |
| `Forge App.sh` | Linux click launcher | Foundry compatibility | Preserve because file name is user-facing compatibility. |
| `install-forge-arch.sh` | Legacy Linux app installer | Foundry compatibility; Operations consumer | Preserve as source evidence until deployment ownership is extracted. |
| `forge-app.desktop.in` | Legacy Linux desktop entry template | Foundry compatibility; Operations consumer | Preserve app identity evidence. |
| `forge-app.svg` | Legacy Linux app icon | Foundry compatibility; Operations consumer | Preserve app identity evidence. |
| `ark/forge_planner.py` | Foundry planner ingress facade | Foundry | Preserve path until planner API compatibility is proven. |
| `ark-core/forge/*` | Foundry runtime, UI, proof, and workflow modules | Foundry | Preserve module path until package rename parity is proven. |
| `.forge/` | Legacy generated session/artifact state | Foundry egress with Storage dependency | Do not treat as canonical durable storage without proof and Storage boundary. |

## Canonical Replacement Guidance

| Compatibility surface | Future canonical target | Required proof before rename |
| --- | --- | --- |
| CLI and launcher scripts | Foundry CLI or internal application command | Command parity tests, migration note, rollback path |
| UI app shell | `internal/desktop/` or `internal/web/` | Session restore parity, status/stop behavior parity, operator workflow proof |
| Runtime modules | `engines/foundry/core/` | Bounded execution tests, health signal tests, failure object coverage |
| Planner facade | `engines/foundry/ingress/` | Input/output schema parity and plan publication tests |
| Proposal workspace | `engines/foundry/ephemeral/` | Disposable-state proof and invalid-input rejection tests |
| Verification suite | `engines/foundry/proofs/` | Test execution parity and red-team check parity |
| Artifacts/logs | `engines/foundry/egress/` plus Storage service | Structured artifact schema, rollback reference proof, persistence boundary proof |

## Compatibility Invariants

- Legacy names remain discoverable from Foundry docs.
- Legacy entrypoints are not removed in documentation-only phases.
- Canonical Foundry names may be introduced as additive aliases.
- A legacy name may be deprecated only after parity tests and migration notes
  exist.
- No compatibility shim may bypass policy, sandbox, proof, or rollback
  requirements.

## Failure Modes

```json
{
  "status": "error",
  "error_code": "LEGACY_ENTRYPOINT_MISSING",
  "reason": "A documented Forge compatibility entrypoint is absent from the Foundry legacy fold.",
  "context": {},
  "recoverable": true
}
```

```json
{
  "status": "error",
  "error_code": "CANONICAL_RENAME_WITHOUT_PARITY",
  "reason": "A Forge name was replaced by a Foundry name before compatibility parity was proven.",
  "context": {},
  "recoverable": true
}
```

```json
{
  "status": "error",
  "error_code": "DUPLICATE_ENGINE_IDENTITY",
  "reason": "Forge was treated as a canonical engine instead of an alias for Foundry.",
  "context": {},
  "recoverable": true
}
```

## Complexity

- Time: O(n) over the finite compatibility-name set.
- Space: O(n) documentation entries; no runtime state allocation.
