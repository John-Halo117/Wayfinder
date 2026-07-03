"""Host Groundskeeper engine foundation.

The package exposes registration, dependency injection, lifecycle, event
subscription, logging, metrics, configuration, and health primitives only.
Compute optimization, learning, broker behavior, and automatic execution are
intentionally outside this foundation. Recommendations are advisory only.
"""

from .core.module import HostGroundskeeperModule, register_host_groundskeeper
from .core.recommendations import HostRecommendationEngine
from .contracts.interfaces import HostGroundskeeperConfig, HostGroundskeeperDependencies

__all__ = [
    "HostGroundskeeperConfig",
    "HostGroundskeeperDependencies",
    "HostGroundskeeperModule",
    "HostRecommendationEngine",
    "register_host_groundskeeper",
]
