# Reality Intelligence Anti-Pattern & Failure-Mode Canon v1

Status: canonical negative specification for Model `0.1.0-alpha.26`.

This is the inverse compiler for the fused Reality Intelligence architecture. It does **not** create a new Fabric, truth store, dashboard, score, or mega-graph.

## Governing rejection laws

> More observation is not automatically more awareness.

> More retained data is not automatically more recoverability.

> More compute is not automatically more intelligence.

> A sensor that cannot change interpretation, confidence, choice, or action at adequate resolution is not an active sensor merely because it is obtainable.

> A local optimization is invalid when it moves greater burden into storage, bandwidth, compute, maintenance, latency, fragility, uncertainty, or human attention.

> No change means no downstream work unless a scheduled integrity/revalidation obligation independently requires it.

## 1. Registry anti-patterns

### Registry-as-database
The watch registry becomes a second truth store.

**Reject:** canonical evidence/state remains owned by Evidence/EWS; registry is routing/discovery metadata.

### Dataset = subsystem
Every new dataset creates a new service/domain store.

**Reject:** new source attaches to existing observation mechanics unless it truly needs distinct state/evidence/authority mechanics.

### Watch proliferation without admission
Everything interesting becomes continuously active.

**Reject:** use resource admission; dormant/on-demand is a valid state.

### Zombie watch
A watch remains active after its information contribution disappears.

**Reject:** measure unique discrimination/reuse and demote/sleep/remove.

## 2. Source/evidence anti-patterns

### Source = truth
A publisher/source label is promoted into fact.

**Reject:** preserve artifact -> observation -> interpretation.

### Echo-chamber confidence
Twenty sites repeat one upstream release and confidence is counted twenty times.

**Reject:** count independent evidence/mechanisms, not URLs.

### Raw-bytes hoarding
All source bytes are retained forever because deletion feels unsafe.

**Reject:** preserve raw bytes only when volatility, auditability, reproducibility, future reinterpretation, legal importance, or reacquisition cost justify them.

### Evidence evaporation
Only derived state is stored and the underlying observation/provenance disappears.

**Reject:** consequential interpretation remains inspectable/replayable.

### Mutable-history overwrite
A new interpretation rewrites what was observed historically.

**Reject:** observation immutable; interpretation corrigible/versioned.

### Scrape-first acquisition
Pages are repeatedly fetched when structured/delta feeds exist.

**Reject:** prefer cheapest stable source with adequate semantics.

## 3. Proxy / weird-OSINT anti-patterns

### Proxy literalism
A proxy arrow is treated as deterministic truth.

**Reject:** observable -> mechanism -> latent state must carry confounders, validity, confidence, and ignore/recalibration conditions.

### Proxy monoculture
One indirect signal becomes the entire estimate of a latent state.

**Reject:** seek independent corroboration when consequence/action sensitivity requires it.

### Proxy pile
Highly correlated proxies are added until the dashboard looks convincing.

**Reject:** prune correlation and optimize independent information gain.

### Mechanism-free correlation
A statistical association is promoted to a causal explanation.

**Reject:** causal DAG edges require an explicit plausible mechanism and discriminating evidence.

### Exhaust opportunism
Every available exhaust stream gets collected because it might someday be useful.

**Reject:** dormant capability is preferable when expected information value does not beat lifecycle burden.

## 4. Tail-sensor anti-patterns

### Mean-only blindness
Only aggregate means are monitored.

**Reject:** use tails/thresholds/distributions when they can lead aggregate movement or change decisions.

### Quantile fetish
P1/P5/P95/P99 are calculated everywhere without mechanistic value.

**Reject:** use consequential thresholds when better; quantiles are implementation choices.

### Tail-noise panic
Any extreme observation escalates the system.

**Reject:** distinguish measurement error, isolated outlier, recurrent tail, cluster, transition, and regime shift.

### Tail permanence
A tail-triggered high-resolution watch never decays.

**Reject:** escalation must have demotion/quiet conditions.

### Expected-event blindness
Only observed anomalies are monitored; consequential absence is ignored.

**Reject:** support expected-event absence when the expectation is evidence-grounded.

## 5. Housing-intelligence anti-patterns

### Housing-score collapse
Price, supply, demand, clearing, pressure, distress, ownership cost, build, and place are averaged into one score.

**Reject:** preserve dimensions and divergences.

### Headline-price myopia
Closed prices are treated as sufficient market state.

**Reject:** preserve DOM, cuts, concessions, failed contracts, inventory age, effective builder repricing, etc.

### Sticker-price blindness
Builder incentives/buydowns are ignored because nominal price is unchanged.

