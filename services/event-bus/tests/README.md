# Event Bus Service Tests

No executable tests are added in Wave 2 because no runtime implementation is promoted.

Future tests must prove behavior preservation against the legacy implementation before any engine consumer is rewired.

## Implementation Proof Tests

- `test_event_bus_service.py` verifies transport-neutral route matching, publish/subscribe, replay, bounded failures, and health.
