# Architecture Homeostasis

Wayfinder architecture should remain capable of change without drifting into
unbounded coupling, permanent scaffolding, or repeated rediscovery of solved
structure.

## Architectural Pressure

Architectural Pressure is the derived force indicating whether an artifact,
concept, service, or responsibility should:

- settle inward toward a stable canonical core;
- float outward into a replaceable implementation;
- separate behind a Membrane;
- compose with an existing capability; or
- remain provisional while evidence is insufficient.

Pressure may come from repeated reuse, duplicated semantics, recurring exceptions,
latency, security, authority, continuity, maintenance burden, coupling, or a newly
mature upstream capability.

## Architectural Viscosity

Architectural Viscosity is resistance to safe structural movement caused by
coupling, exceptions, shared mutable state, hidden authority, unclear ownership,
provider leakage, and broad blast radius.

High viscosity is a signal to improve boundaries and legibility before attempting
a large migration. It is not a reason to freeze an unhealthy architecture forever.

## Architecture Composting

When machinery becomes obsolete, harvest its useful residue before deletion:

- invariants;
- tests;
- evidence;
- contracts;
- failure cases;
- operational lessons;
- useful interfaces; and
- negative knowledge about what did not work.

Then remove the obsolete runtime machinery rather than preserving it as permanent
archaeology.

Architecture Composting complements the Bespoke-Code Deletion Rule: deletion should
remove displaced code while retaining durable knowledge that prevents relearning
the same lesson.

## Architecture Homeostasis

Homeostasis is feedback-driven maintenance of healthy architectural operating
bands. The system should detect drift, degrade gracefully, and recover toward
canonical boundaries rather than depending on periodic heroic refactors.

Examples include:

- duplicated concepts drifting toward one canonical home;
- provider-specific assumptions leaking into core policy;
- interfaces accumulating responsibilities they should not own;
- temporary exceptions becoming permanent pathways;
- observability degrading until failure becomes opaque; and
- custom code remaining after upstream capability fully displaces it.

## Architecture Ratchet

Once a hard architectural debt or unsafe dependency is removed, the accepted
baseline should not silently regress.

A regression requires an explicit, scoped exception with rationale, owner,
consequence, review condition, and removal path. "Temporary" without an exit path
is not an exception; it is new architecture debt.

## WET Under Uncertainty

Do not prematurely unify two implementations or concepts when evidence is
insufficient to prove that they share one durable abstraction. Preserve separate
paths until the common invariant is demonstrated.

This is the stopping boundary for aggressive DRY/compression. Compression continues
until another merger would erase a distinction that changes behavior.

## AHA Transition

When evidence becomes strong enough that formerly separate paths are now proven to
share one invariant, perform an explicit transition:

observe duplication -> identify invariant -> prove compatibility -> migrate ->
verify -> compost old machinery -> ratchet the new boundary.

## Healthy Architecture Region

Architecture itself follows the same anti-asymptote rule as other Bearings.

Too little structure creates ambiguity and repeated work. Too much structure
creates bureaucracy and rigidity. Too little abstraction creates duplication. Too
much abstraction erases meaningful distinctions. Too little optionality traps the
system; too much optionality prevents commitment.

Seek the smallest architecture that preserves reality, required capability,
continuity, authority boundaries, serviceability, and maneuverability.
