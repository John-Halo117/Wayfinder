# Environmental External-World Projection

**Semantic owner:** Wayfinder  
**Version:** `0.1.0-alpha.19`  
**Parent contract:** External World State

## Purpose

This contract generalizes the former Weather Fabric / External Local Twin work into a domain projection of External World State. It does not create a separate world-state owner.

The same model supports candidate-site historical replay, current observation, forecast/scenario comparison, and post-acquisition operational sensing.

## Primitive External Domains

Where relevant, environmental EWS may represent:

- atmosphere, weather, climate, and air;
- light, solar exposure, and night sky;
- water and hydrology;
- soil;
- terrain;
- geology;
- ecology;
- fire and other hazards;
- acoustics/noise;
- access and mobility;
- utilities, power, and telecom;
- surrounding human/development/externality state.

Derived views compile from these domains rather than duplicating their truth.

## Spatial and Temporal Scope

Spatial scope uses the universal spatial ontology and may range from point/site/parcel through corridor, watershed, locality, region, macroregion, and larger relevant scopes.

Temporal scope may include historical replay, current state, observed trend, forecast, scenario, and long-horizon climate/development context.

Observed trend and forecast trajectory remain distinct.

## Meaningful Bands

A physical variable may define domain/use-specific threshold bands when crossing a boundary changes comfort, capability, failure mode, infrastructure need, or action.

Examples include temperature, dew point, precipitation, gusts, particulate matter, well yield, water-table depth, infiltration, soil properties, slope, bedrock depth, radon, direct sun, noise events, travel delay, outage duration/frequency, latency/signal, traffic, canopy/invasives, fuel distance, or response time.

Bands preserve raw units and provenance beneath derived grades.

## Shared Temporal / Field Operators

The following operators are domain-general and may be applied where their semantics fit:

- magnitude;
- frequency;
- duration;
- persistence;
- timing;
- recovery;
- variability;
- observed trend;
- tails / extremes;
- compound or joint state.

They are not weather-owned primitives.

## Evaluation

When several orthogonal evaluated dimensions matter, environmental Bearings SHOULD use the SBDTT contract. Polarity is objective-relative; the same physical event may be beneficial for one capability, neutral for another, and harmful for another.

Constraint-aware composition is required. A binding harmful dimension cannot disappear through averaging with unrelated healthy dimensions.

## Continuity Across Acquisition

Historical candidate-site replay and post-acquisition sensing are two operating modes over the same External World State semantics. Acquisition does not create a second environmental model.
