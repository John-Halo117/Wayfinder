# Polaris Reality Intelligence — Fused Canon v1

Status: canonical semantic/engineering contract for `0.1.0-alpha.25`.

## Objective

Maintain broad, long-lived awareness of consequential reality on ordinary hardware while maximizing:

`useful information × confidence × reuse / storage × compute × bandwidth × maintenance × latency × attention`

The Master Reality Watch Registry may be enormous. The active working set MUST remain tiny.

## Core architecture

1. **Master Reality Watch Registry** — one extensible observation registry for all consequential reality watches; a new dataset/domain does not create a new subsystem by itself.
2. **Weird OSINT / behavioral exhaust** — indirect observations are first-class only when the observable, mechanism, confounders, space/time validity, confidence, and affected latent state are explicit.
3. **Tail sensors** — suitable watched quantities may expose level, delta, velocity, acceleration, distributions/tails, threshold crossings, transitions, duration, recurrence, spatial clustering/propagation, subpopulation divergence, cross-signal divergence/convergence/reversal, and expected-event absence. Use quantiles only when they preserve consequential structure; mechanistic thresholds dominate when better.
4. **Composition** — `RAW EVIDENCE -> OBSERVATION/EVENT -> QUALIFIED SIGNAL -> PROXY/TAIL SENSOR -> LATENT STATE -> DIMENSION STATE -> DOMAIN STATE -> CROSS-DOMAIN COMPOUND STATE -> OBJECTIVE/CAPABILITY EFFECT -> OPERATIVE STATE -> ACTION`. Composition is constraint-aware, reversible, sparse, causal/spatiotemporal where justified, and never simple averaging.
5. **Observe once, resolve many** — `SOURCE -> OBSERVATION -> CANONICAL EVENT/FACT -> RELATIONS -> MANY DERIVATIONS`. Acquire once, canonicalize once, store once, relate once, reuse everywhere, compose late.
6. **Primitive shape vocabulary** — scalar/tuple, event, event log, time series, state machine, set/bitmap, rollup tree, graph, DAG, sparse tensor, spatial field, sketch, stream/queue, CAS, Merkle tree/DAG, CRDT, cache. Domains compile into these shapes rather than inventing bespoke machinery.
7. **Multiple DAGs, not one mega-graph** — keep Evidence, Derivation, Causal, Execution/Invalidation, and Capability/Question DAGs distinct but interoperable.
8. **Rollups and pyramidal resolution** — spatial, temporal, and distribution resolution follow the question; aggregation semantics travel with the variable. Never average averages by convenience.
9. **Progressive attention** — operational tiers: `BACKGROUND -> WATCH -> FOCUS`; cadence: `QUIET -> ACTIVE -> HOT`. Promote on consequence/uncertainty/tail/transition; decay automatically when stable.
10. **Event > snapshot** — prefer state transitions/events plus periodic checkpoints over repeated unchanged full snapshots.
11. **Merkle + CAS where useful** — immutable evidence/chunks use content identity and Merkle structure when integrity, sync, changed-subtree localization, or reproducibility earns the overhead.
12. **CRDTs sparingly** — distributed mutation may merge through appropriate CRDTs; replication conflict is never treated as epistemic conflict.

## Housing microstructure profile

Housing is represented as independent named dimensions, not one score:

`PRICE × SUPPLY × DEMAND × CLEARING × PRESSURE × DISTRESS × COST × BUILD × PLACE`

Housing tail sensors may include rapid/deep/repeated cuts, shrinking cut intervals, below-basis listings, concession stacking, withdrawals/delist-relist, vacant/estate supply, high DOM tails, time-to-cut, cut-to-contract, fast-contract tails, over-ask/cash tails, contract fallout, builder finished-unsold age/incentives/buydowns/cancellations/starts/permits/lot options, distress/equity transitions, investor exits/short holds/flip margin collapse, STR/LTR/sale transitions, rental concessions/vacancy/DOM, insurance/tax/HOA/utility shocks, property-viability tails, and development-front inputs.

Divergence remains visible. Examples include price flat + seller pressure rising; price flat + volume falling + DOM rising; price falling + volume rising; inventory rising + new listings flat; price falling + ownership cost rising; distress rising + inventory flat; incentives rising + sticker price flat.

Derived `DEVELOPMENT FRONT` may expose position, direction, velocity/acceleration, reach/horizon, confidence, support mechanisms, and contradictions.

## Evidence strength and realization

When evidence answers the same realization question, later costly/physical stages often provide stronger evidence of realized state:

`CLAIM -> PLAN -> PERMIT -> CONTRACT -> EXPENDITURE -> MOBILIZATION -> PHYSICAL CHANGE -> OPERATION`

