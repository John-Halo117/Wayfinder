# Semantic Shape Standards v1

Status: canonical for Model `0.1.0-alpha.29`.

## Purpose
Compress shared meaning before compressing bytes. Repeated semantics are defined once at the nearest valid shared shape and inherited by children; children store only consequential deltas.

## Resolution law
EXTERNAL STANDARD / CANONICAL IDENTIFIER / UNIT
-> CANONICAL POLARIS SHAPE
-> COMPOSITION OF SHAPES
-> CHILD REFINEMENT
-> NEW PRIMITIVE ONLY FOR UNRESOLVED DELTA

A new named thing does not imply a new schema.

## Core standard shapes
The initial reusable vocabulary includes:

- ENTITY_IDENTITY
- LOCATION_GEOMETRY_REACH
- TIME_EVENT_TRANSITION
- OBSERVATION_EVIDENCE_CONFIDENCE
- STOCK_FLOW_BALANCE
- RESOURCE_RESERVE_INVENTORY
- PRODUCTION_TRANSFORMATION_LOSS_RECOVERY
- CAPACITY_UTILIZATION_BOTTLENECK
- SUPPLY_DEMAND_CLEARING_PRESSURE
- PRICE_COST_VALUE_FINANCING
- NETWORK_NODE_EDGE_FLOW
- POPULATION_COHORT_ENTRY_EXIT
- ORGANIZATION_OWNERSHIP_AUTHORITY
- ASSET_LIABILITY_CLAIM_CASHFLOW
- FACILITY_EQUIPMENT_INPUT_OUTPUT
- ECOLOGICAL_STOCK_FLOW_HABITAT_PRESSURE_RECOVERY
- INFRASTRUCTURE_CAPACITY_CONDITION_FAILURE_RECOVERY
- RISK_HAZARD_EXPOSURE_VULNERABILITY_LOSS
- LIFECYCLE_STATE_TRANSITION
- DISTRIBUTION_TAIL_DIVERGENCE
- CONSTRAINT_PRESSURE_SLACK

These are composable semantic shapes, not mandatory single-parent classes.

## Child delta contract
A specialization may contain only:

- ADD — child-only semantics.
- REFINE/OVERRIDE — legitimate narrowing or different mechanism/unit/range.
- N/A — inherited semantic proven inapplicable.
- CONSTRAINT — additional child invariant.
- MAPPING — external standard/source vocabulary mapping.

Unchanged semantics inherit. Copying a parent field into every child is a conformance failure unless an implementation materialization is explicitly generated from the parent and cannot drift.

## Example — copper and silver

THING
-> PHYSICAL_RESOURCE
-> EXTRACTIVE_MATERIAL
-> COMMODITY
-> METAL
-> NON_FERROUS_METAL
-> COPPER | SILVER

Common semantics live above the siblings: resource/reserve estimates, grade, extraction, recovery, processing/refining, production, inventories, transport, scrap/recycling, substitution, energy intensity, geographic concentration, production economics, market price/liquidity, ownership and end-use demand.

COPPER deltas may include electrical conductivity/application structure, grid/construction demand exposure, concentrate/smelter/treatment-charge mechanics, etc.

SILVER deltas may include precious/monetary demand, photovoltaic exposure, by-product production structure, specific refining/recovery mechanics, etc.

The child delta must not be promoted upward until it is proven common to the appropriate siblings.

## Multiple-shape composition
One entity may instantiate several compatible shapes simultaneously. Example: a physical copper inventory position can be MATERIAL + COMMODITY + INVENTORY + LOCATION + MARKET + OWNERSHIP. Shared semantics are referenced, not copied.

## Convergent-delta promotion
When at least two independent children repeatedly implement materially equivalent semantics:
1. identify the nearest valid common ancestor/shape;
2. test other siblings for false inheritance;
3. confirm units/denominators/mechanisms are genuinely compatible;
4. promote the common semantic upward;
5. replace child copies with inheritance references;
6. rerun polar/failure tests.

## Standards-first mapping
Before creating custom names or units, search for adequate existing standards, identifiers, taxonomies, ontologies and unit systems. Polaris normally supplies mapping/composition/lifecycle management, not a competing physical/economic/scientific vocabulary.

## Compression metric
Useful semantic compression may be measured as:

unique consequential semantics represented / unique semantic definitions maintained

Higher is better only while consequential distinctions remain recoverable. Do not optimize this metric into abstraction theater.

## Polars / anti-patterns
- flat sibling duplication;
- name-only standardization without shared ownership;
- premature abstraction;
- false inheritance;
- parent contamination by child-specific semantics;
- child shadow copies that drift;
- taxonomy worship when multiple-shape composition is truer;
- ambiguous inherited semantics / diamond conflict;
- unit or denominator drift;
- alias explosion without canonical mapping;
- external-standard rejection without demonstrated mismatch;
- universal-schema overreach;
- abstraction for compression that destroys causal/mechanistic meaning;
- promotion based on one child or correlated copies rather than independent convergence;
- generated materialization promoted into source truth.

Polar law: factor aggressively until further factoring would erase a consequential distinction; then stop, split, or refine.
