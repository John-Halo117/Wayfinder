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
  middleware. Ollama's direct desktop-client gateway support is a current example;
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
- Embedded home-automation edge: use ESPHome-class maintained firmware before
  inventing dedicated bridge software when it can provide Bluetooth proxying,
  multi-interface Ethernet/Wi-Fi networking, maintained Modbus behavior, OTA key
  rotation, and sensor/actuator integration while preserving local control.
- Home Assistant host management: prefer maintained Supervisor/OS APIs and native
  mount/container/storage management before shell glue, host-side repair scripts,
  duplicate health checks, or parallel lifecycle services.
- Local-model desktop access: when a maintained desktop client can connect directly
  to the local model runtime, use that path before adding an OpenAI-compatibility
  proxy or UI-specific middleware. Pre-release support remains gated by the
  Stability Gate.
- Interoperable smart-home devices: for new cameras, closures, soil sensors,
  irrigation-adjacent sensing, energy devices, and similar categories, evaluate
  adequate Matter support before vendor-specific cloud APIs or custom adapters.
  Matter is preferred only where the required local control, telemetry, security,
  and reliability are actually present.
- Fabrication workflow: prefer maintained slicer/project/plugin capabilities over
  external preprocessing services or custom print-preparation automation when the
  slicer can safely own the transformation.
- Recipe ingestion: prefer the maintained recipe platform's importer, retry,
  browser-signature, proxy, or headless-browser escalation before building a
  separate scraper/import-resilience service. Custom ingestion exists only for a
  demonstrated persistent gap.
- Thread network ownership: treat Thread network identity and credentials as
  platform state rather than radio state. Prefer a maintained OpenThread Border
  Router and platform-managed credentials so border-router hardware can be
  replaced or migrated without redefining the network. Harvest standard Thread
  diagnostics, credential sharing, commissioning, and infrastructure integration
  before creating proprietary Thread-management tooling.
- Home-automation backup: let the automation platform own its maintained backup
  mechanism, encryption format, scheduling, retention primitives, and supported
  backup targets. Basecamp owns backup policy, independent copies, restore
  verification, and continuity requirements; custom archive/encryption/rotation
  scripts exist only for an uncovered requirement.
- Local house-control voice: prefer a maintained fully local speech-to-text,
  intent-processing, and text-to-speech path for house commands before building a
  second voice-control stack. General conversational AI may remain a separate
  capability where its function exceeds deterministic house control.
- Camera-event intelligence: prefer the camera/NVR platform's maintained local
  semantic indexing, embeddings, event search, and similarity capabilities before
  exporting frames into a separate vector database or custom search service.
  Wayfinder should consume the resulting capability rather than duplicate it.
- EV charging and bidirectional energy: for future charger and vehicle-energy
  interfaces, prefer adequate OCPP 2.1 and ISO 15118-20 support, documented local
  control, and interoperable DER behavior before proprietary charger APIs or
  custom orchestration. Standards are preferred only when the required hardware
  implementation is complete and reliable.
- Utility and grid signaling: prefer OpenADR 3 or another adequate open utility
  signaling interface for tariffs, demand response, DER, storage, EV charging,
  and capacity events before one-off utility adapters. Keep local energy policy
  downstream of the standardized signal rather than embedding utility-specific
  behavior throughout automations.
- Document ingestion and household records: prefer the document platform's native
  mail ingestion, scheduled workflows, webhooks, storage/filename templates,
  duplicate handling, custom fields, and routing before building a Basecamp
  document watcher or router. Bills, manuals, warranties, receipts, property
  records, and maintenance documents should enter through maintained document
  semantics where adequate.
- Long-range property sensing: for gates, barns, sheds, tanks, utility structures,
  and other low-bandwidth remote points, evaluate adequate standardized long-range
  options such as Z-Wave Long Range alongside Thread and wired interfaces before
  designing repeater-heavy meshes or custom radio infrastructure.
- Lighting control: evaluate standards-based DALI/DALI+ capability, including
  Thread transport where mature and appropriate, before inventing a proprietary
  lighting-control bus or wireless translation layer. Preserve serviceable local
  lighting operation independent of higher-level automation.
