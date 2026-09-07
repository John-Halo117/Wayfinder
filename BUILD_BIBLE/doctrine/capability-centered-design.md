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

## Native Observability Rule

Before building custom telemetry, inventory, diagnostic, topology, capacity, or
causality tooling, harvest the maintained platform's native observability surface.
Custom observability is justified only for a demonstrated information, retention,
automation, correlation, or sovereignty gap.

For Home Assistant, native protocol and subsystem diagnostics such as Serial,
MQTT, Matter topology, Activity causality, and network-storage capacity should be
used before adding parallel scripts, dashboards, or diagnostic services.

## Upstream Displacement Review

Capability Harvest must actively look for upstream changes that can delete,
collapse, simplify, or defer planned Wayfinder components. Evaluate the capability
provided, not the release novelty or product name.

Current displacement patterns to preserve in architecture reviews include:

- Remote connectivity: prefer a maintained open data-plane primitive when it can
  provide the required point-to-point connectivity without a permanent external
  control-plane dependency. Tailcat is a current candidate for simple WireGuard,
  NAT-traversal, and DERP-based links; managed Tailscale or another control plane
  remains appropriate when identity, policy, ACL, administration, or fleet
  management is actually required.
- Local AI interfaces: prefer direct maintained gateway/provider support between
  an interface and local model runtime over compatibility proxies or custom
  middleware. Ollama's direct Claude Desktop gateway support is a current example;
  it does not displace richer interfaces where their additional capabilities are
  required.
- Home automation observability: harvest Home Assistant's maintained diagnostics,
  protocol panels, topology views, causality traces, and storage-capacity views
  before creating equivalent Basecamp telemetry or glue.
- Storage plus lightweight compute: periodically reassess whether a stable storage
  platform can safely absorb lightweight service hosting and thereby remove a VM
  or separate host layer. TrueNAS 26's LXC and OpenZFS evolution is a current
  watch candidate, not a deployment dependency while the relevant release remains
  pre-stable or otherwise fails the Stability Gate.
- Household photo intelligence: harvest maintained search, clustering, and API
  capabilities from the photo platform before creating a separate indexing or
  household-photo query layer. Immich 3.2 is a current watch candidate and must
  pass the Stability Gate before production adoption.

These examples are replaceable implementation notes, not permanent product
commitments. Future Capability Harvest passes should retire or replace examples
when better maintained primitives emerge.

### Stability Gate

An upstream capability jump may change the preferred architecture immediately,
but deployment or migration waits until the relevant stable release/patch level,
hardware compatibility, rollback path, and required local-control behavior are
verified. Capability availability alone is not sufficient reason to migrate a
working subsystem.

Pre-release capability may justify postponing new bespoke work when waiting has
low mission cost and preserves option value, but it must not become a production
dependency until the gate is satisfied.

## Relationships

- Parent doctrine: [Platform, Not Product](platform-not-product.md)
- Related ontology: [Property Capability Ontology](../registries/ontologies/property-capability-ontology.md)
- Related contract: [Capability Contract](../contracts/capability-contract.md)
- Related review: [Constitutional Review Questions](../governance/reviews/constitutional-review-questions.md)
- Generated artifacts: capability maps, dependency graphs, expansion maps,
  review reports
