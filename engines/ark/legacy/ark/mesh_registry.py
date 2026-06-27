#!/usr/bin/env python3
"""
ARK Mesh Registry - OPTIMIZED
Service discovery with batching, deduplication, and caching
"""

import asyncio
import gc
import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import redis.asyncio as aioredis

try:
    from nats.errors import Error as NATSError
except ImportError:
    NATSError = RuntimeError

from ark.security import (
    registration_rate_limiter,
    validate_capability,
    validate_instance_id,
    validate_service_name,
)
from ark.maintenance import (
    HealthCheck,
    ResilientNATSConnection,
    ShutdownCoordinator,
)
from ark.event_schema import EventSource
from ark.gsb import GlobalStateBus, build_global_state_bus
from ark.policy_engine import load_policy_set
from ark.reducers import MeshViewReducer, ReducerEngine
from ark.runtime_contracts import runtime_contract_registry
from ark.runtime_flow import RuntimeAudit
from ark.subjects import MESH_REGISTER, MESH_HEARTBEAT, MESH_REGISTERED
from ark.time_utils import utc_now_iso, utc_now_naive
from ark.performance import (
    MessageBatcher,
    RequestDeduplicator,
    RateLimitedCache,
    NATSConnectionPool,
)

# Optimize Python GC
gc.set_threshold(700, 10, 10)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger('ARK-MeshRegistry')


