# Host Shell Compatibility

`host_shell/` is retained as a compatibility shim for the generalized
`execution_runtime/` architecture.

Use `execution_runtime/` for new code:

- `HostShellProvider` → `ExecutionRuntimeProvider`
- `HostShellRequest` → `ExecutionRuntimeRequest`
- `HostShellResponse` → `ExecutionRuntimeResponse`
- `HOST_SHELL` → `EXECUTION_RUNTIME`

The authority boundary is unchanged: runtime output is noncanonical, does not
write ARK, does not create observations, and cannot bypass artifact promotion or
ARK admission membranes.
