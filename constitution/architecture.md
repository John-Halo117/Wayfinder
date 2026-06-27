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

