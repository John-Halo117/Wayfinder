# Spatial Scope and Jurisdiction

**Canonical semantic owner:** Wayfinder  
**Version:** `0.1.0-alpha.19`

## Purpose

Spatial scope is a universal coordinate for External World State, evidence, classification, Bearings, decisions, and projections. It is not weather-specific and it is not one rigid containment hierarchy.

## Physical Spatial Scales

Typical physical scales include:

`point -> site -> zone -> parcel -> adjacency -> locality -> corridor/watershed -> region -> macroregion -> continental -> global`

These names are semantic handles, not mandatory geometry nesting. A watershed, airshed, road corridor, labor market, ecological region, and cultural region may overlap the same parcel without containing one another.

## Administrative Scope

Administrative or jurisdictional relations are modeled separately from physical region:

`parcel -> municipality -> county -> state -> federal`

Additional jurisdictions may include utility districts, school districts, fire districts, zoning overlays, HOAs, conservation areas, tribal jurisdictions, service territories, or other governed boundaries.

`administrative scope != physical region`

## Functional Regions

Functional regions are derived classifications or fields, for example:

- commute shed;
- labor / housing market;
- healthcare catchment;
- retail / service area;
- utility service territory;
- emergency-response area;
- media market;
- agricultural region;
- cultural region;
- development-pressure field.

They are projections over evidence/EWS and may change without changing entity identity.

## Typed Spatial Relations

Use registered typed relations rather than implied nesting:

- `contains`
- `within`
- `overlaps`
- `intersects`
- `adjacent_to`
- `upstream_of`
- `downstream_of`
- `within_airshed`
- `within_travel_shed`
- `served_by`
- `influences`

Implementations may extend the relation vocabulary only through normal ontology governance.

## Canonical Spatial Coordinate

A consequential state or observation may carry:

`Space = (entity, geometry/ref, scale, spatial relations, jurisdiction, functional scopes)`

Only populate dimensions that materially affect interpretation or action.

## Propagation

Cross-scale effects remain causal rather than merely hierarchical. Examples:

`road closure -> corridor access -> parcel reachability`

`state law -> jurisdiction -> local implementation -> parcel constraint`

`regional drought -> watershed/aquifer -> well yield -> household capability`

## Invariants

1. Location, region, jurisdiction, and classification are distinct.
2. A named region is not entity identity.
3. Multiple spatial and functional scopes may be simultaneously true.
4. Spatial scope carries with quantitative claims when material.
5. Physical containment must not be inferred from administrative or cultural labels.
6. Derived functional regions preserve provenance, valid time, uncertainty, and recomputation conditions.
