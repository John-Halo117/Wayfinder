# Dependency Constitution

Wayfinder dependencies follow constitutional direction.

Architecture is organized by responsibility. Execution is organized by
durability. Dependencies must preserve both.

## Layer Order

```text
Constitution
  |
Contracts
  |
Capabilities
  |
Services
  |
Engines
  |
Domains
  |
Internal Applications
  |
External Integrations
  |
Operations
  |
Tooling
```

Dependencies may point upward in this diagram only when the lower visual layer
is a runtime wrapper around the higher canonical owner. The canonical
architecture rule is: implementation depends on more stable language and
infrastructure, not on its consumers.

## Allowed Dependencies

| From | May Depend On |
| --- | --- |
| `constitution/` | Nothing inside implementation layers |
| `contracts/` | `constitution/` |
| `capabilities/` | `constitution/`, `contracts/` |
| `services/` | `constitution/`, `contracts/`, `capabilities/` |
| `engines/` | `constitution/`, `contracts/`, `capabilities/`, `services/` |
| `domains/` | `contracts/`, `capabilities/`, `services/`, `engines/` |
| `internal/` | `contracts/`, `services/`, `engines/`, `domains/` |
| `external/` | `contracts/`, `services/` |
| `operations/` | Deployment targets and configuration for all layers |
| `tooling/` | Repository files required for development and validation |

## Forbidden Dependencies

| Rule | Forbidden Example |
| --- | --- |
| Contracts must not contain implementation. | `contracts/events/publisher.py` |
| Services must not depend on engines. | `services/storage` importing `engines/ark` |
| Services must not depend on domains. | `services/identity` importing `domains/homestead` |
| Engines must not depend on other engines without an explicit contract boundary. | `engines/ark` importing `engines/foundry/core` |
| Engines must not own reusable infrastructure. | `engines/ark/storage` as canonical storage |
| Domains must not own infrastructure. | `domains/finance/event_bus.py` |
| Internal apps must not become canonical owners of concepts. | `internal/api/identity.py` defining RID semantics |
| External integrations must remain replaceable. | `external/home-assistant` owning Wayfinder automation rules |
| Operations must not define business or engine behavior. | `operations/deployment/reality_graph.py` |

## Engine-to-Engine Rule

Engine-to-engine imports are forbidden by default.

Allowed communication paths:

- Contracts
- Services
- Event Bus
- Domain orchestration

If two engines need direct coordination, define the shared language in
`contracts/` and route execution through a service or domain.

## Service-to-Service Rule

Service-to-service dependencies are allowed only when both services remain
generic and the dependency is explicitly documented.

Examples:

- Event Bus may use Storage for replay support.
- Storage may use Identity references for ownership metadata.
- Policy may use Contracts for policy document schemas.

## Validation Strategy

The constitutional linter should:

1. Build a filesystem ownership map.
2. Parse import/module references where language tooling is available.
3. Scan documentation links for architectural owner claims.
4. Compare dependencies against the allowed matrix.
5. Report forbidden dependencies as structured findings.
6. Fail promotion checks when high-severity violations are unresolved.

## Structured Finding

```json
{
  "status": "error",
  "error_code": "DEPENDENCY_RULE_VIOLATION",
  "reason": "A service depends on an engine.",
  "context": {
    "from": "services/storage",
    "to": "engines/ark"
  },
  "recoverable": true
}
```

