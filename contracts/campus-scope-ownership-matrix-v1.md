# Polaris Campus Scope & Ownership Matrix v1

Status: CANONICAL

## Purpose
Separate **what a capability means and who owns its truth** from **where a particular implementation is deployed**. GH, MH, Campus, digital systems, vehicles, field kits, and external-world sensing may share semantics without duplicating machinery or forcing every capability into every place.

## Two independent axes
Every consequential capability/object/service SHOULD resolve both:

1. **SEMANTIC OWNER** — canonical truth/logic owner.
2. **DEPLOYMENT SCOPE** — physical/digital place(s) where an implementation instance lives.

Never infer deployment from semantic ownership or ownership from deployment.

Example: AUTHORITY/IDENTITY semantics are SHARED/DIGITAL; a lock actuator may be deployed at GH, MH, workshop, gate, vehicle, or package boundary. One authority model, many scoped actuators.

## Deployment scopes
- `SHARED` — campus-wide semantics/infrastructure available to multiple scopes; not synonymous with physical duplication.
- `GH` — compact first-stage house.
- `MH` — long-term primary house.
- `CAMPUS_CORE` — shared fixed campus infrastructure/backbones outside a single building: utility distribution, network backbone, water storage/distribution, shared service yard, common paths, central docks where justified.
- `WORKSHOP` — fabrication/repair/tooling/material handling/dirty-noisy technical work.
- `GARAGE` — vehicle shelter/service support, tires, charging where applicable, automotive storage and staging.
- `GREENHOUSE_GARDEN` — greenhouse, food forest, garden production, harvest handling, irrigation and plant-support infrastructure.
- `ANIMAL` — chickens/ducks/alpacas and associated shelter, feed, water, health, waste, fencing and handling.
- `LANDSCAPE_WATER` — pond/pool/trails/swales/rainwater/land drainage/site ecology and outdoor spatial systems.
- `UTILITY_PLANT` — well/water treatment, energy storage/generation, pumps, distribution hardware, septic/wastewater interfaces, mechanical service equipment where centralization is lifecycle-positive.
- `BULK_STORAGE` — seasonal/bulky/low-frequency inventory not worth residential floor area.
- `MOBILE_FIELD` — portable kits, PACKOUT/loadouts, carts, temporary workstations, camping/preparedness/field tools.
- `VEHICLE` — vehicle-installed capability and vehicle-specific inventory.
- `DIGITAL_CORE` — Basecamp/NAS/NVR/identity/authority/evidence/automation/data services and canonical digital truth.
- `EDGE_NODE` — AMOS/edge participants, local sensing/actuation/compute nodes.
- `PERSONAL_DEVICE` — phone/wearable/personal client projections and credentials.
- `EXTERNAL_WORLD` — off-property observations/sources/EWS; represents external reality, not campus-owned infrastructure.
- `UNKNOWN_SCOPE` — unresolved historical deployment; cannot inherit automatically.
- `N_A` — explicitly not applicable.

`CAMPUS` in older contracts is now a family/umbrella term; new material should prefer the more specific subscopes above when useful.

## Semantic owner families
- `HABITAT` — spatial/building requirements, rooms, envelopes, boundaries, accessibility, service geometry.
- `UTILITY` — water, wastewater, energy, HVAC distribution semantics, utility routing/isolation.
- `PHYSICAL_EXECUTION` — tools, kits, carts, staging, readiness, reset/park, mechanical assistance.
- `INVENTORY_RESOURCE` — identity, quantity, replenishment, location, stock/flow and lifecycle.
- `AUTHORITY_DEFENSE` — identity, authorization, security policy, least-authority, safety boundaries.
- `DIGITAL_PLATFORM` — Basecamp/AMOS service orchestration, networking, compute, storage and local applications.
- `EVIDENCE_REALITY` — observation, provenance, EWS/world-state, sensing and composition.
- `AUTOMATION_CONTROL` — execution policy, scheduling, actuators, state machines; authority remains separate.
- `SANCTUARY_HUMAN` — comfort, peace, restorative life, human-interface and attention constraints.
- `MOBILITY_VEHICLE` — vehicle-specific operation/maintenance/readiness semantics.
- `LAND_ECOLOGY` — land, watershed, ecology, agriculture and external/local environmental interaction.

These are ownership families/projections over canonical Polaris owners, not new sovereign databases.

## Placement laws
1. Put capability at the **lowest total lifecycle-burden scope** that still satisfies frequency, accessibility, latency, security, weather, service and consequence requirements.
2. **Share expensive/specialized capability; duplicate cheap friction-killers at point of use** when lifecycle-positive.
3. Do not force noisy, dirty, bulky, hazardous, seasonal or industrial capability into GH/MH merely because the campus needs it.
4. Do not externalize high-frequency essential household capability so far that routine life becomes travel/setup burden.
5. Digital truth is preferentially centralized/replicated by semantics; UI projections may exist everywhere without becoming independent truth stores.
6. Physical payloads may move across scopes; semantic identity does not change with location.
7. A shared backbone does not imply shared failure domain: preserve local isolation/manual fallback where consequence requires.
8. GH and MH may each have local minimum viable utility/control capability even when supplied by Campus Core.
9. Placement follows actual concurrency and workflow, not noun convention.
10. `UNKNOWN_SCOPE` is quarantine, never a universal default.

