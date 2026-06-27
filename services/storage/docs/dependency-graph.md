# Storage Service Dependency Graph

```mermaid
graph TD
  constitution["constitution/"] --> contracts["contracts/"]
  contracts --> service["services/storage/"]
  service -.future consumer.-> ark["engines/ark/"]
  service -.future consumer.-> jarvis["engines/jarvis/"]
  service -.future consumer.-> foundry["engines/foundry/"]
```

## Allowed Inbound References

Engines, domains, internal applications, and operations may consume this service through public contracts.

## Forbidden Outbound References

`services/storage/` must not depend on engines, domains, internal applications, external integrations, or operations.
