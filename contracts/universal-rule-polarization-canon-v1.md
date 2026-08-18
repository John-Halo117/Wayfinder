# Universal Rule Polarization Canon v1

Status: canonical for Model `0.1.0-alpha.27`.

## Law

Every normative Polaris rule MUST have an explicit negative specification. No rule is exempt because it is constitutional, safety-oriented, architectural, semantic, physical, computational, economic, operational, UX, privacy, evidence, lifecycle, or merely a default.

`RULE -> SCOPE -> INTENDED STATE -> POLAR/ANTI-PATTERN -> FAILURE MODES -> DETECTION -> RESPONSE -> RECOVERY -> RETEST`

A rule without its polar is incomplete canon and MUST NOT be promoted as fully qualified.

## What “polarize” means

Polarization is **not** naive logical negation. It generates the smallest negative specification capable of detecting when the positive rule fails, is over-applied, is gamed, leaks scope, creates displaced burden, or becomes obsolete.

For every rule R, derive at least:

1. **Direct violation** — the named requirement is not satisfied.
2. **Over-application** — R is applied outside its valid scope or beyond diminishing returns.
3. **Mechanism capture** — one implementation is mistaken for R itself.
4. **Metric capture / Goodhart failure** — a proxy/metric improves while the intended state worsens.
5. **Local-optimization failure** — R succeeds locally by moving larger burden elsewhere.
6. **Boundary leakage** — scope, authority, privacy, temporal, spatial, population, lifecycle, or abstraction boundaries are crossed without qualification.
7. **Failure/recovery gap** — R works only in the happy path or cannot return to a valid state.
8. **Epistemic failure** — unknown, inference, estimate, prediction, assumption, preference, or contested state is promoted to stronger evidence type.
9. **Lifecycle failure** — R is valid at creation but becomes stale, unserviceable, irrecoverable, or impossible to retire.
10. **Inverse Goodhart** — fear of violating R causes excessive conservatism that defeats the parent objective.

Only applicable polar modes need concrete mechanics; `N/A` is valid when justified. `UNKNOWN` is not `N/A`.

## Rule pair schema

Every durable normative rule should resolve to a `PolarizedRule` record with:

- stable `rule_id`
- canonical owner/source
- normative strength: HARD / REQUIRED / PREFERRED / DEFAULT / OPTIONAL
- scope and applicability predicate
- intended state / parent objective
- positive rule text
- protected constraints
- anti-pattern / polar statement
- applicable failure modes
- discriminating detection evidence
- response/disposition
- recovery or rollback path where meaningful
- verification/retest condition
- successor/deprecation relation

The polar record is metadata/contract, not a second copy of the underlying doctrine.

## Strength semantics

**HARD / REQUIRED** rules: polar violation blocks promotion or execution unless a higher-order canonical rule explicitly defines an exception.

**PREFERRED / DEFAULT** rules: polar violation triggers comparison/requalification; deviation may be valid when evidence shows a better route to the parent objective.

**OPTIONAL** rules: the polar mainly prevents mechanism promotion, lifecycle burden, and accidental inheritance.

A negative specification MUST NOT silently strengthen a preference into a hard prohibition.

## Parent-child law

Polarization preserves abstraction:

`OBJECTIVE != REQUIREMENT != FUNCTION != MECHANISM != IMPLEMENTATION`

The anti-pattern for a mechanism cannot veto an objective merely because that implementation failed. Back up to the smallest valid parent and reroute.

## Pair completeness invariant

For the active canon:

`NORMATIVE_RULE_COUNT == POLARIZED_RULE_COUNT + JUSTIFIED_EXEMPTION_COUNT`

The target justified exemption count is zero. Temporary exemptions require owner, reason, expiry/review condition, and must remain visible as qualification debt.

New normative rules cannot enter qualified canon without a polar. Existing unpaired rules are migration debt and must be backfilled.

## Coverage sources

The rule harvester must inspect all canonical normative surfaces, including constitution, natural laws, reality/evidence, ontology, governance, authority, decision, execution, resilience, privacy/security, lifecycle, resource stewardship, attention/human interface, physical/Build Bible, standards mappings, model/system/app contracts, and future canonical owners.

Filename or subsystem names are not authoritative coverage boundaries. Normative statements may exist in prose, schemas, registries, code assertions, tests, ADRs, or generated contracts.

## Polar composition

Do not create one mega anti-pattern score. Preserve independent failures.

A child polar may:

- block a parent when it violates a protected/binding constraint;
- trigger requalification when it exposes a tradeoff;
- cause rerouting when only a mechanism failed;
- remain local when consequence is local.

Multiple polars may coexist. Benefits do not cancel harms by averaging.

## Symmetry requirement

Positive and negative specifications are co-maintained:

- change R -> re-evaluate its polar;
- change scope -> re-evaluate boundary failures;
- change mechanism -> do not rewrite the requirement unless Reality changed;
- retire R -> retire or redirect its polar;
- supersede R -> polar follows the successor relation;
- new evidence contradicts either side -> update both from Reality.

## Canonical universal anti-pattern families

These families apply across domains when relevant:

