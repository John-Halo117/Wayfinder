# Architecture

Repository organization follows responsibility.

```text
Reality
  |
CivPhys
  |
Constitution
  |
Objectives
  |
Capability Grammar
  |
Capabilities
  |
Contracts
  |
Services
  |
Engines
  |
Domains
  |
Internal Applications
  |
External Systems
  |
Operations
```

Dependencies only point downward. When a dependency would point upward, the
concept must be reclassified or expressed as a contract.



## Repository And Execution

Repository organization follows responsibility. Execution semantics are defined separately in [execution.md](execution.md).

The repository stack is not an execution pipeline. When a concept appears to belong to multiple layers, classify it by canonical ownership and express cross-layer communication through contracts.
