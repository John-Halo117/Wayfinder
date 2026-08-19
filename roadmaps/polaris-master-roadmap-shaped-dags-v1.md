# Polaris Master Roadmap — Shaped DAG Portfolio v1

Status: CANONICAL ACTIVE ROADMAP

## Portfolio law
The roadmap is not one mega-graph. It is a family of typed DAGs sharing stable node IDs and cross-DAG edges. Each graph uses the shape appropriate to its causal structure. Stable background is machine-readable/drillable; the human surface remains delta-only.

Roadmap node states: DISCOVERED, SPECIFIED, PLANNED, READY, IN_PROGRESS, VERIFIED, DEPLOYED, OPERATING, DEGRADED, BLOCKED, DEFERRED, SUPERSEDED, RETIRED, IMPOSSIBLE, N_A, UNKNOWN.

Every node carries: ID, owner, scope, objective, current state, next verified successor state, required parents/dependencies, blocker if any, verification receipt requirement, invalidation/revisit condition, and physical-guide link when physical.

---

# DAG A — Constitutional / Architecture Kernel
Shape: dependency DAG. Objective: preserve the narrow waist and prevent drift.

```mermaid
graph TD
  A00[Reality primacy / VERIFIED] --> A01[Constitutional invariants / SPECIFIED]
  A01 --> A02[Burden conservation ledger / SPECIFIED]
  A01 --> A03[No-new-noun gate / SPECIFIED]
  A01 --> A04[Regression-by-principle / SPECIFIED]
  A01 --> A05[Pithy projection constitution / SPECIFIED]
  A01 --> A06[Standards-first / SPECIFIED]
  A01 --> A07[Optimization receipts + ratchet / SPECIFIED]
  A02 --> A08[Cross-layer non-evasion / SPECIFIED]
  A04 --> A09[Root-cause batch repair / PLANNED]
  A07 --> A10[Automatic self-pruning / PLANNED]
  A03 --> A11[Architecture drift sentinel / PLANNED]
  A08 --> A12[Whole-system recompilation gate / PLANNED]
  A05 --> A13[Human-interface conformance / IN_PROGRESS]
```

Successor state: architecture changes cannot land without invariant/burden/ownership checks. Verification: governance tests + release receipt.

---

# DAG B — Reality / Evidence / State / Decision Kernel
Shape: causal + derivation DAG. Objective: one universal world-model loop.

```mermaid
graph LR
  B00[Source / Observation] --> B01[Evidence qualification]
  B01 --> B02[Canonical event/fact]
  B02 --> B03[External/Internal World State]
  B03 --> B04[Operative State]
  B03 --> B05[Distribution/Tails]
  B03 --> B06[Relations/Topology]
  B05 --> B07[Pressure/Flow/Slack]
  B06 --> B07
  B07 --> B08[Transitions/Dynamics]
  B08 --> B09[Effects]
  B09 --> B10[Constraints]
  B10 --> B11[Possibility/Reachability]
  B11 --> B12[Telos-relative consequence]
  B12 --> B13[Bearings]
  B13 --> B14[Authority gate]
  B14 --> B15[Minimal execution delta]
  B15 --> B16[Verification]
  B16 --> B17[Successor baseline]
  B17 --> B03
```

Roadmap state:
- B00-B02: IN_PROGRESS — shared acquisition/evidence substrate exists in pieces; reconcile into one owner.
- B03: SPECIFIED — External World State canonicalization and internal-state boundary require source consolidation.
- B04: SPECIFIED.
- B05-B08: SPECIFIED/IN_PROGRESS — sparse tensor/tail/transition operators exist conceptually; complete executable common library.
- B09-B13: SPECIFIED — preserve mission-relative interpretation bridge.
- B14: IN_PROGRESS — authority fabric exists but needs universal conformance.
- B15-B17: IN_PROGRESS — execution/closure persistence exists; unify successor-state verification.

Next verified successor: one end-to-end replay from source observation to verified successor state without domain-specific engine logic.

---

# DAG C — Semantic Shapes / Standards / Data Substrate
Shape: inheritance lattice + derivation DAG.