This is not a universal truth-ranking: earlier stages remain useful for intention/forecasting; stage strength is objective-relative and mechanism-aware.

## Semantic optimization before machine optimization

Canonical optimization order:

`PRUNE -> DEDUP -> DELTA -> SPARSE -> REUSE -> ROLL UP -> INCREMENT -> CACHE -> LAYOUT -> VECTORIZE -> COMPRESS`

Do not SIMD unnecessary work, compress unnecessary bytes, cache unnecessary queries, or use an LLM where deterministic/indexed machinery is adequate.

## Acquisition and shared parsing

Prefer feeds, changed records, release deltas, hashes/timestamps, conditional requests, and incremental queries. `NO CHANGE -> NO DOWNSTREAM WORK`.

Collectors SHOULD be generic where mechanics are shared: HTTP/API, RSS/Atom, GIS/WFS, CSV/table, document release, change detector, database query. Extraction primitives SHOULD be reusable across domains for dates, money, quantity, address/parcel/location, organization, permit, status change, etc.

Polling cadence follows source cadence and decision need, not habit.

## Cheapest adequate compute

Escalation ladder:

`LOOKUP -> BOOLEAN -> COUNTER -> RATIO -> RULE -> SKETCH/DISTRIBUTION -> STATISTICS -> OPTIMIZATION/MODEL -> ML -> LLM`

LLM workload scales with novel ambiguity, not raw data volume.

## Incremental / sparse execution

Maintain reusable incremental counts, rolling statistics, histograms/quantile sketches, top-K, distinct estimates, transition counts, and state summaries where they change decisions.

On change: `EVENT -> AFFECTED SUBGRAPH -> UPDATE`. Only reachable dependencies awaken. Rollups update only where affected.

Sparse state stores only meaningful coordinates such as `{space,time,dimension,objective} -> state`; ordinary normality does not require explicit rows.

Sparse human output surfaces only material delta, threshold/tail, contradiction, binding constraint, opportunity, regime transition, material uncertainty, cause, or action threshold.

## Storage / temperature / retention

Retention belongs to the information, not the subsystem.

Storage classes: `PERMANENT`, `LONG`, `ROLLING`, `CACHE`, `EPHEMERAL`.

Temperature tiers: `HOT`, `WARM`, `COLD`, `EXTERNAL/REHYDRATABLE`.

Default compression policy where suitable:
- hot: compact binary or low-latency codec such as LZ4/uncompressed;
- warm: low/moderate Zstd;
- cold: stronger Zstd;
- incompressible/already-compressed objects: do not recompress pointlessly.

Columnar analytical workloads SHOULD prefer interoperable columnar layouts (Arrow/Parquet-style) with column pruning/predicate pushdown/dictionary encoding/vectorization where implementation permits. Object-heavy JSON is not the default permanent analytical substrate.

Use dictionary/delta/varint/bit packing/Roaring-style compact encodings when semantics fit.

Large immutable/read-mostly structures MAY use mmap/zero-copy/shared immutable buffers when the lifecycle and platform justify it.

Partitions follow consequential access axes such as time/geography/source-domain; filters should push down toward acquisition/storage.

## Geometry

Retain authoritative geometry where necessary while deriving bounding boxes, simplified vectors, spatial indexes, and multi-resolution tiles as cheaper views. Geometry resolution follows query resolution. Expensive intersections are precomputed only when reuse justifies materialization.

## Scheduling / concurrency

Batch fetches, parsing, hashing, writes, compression, graph updates, rollups, and model calls when it reduces fixed overhead.

Parallelism is bounded by useful throughput, cache locality, thermals, power, latency, and interactive responsiveness. Use bounded queues/backpressure; when downstream saturates, ingestion slows rather than allowing unbounded queue/RAM growth.

Low-priority compaction, archival, index cleanup, stronger compression, and integrity checks SHOULD coalesce into efficient idle/low-cost windows.

## Evidence preservation

Preserve raw bytes when source volatility, auditability, reproducibility, legal/evidentiary value, future reinterpretation, or acquisition difficulty justifies it. Otherwise a canonical observation + provenance + retrievable source MAY be sufficient.

Preserved source objects use CAS where useful: one artifact with many references, not duplicated bytes per observation.

Observation is immutable/corrigible only by new evidence; interpretation remains versioned/corrigible. Preserve what was observed at time T separately from what operator/model version concluded from it.

Version only consequential semantics: source schema, parser/transformation/operator/classification methodology when a change can alter meaning.

## Evidence independence

Source count is not independent evidence count. Repeated reporting of one upstream release remains one evidence lineage. Prefer mechanistically independent corroboration.

Sensor dominance/correlation pruning MAY demote/sleep/remove a sensor whose unique information contribution is negligible once other sensors are known. The registry records what can be observed; it does not require every watch to remain continuously active.

