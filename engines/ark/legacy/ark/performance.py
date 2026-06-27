#!/usr/bin/env python3
"""
Message Batching, Deduplication, and Event-Driven Utilities
Performance-optimized patterns for ARK services
"""

import asyncio
import hashlib
import json
import logging
import time
from collections import defaultdict
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


class MessageBatcher:
    """Batch small messages to reduce NATS round-trips"""
    
    def __init__(self, nc, subject: str, max_batch: int = 50, max_wait: float = 0.1):
        self.nc = nc
        self.subject = subject
        self.batch: List[Dict[str, Any]] = []
        self.max_batch = max_batch
        self.max_wait = max_wait
        self.last_flush = time.time()
        self.lock = asyncio.Lock()
        self._flush_task = None
    
    async def add(self, payload: Dict[str, Any]):
        """Add message to batch, flush if threshold reached"""
        async with self.lock:
            self.batch.append(payload)
            
            if len(self.batch) >= self.max_batch:
                await self._flush()
            elif self._flush_task is None:
                # Schedule auto-flush after max_wait
                self._flush_task = asyncio.create_task(self._auto_flush())
    
    async def _auto_flush(self):
        """Automatically flush after max_wait time"""
        await asyncio.sleep(self.max_wait)
        async with self.lock:
            await self._flush()
            self._flush_task = None
    
    async def _flush(self):
        """Internal flush - caller must hold lock"""
        if not self.batch:
            return
        
        try:
            payload = json.dumps({
                "batch": self.batch,
                "count": len(self.batch),
                "timestamp": time.time()
            }).encode()
            
            await self.nc.publish(self.subject, payload)
            logger.debug(f"Flushed {len(self.batch)} messages to {self.subject}")
            
            self.batch.clear()
            self.last_flush = time.time()
        
        except Exception as e:
            logger.error(f"Batch flush error: {e}")
    
    async def flush(self):
        """Manually flush remaining messages"""
        async with self.lock:
            await self._flush()


class RequestDeduplicator:
    """Prevent duplicate request processing"""
    
    def __init__(self, ttl_seconds: int = 5, max_entries: int = 10000):
        self.ttl = ttl_seconds
        self.max_entries = max_entries
        self.seen: Dict[str, float] = {}
        self.lock = asyncio.Lock()
        self._cleanup_task = None
    
    def _compute_key(self, request_data: Dict[str, Any]) -> str:
        """Compute deterministic hash of request"""
        canonical = json.dumps(request_data, sort_keys=True)
        return hashlib.blake2b(canonical.encode(), digest_size=16).hexdigest()
    
    async def is_duplicate(self, request_data: Dict[str, Any]) -> bool:
        """Check if request is duplicate within TTL window"""
        key = self._compute_key(request_data)
        now = time.time()
        
        async with self.lock:
            # Check if seen recently
            if key in self.seen:
                if now - self.seen[key] < self.ttl:
                    return True
            
            # Record new request
            self.seen[key] = now
            
            # Periodic cleanup (every 1000 requests)
            if len(self.seen) > self.max_entries:
                await self._cleanup(now)
            
            return False
    
    async def _cleanup(self, now: float):
        """Remove expired entries"""
        expired = [k for k, v in self.seen.items() if now - v > self.ttl]
        for k in expired:
            del self.seen[k]
        
        logger.debug(f"Cleaned {len(expired)} expired dedup entries")


class BackpressureManager:
    """Manage backpressure to prevent overload"""
    
    def __init__(self, max_queue_depth: int = 1000, warn_threshold: float = 0.8):
        self.max_queue_depth = max_queue_depth
        self.warn_threshold = warn_threshold
        self.current_depth = 0
        self.lock = asyncio.Lock()
        self.rejected_count = 0
        self.last_warn_time = 0
    
    async def should_accept(self) -> bool:
        """Check if new request should be accepted"""
        async with self.lock:
            utilization = self.current_depth / self.max_queue_depth
            
            # Warn if approaching limit
            if utilization > self.warn_threshold:
                now = time.time()
                if now - self.last_warn_time > 10:  # Warn max once per 10s
                    logger.warning(
                        f"Backpressure: {self.current_depth}/{self.max_queue_depth} "
                        f"({utilization:.1%} utilization)"
                    )
                    self.last_warn_time = now
            
            # Reject if at limit
            if self.current_depth >= self.max_queue_depth:
                self.rejected_count += 1
                return False
            
            return True
    
    async def increment(self):
        """Increment queue depth"""
        async with self.lock:
            self.current_depth += 1
    
    async def decrement(self):
        """Decrement queue depth"""
        async with self.lock:
            self.current_depth = max(0, self.current_depth - 1)
    
    async def stats(self) -> Dict[str, Any]:
        """Get backpressure stats"""
        async with self.lock:
            return {
                "current_depth": self.current_depth,
                "max_depth": self.max_queue_depth,
                "utilization": self.current_depth / self.max_queue_depth,
                "rejected_count": self.rejected_count
            }