```mermaid
graph TD
  C00[External standards/IDs/units] --> C01[Canonical primitive shapes]
  C01 --> C02[Semantic mixins]
  C02 --> C03[Domain families]
  C03 --> C04[Specific entities]
  C04 --> C05[Instances]
  C01 --> C06[Canonical record]
  C06 --> C07[CAS / immutable evidence]
  C06 --> C08[Event log]
  C06 --> C09[Columnar analytical store]
  C07 --> C10[Merkle integrity/sync]
  C08 --> C11[Incremental rollups]
  C09 --> C11
  C11 --> C12[Sparse tensor state]
  C12 --> C13[Derived projections]
  C02 --> C14[Convergent-delta promotion]
  C14 --> C02
```

Nodes to finish:
- shared shapes: ENTITY/IDENTITY; STOCK/FLOW/BALANCE; RESOURCE/RESERVE/INVENTORY; PRODUCTION/TRANSFORMATION/LOSS/RECOVERY; CAPACITY/UTILIZATION/BOTTLENECK; SUPPLY/DEMAND/CLEARING/PRESSURE; PRICE/COST/VALUE; NETWORK/FLOW; LOCATION/GEOMETRY; POPULATION/COHORT; ORGANIZATION/AUTHORITY; ASSET/LIABILITY/CLAIM; RISK/HAZARD/EXPOSURE/LOSS; LIFECYCLE/TRANSITION; OBSERVATION/EVIDENCE/CONFIDENCE; DISTRIBUTION/TAIL; CONSTRAINT/PRESSURE/SLACK.
- standards mappings: units, geographic IDs, materials/commodities, financial instruments, building/electrical/plumbing/network interfaces, product identifiers.
- storage: RAW != NORMALIZED != DERIVED; acquire/store once; provenance preserved.

Next verified successor: adding a new commodity/entity requires only its semantic delta + source mappings, with no sibling field duplication.

---

# DAG D — Acquisition / Observation / Reality Intelligence
Shape: event-driven execution DAG.

```mermaid
graph LR
  D00[Master Reality Watch Registry] --> D01[Source capability registry]
  D01 --> D02[Cadence/value admission]
  D02 --> D03[Delta-first collectors]
  D03 --> D04[Canonical parsers]
  D04 --> D05[Dedup/provenance]
  D05 --> D06[Event/fact store]
  D06 --> D07[Tail/divergence sensors]
  D07 --> D08[Latent states]
  D08 --> D09[Cross-domain composition]
  D09 --> D10[Materiality gate]
  D10 --> D11[Pithy projection]
  D07 --> D12[Escalate resolution]
  D12 --> D03
  D10 --> D13[Quiet/decay]
```

Coverage backlog adapters: weather/climate; ecology/ecoregions/watersheds/forestry; housing/land/development; demographics; economy/CoL; elections; government/civic capacity; infrastructure; insurance; health/emergency capacity; mobility/freight; tourism/culture; agriculture/food; energy; water; minerals/commodities; companies/markets; technology/capability ratchets; conservation/stewardship; Great Rebasement; products/procurement/ownership; legal; automotive; household; preparedness.

Next verified successor: three unrelated domains run through identical collectors/events/tails/composition machinery with only adapter deltas.

---

# DAG E — Human Interface / Jarvis / Attention Sovereignty
Shape: progressive-disclosure tree feeding action DAG.

```mermaid
graph TD
  E00[Full internal state] --> E01[Material delta]
  E01 --> E02[Direction]
  E02 --> E03[Consequence]
  E03 --> E04{Can Polaris handle?}
  E04 -->|yes| E05[Execute within authority]
  E04 -->|no| E06[Minimum human action]
  E05 --> E07[Receipt]
  E06 --> E07
  E03 --> E08[Why?]
  E08 --> E09[Components]
  E09 --> E10[Evidence]
  E10 --> E11[Original observation]
```

