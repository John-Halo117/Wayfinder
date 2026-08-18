# Universal Rule Polarization Canon v2

Status: canonical correction for Model `0.1.0-alpha.27`. Supersedes v1 for qualification semantics.

## Governing law

Every active normative Polaris rule must have a paired negative specification before that rule can be considered fully qualified.

`RULE -> OWNER/SOURCE -> SCOPE/APPLICABILITY -> INTENDED STATE/PARENT -> APPLICABLE POLARS -> DETECTION -> RESPONSE -> RECOVERY/REROUTE -> RETEST`

The negative specification is not a second doctrine and not a naive negation. It is an immune layer around the positive rule.

## Critical correction: coverage is evidence, not assertion

A release may not claim universal polarization merely because a hand-maintained list of sample rules pairs with itself.

Pair-completeness must be measured against an **independent source census** of canonical normative surfaces.

For each canonical source:

- `HARVESTED` — its active normative rules are represented by stable rule IDs and source anchors.
- `REVIEWED_NO_RULES` — reviewed and found not to contain active normative rules.
- `QUALIFICATION_DEBT` — not yet fully harvested/reviewed; owner, reason, and review condition remain visible.

Release-level polarization status is therefore:

`FULLY_QUALIFIED` only when every in-scope source is HARVESTED or REVIEWED_NO_RULES and every harvested rule is paired.

Otherwise the release is `MIGRATION_QUALIFIED` and must expose the remaining debt. Unknown coverage is never treated as complete coverage.

## Smallest applicable polar set

“Every rule gets an immune system” does **not** mean every anti-pattern family applies to every rule.

Every rule receives the universal minimum:

- direct violation
- over-application
- under-application
- scope leakage
- displaced burden/local optimization
- reality-veto failure
- excessive-compliance counter-polar

Additional families are derived only when the rule’s semantics make them relevant, for example:

- authority rules -> authority leakage / authority paralysis
- privacy rules -> privacy leakage / over-withholding
- epistemic rules -> epistemic promotion / unknown-as-neutral / false precision
- metric rules -> metric substitution / Goodhart / denominator or population loss as applicable
- spatial or temporal rules -> scale leakage
- operational rules -> happy-path-only / recovery gap / single-point failure
- lifecycle rules -> stale state / orphan / failure to retire
- interface rules -> custom-when-standard-exists / proprietary lock-in
- attention rules -> attention externality / automation creep
- mechanism or implementation rules -> mechanism promotion / dependency capture

`N/A` is valid only when applicability is actually resolved. `UNKNOWN` is not `N/A`.

This prevents the polarization law from violating itself through blanket over-application.

## Rule schema

A durable normative rule carries, at minimum:

- stable `rule_id`
- canonical owner and source anchor
- positive rule text
- intended state
- scope and applicability boundary
- normative strength
- abstraction layer: OBJECTIVE / REQUIREMENT / FUNCTION / MECHANISM / IMPLEMENTATION / METRIC / POLICY
- parent rule/objective where a lower layer depends on one
- protected constraints
- semantic traits that determine applicable polar families
- lifecycle/successor relation where relevant

A polarized pair carries:

- applicable failure families
- direct anti-pattern
- counter-polar
- discriminating detection condition
- response/disposition
- recovery, rollback, or reroute path where meaningful
- retest/verification condition

## Abstraction preservation

`OBJECTIVE != REQUIREMENT != FUNCTION != MECHANISM != IMPLEMENTATION`

Failure of a mechanism or implementation must normally reroute to the smallest valid parent rather than killing the parent objective.

A lower-layer rule without a resolvable parent is qualification debt unless it is explicitly demonstrated to be independent.

## Strength preservation

- HARD / REQUIRED: direct violation may block promotion/execution while the rule is applicable.
- PREFERRED / DEFAULT: violation triggers comparison/requalification, not automatic prohibition.
- OPTIONAL: mainly guards accidental promotion, inheritance, or lifecycle burden.

The polar may never silently strengthen the positive rule.

## Protected constraints are executable semantics

Protected constraints are not decorative metadata. Polar review must preserve them in detection and disposition. A local optimization that violates a protected constraint cannot be rescued by unrelated benefit.

## Source anchoring and drift

A local mirror of a canonical rule must retain an independent source anchor. The source is checked for drift; the mirror cannot silently become the authority.

Stable rule identity must not be derived solely from mutable wording, owner, location, or ordinal position. Legacy sources without stable IDs require an explicit compatibility map until their canonical records are upgraded.

## Domain inverse canons

Sanctuary, Reality Intelligence, security, finance, execution, and future domain anti-pattern canons are specialized extensions of universal polarization.

They may add domain-specific failure families, detectors, responses, recovery paths, and tests. They may not replace the universal pair, create a competing rule identity, or exempt a rule from source coverage.

## Qualification audit

The audit must independently detect at least:

1. active normative source not reviewed/harvested;
2. harvested rule without polar;
3. polar without source-backed rule;
4. source drift against a registered compatibility map;
5. duplicate rule identity;
6. lower-layer rule with missing parent;
7. preference/default accidentally made blocking;
8. blanket failure-family assignment beyond applicability;
9. protected constraints present but ignored;
10. domain inverse rule disconnected from its universal pair;
11. retired/superseded rule whose polar remains active;
12. claimed full qualification while debt remains.

## Current migration rule

The initial universal-polarization release is migration-qualified until the canonical source census reports zero unresolved qualification debt. Existing paired rules remain valid; the release must not overstate coverage while backfill proceeds.

## Human interface

The user normally sees the practical question, not the ontology:

- What would violating this look like?
- What goes wrong if we follow it too aggressively?
- Did the burden move somewhere else?
- Is this rule still applicable here?
- Did a mechanism fail, or did the objective actually become invalid?

## Stop condition

Polarization is complete only when:

`SOURCE_CENSUS_COVERED && HARVESTED_RULES == POLARIZED_RULES && QUALIFICATION_DEBT == 0`

No tautological self-counting is accepted as evidence of completeness.

> **EVERY RULE GETS AN IMMUNE SYSTEM; THE IMMUNE SYSTEM IS ALSO SUBJECT TO ITS OWN RULES.**