## Default sorting — SHARED / DIGITAL
Campus-wide shared semantics and mostly-digital truth:
- Polaris/Wayfinder/Jarvis logic and policy.
- identity, authority, credentials, permissions and least-authority policy.
- evidence/provenance/CAS/World State/EWS.
- Master Reality Watch Registry and composition graph.
- inventory identity/schema and cross-campus location graph.
- maintenance records, manuals, standards mappings, receipts and lifecycle history.
- automation schedules/policies and event routing.
- household calendar/task/notification semantics.
- network identity/addressing, service discovery and device registry.
- media library/catalog, document library and knowledge corpus.
- security event semantics and audit receipts.
- resource/finance/accounting semantics.
- shared semantic shape standards and ontology resolution.

Deployment: `DIGITAL_CORE` with selected replication to `EDGE_NODE` and projections to `PERSONAL_DEVICE`, GH/MH panels/clients, workshop clients, vehicle clients where useful.

## Default sorting — GH
GH owns only the compact complete residential minimum plus GH-specific convenience:
- two bedrooms/two baths and associated accessible residential storage.
- compact wet/service core, shared plumbing geometry, manifold/shutoffs and accessible service panels.
- compact kitchen and efficient pantry wall/storage.
- right-sized laundry operating envelope, linen transfer/storage, ceiling airer where justified.
- ordinary dining/living/rest/sleep capability.
- basic residential HVAC/ventilation and local controls.
- essential electrical/data endpoints; future pathways without speculative payload population.
- local network/voice/sensor endpoints only as needed; canonical services remain Digital Core.
- robot dock/passages where nearly free.
- cat portals/elevated routes where low burden.
- small utility/household cart + parking pocket.
- passive accessibility: drawers/pull-outs/flush floors/reachability.
- local life-safety, egress, manual access and emergency controls.

Prefer Campus/Workshop/Bulk Storage for bulky, noisy, dirty, specialized or low-frequency capability. GH spends space reluctantly.

## Default sorting — MH
MH is the long-term human habitat and can justify more dedicated, permanent, experiential capability:
- primary bedrooms/baths/family spaces.
- hallways/transition space where privacy, acoustics, navigation or experience earns them.
- library/reading/craft capability and dedicated rooms where recurring use justifies permanence.
- more generous storage, closets and some walk-ins when circulation earns its area.
- grooming/barber capability where desired.
- hospitality/guest functions and stronger public/private zoning.
- more permanent furniture and fewer daily transformations.
- richer AV/media projection endpoints without owning the media truth store.
- residential comfort sensing/control endpoints.
- local utility isolation/control/service access.
- selected deployables/hidden functions only when calm and lifecycle burden remain favorable.
- protected negative/restorative space, views and architectural delight.

MH does not inherit GH compression as a default. MH spends space intentionally.

## Default sorting — CAMPUS CORE / UTILITY PLANT
Shared fixed infrastructure where centralization has real lifecycle advantage:
- well head and water treatment/UV where site design favors central service.
- bulk water storage/rainwater tanks and main distribution.
- septic/wastewater backbone and cleanouts according to actual system geometry.
- photovoltaic generation, batteries/inverters and energy distribution when centralization is appropriate.
- main network fiber/copper backbone and outdoor AP/backhaul infrastructure.
- central utility/service routes, isolation points and metering.
- package/exchange boundary where useful.
- shared waste/recycling/compost logistics where practical.
- campus-level emergency shutoff/isolation topology.
- shared paths/drive/access and service staging.

Do not create a giant central plant if distributed simple systems have lower lifecycle burden or better failure isolation.

## Default sorting — WORKSHOP
- fabrication, welding, machining, 3D printing and electronics benches.
- lumber/sheet-goods/material racks.
- heavy jacks, machinery skates, hoists, lifts, panel carts and mechanical handling aids.
- tool storage, PACKOUT modules and job staging.
- dirty/noisy repair, painting/finishing where suitably controlled.
- calibration/metrology stations.
- spare parts and technical consumables near point of use.
- service documentation/client terminal as a projection of Digital Core.
- dust/fume/noise controls appropriate to operations.

Do not put routine household capability here if the walk/setup tax exceeds the saved residential burden.

## Default sorting — GARAGE / VEHICLE
Garage:
- vehicle shelter, tire/wheel storage, chargers/maintainers where applicable.
- rolling tire racks, vehicle fluids/consumables, automotive maintenance modules.
- overhead bulky storage only when retrieval/safety justify it.
- vehicle staging and loading/unloading support.