Program nodes:
- pithy delta-first app/report/voice projection — IN_PROGRESS.
- ontology-remembers-itself alias/natural-language resolver — SPECIFIED.
- <=2 navigation levels by default — SPECIFIED.
- Attention Sovereignty/Tail Delegation — SPECIFIED.
- Task Telos compilation — SPECIFIED.
- Universal Micro-Judgment Fabric — SPECIFIED.
- Task Execution Copilot — PLANNED/partial.
- notification suppression/materiality escalation — IN_PROGRESS.
- voice/audio Jarvis — PLANNED.
- user-controlled expansion/decompression — PLANNED.

Next verified successor: app, Wayfinder and Jarvis return the same minimum delta packet from one state source.

---

# DAG F — Software / Runtime / Basecamp / AMOS
Shape: deployment dependency DAG.

```mermaid
graph TD
  F00[Canonical Polaris runtime] --> F01[Basecamp service core]
  F00 --> F02[Phone app]
  F00 --> F03[Model registry/router]
  F01 --> F04[Data/CAS/NAS]
  F01 --> F05[Identity/authority]
  F01 --> F06[Observability/receipts]
  F03 --> F07[Local model mesh]
  F01 --> F08[AMOS node fabric]
  F08 --> F09[Edge discovery]
  F08 --> F10[LAN delta propagation]
  F10 --> F11[Offline/rejoin reconciliation]
  F02 --> F12[Demo/offline mode]
  F02 --> F13[Thin projection client]
  F04 --> F14[Backup/recovery]
  F14 --> F15[Drive/offsite backup]
  F00 --> F16[Release/migration system]
```

Known debt:
- exact historic alpha.237-248 semantics UNKNOWN.
- exact alpha.252-255 sequence UNKNOWN.
- alpha.259 release proof UNKNOWN.
- Finance->Wayfinder generic routing survival UNKNOWN.
- owned-item recall/news binding UNKNOWN.
- current native Android build proof UNKNOWN.

Next verified successor: clean reproducible Basecamp + Phone install can bootstrap, operate offline locally, reconcile on rejoin, and restore from backup.

---

# DAG G — Security / Privacy / Authority
Shape: authority graph + failure-containment DAG.

```mermaid
graph TD
  G00[Human sovereignty] --> G01[Identity]
  G00 --> G02[Authority graph]
  G02 --> G03[Purpose-bound grants]
  G03 --> G04[Execution authorization]
  G04 --> G05[Receipts/audit]
  G01 --> G06[Passwordless credentials]
  G06 --> G07[Provision/revoke/recover]
  G02 --> G08[Least-authority edge nodes]
  G02 --> G09[Scoped contractor/service access]
  G03 --> G10[TTL/privacy credentials]
  G04 --> G11[Manual/local fallback]
  G08 --> G12[Blast-radius containment]
```

Roadmap nodes: local-first authentication; hard admin path; hardware segregation where justified; privacy browser/credential broker; credential loss/recovery; offline physical access; camera/privacy zoning; authority non-amplification tests; provider-independent fallback.

Next verified successor: loss of cloud/phone/edge node cannot amplify authority or block consequential local recovery.

---

# DAG H — Physical Polaris Deployment
Shape: staged successor-state DAG. Detailed guides live in the Physical Deployment Guide Registry.

```mermaid
graph LR
  H00[Software-only] --> H01[Basecamp physical core]
  H01 --> H02[Network/storage/security backbone]
  H02 --> H03[GH first inhabited node]
  H03 --> H04[Campus backbone]
  H04 --> H05[Utility plant]
  H04 --> H06[Workshop/garage]
  H04 --> H07[Greenhouse/garden/animals]
  H04 --> H08[Landscape/water]
  H04 --> H09[Edge nodes/sensors]
  H03 --> H10[Vehicle/mobile/field]
  H09 --> H11[Robots/automation]
  H04 --> H12[MH successor habitat]
  H12 --> H13[Mature resilient campus]
  H13 --> H14[Self-pruning/refresh]
```

Timing shapes: RESERVE_DURING_DESIGN -> ROUGH_IN -> MOVE_IN_REQUIRED -> EARLY_OPERATION -> LATER -> ON_DEMAND; speculative hardware = NEVER_BY_DEFAULT.

Next verified successor: every physical node has commissioning, safe-state, maintenance, replacement and decommission receipts.

