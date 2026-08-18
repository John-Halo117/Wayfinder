# Standard Reference Contract

## Purpose

The Standard Reference contract identifies an external consensus standard, code, mature de facto interface, or established commercial/industrial interface selected to satisfy a requirement.

Polaris does not create a competing physical interface merely to obtain internal naming consistency.

The resolution order is:

`REQUIREMENT -> applicable mandatory code/standard -> adequate consensus standard -> mature interoperable interface -> standardized-component adaptation -> composed standards -> custom residual`

A custom residual is admissible only when the preceding options do not preserve the requirement.

## Standard Reference

A Standard Reference carries, where material:

- issuing body or ecosystem owner;
- standard/interface identifier and title;
- edition, revision, profile, class, size, or other compatibility discriminator;
- jurisdiction and applicability conditions;
- requirement(s) satisfied;
- evidence/provenance used to select it;
- compatibility and transition/adaptation relations;
- known deviations;
- lifecycle status and supersession/review trigger.

A friendly Polaris alias is a projection only. It does not replace the external identifier.

## Standards-First Interface Resolution

For physical interfaces and subsystems, consumers MUST search for and evaluate existing standards/interfaces before proposing a custom interface.

A custom physical interface requires a Residual Justification containing:

1. the unresolved requirement;
2. standards/interfaces evaluated;
3. why each adequate-looking candidate failed;
4. the minimum novel delta;
5. how the delta transitions back to standardized components where possible;
6. test/verification obligations;
7. a deletion or migration trigger if an adequate external standard later becomes available.

Absence of a locally known standard is not proof that no standard exists.

## Composition

Different standards may legitimately govern different sides of one boundary. Composition does not merge their authorities. For example, structural load, electrical connection, accessibility geometry, labeling, and data transport may each retain separate governing references.

Adapters SHOULD preserve the standard interface on each side rather than inventing a third ecosystem.

## Anti-Reinvention Rules

- requirement != implementation;
- internal alias != physical standard;
- standard selection != evidence of compliance;
- commercial maturity != formal consensus status;
- custom residual != permission to replace adequate standard components;
- version/revision/profile distinctions MUST remain explicit when compatibility depends on them.

## Ownership

Wayfinder owns the semantics of Standard References and Residual Justifications. Domain owners determine applicability. Evidence owners preserve source/provenance. Execution and implementation repositories realize selected standards without redefining them.
