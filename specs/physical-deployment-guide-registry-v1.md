# Polaris Universal Physical Deployment Guide Registry v1

Status: CANONICAL ROADMAP / GENERATIVE GUIDE CONTRACT

## Objective
Every Polaris capability that can manifest in physical reality must have a deployable guide or an explicit N/A/DEFERRED classification. Guides are generated from shared primitives and standards; they are not bespoke manuals duplicated per feature.

## Guide contract
For each deployable capability record:
REQUIREMENT -> SCOPE/OWNER -> PRECONDITIONS -> EXISTING STANDARD(S) -> SITE/GEOMETRY -> PASSIVE BASELINE -> MINIMUM HARDWARE -> POWER/DATA/UTILITY -> INTERFACES -> INSTALL SEQUENCE -> COMMISSIONING TEST -> NORMAL OPERATION -> INSPECTION/MAINTENANCE -> FAILURE/SAFE STATE -> MANUAL FALLBACK -> REPAIR/REPLACEMENT -> SPARES/TOOLS -> DECOMMISSION/RECOVERY -> UPGRADE PATH -> COST/RESOURCE BAND -> AUTHORITY/PRIVACY/SAFETY -> EVIDENCE/AS-BUILT RECEIPT.

Each guide declares deployment states: NOT_NEEDED, RESERVED, READY, DEPLOYED, COMMISSIONED, DEGRADED, SERVICE, RETIRED, UNKNOWN.

## Universal scope registry
### Site / land
survey/control points; access; grading/earthwork; drainage; erosion; roads/paths; retaining only where required; fencing/gates; exterior exchange; fire/fuel management; ecological protection; conservation zones; soil/water monitoring; site lighting where justified.

### Structure / enclosure
foundation; frame; roof; walls; windows/openings; doors; waterproofing; air barrier; insulation; vapor control; acoustic assemblies; fire/smoke separation; service cavities; attachment infrastructure; accessibility geometry; pest exclusion.

### Water / wastewater
well/source; storage; treatment; distribution; manifolds; hot water; recirculation where justified; drainage; floor drains; septic/wastewater; rainwater capture; irrigation; pond/pool; leak isolation; gravity fallback; sampling/monitoring.

### Energy / electrical
utility service; service entrance; grounding/bonding; panels/subpanels; branch circuits; receptacles; lighting; PV; batteries; inverter; generator interface if justified; critical-load islanding; surge protection; metering; load shedding; manual bypasses.

### Thermal / air / IEQ
heating/cooling; mini-splits; ventilation/ERV-HRV; filtration; dehumidification/humidity; combustion/wood heat; kitchen/bath exhaust; smoke/CO/radon/air-quality sensing; passive solar/shading; thermal storage/PCM where justified.

### Network / compute / data
WAN; LAN; structured cabling; Wi-Fi; racks; Basecamp compute; NAS; NVR; UPS; backup; time; DNS; identity/credentials; hardware admin path; edge nodes; sensors; local buses; offline operation; sync; logs; recovery media.

### Security / authority / privacy
physical locks; access boundaries; gate/door control; cameras; intrusion sensing; fire/life safety; scoped service access; local/manual entry; credential provisioning/revocation; purpose-bound authority; privacy zones; emergency override; audit/receipts.

### GH
wet/service core; kitchen/pantry; bath/laundry; bedroom/living; productive boundaries; storage; carts; robot/pet accommodation; local HVAC; local life safety; local network; service panels; point-of-use shutoffs; move-in minimum.

### MH
long-term residential zones; halls/circulation; library/craft; grooming; hospitality; richer storage; AV; accessibility; comfort; distributed endpoints; productive/deployable spaces; local isolation and fallback.

### Campus core
backbone utilities; network trunks; shared distribution; isolation; common paths; package/exchange boundary; service routes; common sensing; campus identity topology; shared resource routing; emergency/service access.

### Workshop
power; lighting; dust/fume extraction; compressed air if justified; benches; fabrication; electronics; 3D printing; material storage; tool interfaces; lifts/hoists where qualified; fire safety; dirty/clean zoning; PACKOUT/kits; service documentation.

### Garage / automotive
vehicle bays; charging/maintainers; tire/storage; fluids/consumables; jacking/lifting interfaces; wash/drainage where allowed; diagnostics; maintenance stations; vehicle data boundary; loading/staging.

### Greenhouse / garden / food production
structure; thermal control; ventilation; irrigation; water storage; propagation; beds; trellis/support; lighting only where justified; sensors; harvest staging; food forest; compost; tool/storage; passive season extension.

### Animals
shelter; fencing; gates; feed/water; handling; health/isolation; waste; predator protection; shade/thermal; transport; sensors only where useful; emergency/manual care.

### Landscape / recreation / water
trails; meadow; pond; natural pool; sauna; outdoor structures; drainage/swales; erosion; irrigation; habitat; lighting; attachment/play/fitness interfaces where engineered; maintenance access.