## Uncertainty / contradiction / tail escalation

Additional evidence is acquired when roughly:

`remaining uncertainty × consequence × action sensitivity`

justifies acquisition/storage/compute/bandwidth/maintenance/latency/attention burden.

Normal mode stays cheap. Contradiction path:

`CONTRADICTION -> TARGETED RETRIEVAL -> DISCRIMINATE -> RESOLVE OR PRESERVE UNKNOWN`.

Tail path:

`CHEAP SENSOR -> TAIL TRIGGER -> HIGHER RESOLUTION -> CORROBORATE -> COMPOSE -> QUIET`.

## LLM-last / Jarvis packet

Jarvis receives compact packets such as `state + delta + anomaly/tail + contradiction + discriminating evidence`, not raw document piles. Expensive interpretations should persist stable structured derivatives when reuse/lifecycle value justifies it.

## Degradation / replay

Missing sources yield `STALE`, `UNKNOWN`, or `PARTIAL`, not total system failure. Avoid unnecessary single-source dependencies.

Canonical events + retained evidence + versioned operators support offline replay/historical reconstruction where retained information permits it.

## Self-pruning / self-accounting

Polaris monitors its own observation machinery: source usefulness, retained bytes, bandwidth, compute, failures, maintenance burden, unique information contribution, cache reuse, derivation reuse, unused derivations, escalations, and human attention events.

Useful internal metrics include ingested/retained bytes, dedup ratio, compression ratio, cache hit rate, active/quiet sources, compute/bandwidth per watch, derivation reuse, unused derivations, escalations, and attention events. Do not collapse these into one score when tradeoffs matter.

Dead weight is demoted automatically where authority allows or proposed for removal.

## Storage target

With semantic pruning, shared observations, sparse state, event storage, rollups, CAS, compact/columnar encoding, and compression, core decade-scale intelligence SHOULD target `<100 GB` where realistically achievable and remain comfortably within a few hundred GB as scope expands. This is an engineering target, not a correctness requirement.

Preserved evidence archives and large raster/satellite/image collections are separately governed because they may dominate storage independently of intelligence-graph size.

Invariant: if storage grows materially faster than unique consequential information, investigate the architecture before merely adding disks.

## Resource admission

Every continuously active source/sensor/derivation faces:

`EXPECTED INFORMATION VALUE × CONSEQUENCE × REUSE`

versus

`ACQUISITION + STORAGE + COMPUTE + BANDWIDTH + MAINTENANCE + LATENCY + ATTENTION`.

Failure does not erase capability: a source may remain dormant/on-demand rather than continuously tracked.

## Marginal capability law

Once primitives/evidence already exist, new analytical views SHOULD approach trivial marginal infrastructure cost. A new source usually adds real marginal burden; a new interpretation of existing canonical evidence should usually reuse existing acquisition/storage.

## Anti-patterns

Reject: collect everything; poll constantly; snapshot everything; duplicate per-domain databases; store every derived view; average away distributions; unknown=neutral; correlated reports as independent evidence; LLMs for deterministic work; global recompute after local change; parcel resolution nationally; unjustified raw retention; compressing garbage before pruning; SIMD unnecessary work; useless caches; CRDT epistemic disagreement; one mega-DAG; dashboards as truth stores; surfacing every anomaly; machine optimization that wastes human attention.

## Full compiler

`DISCOVER SIGNAL -> REGISTER CAPABILITY -> ESTIMATE VALUE/COST -> SCHEDULE CHEAPEST ADEQUATE OBSERVATION -> DETECT DELTA -> ACQUIRE MINIMALLY -> CANONICALIZE -> DEDUP -> ATTACH PROVENANCE -> STORE EVENT/FACT ONCE -> UPDATE SHARED ENTITIES/RELATIONS -> INCREMENT AFFECTED STATISTICS -> TRAVERSE AFFECTED DAG ONLY -> UPDATE TAILS/LATENT STATES -> ROLL UP AS REQUIRED -> COMPOSE ACROSS DOMAINS -> PROMOTE MATERIAL CHANGE -> ESCALATE RESOLUTION IF JUSTIFIED -> JARVIS ONLY IF NECESSARY -> CACHE EXPENSIVE REUSABLE RESULTS -> COMPRESS/TIER/ARCHIVE/EXPIRE -> RETURN TO QUIET`.

Canonical engineering summary:

**CHOOSE THE RIGHT SHAPE -> FETCH LESS -> STORE ONCE -> REUSE EVERYTHING -> COMPUTE ON CHANGE -> ROLL UP -> COMPOSE LATE -> MATERIALIZE SPARINGLY -> VECTORIZE NECESSARY WORK -> COMPRESS IT -> SURFACE ALMOST NOTHING -> SLEEP.**
