# Habitat Assumption Scope v1

Status: canonical habitat-scope contract for Model `0.1.0-alpha.22`.

## Purpose

Prevent one building profile's optimization from silently becoming a universal Sanctuary requirement.

Every habitat/building assumption, recommendation, test, and projection MUST carry one of these scopes:

- `SHARED` — applies across GH and MH unless a narrower profile overrides it.
- `GH` — Guest House / compact first-stage house only.
- `MH` — Main House / long-term primary house only.
- `CAMPUS` — outbuildings, workshop, garage, greenhouse, landscape, animal, utility, storage, or other campus capability not inherently part of GH/MH.
- `UNKNOWN_SCOPE` — historical material whose intended scope is not yet resolved; it MUST NOT be inherited by GH or MH by default.
- `N_A` — explicitly not applicable.

## Shared protected constraints

The following are `SHARED` unless Reality or explicit user intent changes them:

- one human-occupied story;
- no design may depend on a second occupied story;
- accessibility and long-term physical independence;
- serviceability and non-destructive routine maintenance where practical;
- standards-first physical interfaces and mechanisms;
- mechanism-neutral requirements;
- no unnecessary technological dependence or lock-in;
- mechanical assistance where it reduces force/holding/positioning burden at acceptable lifecycle cost;
- restorative/sleep/privacy/acoustic requirements are protected;
- useful negative space and maneuverability may be intentional capability;
- future-ready interfaces do not imply maximum future capacity installed now;
- capability/authority/evidence semantics remain separate from physical implementation.

## Obsolete assumptions — reject globally

The following legacy assumptions are invalid unless explicitly reintroduced as a new requirement:

- second-story human circulation as a default or design dependency;
- stair-dependent architecture;
- inter-floor human/cargo/laundry/grocery transfer as a required capability;
- person/cargo lifts whose purpose is serving an upper occupied story;
- upper occupied floors as storage/service assumptions;
- minimum square footage as the objective;
- maximum utilization or maximum function count as the objective;
- every surface/volume must be populated with a function;
- more capability requires more visible objects;
- every capability should be mechanized, powered, smart, or automated;
- every room should transform;
- reserve/contingency/equity/savings collapsed into project cost;
- `Lean/Defensive/Expanded` used simultaneously as scope and cost-confidence labels;
- custom Polaris physical standards where adequate external standards/interfaces exist.

Vertical volume within a single occupied story remains allowed when structure, code, accessibility, serviceability, and protected human clearances permit it.

## GH profile

Role: compact complete first-stage home; approximately 1,000 ft² is a planning baseline, not a hard semantic requirement.

Default tendencies:

- aggressively minimize circulation-only area;
- **avoid conventional hallways** unless code, accessibility, privacy, acoustics, geometry, or another protected requirement justifies one;
- direct room-to-room or useful transition-space connections are preferred when they remain legible and private enough;
- tightly cluster wet/service functions;
- prefer reach-in, full-height, built-in, wall-depth, pull-out, or other compact storage before walk-ins;
- share intermittent capability where conversion is easy and low-friction;
- use deployable/mobile capability more aggressively than MH when it materially reduces permanent encumbrance;
- keep shell geometry simple, utility runs short, corners/penetrations low, and dimensions/openings standardized when adequate;
- minimize duplicate rooms/equipment unless resilience, convenience, or concurrent demand justifies them;
- preserve negative/restorative space despite footprint pressure;
- do not use tiny-house gymnastics, repeated daily furniture Tetris, inaccessible storage, or strength-intensive conversion;
- do not import eventual MH functions merely because MH may later contain them;
- after MH exists, GH should retain useful independent capability rather than become stranded infrastructure.

Human-facing summary: **GH spends space reluctantly.**

## MH profile

Role: long-term primary home; approximately 2,700 ft² is a planning baseline, not a hard semantic requirement.

Default tendencies:

- **hallways are allowed and may be desirable** when they improve privacy, acoustic separation, intuitive navigation, accessibility, service/egress behavior, visual pacing, or public/private zoning;
- reject pointless circulation, not circulation itself;
- allow dedicated rooms where they reduce recurring friction or support privacy/acoustics/concurrency;
- use fewer transformations for high-frequency activities than GH;
- permit more permanent furniture and larger storage when it improves ordinary life;
- walk-in storage is allowed when its internal circulation/access actually earns its area;
- allow deliberate transition spaces and more generous clearances;
- allow selective redundancy where convenience or resilience earns lifecycle burden;
- wet/service infrastructure should remain coherent and serviceable but need not be compressed at the expense of a good long-term layout;
- architectural experience, views, procession, delight, spaciousness, and negative space may justify area;
- capability density is desirable but is not maximized at the expense of calm or spaciousness;
- MH must not inherit GH compression tricks merely because they save floor area.

Human-facing summary: **MH spends space intentionally.**

## Campus profile

Capabilities whose location is not inherently residential interior space SHOULD be evaluated for CAMPUS placement before forcing them into GH or MH. Examples include workshop/fabrication, bulk storage, greenhouse production, animal systems, garden processing, utility plant, seasonal equipment, material handling, and other noisy/dirty/space-intensive functions.

This is not an automatic externalization rule; accessibility, weather, workflow, security, frequency, and connection burden still decide placement.

## Assumption inheritance

Resolution order:

`explicit current requirement -> building-specific profile -> SHARED -> UNKNOWN_SCOPE`

`UNKNOWN_SCOPE` is a quarantine state, not a weak universal default.

A profile-specific rule MUST NOT propagate horizontally into another profile without explicit evidence that the requirement is shared.

Examples:

- `GH:no_conventional_hallways` does not imply `MH:no_conventional_hallways`.
- `MH:hallways_allowed` does not force a hallway into GH.
- `CAMPUS:workshop` does not prohibit a small indoor repair capability.

## Assumption quality gate

For every inherited conventional-house feature or old Polaris design claim, ask:

1. What requirement does it satisfy?
2. Which building/profile owns that requirement?
3. Is it hard, preferred, optional, or obsolete?
4. Is the proposed mechanism merely conventional habit?
5. Does a smaller/safer/lower-burden alternative satisfy the same requirement?
6. Does removing it create hidden human labor, privacy, acoustic, accessibility, service, code, or lifecycle cost?

Conventional presence is not evidence of requirement. Likewise, novelty is not evidence of improvement.

## Compatibility

This contract scopes Physical Habitat/Build Bible/Sanctuary projections; it creates no new truth owner. Historical material remains evidence/provenance but must resolve through the scope contract before becoming current design state.
