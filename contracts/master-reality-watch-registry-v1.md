# Master Reality Watch Registry v1

Status: canonical observation/composition contract for `0.1.0-alpha.24`.

## Purpose

Anything worth watching is registered here rather than spawning another observation subsystem.

The registry defines **what reality can tell us**. The composition graph defines **what qualified observations jointly mean**. Bearings/Decision determine **what matters now** relative to an objective.

The registry is not a dashboard, world-state store, source catalog, or universal scoring system.

## Canonical observation entry

A watch is the smallest useful registered observation relation:

`WATCH -> OBSERVABLE -> SOURCE -> SPACE -> TIME -> MECHANISM -> INFERRED_STATE -> CONFIDENCE -> DELTA -> CONSEQUENCE`

Required semantic separations:

- source != observable variable
- observable != proxy inference
- proxy != inferred state
- inferred state != consequence
- consequence != action
- evidence != derived state
- one source may feed many watches
- one state may be estimated by many independent sources/mechanisms

Raw evidence/provenance remains owned by the evidence layer; External World State owns qualified derived external state. The registry is a discovery/routing index over these owners.

## Master watch domains

The registry may classify watches under one or more domains without creating domain truth stores:

1. Land & Ecology
2. Climate & Physical Environment
3. Housing & Real Estate
4. Development & Land Use
5. Population & Demography
6. Economy & Cost of Living
7. Physical Commerce
8. Infrastructure
9. Government & Civic Capacity
10. Agriculture & Food Systems
11. Health & Emergency Capacity
12. Insurance & Physical Risk Pricing
13. Mobility & Accessibility
14. Public Safety & Disorder
15. Tourism & Transient Pressure
16. Culture & Community
17. Technology & Capability Ratchets
18. Conservation & National Stewardship
19. Great Rebasement
20. Sanctuary / Property External Twin

Domains are organizational tags/projections. A watch may inform several domains or bypass domain presentation entirely.

## Proxy & Exhaust Watch

Indirect signals are first-class when their mechanism is explicit and evidence is reasonably obtainable.

Examples include storage prices, dumpster permits, school-bus routes, well permits, sewer contracts, public equipment procurement/auctions, insurance filings, repeated price cuts, mosquito treatment, road-salt consumption, utility connections, freight/parking/footfall exhaust, and other newly discovered signals.

There is no fixed proxy list. New signals are appended when they provide discriminating evidence of consequential reality.

Every proxy MUST state:

- directly observed quantity/event;
- hypothesized mechanism connecting it to a latent state;
- spatial and temporal validity;
- alternative mechanisms/confounders when material;
- confidence/evidence state;
- affected state dimensions;
- conditions under which the proxy should be ignored or recalibrated.

## Composition pipeline

`RAW OBSERVATIONS`
`-> QUALIFIED SIGNALS`
`-> PROXIES`
`-> DIMENSION STATES`
`-> DOMAIN STATES`
`-> CROSS-DOMAIN COMPOUND STATES`
`-> OBJECTIVE / CAPABILITY EFFECTS`
`-> OPERATIVE STATE / ACTION`

Each stage is optional. Direct evidence may inform a state without a proxy stage, and an observation need not be promoted beyond the lowest level that changes understanding/action.

## Composition laws

1. **No averaging-away** — materially independent realities remain separate. Positive and negative consequences may coexist.
2. **Constraint composition** — one binding constraint may dominate feasibility without becoming a universal score.
3. **Convergence composition** — independent mechanisms supporting the same latent state increase confidence; duplicated/correlated sources do not count as independent confirmation.
4. **Contradiction composition** — disagreement stays visible and triggers discrimination/probing rather than averaging to false neutrality.
5. **Causal composition** — justified upstream/downstream relationships form typed DAGs; bags of correlation are not promoted to causal chains.
6. **Spatial composition** — propagation follows justified point/parcel/tract/corridor/watershed/jurisdiction/region relationships, never arbitrary radius alone.
7. **Temporal composition** — distinguish event, persistence, trend, acceleration/deceleration, regime transition, forecast trajectory, and scenario.
8. **Objective-relative composition** — the same state may have different consequences for affordability, conservation, privacy, employment, resilience, accessibility, etc.
9. **Sparse composition** — ordinary known state collapses; surface material opportunity, binding constraint, transition, contradiction, uncertainty, cause, or action threshold.
10. **Reversible composition** — every composed state exposes its supporting observations/mechanisms, spatial/temporal scope, confidence, and contradictions.
11. **Denominator preservation** — rates, shares, counts, stocks, flows, and cumulative totals keep their population/quantity semantics through composition.
12. **Source independence accounting** — evidence count is not mechanism count. Shared upstream data/provider lineage must not masquerade as independent convergence.

## Development-front example

Subdivision filings + sewer expansion + parcelization + school-capacity investment may jointly support a derived `development_front` state only when spatial/temporal relationships and mechanisms justify the composition.

A useful derived front may expose:

- geometry/isoshape;
- direction;
- velocity/acceleration;
- reach/horizon;
- initiating/supporting observations;
- independent mechanism count;
- contradiction set;
- objective-relative effects.

The derived state remains inspectable; it is not a magic score.

## Hot-state policy

The registry may become enormous. Human output MUST NOT.

Default presentation is delta-first and sparse. Local and national scopes may be preferred human-facing hot scopes where relevant, while intermediate scales are pulled in when they explain causality, propagation, jurisdiction, or action.

A watch stays quiet when it is known, ordinary, non-material, and not changing. It becomes hot when it materially changes a decision, capability, protected constraint, risk/opportunity state, uncertainty, or causal interpretation.

## Admission rule

When a newly encountered signal appears useful:

1. identify the observable;
2. identify available source(s);
3. specify spatial/temporal semantics;
4. state the mechanism if it is a proxy;
5. connect it to existing state dimensions;
6. identify alternatives/confounders where material;
7. define confidence and delta semantics;
8. register it;
9. allow the composition graph to update affected projections.

Do not create a standalone subsystem unless the candidate requires genuinely different state/authority/evidence/execution mechanics that cannot be expressed through existing owners.

## Privacy / safety boundary

Place-level and aggregate public-reality watches must not become private-person tracking. Public-safety/disorder, health, mobility, commerce, demographic, or similar signals are aggregated/scoped to the consequential place/system state rather than used to build dossiers on private individuals.

## Human interface

The human should normally see a statement such as:

`Development pressure is accelerating east of the parcel; sewer extension and subdivision filings are the strongest independent signals.`

Internal watch names, source identifiers, tensors, and composition nodes are progressive disclosure.

Canonical summary:

**MASTER WATCH REGISTRY = what reality can tell us**

**COMPOSITION GRAPH = what those observations jointly mean**

**POLARIS = what matters now**