---

# DAG I — Sanctuary / Land / GH / Construction / MH
Shape: causal construction DAG with economic gates.

```mermaid
graph TD
  I00[Desired lived state] --> I01[Parcel search]
  I01 --> I02[Due diligence]
  I02 --> I03[Parcel acquisition]
  I02 --> I04[Reject parcel]
  I03 --> I05[Micro-siting/drainage]
  I05 --> I06[Minimum earthwork]
  I06 --> I07[Cheapest adequate foundation]
  I07 --> I08[Simple structure/enclosure]
  I08 --> I09[Wet/service core + utilities]
  I09 --> I10[Minimum Sufficient Capability]
  I10 --> I11[GH move-in]
  I11 --> I12[Attack CoL/utilities/debt/admin]
  I11 --> I13[Campus rolling waves]
  I13 --> I14[Optional MH successor]
  I14 --> I15[2700 ft2 optimized MH]
```

Construction compiler applied at every node: DELETE PARTS -> DELETE OPERATIONS -> DELETE UNIQUE DETAILS -> SIMPLIFY -> STANDARDIZE -> SHARE -> PASSIVE -> ASSIST NECESSARY WORK.

GH protected state: ~1,000 ft2 baseline/ceiling, test ~925-975 ft2; 2 bed/2 bath; no hallway by default; compact Wet Core; pantry wall; right-sized laundry; productive boundaries; passive logistics; simple shell; standards-first; no miniature-MH cleverness.

MH protected state: one story; ~2,700 ft2; 4 real bedrooms; halls where useful; accessible circulation/baths; library; craft; family capacity; acoustic/privacy separation; high storage; negative space; no forced transformer-house rituals.

Cost gates: whole-system installed cost; P50/P80/P95 separate; deferred != saved; avoided tail risk != invoice saving; liquidity reserve != project cost; no savings double counting.

Current actionable successor: qualify real parcels against GH footprint/covenants, soil/perc, water, access, drainage, build pad, utility path and total P80/P95 MSC burden.

---

# DAG J — Capital / Finance / Economic Intelligence
Shape: state + strategy + authority + execution DAG.

```mermaid
graph TD
  J00[Accounts/holdings/liabilities] --> J01[Financial state]
  J01 --> J02[Capital routing]
  J01 --> J03[Strategy definitions]
  J03 --> J04[Backtest/replay]
  J04 --> J05[Shadow portfolio]
  J05 --> J06[Risk/constraint gate]
  J06 --> J07[Allocation]
  J07 --> J08[Authority]
  J08 --> J09[Execution]
  J09 --> J10[Reconciliation]
  J10 --> J11[Performance/risk attribution]
  J11 --> J12[Promote/demote/retire]
  J01 --> J13[Tax-aware transition]
  J13 --> J07
  J14[Economic feedstock] --> J15[Signals]
  J15 --> J03
```

Nodes: passive obligation routing; emergency/goal/cash semantic separation; debt optimization; contribution-first rebalancing; Core 50; experimental sleeves; disclosure/copy/inverse/model strategies; shadow controls; tax-aware transitions; economic feedstock; personal finance integration; recurring bills/subscriptions; property/GH capital plan.

Next verified successor: all live strategy/action outputs derive from reconciled actual financial state + explicit authority, with shadow/control comparison and tax/transition costs preserved.

---

# DAG K — Wayfinder / Publications / Elections / External Bearings
Shape: acquisition -> composition -> publication DAG.

```mermaid
graph LR
  K00[Reality Watch deltas] --> K01[Qualified evidence]
  K01 --> K02[Wayfinder composition]
  K02 --> K03[Priority/materiality]
  K03 --> K04[Morning/Evening/Extra]
  K03 --> K05[Standing watches]
  K03 --> K06[Immediate alert]
  K04 --> K07[Archive/receipt]
```

Programs: Navigator/Workshop/Garden/Gazette/Quartermaster; election-delta auto inclusion; demographics watch; property/local external bearings; finance folded where relevant; ICE Removal + Gap Mine; pithy delta-only output.

Next verified successor: publications are projections of shared reality state, not separate research/data stores.

