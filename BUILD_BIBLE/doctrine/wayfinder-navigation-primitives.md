# Wayfinder Navigation Primitives

Wayfinder is a navigation system, not an optimization system. It exists to help
humans continue, navigate, and improve reality without losing future options.

This doctrine restores the durable navigation concepts that predate current
implementation choices. These concepts are Wayfinder-owned. Applications,
platforms, agents, models, protocols, and harvested capabilities may supply
observations, execution, state, or interfaces, but they do not replace this
navigation grammar.

## Canonical Architecture Chain

Reality -> CivPhys / Mechanics -> Constitutional Principles -> Root Objectives ->
Capability Grammar -> Bearings -> Functions -> Systems -> Actions.

Reality is the source layer. State is inferred from evidence; it is not treated as
more authoritative than reality itself.

## Root Objectives

Wayfinder evaluates architecture and action against four root objectives:

- Capability — What can we do?
- Continuity — What survives and can be resumed?
- Attention — What still requires the human?
- Maneuverability — What useful future paths remain available?

Maneuverability is the long-horizon governor. Capability, continuity, and attention
improvements that destroy future options must be treated with suspicion.

## Theseus Principle

Preserve the invariant. Replace the rest.

Capabilities, continuity, objectives, and required behavior may remain stable while
components, products, providers, implementations, protocols, and substrates evolve.
A replacement is successful when the invariant survives the replacement rather
than when the old implementation survives unchanged.

This principle constrains Capability Harvest: upstream capability may displace an
implementation, but not the invariant that made the capability worth preserving.

## Capability Lifecycle

Every durable capability should be legible through the same lifecycle:

Acquire -> Observe -> Preserve -> Upgrade -> Transfer.

- Acquire — Can the capability be gained?
- Observe — Can its state and effects be established?
- Preserve — Can it survive ordinary disruption and time?
- Upgrade — Can it improve without unnecessary replacement?
- Transfer — Can it survive substrate, provider, ownership, or implementation
  change?

Capabilities are distinct from the substrates hosting them.

## Bearings Principle

Bearings provide orientation. They are not objectives.

Metrics, scores, and indicators exist to help navigation relative to reality. They
must not silently become optimization targets merely because they are measurable.

### Healthy-Region / Asymptote Principle

Every useful Bearing can have pathological low and pathological high states.
Navigation seeks the healthy operating region, not the asymptote.

Examples:

- Attention independence: too low means constant interruption; too high can become
  automation blindness or disengagement.
- Ambient Certainty: too low means recurring disorientation; too high can become
  obsessive sensing or surveillance.
- Capability: too low means inability; too high can become capability accumulation
  without deployment.
- Continuity: too low means fragility; too high can become preservation hoarding
  that prevents evolution.
- Maneuverability: too low means being trapped; too high can become endless
  optionality without commitment.

Prefer attractor regions and stopping rules over arbitrary maxima. Additional
precision, testing, resilience, personalization, knowledge, or optimization should
stop when another increment no longer materially changes the decision or when its
marginal cost exceeds its navigational value.

## Canonical Bearing Families

These are navigation families, not mandatory dashboard widgets. They may be
computed when useful and omitted when not.

### Capability Bearings

- Capability Index — current useful capability state.
- Effective Capability Yield — useful capability produced per unit resource.
- Upgrade Potential — reachable improvement capacity.
- Transferability — ability to survive replacement or substrate change.

### Continuity Bearings

- Capsule Density — recoverable capability per retrieval effort.
- Continuity Recovery Velocity — speed at which useful operation can be restored.
- Context Restoration Capability — ability to resume a task, mission, or system
  state without reconstructing everything from scratch.
- Labor Freedom Index — capability maintained per unit required labor.

### Attention Bearings

- Ambient Certainty — useful certainty available without active checking.
- Bearings Availability — attention remaining after orientation costs.
- Bearing Velocity — speed of becoming sufficiently oriented to act.
- Attention Independence — freedom from unnecessary recurring attention burdens.

### Maneuverability Bearings

- Runway — time before a forced decision.
- Optionality — useful future paths still available.
- Affordance Expansion — newly reachable actions or capabilities.
- Financial Freedom — ability to act without excessive financial constraint.

### Resource-Recovery Bearings

- Resource Recovery Efficiency — discarded or idle flow converted to capability.
- Capability Recapture Rate — potential loss converted back into useful capability.

### Upgrade Bearings

- Upgrade Readiness — ability to absorb an improvement cleanly.
- Capability Evolution Rate — rate of useful capability growth without destructive
  churn.

## Ambient Certainty

Ambient Certainty is the capability of removing recurring uncertainty from human
attention without requiring active checking.

Automation is not the goal. Reduced recurring uncertainty is the goal.

Examples include knowing that a washer finished, a freezer remains healthy, mail
arrived, a tank reached a threshold, or a backup completed successfully without the
human repeatedly checking each condition.

Ambient Certainty should be judged by the uncertainty loop it closes, not by the
number of notifications or automations it creates.

## Bearings Economy

Every unresolved uncertainty can impose a Bearing Maintenance Cost.

Bearing Maintenance Cost may include:

- checking cost;
- switching/context cost;
- interpreting cost;
- remembering cost;
- deciding cost; and
- rechecking cost.

Jarvis should reduce orientation cost as aggressively as it reduces direct task
cost. Saving five minutes can be less valuable than eliminating hundreds of tiny
attention loops that repeatedly consume working memory.

Ambient Certainty is the production side of this economy; Bearings Economy is the
cost side.

## Expected Uncertainty Reduction

