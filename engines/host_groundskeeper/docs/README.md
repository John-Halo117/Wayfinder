# Host Groundskeeper

## Responsibility

Host Groundskeeper owns the host-level module foundation for future bounded
groundskeeping workflows. This prompt adds registration, plugin metadata,
subscription wiring, structured logging, configuration loading, metrics, health,
dependency injection, and lifecycle management only.

## Boundaries

This module does not implement CPU optimization, GPU optimization, AI, learning,
compute brokering, delta processing, recommendations, or self optimization.

## Health

`HostGroundskeeperModule.health()` returns a bounded, framework-neutral health
record that can later be adapted to an HTTP route without changing core logic.