- `DIRECT_VIOLATION`
- `OVER_APPLICATION`
- `UNDER_APPLICATION`
- `SCOPE_LEAKAGE`
- `AUTHORITY_LEAKAGE`
- `PRIVACY_LEAKAGE`
- `ABSTRACTION_COLLAPSE`
- `MECHANISM_PROMOTION`
- `METRIC_SUBSTITUTION`
- `GOODHART_CAPTURE`
- `LOCAL_OPTIMIZATION`
- `DISPLACED_BURDEN`
- `COMPLEXITY_RATCHET`
- `NOVELTY_RATCHET`
- `DEPENDENCY_CAPTURE`
- `SINGLE_POINT_FAILURE`
- `HAPPY_PATH_ONLY`
- `RECOVERY_GAP`
- `IRREVERSIBILITY_BLINDNESS`
- `STALE_STATE`
- `LIFECYCLE_ORPHAN`
- `EPISTEMIC_PROMOTION`
- `UNKNOWN_AS_NEUTRAL`
- `CORRELATION_AS_CAUSATION`
- `DENOMINATOR_LOSS`
- `SPATIAL_SCALE_LEAKAGE`
- `TEMPORAL_SCALE_LEAKAGE`
- `POPULATION_BOUNDARY_LEAKAGE`
- `AGGREGATION_ERASURE`
- `ATTENTION_EXTERNALITY`
- `MAINTENANCE_EXTERNALITY`
- `OPTION_VALUE_DESTRUCTION`
- `FALSE_PRECISION`
- `OVER_VERIFICATION`
- `UNDER_VERIFICATION`
- `AUTOMATION_CREEP`
- `CUSTOM_WHEN_STANDARD_EXISTS`
- `PROPRIETARY_LOCK_IN`
- `FAILURE_TO_DECAY_OR_RETIRE`
- `ARCHITECTURE_FOR_THE_DIAGRAM`
- `REALITY_VETO_FAILURE`

Domain-specific anti-patterns extend these rather than replacing them.

## Examples of polarization

Positive: `Reality > models.`
Polar: **Model Preservation** — observations are bent, discarded, or reinterpreted merely to keep the model consistent. Detection: contradictory qualified evidence. Response: reopen representation/assumptions before defending the model.

Positive: `Evidence > claims.`
Polar: **Claim Promotion** — repetition, authority, confidence, or fluency substitutes for evidence. Counter-polar: **Evidence Maximalism** — endless verification is demanded after further evidence cannot change action.

Positive: `Use existing standards before inventing.`
Polar: **Not-Invented-Here Interface** — custom physical/software semantics appear despite adequate mature standards. Counter-polar: **Standard Worship** — an inadequate standard is forced onto a requirement it cannot satisfy.

Positive: `Human attention is scarce.`
Polar: **Attention Externality** — machine optimization shifts review/decision burden onto the human. Counter-polar: **Over-Automation** — attention preservation removes the human from consequential preference/authority decisions.

Positive: `No change -> no downstream work.`
Polar: **Busy Recompute** — unchanged inputs trigger work. Counter-polar: **No-Change Dogma** — integrity, expiry, or scheduled revalidation obligations are skipped merely because source bytes did not change.

Positive: `Prefer reversible action under uncertainty.`
Polar: **Premature Commitment** — irreversible action occurs before required evidence/authority. Counter-polar: **Reversibility Fetish** — the system refuses necessary commitment after delay costs exceed information/option value.

Positive: `Capability != authority.`
Polar: **Reachability-as-Permission** — because a system can perform an action, it treats itself as authorized. Counter-polar: **Authority Paralysis** — valid standing/delegated authority is ignored and routine execution needlessly returns to the human.

Positive: `Closure persists through recoverable failure.`
Polar: **Incidental Failure = Objective Death** — timeout/provider/tool friction silently terminates a still-valid objective. Counter-polar: **Zombie Persistence** — retries continue after objective invalidation, protected-boundary failure, or terminal impossibility.

## Universal compiler

For each normative rule:

`PARSE NORMATIVE CLAIM`
`-> RESOLVE OWNER + STRENGTH + SCOPE`
`-> RESOLVE PARENT OBJECTIVE / PROTECTED CONSTRAINTS`
`-> DERIVE DIRECT VIOLATION`
`-> TEST OVER/UNDER APPLICATION`
`-> TEST MECHANISM/METRIC CAPTURE`
`-> TEST BOUNDARY LEAKAGE`
`-> TEST DISPLACED BURDEN / LOCAL OPTIMUM`
`-> TEST FAILURE / RECOVERY / LIFECYCLE`
`-> TEST EPISTEMIC FAILURE`
`-> TEST COUNTER-POLAR / EXCESSIVE COMPLIANCE`
`-> ATTACH DETECTION + RESPONSE + RETEST`
`-> REGISTER PAIR`
`-> PROPAGATE TO DESCENDANTS / TESTS / UI ONLY WHERE MATERIAL`

## Human interface

The human does not need to memorize anti-pattern names. Polaris should normally surface the practical question or consequence:

- “What could go wrong if we follow this too aggressively?”
- “What would violating this look like?”
- “Did the burden move somewhere else?”
- “Is this still the right rule here?”

Technical polar names remain optional drill-down handles.

## Stop condition

Polarization is complete for a release only when every active normative rule is paired or explicitly marked temporary qualification debt. Do not hand-write thousands of duplicate essays when a rule can inherit a universal failure family plus a small domain-specific delta.

The invariant is:

> **EVERY RULE GETS AN IMMUNE SYSTEM, INCLUDING THE RULES THAT CREATE IMMUNE SYSTEMS.**