class EventBuffer:
    """Buffer events for batch processing"""
    
    def __init__(self, flush_callback: Callable, max_size: int = 100, max_wait: float = 1.0):
        self.flush_callback = flush_callback
        self.max_size = max_size
        self.max_wait = max_wait
        self.buffer: List[Dict[str, Any]] = []
        self.lock = asyncio.Lock()
        self.last_flush = time.time()
        self._flush_task = None
    
    async def add(self, event: Dict[str, Any]):
        """Add event to buffer"""
        async with self.lock:
            self.buffer.append(event)
            
            if len(self.buffer) >= self.max_size:
                await self._flush()
            elif self._flush_task is None:
                self._flush_task = asyncio.create_task(self._auto_flush())
    
    async def _auto_flush(self):
        """Auto-flush after max_wait"""
        await asyncio.sleep(self.max_wait)
        async with self.lock:
            await self._flush()
            self._flush_task = None
    
    async def _flush(self):
        """Flush buffer to callback"""
        if not self.buffer:
            return
        
        try:
            batch = self.buffer.copy()
            self.buffer.clear()
            self.last_flush = time.time()
            
            # Call flush callback (non-blocking)
            await self.flush_callback(batch)
            
            logger.debug(f"Flushed {len(batch)} events")
        
        except Exception as e:
            logger.error(f"Event buffer flush error: {e}")
    
    async def flush(self):
        """Manually flush buffer"""
        async with self.lock:
            await self._flush()


class CircuitBreaker:
    """Circuit breaker for external API calls"""
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60,
        success_threshold: int = 2
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[float] = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self.lock = asyncio.Lock()
    
    async def call(self, func: Callable, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        async with self.lock:
            # Check if circuit is open
            if self.state == "OPEN":
                if self.last_failure_time and \
                   (time.time() - self.last_failure_time) > self.recovery_timeout:
                    self.state = "HALF_OPEN"
                    self.success_count = 0
                    logger.info("Circuit breaker entering HALF_OPEN state")
                else:
                    raise Exception(f"Circuit breaker is OPEN (failures: {self.failure_count})")
        
        try:
            result = await func(*args, **kwargs)
            await self._on_success()
            return result
        
        except Exception as e:
            await self._on_failure()
            raise e
    
    async def _on_success(self):
        """Handle successful call"""
        async with self.lock:
            self.failure_count = 0
            
            if self.state == "HALF_OPEN":
                self.success_count += 1
                if self.success_count >= self.success_threshold:
                    self.state = "CLOSED"
                    logger.info("Circuit breaker CLOSED after recovery")
    
    async def _on_failure(self):
        """Handle failed call"""
        async with self.lock:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                if self.state != "OPEN":
                    self.state = "OPEN"
                    logger.warning(
                        f"Circuit breaker OPEN after {self.failure_count} failures"
                    )
    
    async def stats(self) -> Dict[str, Any]:
        """Get circuit breaker stats"""
        async with self.lock:
            return {
                "state": self.state,
                "failure_count": self.failure_count,
                "success_count": self.success_count,
                "last_failure_time": self.last_failure_time
            }


class RateLimitedCache:
    """Simple rate-limited in-memory cache"""
    
    def __init__(self, ttl: int = 5, max_size: int = 1000):
        self.ttl = ttl
        self.max_size = max_size
        self.cache: Dict[str, tuple[Any, float]] = {}
        self.hits = 0
        self.misses = 0
        self.lock = asyncio.Lock()
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        async with self.lock:
            if key in self.cache:
                value, timestamp = self.cache[key]
                if time.time() - timestamp < self.ttl:
                    self.hits += 1
                    return value
                else:
                    del self.cache[key]
            
            self.misses += 1
            return None
    
    async def set(self, key: str, value: Any):
        """Set value in cache"""
        async with self.lock:
            # Evict oldest if at max size
            if len(self.cache) >= self.max_size:
                oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k][1])
                del self.cache[oldest_key]
            
            self.cache[key] = (value, time.time())
    
    async def stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        async with self.lock:
            total = self.hits + self.misses
            hit_rate = self.hits / total if total > 0 else 0
            return {
                "size": len(self.cache),
                "max_size": self.max_size,
                "hits": self.hits,
                "misses": self.misses,
                "hit_rate": hit_rate
            }


class NATSConnectionPool:
    """Optimized NATS connection with pooling"""
    
    @staticmethod
    async def create_connection(nats_url: str):
        """Create optimized NATS connection"""
        import nats
        
        nc = await nats.connect(
            servers=[nats_url],
            max_reconnect_attempts=-1,  # Infinite reconnects
            reconnect_time_wait=2,      # 2s between reconnects
            ping_interval=20,            # Ping every 20s
            max_outstanding_pings=3,    # Allow 3 missed pings
            drain_timeout=5,             # 5s drain timeout
            connect_timeout=10,          # 10s connect timeout
            name="ark-optimized",
            verbose=False
        )
        
        logger.info(f"NATS connected with optimized settings: {nats_url}")
        return nc