---

# DAG L — Products / Ownership / Procurement / Physical Execution
Shape: lifecycle DAG.

```mermaid
graph LR
  L00[Need] --> L01[Requirement]
  L01 --> L02[Existing capability?]
  L02 -->|yes| L03[Reuse/share]
  L02 -->|no| L04[Market/product evidence]
  L04 --> L05[Ownership lifecycle comparison]
  L05 --> L06[Procure]
  L06 --> L07[Receive/identify]
  L07 --> L08[Home/park/source/destination]
  L08 --> L09[Ready]
  L09 --> L10[Deploy/use]
  L10 --> L11[Inspect/maintain]
  L11 --> L12[Reset/restock]
  L12 --> L09
  L11 --> L13[Repair/replace/retire]
```

Programs: product/catalog delta discovery; unit economics; standards->bins->kits->modules->loadouts->stations; PACKOUT as implementation not ontology; automotive/workshop/home/garden/field workflows; time-envelope/friction compiler; recall/ownership watches; subscriptions/services/consumables.

Next verified successor: owned-item state automatically links maintenance, recall, consumables, replacement and deployment guides without duplicate databases.

---

# DAG M — Household / Food / Garden / Life Operations
Shape: material-flow + recurring workflow DAG.

```mermaid
graph LR
  M00[Demand] --> M01[Plan]
  M01 --> M02[Procure/harvest]
  M02 --> M03[Receive/store]
  M03 --> M04[Transform/cook/preserve]
  M04 --> M05[Consume/use]
  M05 --> M06[Waste/reuse/compost]
  M06 --> M07[Reset/restock]
  M07 --> M03
```

Programs: procurement hierarchy/two-source rule; pantry/inventory; recipes; sauces/ferments/dairy/meat/preservation; zero-waste; laundry/cleaning/hygiene; greenhouse/garden/food forest; animals; household transformation fabric; Sanctuary rituals.

Next verified successor: recurring household administration compiles into low-attention loadouts/routines with material balance and replenishment paths.

---

# DAG N — Preparedness / Resilience / Recovery
Shape: consequence x failure x recovery DAG.

```mermaid
graph TD
  N00[Critical capability] --> N01[Failure modes]
  N01 --> N02[Consequence/recovery time]
  N02 --> N03[Passive/manual fallback]
  N02 --> N04[Redundancy if justified]
  N03 --> N05[Exercise/test]
  N04 --> N05
  N05 --> N06[Verified readiness]
  N06 --> N07[Incident]
  N07 --> N08[Degraded operation]
  N08 --> N09[Recover/reconcile]
  N09 --> N06
```

Programs: water, power, thermal, lighting, communications, medical/first aid, fire/weather, vehicle/field bags, 3-day disappearance capability, offline docs/maps, critical spares, recovery drills.

Next verified successor: every consequential fallback is exercised and has a real recovery receipt rather than paper redundancy.

---

# DAG O — Release / Migration / Backfill / Historical Debt
Shape: release qualification DAG.

```mermaid
graph TD
  O00[Canonical model delta] --> O01[Implementation delta]
  O01 --> O02[Tests/conformance]
  O02 --> O03[Migration/backfill]
  O03 --> O04[App/runtime compatibility]
  O04 --> O05[Release candidate]
  O05 --> O06[Verification evidence]
  O06 --> O07[Release]
  O07 --> O08[Observe regressions]
  O08 --> O09[Repair/prune]
  O09 --> O00
```

Explicit historical debt nodes:
- O20 alpha.237-248 exact semantics — UNKNOWN; blocker: missing exact canonical reconstruction.
- O21 alpha.252-255 exact sequence — UNKNOWN.
- O22 alpha.259 source/release proof — UNKNOWN.
- O23 Finance->Wayfinder routing survival — UNKNOWN.
- O24 owned-item recall/news binding — UNKNOWN.
- O25 native Android build proof — UNKNOWN.
- O26 branch/release divergence prevention — IN_PROGRESS; successor: every vNext branch forks/rebases from current accepted base with minimal delta.
- O27 backup continuity to Drive/offsite — IN_PROGRESS.

