# Execution Runtime

Execution Runtime is the generalized boundary for bounded environments capable
of executing work and returning noncanonical results.

Examples of future runtimes include Odysseus, Codex, Docker, Python, Browser,
Home Assistant, Shell, Remote Worker, and future AI systems.

```text
Jarvis
↓
ExecutionRequest
↓
ExecutionRuntimeRegistry
↓
ExecutionRuntimeProvider
↓
OdysseusExecutionRuntime
↓
external/odysseus
↓
Odysseus
```

The runtime response flows into the review membrane:

```text
ExecutionRuntimeResponse
↓
CandidateArtifact
↓
PromotionDecision
↓
AdmissionCandidate
```

## Owns

- execution
- sessions
- temporary workspaces
- runtime lifecycle
- model routing
- tool invocation

## Never Owns

- ARK
- observations
- canonical memory
- bearings
- constitutional policy
- inventory
- promotion
- admission

Execution Runtime output must remain noncanonical. Provider responses carry
`ProvenanceRecord(canonical=False)` and cannot directly become observations.
ARK admission remains a later separate owner boundary.

## Configuration

```bash
EXECUTION_RUNTIME=none
```

disables runtime use.

```bash
EXECUTION_RUNTIME=odysseus
ODYSSEUS_ENABLED=true
ODYSSEUS_BASE_URL=http://127.0.0.1:7000
ODYSSEUS_TIMEOUT_SECONDS=5
```

selects Odysseus as the first runtime implementation. Provider construction does
not call the network; only explicit `health()` and `send()` calls may delegate to
the configured adapter.

## Migration Notes

- `host_shell/` is now a compatibility shim for `execution_runtime/`.
- `HOST_SHELL` is deprecated; use `EXECUTION_RUNTIME`.
- `HostShellProvider` → `ExecutionRuntimeProvider`
- `HostShellRequest` → `ExecutionRuntimeRequest`
- `HostShellResponse` → `ExecutionRuntimeResponse`
- `JarvisHostShellBridge` → `JarvisExecutionBridge`
- `OdysseusHostShellProvider` → `OdysseusExecutionRuntime`

