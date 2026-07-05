# ADR 0008: Introduce A Compatibility Layer For External Integrations

Status: Proposed

Date: 2026-07-05

## Context

External integrations are currently visible mostly in preserved legacy code:
Home Assistant, Jellyfin, UniFi, Docker, maps, web fetch/search, MCP tools,
Ollama/local model clients, broker/database transports, and deployment
scripts. The canonical repository already has `external/` and `operations/`
homes, but they are mostly placeholders.

If engines directly absorb provider SDKs or deployment choices, internal
architecture becomes harder to evolve.

## Decision

Create a Compatibility Layer pattern for external integrations. Provider,
protocol, API, deployment, and legacy entry-point concerns should live behind
adapter boundaries that emit contract-shaped requests, observations, or service
calls.

The layer should preserve compatibility while preventing external systems from
owning Wayfinder concepts.

## Alternatives Considered

- Move all external code immediately. Rejected because compatibility parity is
  not proven.
- Leave integrations in engine legacy forever. Rejected because it obscures
  ownership and duplicates infrastructure.
- Put all integrations in services. Rejected because provider-specific behavior
  is not reusable platform infrastructure.

## Tradeoffs

The Compatibility Layer adds a boundary, but it reduces engine coupling and
keeps replaceable providers from becoming architectural owners.

## Migration Plan

1. Classify each legacy integration as `external/`, `operations/`, service
   adapter, or engine-specific adapter.
2. Pick one low-risk integration for a parity proof.
3. Preserve legacy entry points as aliases or shims.
4. Add adapter contract tests.
5. Repeat only when evidence shows behavior parity.