No version label promotes UNKNOWN implementation to VERIFIED.

---

# DAG P — Roadmap / Mining / Reconciliation Itself
Shape: ingestion/reconciliation DAG.

```mermaid
graph LR
  P00[Conversation/shared chat/source/repo discovery] --> P01[Extract consequential delta]
  P01 --> P02[Resolve canonical owner]
  P02 --> P03{Existing roadmap node?}
  P03 -->|same| P04[Link/dedupe]
  P03 -->|refine| P05[Update]
  P03 -->|conflict| P06[Preserve + discriminate]
  P03 -->|new| P07[Add]
  P03 -->|superseded| P08[Tombstone/link successor]
  P03 -->|unknown| P09[Explicit blocker]
  P04 --> P10[Propagate affected DAGs]
  P05 --> P10
  P06 --> P10
  P07 --> P10
  P08 --> P10
  P09 --> P10
  P10 --> P11[Recompute active frontier]
  P11 --> P12[Pithy roadmap delta]
```

Next verified successor: mining cannot produce a consequential concept that lacks roadmap ownership/state after reconciliation.

---

# Cross-DAG typed edges
Allowed cross-links are explicit, not graph collapse:
- REQUIRES: target cannot advance without source.
- FEEDS: evidence/state signal contributes but does not gate.
- CONSTRAINS: source limits target possibility/authority.
- IMPLEMENTS: runtime/physical mechanism implements model capability.
- PROJECTS: UI/report is a view of canonical state.
- VERIFIES: receipt/evidence qualifies target state.
- SUPERSEDES: replacement relation.
- DEPLOYS_AT: semantic capability -> physical scope.
- FINANCES: capital state enables physical/software work.
- INVALIDATES: changed reality forces recompilation.

Highest-value cross-links:
A -> all DAGs: constitutional invariants constrain every change.
B -> D/E/I/J/K: world state feeds intelligence, human bearings, land/build, capital, publications.
C -> B/D/F/J/L: shared shapes/data substrate prevent domain duplication.
E -> F/K: all human projections obey pithy contract.
F -> D/E/G/H/K: Basecamp/runtime hosts observation, Jarvis, authority, physical nodes, Wayfinder.
G -> F/H/J/L: authority gates software, physical actuation, finance and procurement.
I -> H/J: land/GH/MH deployment requires physical guides and capital.
O -> all implemented DAGs: release qualification verifies actual propagation.
P -> all DAGs: mining/reconciliation updates roadmap state.

---

# Active frontier — next globally useful successor states
1. ROADMAP POPULATION VERIFIED: machine representation matches this portfolio; acyclic within each DAG; cross-links typed.
2. CONSTITUTIONAL ENFORCEMENT VERIFIED: architecture changes run invariant/burden/roadmap gates automatically.
3. UNIVERSAL REALITY LOOP VERIFIED: three different domains traverse the same source->state->bearing path.
4. ONE TRUTH / MANY VIEWS VERIFIED: App, Jarvis and Wayfinder project shared canonical state.
5. REPRODUCIBLE BASECAMP + PHONE VERIFIED: local bootstrap, offline operation, backup/restore, rejoin.
6. LAND/GH DECISION-GRADE: real candidate parcels qualified through covenants, soil/perc, water, access, drainage, pad, utilities and P80/P95 MSC burden.
7. PHYSICAL GUIDE COMPLETENESS: every manifestable capability resolves to guide/N_A/deferred/blocked.
8. HISTORICAL DEBT TRIAGE: exact unknown releases remain explicit and are either reconstructed, superseded with receipts, or retired.
9. SELF-PRUNING VERIFIED: replacements automatically identify redundant doctrine/code/roadmap nodes.

## Final law
THE ROADMAP IS A SET OF SHAPED, TYPED, INTEROPERABLE DAGs. EACH DAG PRESERVES ITS OWN CAUSAL SEMANTICS. CROSS-DAG RELATIONS LINK THEM WITHOUT CREATING A MEGA-GRAPH. NOTHING CONSEQUENTIAL MAY REMAIN ONLY IN CONVERSATION.