- UPS and power-device telemetry: prefer Network UPS Tools or another maintained
  standard telemetry/control layer plus the platform's native integration before
  creating a UPS telemetry daemon, duplicate polling service, or proprietary
  dashboard. Custom code exists only for demonstrated missing control or state.
- Household inventory: harvest maintained Grocy-class APIs, add-ons, and native
  product/stock operations before writing synchronization or CRUD middleware whose
  only purpose is reproducing household inventory semantics.
- Parts and workshop inventory: harvest maintained InvenTree-class inventory,
  security, API, and workflow capabilities before creating a Basecamp-specific
  parts database or stock service. Wayfinder should add cross-domain reasoning,
  not duplicate mature inventory semantics.

## Jarvis Capability Harvest

Jarvis is the persistent human-facing identity and intelligence that composes
Basecamp capabilities. It is not required to own the implementation of every
capability it can perceive or invoke.

Prefer harvesting maintained applications, protocols, and platform primitives for
Jarvis organs before creating equivalent Wayfinder services:

- House nervous system and voice: use Home Assistant Assist for deterministic
  house intent and Home Assistant's local voice pipeline where adequate. Use
  Wyoming as the modular transport for maintained speech-to-text, text-to-speech,
  and wake-word engines such as Whisper, Speech-to-Phrase, Piper, and
  openWakeWord. Do not create a second house-command intent or audio RPC stack.
- Physical-world tool bridge: use Home Assistant's MCP Server and Assist API to
  expose explicitly permitted entities, tools, and live home context to Jarvis.
  Device protocols stay behind Home Assistant rather than becoming Jarvis tools
  one device at a time.
- External tool acquisition: where Home Assistant is the active conversation
  surface, use its MCP client integration to acquire maintained external tools
  before implementing bespoke tool adapters. Account for the integration's
  supported MCP feature subset rather than assuming full protocol coverage.
- Conversational console and RAG: evaluate maintained self-hosted conversational
  interfaces such as Open WebUI before creating a Basecamp-specific chat/RAG
  frontend. Keep the interface replaceable and keep canonical Basecamp state out
  of interface-specific storage where practical.
- Local inference: use maintained local-model runtimes such as Ollama as
  interchangeable inference substrates rather than making one model runtime the
  identity of Jarvis.
- Digital workflow execution: evaluate maintained workflow engines such as n8n
  for non-house digital workflows before creating a generic Wayfinder workflow
  engine. Home Assistant remains the preferred owner for physical-house
  automation where adequate.
- Assistant implementation references: mine maintained open-source personal-agent
  projects for proven interaction, routing, desktop-presence, computer-use,
  channel, and worker-delegation patterns. Personal Jarvis and similar projects
  are implementation references or replaceable components, not canonical
  Basecamp identity.
- Persistent memory: prefer a maintained, inspectable memory or knowledge layer
  that can separate working context, durable personal knowledge, source history,
  and user-editable records before building a bespoke memory database. QwenPaw's
  ReMe-style layered memory is a current implementation reference; evaluate its
  boundaries and maturity before adoption.
- Cross-device continuity: prefer an assistant substrate that can preserve
  conversation/task continuity across browser, desktop, mobile, terminal, and
  messaging surfaces without making any one UI canonical. Self-hosted multi-user
  and multi-channel agent platforms are candidates when they preserve required
  sovereignty and exportability.
- Agent and model routing: harvest maintained routing between fast/local models,
  deeper models, coding agents, browser/computer-use workers, and long-running
  tasks before creating a bespoke dispatcher. Routing policy remains a Wayfinder
  concern even when execution mechanics are harvested.
- Computer and screen agency: evaluate maintained browser-use, computer-use, OS
  shell, workspace, and checkpoint primitives before implementing screen scraping,
  mouse/keyboard automation, or desktop-control daemons. Expose only bounded
  capabilities and retain confirmation/permission boundaries for consequential
  actions.
