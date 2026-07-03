"""Egress endpoints for Host Groundskeeper."""

from .health import build_health_response

__all__ = ["build_health_response"]
