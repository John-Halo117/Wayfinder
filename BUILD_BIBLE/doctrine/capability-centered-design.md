# Capability-Centered Design

The Build Bible is organized around durable capabilities, not products.

## Rule

Capabilities remain stable while technologies, products, vendors, and
implementations evolve.

## Capability Examples

- shelter
- water
- energy
- communications
- food
- climate
- security
- observation
- storage
- workshop
- mobility

## Product Rule

Products are replaceable implementations. A product selection should not become
canonical doctrine unless it represents a stable physical principle.

## Integration Escalation Rule

When satisfying a capability through a software-controlled device or subsystem,
prefer the least bespoke maintained integration that preserves local control,
serviceability, reversibility, and required observability:

1. maintained native integration
2. standardized or device-aware protocol integration
3. custom mapping, adapter, or integration

For Home Assistant-connected physical systems such as energy, HVAC, water,
meters, inverters, and similar equipment, this means preferring a maintained
native Home Assistant integration first, then a standardized/device-aware shared
protocol connection (including Modbus where supported), and only then custom
register maps, YAML glue, or bespoke adapters.

A new upstream capability is a displacement candidate when it can eliminate,
shrink, simplify, or postpone planned custom work. Prefer deleting future bespoke
work over migrating a stable working system merely because a newer integration
path exists.

### Stability Gate

An upstream capability jump may change the preferred architecture immediately,
but deployment or migration waits until the relevant stable release/patch level,
hardware compatibility, rollback path, and required local-control behavior are
verified. Capability availability alone is not sufficient reason to migrate a
working subsystem.

## Relationships

- Parent doctrine: [Platform, Not Product](platform-not-product.md)
- Related ontology: [Property Capability Ontology](../registries/ontologies/property-capability-ontology.md)
- Related contract: [Capability Contract](../contracts/capability-contract.md)
- Related review: [Constitutional Review Questions](../governance/reviews/constitutional-review-questions.md)
- Generated artifacts: capability maps, dependency graphs, expansion maps,
  review reports
