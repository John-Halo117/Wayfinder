# Universal Rule Polarization Canon v2.1

Status: canonical correction for Model `0.1.0-alpha.27`. Supersedes v1 and v2 for qualification semantics.

## Governing law

Every active normative Polaris rule must have a paired negative specification before that rule can be considered fully qualified.

`RULE -> OWNER/SOURCE -> SCOPE/APPLICABILITY -> INTENDED STATE/PARENT -> APPLICABLE POLARS -> DETECTION -> RESPONSE -> RECOVERY/REROUTE -> RETEST`

The negative specification is an immune layer around the positive rule, not a second truth store and not a naive logical negation.

## Coverage is evidence, not assertion

Universal applicability of the law does not imply completed migration of the corpus.

Pair completeness is measured against an independent canonical-source census, not against a hand-maintained tuple that generates both the expected rules and the polars.

Each canonical surface is one of:

- `HARVESTED` — active normative rules have stable IDs/source anchors and are paired;
- `REVIEWED_NO_RULES` — reviewed and found not to contain active normative rules;
- `QUALIFICATION_DEBT` — not yet fully harvested/reviewed, with owner/reason/review condition visible.

Release status is `FULLY_QUALIFIED` only when source debt is zero and every harvested active rule is paired. Otherwise it is `MIGRATION_QUALIFIED`.

Unknown coverage never counts as complete coverage.

## Fixed-point / idempotence law

Polarization must terminate.

Generated polar fields — anti-pattern text, detection, response, recovery, retest, rendered explanations, generated tests, and generated contract projections — are **derived metadata of the source `rule_id`**. They are not independently harvested as new normative rules merely because they contain words such as MUST, should, block, reroute, recover, or retest.

Therefore:

`SOURCE RULE R -> POLAR PAIR P(R) -> derived projections/tests`

and never:

`P(R) -> new rule R2 -> P(R2) -> new rule R3 -> ...`

A generated artifact may create a new rule candidate only when a human or qualified compiler adds genuinely new normative semantics that are not derivable from the source rule/polar contract. Such a candidate must receive its own stable identity and canonical owner before entering the active corpus.

The harvester must distinguish:

- authoritative positive-rule sources;
- manually authored domain extension sources;
- generated/derived polarization artifacts.

Derived polarization artifacts are excluded from recursive harvesting and instead map back to their source `rule_id`.

Resource bound: one active source rule produces at most one universal `PolarizedRule` pair plus finite references to domain extensions. Domain extensions enrich that pair; they do not recursively spawn new pairs.

This fixed-point rule is itself polarized: over-exclusion that hides genuinely new authored normative semantics is a coverage failure and must be surfaced as qualification debt.

## Smallest applicable polar set

“Every rule gets an immune system” does not mean every failure family applies to every rule.

Every rule receives the universal minimum:

- direct violation;
- over-application;
- under-application;
- scope leakage;
- displaced burden/local optimization;
- reality-veto failure;
- excessive-compliance counter-polar.

Additional families are derived only when semantics make them relevant:

- authority -> authority leakage / authority paralysis;
- privacy -> privacy leakage / over-withholding;
- epistemic -> epistemic promotion / unknown-as-neutral / false precision;
- metric -> metric substitution / Goodhart / denominator-population loss where applicable;
- spatial/temporal -> scale leakage;
- operational -> happy-path-only / recovery gap / single-point failure;
- lifecycle -> stale state / orphan / failure to retire;
- interface -> custom-when-standard-exists / proprietary lock-in;
- attention -> attention externality / automation creep;
- mechanism/implementation -> mechanism promotion / dependency capture.

`N/A` is valid only after applicability is resolved. `UNKNOWN` is not `N/A`.

This prevents polarization from violating itself through blanket over-application.

## Rule schema

A durable normative rule carries at minimum:

- stable `rule_id`;
- canonical owner and source anchor;
- positive rule text;
- intended state;
- scope and applicability boundary;
- normative strength;
- abstraction layer: OBJECTIVE / REQUIREMENT / FUNCTION / MECHANISM / IMPLEMENTATION / METRIC / POLICY;
- parent rule/objective where a lower layer depends on one;
- protected constraints;
- semantic traits that determine applicable polar families;
- lifecycle/successor relation where relevant.

A polarized pair carries:

- source `rule_id`;
- applicable failure families;
- direct anti-pattern;
- counter-polar;
- discriminating detection condition;
- response/disposition;
- recovery, rollback, or reroute path where meaningful;
- retest/verification condition;
- marker that the pair is derived from, not authoritative over, the source rule.

## Abstraction preservation

`OBJECTIVE != REQUIREMENT != FUNCTION != MECHANISM != IMPLEMENTATION`

Failure of a mechanism or implementation normally reroutes to the smallest valid parent rather than killing the parent objective.

A lower-layer rule without a resolvable parent is qualification debt unless explicitly shown to be independent.

## Strength preservation

- HARD / REQUIRED: direct violation may block promotion/execution while applicable.
- PREFERRED / DEFAULT: violation triggers comparison/requalification, not automatic prohibition.
- OPTIONAL: mainly guards accidental promotion, inheritance, or lifecycle burden.

The polar may never silently strengthen the positive rule.

## Protected constraints are executable semantics

Protected constraints are not decorative metadata. Detection and disposition must preserve them. A local optimization that violates a binding protected constraint cannot be rescued by unrelated benefit.

## Source anchoring and drift

A local mirror of a canonical rule retains an independent source anchor. Source drift triggers requalification; the mirror cannot silently become authority.

Stable rule identity must not be derived solely from mutable wording, owner, location, or ordinal position. Legacy sources without stable IDs require an explicit compatibility map until upgraded.

## Domain inverse canons

Sanctuary, Reality Intelligence, security, finance, execution, and future domain anti-pattern canons are finite specialized extensions of universal pairs.

They may add domain-specific failure families, detectors, responses, recovery paths, and tests. They may not replace the universal pair, create a competing rule identity, exempt a source from coverage, or recursively generate additional rule identities from their own generated output.

## Qualification audit

The audit independently detects at least:

1. canonical source not reviewed/harvested;
2. harvested rule without polar;
3. polar without source-backed rule;
4. source drift against compatibility map;
5. duplicate rule identity;
6. lower-layer rule with missing parent;
7. preference/default accidentally made blocking;
8. blanket failure-family assignment beyond applicability;
9. protected constraints present but ignored;
10. domain inverse extension disconnected from universal pair;
11. retired/superseded rule whose polar remains active;
12. claimed full qualification while debt remains;
13. generated polar artifact recursively harvested as a new rule;
14. genuinely new normative semantics incorrectly hidden as generated metadata.

## Current migration rule

The initial universal-polarization release remains migration-qualified until the canonical source census reports zero unresolved qualification debt. Existing paired rules remain valid; the release must not overstate coverage while backfill proceeds.

## Human interface

The user normally sees the practical question:

- What would violating this look like?
- What goes wrong if we follow it too aggressively?
- Did the burden move somewhere else?
- Is this rule still applicable here?
- Did a mechanism fail, or did the objective actually become invalid?

Technical polar names remain optional drill-down handles.

## Stop condition

Polarization is complete only when:

`SOURCE_CENSUS_COVERED && HARVESTED_RULES == POLARIZED_RULES && QUALIFICATION_DEBT == 0 && GENERATED_POLAR_REHARVEST == 0`

No tautological self-counting or recursive generated-contract expansion is accepted as evidence of completeness.

> **EVERY RULE GETS AN IMMUNE SYSTEM; THE IMMUNE SYSTEM IS ALSO SUBJECT TO ITS OWN RULES, AND THE COMPILER MUST REACH A FIXED POINT.**
