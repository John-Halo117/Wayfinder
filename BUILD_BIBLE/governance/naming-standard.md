# Naming Standard

Every physical scope and interface should have one clear name and one stable
ID.

## Applies To

- rooms
- circuits
- valves
- sensors
- conduit
- drains
- access panels
- cameras
- network drops
- trees
- equipment
- vehicles
- appliances
- utility interfaces

## ID Rule

Stable IDs follow `bb:<namespace>:<slug>`.

## Spatial Address Rule

Canonical spatial addresses use:

```text
[Domain].[Space].[Vertical].[Bearing]
```

## Label Rule

Visible labels should match canonical IDs or documented aliases. Field labels
must not introduce a third naming system.

## Rename Rule

Human names may change. Stable IDs do not change. Renames require alias
history.

## Relationships

- Related governance: [Identity And Addressing](identity-and-addressing.md)
- Related registry: [Identity Namespaces](../registries/identity-namespaces.md)
- Related schema: [universal-scope.schema.json](../schemas/universal-scope.schema.json)
- Generated artifacts: label schedules, circuit maps, valve maps, network drop
  maps, digital twin IDs

