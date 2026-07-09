# 18 Cross-Cutting Systems

Cross-cutting systems are reusable concerns that appear across layers but must
not become hidden owners of domain or engine behavior.

## Architecture Health Dashboard

### Dependency Health

| Metric | Current Value | Status |
| --- | ---: | --- |
| Active service-to-engine violations | 0 | Pass |
| Active contract-to-implementation violations | 0 | Pass |
| Generated graph circular references | 0 | Pass |
| Active internal Python import edges | 28 | Informational |
| Cross-layer shortcuts | Present mainly in legacy | Registered debt |

### Repository Health

| Metric | Current Value | Status |
| --- | ---: | --- |
| Tracked files | 879 | Informational |
| Active Python files | 38 | Informational |
| Legacy Python files | 199 | High migration surface |
| Duplicate tracked hash groups | 67 | Registered debt |
| Knowledge source files | 525 | Generated evidence |
| Knowledge graph nodes | 39,325 | Generated |
| Knowledge graph edges | 122,877 | Generated |

### Repository Size By Layer

| Layer / Area | Tracked Files | Approx Bytes |
| --- | ---: | ---: |
| Knowledge | 59 | 220,675,240 |
| Engines | 620 | 2,992,117 |
| Docs | 81 | 360,847 |
| Tooling | 7 | 86,068 |
| Services | 61 | 84,283 |
| Canon | 3 | 54,978 |
| Contracts | 30 | 52,090 |
| Constitution | 8 | 33,629 |
| Capabilities | 1 | 1,322 |
| Domains | 1 | 274 |
| Internal | 1 | 242 |
| External | 1 | 258 |
| Operations | 1 | 605 |

## Cross-Cutting Audit

| System | Current Home | Status | Recommendation |
| --- | --- | --- | --- |
| Identity | `services/identity/` | Stage 2 proof | Add vertical slice consumers later. |
| Event Bus | `services/event-bus/` | Stage 2 proof | Add adapter consumers later. |
| Storage | `services/storage/` | Scaffold | Next Stage 2 proof. |
| Configuration | `services/configuration/` | Scaffold | After Storage. |
| Policy | `services/policy/` | Scaffold | After Configuration. |
| Search/Index | Retrieval + tooling | Split | Revisit after Storage. |
| Progressive Discovery | Constitution + Retrieval Strategy | Canonical invariant | Apply across ARK, conversation memory, repositories, containers, OSINT, home systems, media, and future domains. |
| Logging/Telemetry | Legacy/docs | Not canonicalized | Future service only with evidence. |
| Scheduling/Caching | Legacy/tooling | Not canonicalized | Do not extract prematurely. |
| Serialization | repeated helpers | Low-risk duplication | Extract only after service need. |

## Knowledge Health

- Knowledge is derived: pass.
- Knowledge never replaces reality: pass by documentation and generated
  manifest.
- Knowledge maintains provenance: pass, compile report has missing provenance
  count `0`.
- Knowledge remains reproducible: pass, source manifest and source hash are
  recorded.

## Progressive Discovery Health

Cross-cutting retrieval, indexing, import, and repository workflows should
prefer bounded inventories, metadata, summaries, relationships, deltas, hashes,
and references before full content. New implementations should expose enough
status to show retrieval depth, confidence, and stop conditions.