### Storage / logistics
bulk storage; pantry; cold storage where justified; consumables; bins; standards->bins->kits->stations; carts; docks; transfer openings; package handling; inventory identity; reserve levels; FIFO/FEFO where relevant.

### Robots / machines / automation
robot clearances; docks; charging; local control; authority boundaries; machine routes; vacuum/mower/etc.; actuators; manual override; safe stop; maintenance; replaceable protocol adapters; no permanent geometry tied to one vendor without proof.

### Personal devices / interfaces
phone/tablet/wearable; local UI; credentials; capture; voice endpoints; charging; replacement/bootstrap; loss recovery; accessibility; offline emergency functions; no canonical truth only on personal device.

### Vehicle / mobile / field
vehicle node; navigation; comms; maintenance kit; preparedness; inspection kit; camping/field modules; portable power; water; offline maps/docs; secure credentials; sync-on-return; loss/theft boundary.

### Preparedness / resilience
critical loads; water reserve; thermal fallback; lighting; communications; medical/first aid storage; fire response; weather readiness; outage modes; manual controls; recovery drills; spares; offline documentation.

### Household transformation / food / laundry / cleaning
procurement receiving; pantry; cooking; preservation/fermentation; cleaning; laundry; drying; waste/reuse; tool/consumable stations; passive transfers; deploy/reset/park; hygiene/grooming; service/maintenance.

### Media / knowledge / education
library; local media; displays/audio; classroom/homeschool surfaces; scanners/capture; printing; archival storage; offline reference; network projection; repair/replacement.

### Health / accessibility / assistive
accessible routes/reach; grab/support interfaces; seating/rest; transfer assistance; exercise/rehab interfaces; medication storage/organization; emergency access; assistive-device parking/charging; passive/manual baseline; professional/code requirements preserved.

### External observation / property twin
weather station; air; water; soil; energy; utility; noise; cameras only where authorized; ecological sensors; network placement; calibration; sampling cadence; local buffering; provenance; replacement; sensor-dominance pruning.

## Guide generation law
Do not hand-author thousands of unrelated guides. Compose each guide from reusable modules: SITE, STRUCTURE, MOUNT, POWER, WATER, AIR, DATA, NETWORK, IDENTITY, AUTHORITY, SAFETY, ACCESS, SERVICE, STORAGE, CALIBRATION, COMMISSIONING, MAINTENANCE, FAILURE, RECOVERY, DECOMMISSION.

Domain guide = shared modules + domain-specific delta.

## Standards law
Before specifying an interface/component, search applicable building/electrical/plumbing/mechanical/fire/accessibility/network/IT/industrial/automotive/agricultural/medical/product standards and mature commodity interfaces. Polaris stores mapping and unresolved delta, not a replacement standards ecosystem.

## Deployment packet
At execution time compile only the relevant packet:
- scope/location and current as-built state;
- prerequisites/blockers;
- drawings/geometry/interfaces;
- applicable standards/code/professional gates;
- BOM/tool list only after design freeze;
- ordered install tasks/dependencies;
- inspection/test points;
- commissioning acceptance criteria;
- labels/IDs/photos/as-built evidence;
- maintenance/failure/recovery/decommission instructions.

## Timing classes
RESERVE_DURING_DESIGN: cheap geometry/routes/interfaces that become expensive later.
ROUGH_IN: penetrations, conduits, blocking, drains, service zones justified before finishes.
MOVE_IN_REQUIRED: life safety, water, sanitation, power, thermal, access, minimum network/compute required for habitation.
EARLY_OPERATION: high-value capabilities justified by actual use.
LATER: useful but nonbinding improvements.
ON_DEMAND: deploy only after trigger/need.
NEVER_BY_DEFAULT: speculative hardware or complexity.

## Completeness audit
Every capability node must resolve to one of:
PHYSICAL_GUIDE, DIGITAL_ONLY, EXTERNAL_ONLY, PROCEDURAL_ONLY, N/A, DEFERRED_WITH_TRIGGER, or UNKNOWN_BLOCKER.
UNKNOWN is surfaced as roadmap debt; it cannot silently disappear.

## Anti-patterns
shopping-list roadmap; vendor-first guide; custom-standard reflex; duplicate manuals; install-before-requirement; rough-in mania; future-proof-everything; mechanism promotion; unsafe DIY substitution for required professional/code work; commissioning omission; undocumented as-built state; no manual fallback; no decommission path; hardware becoming semantic truth; edge authority creep; guide staleness after reality changes; physical feature with no owner; automation that adds administration; maintenance-free fantasy; spare-everything; backup-everything; one giant campus deployment instead of staged closure.

## Final law
EVERY PHYSICAL CAPABILITY GETS A PATH FROM NOTHING -> RESERVED -> INSTALLED -> VERIFIED -> OPERATED -> SERVICED -> RECOVERED -> RETIRED, OR AN EXPLICIT REASON IT DOES NOT NEED ONE.