class ServiceInstance:
    """Represents a registered service instance"""
    
    def __init__(self, service: str, instance_id: str, capabilities: List[str], 
                 metadata: Dict[str, Any] = None, ttl_seconds: int = 10):
        self.service = service
        self.instance_id = instance_id
        self.capabilities = capabilities
        self.metadata = metadata or {}
        self.ttl_seconds = ttl_seconds
        self.registered_at = utc_now_naive()
        self.last_heartbeat = utc_now_naive()
        self.load = 0.0
        self.healthy = True
    
    def is_expired(self) -> bool:
        """Check if heartbeat has expired"""
        elapsed = (utc_now_naive() - self.last_heartbeat).total_seconds()
        return elapsed > self.ttl_seconds
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dict"""
        return {
            "service": self.service,
            "instance_id": self.instance_id,
            "capabilities": self.capabilities,
            "load": self.load,
            "healthy": self.healthy,
            "registered_at": self.registered_at.isoformat(),
            "last_heartbeat": self.last_heartbeat.isoformat(),
            "metadata": self.metadata
        }


class MeshRegistry:
    """Central service registry with caching and batching"""
    
    def __init__(
        self,
        nats_url: str = "nats://nats:4222",
        redis_url: str = "redis://redis:6379",
        gsb: GlobalStateBus | None = None
    ):
        self.nats_url = nats_url
        self.redis_url = redis_url
        self._nats = ResilientNATSConnection(nats_url)
        self.nc = None
        self.js = None
        self.redis: Optional[aioredis.Redis] = None
        
        self.gsb = gsb or build_global_state_bus()
        self.audit = RuntimeAudit(
            self.gsb,
            source=EventSource.ARK_CORE.value,
            surface="mesh",
            default_tags={"surface": "mesh"},
        )
        self.contracts = runtime_contract_registry()
        self.route_policy = load_policy_set(
            Path(__file__).resolve().parents[1] / "policy" / "mesh_routing_rules.json"
        )
        self.shutdown = ShutdownCoordinator()
        self.health = HealthCheck("ark-mesh-registry")
        self.health.register("nats", lambda: self._nats.is_connected)
        self.health.register("gsb", lambda: self.gsb.health()["enabled"])
        self.health.register("redis", lambda: self.redis is not None)
        
        self.reducer_engine = ReducerEngine((MeshViewReducer(),))
        self.health.register("reducers", lambda: self.reducer_engine.health()["healthy"])
        
        # Registry state
        mesh_view = self.reducer_engine.view("mesh.runtime")
        self.registry: Dict[str, Dict[str, ServiceInstance]] = mesh_view["registry"]
        self.capability_index: Dict[str, List[str]] = mesh_view["capability_index"]
        
        # Performance optimizations
        self.deduplicator = RequestDeduplicator(ttl_seconds=5)
        self.route_cache = RateLimitedCache(ttl=5, max_size=1000)
        self.heartbeat_batcher: Optional[MessageBatcher] = None
        
        logger.info("ARK Mesh Registry initialized (optimized)")
    
    async def connect(self):
        """Connect to NATS and Redis with optimizations"""
        # Connect to NATS with optimized settings
        self.nc = await NATSConnectionPool.create_connection(self.nats_url)
        self.js = self.nc.jetstream()
        
        # Connect to Redis
        self.redis = await aioredis.from_url(
            self.redis_url,
            encoding="utf-8",
            decode_responses=True,
            max_connections=10,
            socket_connect_timeout=5,
            socket_keepalive=True
        )
        await self.redis.ping()
        
        # Initialize message batcher
        self.heartbeat_batcher = MessageBatcher(
            self.nc,
            MESH_REGISTERED,
            max_batch=20,
            max_wait=0.5
        )
        
        logger.info("Connected to NATS and Redis")
    
    async def subscribe_registrations(self):
        """Listen for service registrations"""
        try:
            sub = await self.nc.subscribe(MESH_REGISTER)
            logger.info("Subscribed to %s", MESH_REGISTER)
            
            async for msg in sub.messages:
                try:
                    event = json.loads(msg.data.decode())
                    
                    # Deduplicate registration requests
                    if await self.deduplicator.is_duplicate(event):
                        logger.debug("Ignoring duplicate registration")
                        continue
                    
                    event = self.contracts.materialize_payload(
                        "runtime.mesh.registration",
                        event,
                    )
                    await self.handle_registration(event)
                
                except Exception as e:
                    logger.error(f"Error processing registration: {e}")
        
        except NATSError as e:
            logger.error(f"Subscription error: {e}")
    
    async def handle_registration(self, event: Dict[str, Any]):
        """Register or update a service instance"""
        service = event.get('service', '')
        instance_id = event.get('instance_id', '')
        capabilities = event.get('capabilities', [])
        ttl = event.get('ttl', 10)
        metadata = event.get('metadata', {})
        
        # Validation
        try:
            validate_service_name(service)
            validate_instance_id(instance_id)
        except ValueError as exc:
            logger.warning("Invalid registration rejected: %s", exc)
            return
        
        if not isinstance(capabilities, list) or len(capabilities) > 64:
            logger.warning("Invalid capabilities from %s/%s", service, instance_id)
            return
        
        safe_caps = []
        for cap in capabilities:
            try:
                safe_caps.append(validate_capability(cap))
            except ValueError:
                logger.warning("Skipping invalid capability: %s", cap)
        
        # Rate limiting
        if not registration_rate_limiter.allow(service):
            logger.warning("Registration rate-limited for %s", service)
            return
        
        ttl = max(5, min(int(ttl), 300))
        
        if self.audit.record("registration", "mesh.registration", 
                            {"service": service, "capabilities": safe_caps}):
            return
        
        instance = ServiceInstance(service, instance_id, safe_caps, metadata, ttl)
        
        self.reducer_engine.apply(
            "mesh.registration",
            {"service": service, "instance_id": instance_id, "instance": instance},
        )
        
        # Invalidate route cache for affected capabilities
        for cap in safe_caps:
            await self.route_cache.set(f"route:{cap}", None)
        
        logger.info("Registered %s/%s: %s", service, instance_id, safe_caps)
        
        # Batch publish registration event
        await self.heartbeat_batcher.add({
            "event": "registered",
            "service": service,
            "instance_id": instance_id,
            "capabilities": safe_caps,
            "timestamp": utc_now_iso()
        })
    
    async def subscribe_heartbeats(self):
        """Listen for service heartbeats"""
        try:
            sub = await self.nc.subscribe(MESH_HEARTBEAT)
            logger.info("Subscribed to %s", MESH_HEARTBEAT)
            
            async for msg in sub.messages:
                try:
                    event = self.contracts.materialize_payload(
                        "runtime.mesh.heartbeat",
                        json.loads(msg.data.decode()),
                    )
                    service = event.get('service')
                    instance_id = event.get('instance_id')
                    load = event.get('load', 0.0)
                    
                    if service in self.registry and instance_id in self.registry[service]:
                        self.reducer_engine.apply(
                            "mesh.heartbeat",
                            {
                                "service": service,
                                "instance_id": instance_id,
                                "last_heartbeat": utc_now_naive(),
                                "load": load,
                                "healthy": event.get('healthy', True),
                            },
                        )
                        logger.debug(f"Heartbeat: {service}/{instance_id} load={load}")
                
                except Exception as e:
                    logger.error(f"Error processing heartbeat: {e}")
        
        except NATSError as e:
            logger.error(f"Subscription error: {e}")
    
    async def cleanup_expired(self, interval_seconds: float = 5.0, 
                             max_cycles: int = 1_000_000):
        """Periodically remove expired instances"""
        bounded_cycles = max(1, min(int(max_cycles), 1_000_000))
        bounded_interval = max(0.1, min(float(interval_seconds), 300.0))
        
        for _ in range(bounded_cycles):
            if self.shutdown.is_shutting_down:
                break
            
            await asyncio.sleep(bounded_interval)
            
            for service, instances in self.registry.items():
                for instance_id, inst in list(instances.items()):
                    if inst.is_expired():
                        self.reducer_engine.apply(
                            "mesh.instance.expired",
                            {"service": service, "instance_id": instance_id},
                        )
                        
                        # Invalidate cache for affected capabilities
                        for cap in inst.capabilities:
                            await self.route_cache.set(f"route:{cap}", None)
                        
                        logger.info(f"Removed expired: {service}/{instance_id}")
    
    async def route_capability(self, capability: str, 
                              load_aware: bool = True) -> Optional[tuple]:
        """Route capability request with caching"""
        # Check cache first
        cache_key = f"route:{capability}"
        cached = await self.route_cache.get(cache_key)
        if cached is not None:
            logger.debug(f"Route cache hit for {capability}")
            return cached
        
        if self.audit.record("route", capability, {"load_aware": load_aware}):
            return None
        
        if capability not in self.capability_index:
            await self.route_cache.set(cache_key, None)
            return None
        
        candidates = self.capability_index[capability]
        if not candidates:
            await self.route_cache.set(cache_key, None)
            return None
        
        decision = self.route_policy.evaluate({"load_aware": load_aware})
        best_instance = None
        best_load = float('inf')
        best_service = None
        
        for service, instances in self.registry.items():
            for instance_id in candidates:
                if instance_id in instances:
                    inst = instances[instance_id]
                    if not inst.healthy:
                        continue
                    
                    if decision.decision == "lowest_load":
                        if inst.load < best_load:
                            best_load = inst.load
                            best_instance = instance_id
                            best_service = service
                    else:
                        route = (service, instance_id)
                        await self.route_cache.set(cache_key, route)
                        return route
        
        route = (best_service, best_instance) if best_instance else None
        await self.route_cache.set(cache_key, route)
        
        self.audit.record(
            "route.decision",
            capability,
            {"strategy": decision.decision, "matched_rule": decision.rule_name, 
             "routed": bool(route)},
        )
        
        return route
    
    async def get_service_info(self, service: str) -> Dict[str, Any]:
        """Get service inventory"""
        if service not in self.registry:
            return {"service": service, "instances": []}
        
        instances = [inst.to_dict() for inst in self.registry[service].values()]
        
        return {
            "service": service,
            "instance_count": len(instances),
            "total_load": sum(inst['load'] for inst in instances),
            "instances": instances
        }
    
    async def get_mesh_status(self) -> Dict[str, Any]:
        """Get overall mesh status with cache stats"""
        service_count = len(self.registry)
        instance_count = sum(len(insts) for insts in self.registry.values())
        capability_count = len(self.capability_index)
        
        services = {}
        for service in self.registry:
            insts = self.registry[service]
            services[service] = {
                "instance_count": len(insts),
                "total_load": sum(inst.load for inst in insts.values()),
                "healthy_count": sum(1 for inst in insts.values() if inst.healthy)
            }
        
        cache_stats = await self.route_cache.stats()
        
        return {
            "timestamp": utc_now_iso(),
            "services": service_count,
            "instances": instance_count,
            "capabilities": capability_count,
            "service_details": services,
            "cache_stats": cache_stats
        }
    
    async def expose_api(self, host: str = "0.0.0.0", port: int = 7000):
        """Expose REST API with connection pooling"""
        from aiohttp import web, TCPConnector
        from ark.security import (
            auth_middleware,
            error_shield_middleware,
            rate_limit_middleware,
            secure_headers_middleware,
        )
        
        async def get_health_handler(request):
            return web.json_response(self.health.check())
        
        async def get_mesh_status_handler(request):
            status = await self.get_mesh_status()
            return web.json_response(status)
        
        async def get_service_handler(request):
            service = request.match_info.get('service', '')
            info = await self.get_service_info(service)
            return web.json_response(info)
        
        async def route_capability_handler(request):
            capability = request.match_info.get('capability', '')
            route = await self.route_capability(capability)
            if route:
                return web.json_response({
                    "capability": capability,
                    "service": route[0],
                    "instance_id": route[1]
                })
            return web.json_response({"error": "No instances available"}, status=404)
        
        connector = TCPConnector(
            limit=100,
            limit_per_host=30,
            ttl_dns_cache=300
        )
        
        app = web.Application(
            middlewares=[
                error_shield_middleware,
                secure_headers_middleware,
                rate_limit_middleware,
                auth_middleware,
            ],
            client_max_size=1024**2
        )
        app.router.add_get('/api/health', get_health_handler)
        app.router.add_get('/api/mesh', get_mesh_status_handler)
        app.router.add_get('/api/service/{service}', get_service_handler)
        app.router.add_get('/api/route/{capability}', route_capability_handler)
        
        self._runner = web.AppRunner(app)
        await self._runner.setup()
        site = web.TCPSite(self._runner, host, port)
        await site.start()
        logger.info(f"Mesh API listening on {host}:{port}")
    
    async def run(self):
        """Main registry loop"""
        try:
            self.shutdown.install_signal_handlers()
            await self.connect()
            await self.expose_api()
            
            logger.info("ARK Mesh Registry started (optimized)")
            
            await asyncio.gather(
                self.subscribe_registrations(),
                self.subscribe_heartbeats(),
                self.cleanup_expired()
            )
        
        except KeyboardInterrupt:
            logger.info("Shutting down...")
        finally:
            if self.heartbeat_batcher:
                await self.heartbeat_batcher.flush()
            if hasattr(self, '_runner') and self._runner:
                await self._runner.cleanup()
            if self.redis:
                await self.redis.aclose()
            await self._nats.close()
            logger.info("Mesh registry shutdown complete")


async def main():
    registry = MeshRegistry()
    await registry.run()


if __name__ == "__main__":
    asyncio.run(main())