### Inventory-count blindness
Inventory increases are interpreted without age/composition/new-listing/absorption context.

### Distress = supply
Financial distress is assumed to have already propagated into listed inventory.

### Nominal-affordability illusion
Price falls while insurance/taxes/financing/utilities rise, but only price is surfaced.

### Development-front radius
Development pressure is projected by arbitrary radius rather than actual parcels, infrastructure corridors, jurisdictions, topology, and propagation evidence.

## 6. Composition anti-patterns

### Average-away composition
Independent harms/benefits disappear into a moderate aggregate.

### Unknown = neutral
Missing/contested state is rendered as no effect.

### Contradiction erasure
Conflicting evidence is averaged rather than preserved and discriminated.

### Constraint dilution
A binding constraint is averaged with favorable dimensions.

### Correlation bag
Signals are grouped without typed causal/spatial/temporal relations.

### One-way composition
A compound state cannot be traversed backward to supporting observations and mechanisms.

**Reject:** composition must remain reversible/inspectable.

## 7. DAG / graph anti-patterns

### Mega-DAG
Evidence, derivation, causality, execution, and capability requirements are forced into one universal graph.

**Reject:** maintain distinct interoperable DAGs with typed crossings.

### Full-graph wakeup
Any event causes broad recomputation.

**Reject:** only reachable affected nodes and necessary rollups wake.

### Dependency omission
A derived materialization is cached without tracking what invalidates it.

### Graph archaeology
Aliases/obsolete nodes remain reachable as if current.

**Reject:** successors/retirement/compatibility are explicit.

## 8. Spatial anti-patterns

### Radius-as-reality
Euclidean distance substitutes for watershed, corridor, jurisdiction, network, parcel adjacency, viewshed, or other actual spatial relationship.

### National parcel scan
High-resolution national queries touch parcel-level data by default.

### Geometry maximalism
Full authoritative polygons are used for every operation even when bounding boxes/tiles/simplified vectors are decision-equivalent.

### Spatial double counting
The same event contributes multiple times through overlapping geographic rollups.

### Scale leakage
Local evidence is generalized to regional/national state without a justified aggregation/propagation operator.

## 9. Temporal anti-patterns

### Snapshot cemetery
Unchanged state is repeatedly stored as full snapshots.

**Reject:** event + checkpoint where adequate.

### Replay forever
Current state requires replaying a decade from genesis every time.

### Polling cadence blindness
Annual data is checked hourly or event-driven data monthly.

### Recency worship
Newest record is assumed most informative despite reporting lag, revision, seasonality, or low sample size.

### Regime-rebaseline whiplash
A transient excursion is promoted to a new baseline.

## 10. Aggregation / rollup anti-patterns

### Average of averages
Derived means are recombined without original weights/denominators.

### Rate without denominator
The numerator survives while the population/exposure denominator is lost.

### Tail destruction
Rollups preserve means but erase distribution shape/tails.

### State averaging
Discrete/constraint states are numerically averaged instead of composed by semantics.

### Uncertainty laundering
Aggregation increases apparent precision without additional evidence.

## 11. Storage anti-patterns

### One storage class for everything
Hot operational state and cold archive share the same retention/layout assumptions.

### Hot archive
Historical replay material occupies the fastest tier indefinitely.

### Cold working set
Frequently traversed indexes/states are repeatedly decompressed/read from slow storage.

### JSON forever
Object-heavy verbose JSON becomes permanent analytical substrate.

### Sparse-cube materialization
Mostly empty multidimensional state is expanded into dense tables.

### Derived-view hoarding
Every query/view is materialized permanently.

### Rehydratable hoarding
Cheaply reacquirable external material is stored forever without value.

## 12. Compression anti-patterns

### Compress garbage
Unneeded data is compressed instead of pruned.

### Recompress incompressible data
Already-compressed media/documents are pointlessly recompressed.

### Cold compression on hot path
Expensive compression settings damage interactive latency.

### Codec monoculture
One codec/level is used across all temperatures/workloads.

### Compression hides semantics
Compact encodings lose version/schema/denominator/units needed for interpretation.

## 13. Cache anti-patterns

### Cache everything
Cheap or rarely reused computation is cached.

### Cache without identity
Results cannot be safely reused because dependency/content identity is absent.

### Stale-cache certainty
Expired materialization is silently treated as current state.

### No negative cache
Known absence/no-change is repeatedly rediscovered before reasonable expiry.

### Cache as truth
Derived cache becomes authoritative and survives invalidation failure.

## 14. Compute anti-patterns

### LLM-first
Text model is used for lookup, exact parsing, booleans, counters, deterministic rules, or simple statistics.