Expected Uncertainty Reduction (EUR) is the expected amount of consequential
uncertainty removed by an intervention relative to its cost, time, attention, risk,
and reversibility.

Use EUR to compare interventions such as:

- sensors;
- inspections;
- research tasks;
- automations;
- purchases;
- experiments;
- due diligence;
- upgrades; and
- refactors.

The practical question is:

Which action removes the most consequential uncertainty per unit cost, time,
attention, and risk?

EUR is a navigation primitive, not a command to measure everything. If further
measurement would not materially alter a decision, the expected value of more
certainty may be near zero.

## Black State

Unknown is a valid state.

When evidence is insufficient to establish a responsible Bearing, Wayfinder must
preserve the unknown rather than fabricate certainty. Black State is not failure;
it is an explicit recognition that navigation cannot yet be resolved.

Black State should usually trigger one of three responses:

- accept the unknown because it does not affect a consequential decision;
- reduce uncertainty when the expected value justifies it; or
- preserve options until the state can be resolved.

## Parallel Observation Architecture

Humans observe serially. Jarvis can observe in parallel.

Many independent observation streams may therefore feed a single finite Bearings
stream. The purpose of parallel observation is not to produce more human-facing
information. It is to make the human need to observe less.

The system should continuously compress many observations into the smallest set of
material Bearings, transitions, uncertainties, opportunities, and actions.

## Context Restoration

Continuity includes the ability to resume.

Context Restoration is the capability to reconstruct enough relevant state,
relationships, evidence, commitments, open loops, and working context that a human
or system can continue without rereading or rediscovering the entire history.

Restoration should preserve evidence ancestry. Summaries may compress context but
must not erase the source chain needed to recover or challenge the summary.

Capsules are continuity projections, not a second world model. They preserve what
is needed to continue capability across interruptions, handoffs, failures, or long
time gaps.

## Affordance Projection

Wayfinder should ask not only what exists or what changed, but what became possible.

Affordance Projection identifies newly reachable actions created by a change in
reality or capability.

Examples:

Solar installed -> battery optimization becomes possible.
Greenhouse built -> winter growing becomes possible.
New interoperable protocol -> bespoke integration may no longer be necessary.

Serendipity is treated as affordance discovery: the system notices useful actions
that became possible even when the human did not explicitly request them.

## Opportunity Discovery Layer

Opportunity discovery asks:

- What is missing?
- What capability is absent?
- What observation should exist?
- What became possible?
- What bottleneck can now be removed?

Opportunity is not entitlement to attention.

### Opportunity Filter

An opportunity should normally be surfaced only when it is:

- aligned;
- actionable;
- affordable or realistically reachable; and
- relevant to an established objective, constraint, commitment, or path.

Opportunity != distraction.

Long-horizon reviews may periodically ask, "What became possible?" to reassess
technology, property, capabilities, standards, and adjacent infrastructure without
turning every novelty into a project.

## Goal and Pattern to Capability

Automation should be downstream of capability rather than treated as the primitive.

Preferred chains are:

Goal -> Capability -> Automation

and

Observed Pattern -> Capability Gap -> Automation.

A repeated human action is not automatically a reason to automate it. First ask
what capability or certainty gap causes the repetition. Then choose the least
bespoke adequate intervention.

Repeated maintenance may also be compressed into bounded stewardship rituals when
that reduces fragmentation better than another automation.

## Navigation Flywheel

The desired reinforcing loop is:

Uncertainty Reduced
-> Attention Recovered
-> Better Bearings
-> Better Decisions
-> Better Reality
-> More Capability
-> More Opportunities
-> More Uncertainty Reduced.

The extended navigation chain is:

Reality
-> Preserved Reality
-> Continuity
-> Bearings
-> Attention
-> Capability
-> Affordance
-> Opportunity
-> Action
-> Improved Reality.

This is why attention sovereignty and capability growth are coupled rather than
separate concerns.

## Jarvis Functions

Jarvis is the human-facing navigation layer. Its durable functions include:

- Bearings — What happened, what changed, and what matters now?
- Opportunity Detection — What became possible?
- Risk Detection — What threatens continuity or a path?
- Affordance Projection — What actions are newly available?
- Context Restoration — How do we continue from here?
- Resource Recovery — What existing flows can become capability?
- Upgrade Discovery — What bottleneck or capability should improve next?
- Ambient Certainty Generation — What recurring uncertainty can be permanently
  removed from attention?

Systems implement these functions. No single application is the function itself.

## Jarvis Operating Modes

Jarvis may use explicit human-facing modes without splitting its identity:

- Ambient — quiet monitoring and finite surfacing of meaningful change.
- Conversation — ordinary interactive dialogue.
- Whiteboard — exploratory synthesis, alternatives, and design work.
- Mission — focused pursuit of a defined objective with tighter scope and active
  follow-through.
- Debug — diagnosis, traces, contradictions, failures, and system state.
- Socratic — deliberate questioning used to expose assumptions and improve a
  decision or model.

Modes alter interaction posture and working emphasis, not constitutional authority.
They should share the same underlying identity, policy, memory boundaries,
Bearings, and working-context references.

## Capability Injection Test

Technology is evaluated as capability injection, not as novelty.

Ask what it changes in:

- Observation;
- Interpretation;
- Reasoning;
- Navigation;
- Continuity;
- Maneuverability;
- Experience Density; and
- Legibility.

A new technology that improves none of those is unlikely to deserve architectural
weight merely because it is impressive.

## Canonical Compression

ARK preserves reality. Capsules preserve capability. Jarvis preserves bearings.
Wayfinder converts uncertainty into actionable capability while minimizing the
attention required to navigate reality.
