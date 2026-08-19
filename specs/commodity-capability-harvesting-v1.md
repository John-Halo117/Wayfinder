# Polaris Commodity Capability Harvesting v1

Status: CANONICAL

Objective: maximize delivered capability while minimizing custom code, duplicated state, maintenance, compute, hardware, integration burden, security surface, and human attention.

## Governing compiler
NEED -> DISCOVER EXISTING CAPABILITY -> QUALIFY -> ADOPT -> CONFIGURE -> CONNECT -> COMPOSE -> EXTEND ONLY THE GAP -> BUILD ONLY THE IRREDUCIBLE DELTA.

Capability ladder: USE EXISTING -> CONFIGURE -> CONNECT -> COMPOSE -> EXTEND -> BUILD. Stop at the first level satisfying the actual requirement.

Prime inversion: upstream capability improvement should usually shrink Polaris.

## Domain ownership law
Specialized applications own domain operations. Polaris owns cross-domain intelligence, composition, objective/constraint interpretation, authority mediation, and consequential deltas.

Default commodity owners include network/video (UniFi/Protect), household devices (Home Assistant), photos (Immich), documents (Paperless-ngx), media (Jellyfin), recipes (Mealie), food inventory (Grocy), workshop parts (InvenTree), feeds (FreshRSS), model runtime (Ollama or equivalent), generic LLM UI (Open WebUI or equivalent), remote connectivity (Tailscale/UniFi or equivalent), storage (NAS/ZFS/Drive/etc.), and property search (Zillow + other sources). These are examples of commodity roles, not permanent vendor mandates.

## Commodity-first, not vendor-first
Before delegation qualify: requirement fit; interoperability/API/webhook/standard/export/local access; authority boundary; data portability; locality/offline behavior; failure mode; reversibility; lifecycle burden; provider substitutability.

Open standards and replaceable implementations dominate vendor lock-in when materially equivalent.

## Thin Adapter Law
DOMAIN SYSTEM <-> THIN ADAPTER <-> CANONICAL POLARIS PRIMITIVES.

Adapters normally expose only IDENTITY, CAPABILITY, STATE, EVENT, RELATION, EVIDENCE/PROVENANCE, ACTION, AUTHORITY, HEALTH. They must not become second implementations of the domain system.

## System-of-record law
Every operational primitive state has one authoritative owner wherever practical.
RAW != OPERATIONAL != DERIVED != DECISION != PRESENTATION.
Polaris stores only unique derived/relational/evidentiary state it needs.

## Event-first integration
Prefer EVENT -> QUALIFY -> MATERIAL DELTA -> UPDATE DERIVED STATE, with periodic reconciliation. Most upstream events should die quietly before expensive layers.

## Escalation ladder
DETERMINISTIC RULE -> CHEAP LOCAL MODEL -> STRONG LOCAL MODEL -> EXTERNAL MODEL/SERVICE -> HUMAN, escalating only when unresolved and consequential.

## Local remediation law
LOCAL PROBLEM -> LOCAL CONTROL LOOP. CROSS-DOMAIN/PERSISTENT/AUTHORITY-BOUND/CONSEQUENTIAL PROBLEM -> POLARIS.

## Transactional change law
KNOWN-GOOD -> PROPOSE -> ESTABLISH ROLLBACK -> APPLY PROVISIONALLY -> OBSERVE -> VERIFY INVARIANT -> COMMIT/REVERT. Apply wherever practical to network, automation, services, models, storage, routing, energy and physical control.

## Federated twin law
Domain systems may remain authoritative twins of their own operational reality. Polaris is the federated relational world model, not a giant replica database.

## Jarvis law
Jarvis is INTENT INTERFACE + EXPLANATION + QUERY + CONTROL MEDIATION, not a domain application.

## Basecamp law
Basecamp should be boring infrastructure: COMPUTE + STORAGE + NETWORK + CONTAINER/SERVICE RUNTIME + BACKUP + OBSERVABILITY + IDENTITY/AUTHORITY + ADAPTER FABRIC.

## Presumptively commodity subsystem classes
Do not build custom network manager, NVR/video manager, photo manager, media ecosystem, document manager, recipe manager, pantry app, parts inventory app, RSS reader, generic model runtime, generic LLM chat UI, VPN/mesh, NAS manager, or routine household automation engine unless a specific unmet requirement survives qualification.

## Differentiated Polaris core
Evidence substrate; federated world model; Operative State; objective/constraint layer; authority graph; capability graph; decision operators; dependency/execution DAGs; Wayfinder; Jarvis; AMOS; thin adapters.

## Capability-delta compiler / negative backlog
RELEASE/PRODUCT/API/STANDARD CHANGE -> EXTRACT CAPABILITIES -> COMPARE REQUIREMENTS/CAPABILITY GRAPH -> FIND NEWLY SATISFIED REQUIREMENTS -> FIND OBSOLETE PLANNED WORK -> FIND RETIREABLE COMPONENTS -> ESTIMATE MIGRATION -> IGNORE/WATCH/ADOPT/MIGRATE/CONSOLIDATE/RETIRE.

Highest-value output is what can now be deleted, not what feature exists.

## Continuous Capability Harvest
TRACK ECOSYSTEM -> DETECT DELTA -> COMPARE AGAINST BACKLOG/REQUIREMENTS -> IDENTIFY DISPLACED IMPLEMENTATION -> QUALIFY MIGRATION -> DELETE/SHRINK/SUBSTITUTE/ADOPT/WAIT -> UPDATE ROADMAP/ARCHITECTURE -> CONTINUE.

## Quantitative note
Any estimate that commodity delegation can reduce a hypothetical custom ecosystem from 100 units to ~30-50, and perhaps ~20-35 after broader audits, is architectural scenario framing only, not measured LOC or verified implementation reduction. Validate by actual roadmap/component retirement receipts before promoting to measured fact.

## Anti-patterns
NOT-INVENTED-HERE; POLARIS-ALL-THE-THINGS; SHADOW DATABASE; SHADOW AUTHORITY; ADAPTER CREEP; EVENT FIREHOSE; LLM EVERYWHERE; VENDOR WORSHIP; UPDATE=FEATURE ACCUMULATION; DOMAIN APP INSIDE POLARIS; UPSTREAM FEATURE WITHOUT NEGATIVE-BACKLOG CHECK; COMMODITY DELEGATION WITHOUT PORTABILITY/RECOVERY.

Final law: OUTSOURCE THE ORDINARY. STANDARDIZE THE INTERFACE. PRESERVE THE EVIDENCE. COMPOSE THE STATE. BUILD ONLY THE DELTA. DELETE WHEN REALITY MAKES CODE OBSOLETE.