- Proactive awareness: use event-driven automation, calendars, sensors, state
  changes, scheduled summaries, and maintained notification channels to wake
  Jarvis when a meaningful condition changes. Do not create a permanent polling
  loop merely to simulate awareness when upstream event sources exist.
- Briefings and notifications: prefer Home Assistant automation/Assist summary
  patterns and maintained notification integrations for household-state and
  calendar-derived briefings before creating a parallel push-delivery service.
  Wayfinder owns relevance and attention policy; delivery mechanisms are
  replaceable.
- Vision: consume maintained semantic outputs from Frigate for camera events and
  Immich for household-photo intelligence before building a general visual index.
  Add a separate vision layer only for demonstrated real-time or cross-domain
  reasoning gaps.
- Documents and recall: use Paperless-ngx for document ingestion and document
  workflow semantics, then expose selected retrieval capability to Jarvis rather
  than duplicating OCR, filing, and document-routing machinery.
- Calendar, email, contacts, and personal services: prefer maintained provider
  integrations, plugins, or MCP/API connectors with scoped permissions before
  implementing provider-specific clients inside Jarvis. Jarvis owns the unified
  interaction model, not each provider protocol.
- Household identity and presence: prefer explicit household identities plus
  maintained presence/device/person primitives from Home Assistant and relevant
  domain systems. Do not infer sensitive identity or presence beyond the evidence
  needed for the requested automation or interaction.
- Phone and room presence: use Home Assistant companion/mobile clients and
  voice-satellite endpoints as replaceable Jarvis surfaces before creating a
  proprietary mobile client or room audio protocol.

### Jarvis Composition Rule

Jarvis should feel singular to the human while remaining plural underneath.

The preferred flow is:

human interaction surface -> Jarvis orchestration/policy -> model or reasoning
runtime -> permissioned tools/protocols -> harvested domain systems -> physical
and digital reality.

Jarvis owns identity, continuity, permission policy, cross-domain context,
attention policy, reasoning, and composition. Domain systems own their mature
mechanics. A capability may move between implementations without changing the
human-facing Jarvis identity.

### Jarvis Proactivity Rule

Proactivity must be event- and relevance-driven, not chatter-driven. Jarvis may
surface a condition without being asked when evidence indicates that timing,
safety, continuity, cost, a committed plan, or another established Wayfinder path
materially changed. Otherwise archive the event.

Prefer upstream event subscriptions and automation triggers over repeated polling.
Notifications must remain finite, attributable to a real state change, and
controllable by the household.

These examples are replaceable implementation notes, not permanent product
commitments. Future Capability Harvest passes should retire or replace examples
when better maintained primitives emerge.

## Basecamp Composition Boundary

Basecamp should be a sovereign coordination and composition layer over harvested
capability islands, not a monolith that reimplements each island.

Where maintained systems adequately own a domain, Basecamp should primarily own:

- cross-domain policy and orchestration;
- canonical intent and capability requirements;
- identity and relationships between physical and digital scopes;
- verification and operational state;
- lifecycle and maintenance obligations;
- local-control and continuity boundaries;
- cross-system reasoning and derived decisions; and
- the irreducible integration gaps between otherwise capable systems.

A domain platform may own implementation mechanics without owning Basecamp's
canonical intent. Conversely, Basecamp must not reproduce implementation mechanics
merely to make itself appear self-contained.

## Bespoke-Code Deletion Rule

When a harvested upstream capability fully satisfies an existing bespoke
implementation's required function, local-control boundary, observability,
reliability, and rollback needs, delete the displaced custom code rather than
keeping a parallel implementation "just in case." Preserve only the irreducible
gap.

Deletion requires verification that:

1. the upstream path passes the Stability Gate;
2. required behavior and data remain available under loss of external services
   where the capability requires local continuity;
3. migration and rollback are tested;
4. no unique Wayfinder capability is silently removed; and
5. configuration, documentation, tests, and dependency references to the bespoke
   implementation are removed with the code.

If no matching bespoke implementation exists yet, record the displacement rule
and prevent that code from being built in the first place.

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
