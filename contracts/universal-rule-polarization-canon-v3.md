# Universal Rule Polarization Canon v3

Status: **sole active Universal Rule Polarization contract** for Model `0.1.0-alpha.27`.

This document supersedes v1, v2, and v2.1 **in full** for applicability, qualification, harvesting, schema, fixed-point behavior, composition, and release-status semantics. Earlier versions remain historical evidence only.

## Law

Every active normative Polaris rule must have a paired negative specification before that rule can be fully qualified.

`RULE -> SOURCE/OWNER -> SCOPE/APPLICABILITY -> PARENT/INTENDED STATE -> APPLICABLE POLARS -> DETECTION -> RESPONSE -> RECOVERY/REROUTE -> RETEST`

Polarization is not negation and is not a second doctrine. It is an immune layer around the authoritative positive rule.

## Qualification is conjunctive

A release is `FULLY_QUALIFIED` only when **all** of these are true:

1. authoritative source census is complete for the release boundary;
2. every harvested active rule has exactly one universal pair;
3. every pair has authoritative source provenance;
4. all required parent/successor references resolve without cycles;
5. rule strength is preserved;
6. failure families are applicability-qualified rather than blanket-applied;
7. protected constraints participate in detection/disposition;
8. specialized domain extensions are bound to existing universal pairs;
9. generated polarization artifacts are not recursively harvested;
10. qualification debt is zero;
11. **blocking conformance audit findings are zero**.

Anything less is `MIGRATION_QUALIFIED`, `PARTIAL`, or `BLOCKED` as appropriate. Pair-count equality alone can never establish full qualification.

## Authoritative source census

The source universe comes from owner-qualified canonical registries, not a reading list, filename guess, or the polarization implementation itself. Polaris' Specification Registry is an authoritative starting registry for system specifications; additional canonical owners may register sources not represented there.

Each source is recorded as:

`HARVESTED | REVIEWED_NO_RULES | QUALIFICATION_DEBT`

with stable source identity, owner, path/scope, reason, and review condition. Unknown coverage is debt, not absence.

The current migration ledger is `universal-rule-polarization-source-census-v1.json` and remains evidence of incomplete migration until every debt row is resolved.

## Source-backed rule identity

A registered rule requires:

- stable `rule_id`;
- canonical owner;
- `source_id` / `source_path`;
- stable source anchor or compatibility anchor;
- positive text;
- strength;
- scope/applicability;
- abstraction layer;
- intended state / parent objective;
- protected constraints where applicable;
- semantic traits used to select polar families.

Source-less rules may be used as ephemeral local probes, but they cannot enter the qualified corpus or count toward release completeness.

Legacy sources lacking typed rule IDs require an explicit compatibility map validated against source drift.

## Parent graph

`OBJECTIVE != REQUIREMENT != FUNCTION != MECHANISM != IMPLEMENTATION`

For registered lower-layer rules:

- parent must exist;
- parent cannot be self;
- parent graph must be acyclic;
- mechanism/implementation failure reroutes to the smallest valid parent unless a binding protected constraint invalidates the parent objective itself.

Unresolved parentage is qualification debt or a blocking audit finding.

## Smallest applicable polar set

Every rule gets the universal minimum:

- direct violation;
- over-application;
- under-application;
- scope leakage;
- displaced burden/local optimization;
- reality-veto failure;
- excessive-compliance counter-polar.

Additional families appear only when semantic traits justify them: authority, privacy, epistemic, metric, spatial, temporal, population, operational, lifecycle, interface, attention, distributed/dependency, reversibility, or other registered domain traits.

`UNKNOWN != N/A`. Blanket assignment of inapplicable families is itself an over-application violation.

## Strength preservation

- HARD / REQUIRED: applicable direct violation may block.
- PREFERRED / DEFAULT: violation triggers comparison/requalification, not prohibition.
- OPTIONAL: guards accidental promotion, inheritance, and lifecycle burden.

A polar may never silently strengthen its rule.

## Protected constraints

Protected constraints are executable semantics. Detection and disposition must carry them. Unrelated benefits cannot average away a binding protected-constraint failure.

## Domain extensions

Specialized inverse canons enrich universal pairs. A domain extension must have a typed binding contract that resolves its implementation/module and enumerates the universal `rule_id`s it extends. Missing modules, stale bindings, or bindings to unknown rules fail conformance.

Domain extensions do not create competing rule identities.

## Fixed point

Generated polar text, detection, response, recovery, retest, generated explanations, generated tests, and generated projections map back to their source `rule_id`; they are derived artifacts and are excluded from recursive normative harvesting.

A genuinely new human-authored normative statement embedded in a generated surface is **not** hidden by this exclusion: it becomes a new candidate rule and must receive a stable owner/source/identity.

One source rule yields at most one universal pair plus finite domain-extension references. Recursive `rule -> polar -> new rule -> polar...` expansion is forbidden.

## Audit classes

Blocking conformance audit includes at least:

- source missing or source drift;
- rule without pair / pair without rule;
- unresolved source census debt when full qualification is claimed;
- duplicate rule identity;
- invalid/cyclic parent or successor graph;
- strength escalation;
- inapplicable blanket polar family;
- ignored protected constraint;
- unbound/missing domain extension;
- stale active polar for retired/superseded rule;
- recursive generated-artifact harvest;
- false qualification claim.

Audits preserve independent findings; there is no universal anti-pattern score.

## Human projection

Normally surface practical questions:

- What would violating this look like?
- What happens if we follow it too aggressively?
- Did the burden move elsewhere?
- Is it still applicable here?
- Did a mechanism fail, or did the parent objective become invalid?

Technical polar names remain optional.

## Stop condition

`FULLY_QUALIFIED := SOURCE_CENSUS_COMPLETE && PAIRS_COMPLETE && PROVENANCE_COMPLETE && GRAPH_VALID && APPLICABILITY_VALID && EXTENSIONS_BOUND && FIXED_POINT && QUALIFICATION_DEBT==0 && BLOCKING_AUDIT_FINDINGS==0`

> **Every rule gets an immune system; the immune system obeys the same reality, scope, burden, provenance, lifecycle, and stop-condition laws.**
