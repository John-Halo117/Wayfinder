"""Event subscription setup for Host Groundskeeper."""

from __future__ import annotations

from dataclasses import dataclass

from ..contracts.interfaces import EventBusPort, Failure, SubscriptionDescriptor, _normalize_text


@dataclass(frozen=True)
class SubscriptionResult:
    """Bounded subscription setup result."""

    status: str
    subscriptions: tuple[SubscriptionDescriptor, ...]
    failure: Failure | None = None


def subscribe_to_events(
    event_bus: EventBusPort,
    subscriptions: tuple[SubscriptionDescriptor, ...],
    *,
    max_subscriptions: int,
) -> SubscriptionResult:
    """Subscribe to all configured event routes.

    Inputs: injected event bus, descriptors, and explicit subscription cap.
    Outputs: SubscriptionResult. Runtime: O(subscription_count), bounded by
    max_subscriptions. Memory: O(subscription_count). Failure: invalid descriptor,
    exceeded cap, or non-ok bus result. Deterministic: depends on event_bus.
    """

    if max_subscriptions <= 0:
        raise ValueError("max_subscriptions must be positive")
    if len(subscriptions) > max_subscriptions:
        return SubscriptionResult(
            status="error",
            subscriptions=(),
            failure=Failure.build("HOST_SUBSCRIPTION_LIMIT", "subscription count exceeds configured maximum"),
        )
    normalized: list[SubscriptionDescriptor] = []
    for index, subscription in enumerate(subscriptions):
        if index >= max_subscriptions:
            return SubscriptionResult(
                status="error",
                subscriptions=(),
                failure=Failure.build("HOST_SUBSCRIPTION_LIMIT", "subscription iteration exceeded maximum"),
            )
        try:
            descriptor = SubscriptionDescriptor(
                route_pattern=_normalize_text(subscription.route_pattern, field="route_pattern", max_length=256),
                purpose=_normalize_text(subscription.purpose, field="purpose", max_length=512),
            )
        except ValueError as exc:
            return SubscriptionResult(
                status="error",
                subscriptions=(),
                failure=Failure.build("HOST_SUBSCRIPTION_INVALID", str(exc)),
            )
        bus_result = event_bus.subscribe(descriptor.route_pattern)
        if getattr(bus_result, "status", None) != "ok":
            return SubscriptionResult(
                status="error",
                subscriptions=tuple(normalized),
                failure=Failure.build(
                    "HOST_SUBSCRIPTION_FAILED",
                    "event bus rejected subscription",
                    {"route_pattern": descriptor.route_pattern},
                ),
            )
        normalized.append(descriptor)
    return SubscriptionResult(status="ok", subscriptions=tuple(normalized))