### SIMD theater
Vectorization is celebrated while unnecessary work remains.

### Full-history recompute
Incremental statistics exist but history is rescanned anyway.

### Precision theater
Exact computation is paid for when approximate/sketch answers are decision-equivalent.

### Model escalation ratchet
Once an expensive model is introduced, simpler methods stop competing.

### Hardware-shaped semantics
Data meaning is distorted to fit an implementation optimization.

## 15. Sketch / approximation anti-patterns

### Approximation without error contract
Sketch results lack known error/decision tolerance.

### Exactness loss at consequential boundary
Approximate state is used where the error could change action.

### Sketch duplication
Multiple sketches summarize the same stream without distinct use.

### Approximate tail blindness
A sketch cannot resolve the tail/threshold actually driving the decision.

## 16. Acquisition anti-patterns

### Poll everything constantly
Frequency ignores source cadence and consequence.

### Full-fetch reflex
Changed-record, ETag/hash, release delta, or incremental API paths exist but are ignored.

### Source fan-out
Many redundant providers are queried before cheap primary evidence is exhausted.

### No backoff / no backpressure
Failure or downstream saturation causes retry storms and unbounded queues.

### Provider dependency creep
One source becomes an unnecessary single point of failure.

## 17. Parsing / canonicalization anti-patterns

### Parser per domain
Every dataset gets bespoke extraction for dates, money, parcels, organizations, status changes, etc.

### Canonicalization loss
Source-specific nuance is destroyed before it is known to be irrelevant.

### Identity fragmentation
The same parcel/org/project/event receives multiple identities across domains.

### Schema drift silence
Source schema changes alter meaning without parser/version alarm.

### Premature normalization
Ambiguous source fields are forced into a clean ontology instead of preserved as uncertain/raw semantics.

## 18. Merkle / CAS anti-patterns

### Hash = meaning
Content identity is confused with semantic identity or truth.

### Merkle everything
Merkle structures are added where synchronization/integrity/change-localization gain does not justify complexity.

### CAS orphan explosion
Objects are deduplicated but references/lifecycle/garbage collection are unmanaged.

### Hash instability
Noncanonical serialization produces different hashes for equivalent content where equivalence was intended.

## 19. CRDT anti-patterns

### CRDT epistemology
Conflicting claims about reality are auto-merged as replication conflicts.

**Reject:** replication conflict != epistemic conflict.

### Latest-wins truth
LWW semantics resolve authoritative disagreement merely by timestamp.

### CRDT everywhere
Distributed mutation machinery is used for immutable evidence or centrally owned state without need.

## 20. Parallelism / queue anti-patterns

### Thread-count worship
More workers are assumed to mean more throughput.

### Unbounded queue
RAM grows indefinitely to hide downstream saturation.

### Interactive starvation
Background maintenance consumes resources needed by foreground decisions.

### Tiny-work parallelism
Coordination overhead exceeds work saved.

### Batch latency trap
Batching improves throughput while violating action latency.

## 21. Memory / I/O anti-patterns

### Deserialize-copy-parse-repeat
Representations are repeatedly copied/serialized between stages.

### Pointer forest
Hot analytical scans traverse object-heavy indirection.

### Eager-load archive
Large read-mostly structures are loaded entirely when mmap/lazy access suffices.

### Partition miss
Local/time-scoped queries touch unrelated partitions.

### Predicate-late filtering
Huge datasets are loaded before filtering.

## 22. Attention anti-patterns

### Dashboard swamp
Thousands of indicators are human-facing because the backend knows them.

### Alert confetti
Every anomaly generates attention demand.

### Attention laundering
Machine resource savings are claimed while human review burden increases.

### Technical-handle leakage
Internal sensor/operator names become required user vocabulary.

### No quiet state
A watch can escalate but never become silent again.

## 23. Confidence / uncertainty anti-patterns

### Confidence by count
Raw source count substitutes for independent evidence strength.

### False precision
Confidence is reported with more granularity than evidence supports.

### Uncertainty elimination theater
The system spends heavily to resolve uncertainty that cannot change action.

### Staleness concealment
Missing source updates are displayed as current verified state.

### Unknown panic
Unknown automatically escalates even when consequence/action sensitivity is low.

## 24. Contradiction anti-patterns

### Contradiction averaging
Independent disagreement becomes middle-value neutrality.

### Permanent triangulation
Expensive cross-checking runs continuously instead of on contradiction/tail triggers.

### Authority shortcut
One designated source suppresses conflicting evidence even when source authority does not settle the factual question.

### Contradiction amnesia
Disagreement disappears once one temporary interpretation wins.