Vehicle:
- vehicle-specific readiness kit, field repair essentials, emergency/support loadout.
- navigation/communications projection, not canonical map/world truth.
- local vehicle state/maintenance observations synced to Digital Core.

Avoid turning the vehicle or garage into a duplicate workshop unless workflow justifies it.

## Default sorting — GREENHOUSE/GARDEN / LANDSCAPE/WATER / ANIMAL
Greenhouse/Garden:
- seed/propagation, plant tools, irrigation endpoints, harvest staging, selected food processing near production when useful.
- greenhouse environmental sensing/control locally, with data shared upstream.

Landscape/Water:
- rainwater routing, swales/drainage, pond/natural pool, trails, meadow/food forest, outdoor lighting/security only where justified.
- ecology/weather/local external sensing.

Animal:
- shelter, feed storage, water, fencing, handling/health modules, waste/compost routing and dedicated tools.

Dirty biological flows remain separated from clean household flows while sharing inventory/evidence semantics.

## Default sorting — BULK STORAGE
- seasonal decorations.
- bulky low-frequency tools/equipment.
- reserve consumables beyond point-of-use quantities.
- camping/field modules not in current rotation.
- spare furniture/building materials where retention is justified.

Bulk Storage is not a junk sink: everything retained still requires identity/value/home/disposition when tracking earns its keep.

## Default sorting — MOBILE FIELD
- preparedness duffles/modules.
- camping/fishing/field kits.
- job-specific portable loadouts assembled from shared modules.
- temporary carts/mobile stations.
- survey/inspection kits.

Portable capability parks at the scope minimizing retrieval and reset burden; it may temporarily deploy anywhere.

## Default sorting — EDGE NODE / PERSONAL DEVICE
Edge Node:
- local sensing, protocol bridges, low-latency control, bounded offline execution, caches and local models where justified.
- no unnecessary independent semantic truth.

Personal Device:
- human-facing projections, credentials, capture, local emergency capability and portable control surface.
- phone loss/replacement must not destroy canonical household state.

## External World
`EXTERNAL_WORLD` owns no campus hardware by definition; it is the represented environment around the property/candidate places:
- weather/climate/air/light/water/soil/geology/ecology/fire/noise/access/utilities/development/externalities.
- local/regional/state/national Reality Watch observations.
- candidate-parcel history and external risk/opportunity.

Physical sensors located on campus are deployments of Evidence/Reality capability; the observed external state remains External World.

## Duplication policy
For any capability considered at multiple scopes, classify:
- `CANONICAL_SHARED` — one truth, many projections.
- `SHARED_BACKBONE_LOCAL_ENDPOINTS` — common infrastructure with local endpoints.
- `DUPLICATE_POINT_OF_USE` — intentionally duplicated low-cost capability.
- `SPECIALIZED_SHARED` — expensive/specialized capability shared from one location.
- `MOBILE_SHARED` — one portable capability moves to job.
- `LOCAL_REQUIRED` — each scope needs an independent minimum because failure/latency/access consequence demands it.

This field is distinct from deployment scope.

## Anti-patterns
- **Scope by noun:** “laundry belongs in a laundry room,” “tools belong in garage,” without workflow analysis.
- **Campus dumping:** moving everything undesirable out of GH/MH until routine living requires constant trips.
- **Residential hoarding:** keeping campus-scale bulk/specialty capability inside houses.
- **Digital duplication:** separate truth databases per building/device.
- **Centralization religion:** one central failure takes down every building.
- **Duplication religion:** every building gets a full copy of every capability.
- **Mobile-everything syndrome:** shared portable capability causes constant retrieval/reset conflicts.
- **Edge sovereignty creep:** cache/node becomes independent truth authority.
- **Projection authority:** local dashboard becomes canonical state.
- **Location-coupled identity:** moving an object changes its semantic identity.
- **Unknown-scope leakage:** historical assumption silently propagates.
- **GH-to-MH leakage / MH-to-GH leakage.**
- **Dirty/clean flow collision.**
- **Security-zone collapse:** physical reach mistaken for authority.
- **Backbone means dependency:** no local safe/manual mode.

## Resolution compiler
For each capability:

REQUIREMENT
-> SEMANTIC OWNER
-> FREQUENCY / CONCURRENCY / CONSEQUENCE
-> PHYSICAL vs DIGITAL vs HYBRID
-> CLEAN/DIRTY/NOISY/BULKY/HAZARDOUS/WEATHER EXPOSURE
-> ACCESSIBILITY / LATENCY / SECURITY
-> SHARE vs DUPLICATE vs MOBILE vs LOCAL REQUIRED
-> CANDIDATE DEPLOYMENT SCOPES
-> TOTAL LIFECYCLE BURDEN
-> SELECT LOCATION(S)
-> DEFINE INTERFACES / PARK / SERVICE / FAILURE / SYNC
-> VERIFY NO CROSS-SCOPE LEAKAGE

Placement is corrigible: when actual use changes, move payloads without rewriting semantic identity or truth ownership.
