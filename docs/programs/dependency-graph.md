# Cross-Program Dependency Graph

Date: 2026-06-27

This graph is program-level planning. It is distinct from engine dependency graphs and repository topology.

## Primary Program Chain

```text
Platform Services
  -> Reality Identity (RID)
  -> Universal Asset Ingestion
  -> Runtime Kernel
  -> ARK
  -> WEAVE
  -> Interpretation
  -> Reasoning
  -> Views
  -> Jarvis
```

## Expanded Graph

```text
Constitution v1
  -> Platform Services
      -> Identity Service
      -> Event Bus
      -> Storage
      -> Configuration
      -> Policy
  -> Reality Identity (RID)
      -> Universal Asset Ingestion
          -> Runtime Kernel
              -> ARK
                  -> WEAVE
                      -> Interpretation
                          -> Reasoning
                              -> Views
                                  -> Jarvis
                                      -> Capsules
                                      -> ZWLib
                                      -> Foundry
                                      -> NOMAD
                                      -> MIDAS
                                      -> MICE
                                      -> VALOR
                                      -> Blackwall
                                      -> NetWatch
  -> Repository Portfolio
      -> wayfinder-infra
      -> domain repositories
```

## Dependency Rules

- Platform Services provide reusable infrastructure.
- RID depends on Identity Service and the Asset Model.
- Universal Asset Ingestion depends on RID and the Asset Model.
- Runtime Kernel depends on platform services and universal ingestion boundaries.
- ARK depends on Runtime Kernel, Universal Asset Ingestion, RID, and platform services.
- WEAVE and later engines depend on ARK reality outputs.
- Infrastructure and domain repositories depend on Wayfinder platform boundaries, not the reverse.

## Acyclicity Check

| Edge | Status |
| --- | --- |
| Platform Services -> RID | Pass |
| RID -> UAI | Pass |
| UAI -> Runtime Kernel | Pass |
| Runtime Kernel -> ARK | Pass |
| ARK -> WEAVE -> Interpretation -> Reasoning -> Views -> Jarvis | Pass |
| Wayfinder -> Portfolio repositories | Pass |

No program-level dependency points back toward a prerequisite.