## 25. Versioning / replay anti-patterns

### Version everything
Trivial artifacts receive bureaucratic versions that cannot change semantics.

### Version nothing
Parser/operator/classification changes that alter meaning are untracked.

### Nonreproducible replay
Historical state cannot be recomputed because operator/version/provenance is missing.

### Backfill overwrite
Improved historical interpretation silently replaces previous derived history without trace.

## 26. Self-optimization anti-patterns

### Self-metric score
Bytes, cache hits, compute, bandwidth, failures, reuse, and attention are collapsed into one health score.

### Optimize the metric
Dedup ratio rises because useful distinct evidence is discarded; cache hit rises because stale answers are reused.

### Self-pruning blindness
A source is removed for low short-term use despite high rare-event option value.

### Maintenance blindness
A clever optimization requires ongoing tuning nobody accounts for.

### Optimization treadmill
Polaris continuously tunes itself after marginal value has vanished.

## 27. Resource-admission anti-patterns

### Interesting = valuable
Novelty substitutes for consequential information value.

### Free-source illusion
Free data is treated as free despite parsing/storage/maintenance/attention burden.

### Reuse fantasy
Hypothetical future reuse is credited without plausible downstream paths.

### Consequence blindness
Cheap sensors are admitted despite informing no consequential objective.

### Dormant-capability deletion
A useful but rarely needed source is removed rather than kept as an on-demand capability when that is cheap.

## 28. Failure / degradation anti-patterns

### Missing-source cascade
One unavailable source breaks the entire domain pipeline.

### Stale = fresh
Last known state is silently served without age/validity semantics.

### Partial = complete
Incomplete coverage is reported as comprehensive.

### Retry storm
Transient failures trigger identical aggressive retries instead of backoff/substitution/degradation.

### No reconstruction path
An external provider disappears and retained canonical events/evidence are insufficient for replay.

## 29. Security / privacy anti-patterns

### OSINT dossier creep
Place/system watches mutate into private-person tracking.

### Collect-because-public
Publicly accessible personal data is collected despite no legitimate system-state need.

### Secret-bearing cache
Credentials/tokens leak into CAS/cache/evidence archives.

### Provenance overexposure
Human-facing views reveal sensitive source details unnecessarily.

### Retention without minimization
Privacy-sensitive material outlives its purpose.

## 30. Meta anti-patterns

### Architecture for the benchmark
The system looks efficient in synthetic metrics but misses consequential reality.

### Shape worship
Graphs, tensors, Merkle DAGs, CRDTs, Parquet, SIMD, sketches, etc. become goals rather than tools.

### Optimization inversion
Machine efficiency is optimized before semantic pruning/deduplication.

### Complexity ratchet
Every performance problem earns another layer/service/cache/index.

### Novelty ratchet
New methods enter; boring deterministic baselines stop being reconsidered.

### Local optimization
Storage improves while latency/maintenance/attention worsens, or vice versa.

### No stop condition
Optimization continues after added complexity exceeds marginal value.

### Reality veto failure
A clean model is preserved after observations contradict it.

## Universal inverse compiler

Every source/sensor/derivation/storage/cache/compute change must answer:

1. What consequential state/question does this serve?
2. Is there already adequate evidence/capability?
3. What unique discrimination does it add?
4. Is the source/mechanism independent of what we already have?
5. What spatial/temporal/denominator semantics must survive?
6. What burden does it add: acquisition/storage/compute/bandwidth/maintenance/latency/attention/privacy?
7. Can it be dormant/on-demand instead of continuous?
8. What is the cheapest adequate representation/compute method?
9. What changes when the source is stale/missing/wrong?
10. What invalidates derived state/cache?
11. Can the result be replayed/inspected from evidence and versioned operators?
12. Is there a simpler boring baseline?
13. Does the benefit survive whole-system recompilation?
14. What causes promotion, escalation, decay, demotion, or removal?
15. Would we still keep it if novelty and sunk cost vanished?

Disposition:

`ADMIT_ACTIVE | ADMIT_DORMANT | PROBE | DEFER | DEMOTE | PRUNE`

No universal score is required. Hard semantic/privacy/evidence failures may directly PRUNE; uncertainty with cheap reversible learning may PROBE; useful but low-duty-cycle capability may ADMIT_DORMANT.

Canonical negative summary:

**DO NOT COLLECT BECAUSE YOU CAN -> DO NOT COMPUTE BECAUSE YOU STORED -> DO NOT STORE BECAUSE YOU FETCHED -> DO NOT SURFACE BECAUSE YOU KNOW -> DO NOT KEEP BECAUSE YOU BUILT.**
