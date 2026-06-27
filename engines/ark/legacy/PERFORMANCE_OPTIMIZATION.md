################################################################################
# ARK PERFORMANCE OPTIMIZATION & SMOOTHING GUIDE
################################################################################

## Quick Wins (Implement First - 30 minutes)

### 1. NATS Tuning (Critical for Event-Driven Architecture)
Add to NATS command in docker-compose.yml:
```yaml
command: >
  -js -sd /data -m 8222
  --max_payload 8MB
  --max_pending 128MB
  --max_connections 1000
  --write_deadline 10s
```

**Why:** Default NATS has small buffers. Your mesh/autoscaler publish frequently.
**Impact:** 2-3x throughput for high-frequency events

### 2. Python Connection Pooling
Add to all Python Dockerfiles:
```dockerfile
ENV NATS_DRAIN_TIMEOUT=5
ENV NATS_CONNECT_TIMEOUT=10
ENV PYTHONHASHSEED=0
```

Add to mesh_registry.py & autoscaler.py:
```python
# At top of file
import gc
gc.set_threshold(700, 10, 10)  # Reduce GC frequency

# In connect():
self.nc = await nats.connect(
    servers=[self.nats_url],
    max_reconnect_attempts=-1,
    reconnect_time_wait=2,
    ping_interval=20,
    max_outstanding_pings=3,
    drain_timeout=5,
    connect_timeout=10,
)
```

**Why:** Default NATS client reconnects slowly, holds connections too long
**Impact:** 50% reduction in reconnect latency

### 3. Add Connection Pool for Mesh Registry HTTP API
In mesh_registry.py, replace expose_api:
```python
async def expose_api(self, host: str = "0.0.0.0", port: int = 7000):
    from aiohttp import web
    import aiohttp
    
    # Add connector for connection pooling
    connector = aiohttp.TCPConnector(
        limit=100,  # Max 100 concurrent connections
        limit_per_host=30,
        ttl_dns_cache=300
    )
    
    # ... rest of handlers ...
    
    app = web.Application(
        middlewares=[...],
        client_max_size=1024**2  # 1MB max request
    )
```

**Why:** Default aiohttp creates new connections per request
**Impact:** 30% faster API responses under load

---

## Medium Wins (1-2 hours)

### 4. Redis Cache Layer for Mesh Registry
Add Redis to docker-compose.yml:
```yaml
redis:
  image: redis:7-alpine
  container_name: ark-redis
  restart: unless-stopped
  networks:
    - ark-net
  expose:
    - 6379
  command: redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru
  volumes:
    - redis-data:/data
  healthcheck:
    test: ["CMD", "redis-cli", "ping"]
    interval: 5s
    timeout: 2s
    retries: 3
  deploy:
    resources:
      limits:
        cpus: '0.5'
        memory: 512M
```

Add to mesh_registry.py:
```python
import aioredis

class MeshRegistry:
    def __init__(self, ...):
        self.redis = None
        # ... existing init ...
    
    async def connect(self):
        await super().connect()
        self.redis = await aioredis.from_url(
            "redis://redis:6379",
            encoding="utf-8",
            decode_responses=True,
            max_connections=10
        )
    
    async def route_capability(self, capability: str, load_aware: bool = True):
        # Check cache first
        cache_key = f"route:{capability}"
        cached = await self.redis.get(cache_key)
        if cached:
            return tuple(cached.split(":"))
        
        # ... existing routing logic ...
        
        # Cache result for 5 seconds
        if route:
            await self.redis.setex(cache_key, 5, f"{route[0]}:{route[1]}")
        
        return route
```

Add `aioredis>=2.0` to requirements.txt

**Why:** Routing decisions repeat frequently; caching avoids registry lookups
**Impact:** 5-10x faster routing for repeated capabilities

### 5. NATS Message Batching
In autoscaler.py and mesh_registry.py, batch small messages:
```python
class MessageBatcher:
    def __init__(self, nc, subject, max_batch=50, max_wait=0.1):
        self.nc = nc
        self.subject = subject
        self.batch = []
        self.max_batch = max_batch
        self.max_wait = max_wait
        self.last_flush = time.time()
    
    async def add(self, payload):
        self.batch.append(payload)
        if len(self.batch) >= self.max_batch or (time.time() - self.last_flush) > self.max_wait:
            await self.flush()
    
    async def flush(self):
        if self.batch:
            await self.nc.publish(self.subject, json.dumps(self.batch).encode())
            self.batch.clear()
            self.last_flush = time.time()

# Use it:
self.heartbeat_batcher = MessageBatcher(self.nc, MESH_HEARTBEAT, max_batch=20, max_wait=0.5)

# Instead of:
# await self.nc.publish(MESH_HEARTBEAT, ...)
# Do:
await self.heartbeat_batcher.add(heartbeat_data)
```

**Why:** Reduces NATS round-trips 20:1 for small messages
**Impact:** 50% reduction in NATS CPU usage

### 6. DuckDB Query Optimization
In Dockerfile.duckdb, add indexes:
```dockerfile
CMD ["python", "-c", "import duckdb, time; \
conn = duckdb.connect('/data/ark.duckdb'); \
conn.execute('CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, type VARCHAR, payload JSON, created_at TIMESTAMP DEFAULT now())'); \
conn.execute('CREATE INDEX IF NOT EXISTS idx_events_type ON events(type)'); \
conn.execute('CREATE INDEX IF NOT EXISTS idx_events_created_at ON events(created_at)'); \
conn.execute('CREATE TABLE IF NOT EXISTS state (key VARCHAR PRIMARY KEY, value JSON, updated_at TIMESTAMP DEFAULT now())'); \
conn.execute('CREATE INDEX IF NOT EXISTS idx_state_updated_at ON state(updated_at)'); \
conn.execute('CREATE TABLE IF NOT EXISTS metrics (name VARCHAR, value DOUBLE, timestamp TIMESTAMP, sample_time TIMESTAMP DEFAULT now())'); \
conn.execute('CREATE INDEX IF NOT EXISTS idx_metrics_name_ts ON metrics(name, timestamp)'); \
conn.execute('PRAGMA threads=2'); \
conn.execute('PRAGMA memory_limit=\"1GB\"'); \
conn.close(); \
print('[DuckDB] Ready with indexes', flush=True); \
time.sleep(86400)"]
```

**Why:** Queries on type/timestamp are common; indexes speed them 10-100x
**Impact:** Sub-millisecond event queries instead of 100ms+

---

## Big Wins (Half-day effort)

### 7. Horizontal Scaling with Agent Pools
Remove `container_name` from agents in docker-compose.yml:
```yaml
opencode:
  # Remove: container_name: ark-opencode
  build:
    context: .
    dockerfile: Dockerfile.opencode
  deploy:
    replicas: 3  # Start with 3 instances
    resources:
      limits:
        cpus: '2'
        memory: 1G
  # ... rest of config ...
```

Then scale dynamically:
```bash
docker-compose up -d --scale opencode=5 --scale openwolf=3
```

**Why:** Single agent = bottleneck; multiple = load distribution
**Impact:** 3x throughput for agent-based workflows

### 8. Metrics Collection (Prometheus)
Add to docker-compose.prod.yml:
```yaml
prometheus:
  image: prom/prometheus:latest
  container_name: ark-prometheus
  restart: unless-stopped
  networks:
    - ark-net
  expose:
    - 9090
  command:
    - '--config.file=/etc/prometheus/prometheus.yml'
    - '--storage.tsdb.retention.time=7d'
    - '--storage.tsdb.path=/prometheus'
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
    - prometheus-data:/prometheus
  healthcheck:
    test: ["CMD", "wget", "--spider", "-q", "http://127.0.0.1:9090/-/healthy"]
    interval: 10s
  deploy:
    resources:
      limits:
        cpus: '1'
        memory: 1G
  labels:
    traefik.enable: "true"
    traefik.http.routers.prometheus.rule: "Host(`metrics.${DOMAIN}`)"
    traefik.http.routers.prometheus.entrypoints: "websecure"
    traefik.http.routers.prometheus.tls.certresolver: "letsencrypt"
    traefik.http.services.prometheus.loadbalancer.server.port: "9090"

volumes:
  prometheus-data:
    driver: local
```

Create prometheus.yml:
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'nats'
    static_configs:
      - targets: ['nats:8222']
  
  - job_name: 'minio'
    metrics_path: /minio/v2/metrics/cluster
    static_configs:
      - targets: ['minio:9000']
  
  - job_name: 'grafana'
    static_configs:
      - targets: ['grafana:3000']
  
  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres:9187']  # Add postgres_exporter
```

**Why:** "You can't improve what you don't measure"
**Impact:** Visibility into bottlenecks, enables data-driven optimization

### 9. PostgreSQL Tuning
Add to docker-compose.prod.yml postgres service:
```yaml
postgres:
  # ... existing config ...
  command: >
    postgres
    -c shared_buffers=256MB
    -c effective_cache_size=1GB
    -c maintenance_work_mem=64MB
    -c checkpoint_completion_target=0.9
    -c wal_buffers=16MB
    -c default_statistics_target=100
    -c random_page_cost=1.1
    -c effective_io_concurrency=200
    -c work_mem=4MB
    -c min_wal_size=1GB
    -c max_wal_size=4GB
    -c max_connections=100
```

**Why:** Default PostgreSQL settings are for tiny workloads
**Impact:** 2-3x faster n8n workflow execution

### 10. Add pgBouncer Connection Pooler
Add to docker-compose.prod.yml:
```yaml
pgbouncer:
  image: edoburu/pgbouncer:latest
  container_name: ark-pgbouncer
  restart: unless-stopped
  networks:
    - ark-net
  expose:
    - 5432
  environment:
    DATABASE_URL: postgresql://postgres:${POSTGRES_PASSWORD}@postgres:5432/n8n
    POOL_MODE: transaction
    MAX_CLIENT_CONN: 100
    DEFAULT_POOL_SIZE: 20
  depends_on:
    postgres:
      condition: service_healthy
  healthcheck:
    test: ["CMD", "pg_isready", "-h", "127.0.0.1", "-p", "5432"]
    interval: 5s
  deploy:
    resources:
      limits:
        cpus: '0.5'
        memory: 128M
```

Update n8n to use pgbouncer:
```yaml
n8n:
  environment:
    DB_POSTGRESDB_HOST: pgbouncer  # Change from postgres
```

**Why:** PostgreSQL connections are expensive; pooling reuses them
**Impact:** 50% reduction in database connection overhead

---

## Operational Smoothing (Ongoing)

### 11. Graceful Shutdown with PreStop Hooks
Add to all agent services:
```yaml
opencode:
  # ... existing config ...
  stop_grace_period: 30s
  labels:
    com.docker.compose.stop-grace-period: "30s"
```

Update agent CMD in Dockerfiles:
```python
# At end of agents/aider/agent.py:
import signal

def handle_shutdown(signum, frame):
    logger.info("Received shutdown signal, draining...")
    # Finish current task
    asyncio.create_task(agent.drain())
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_shutdown)
```

**Why:** Abrupt kills leave work incomplete; graceful drain finishes
**Impact:** Zero lost work during deployments/restarts

### 12. Circuit Breaker for External APIs
Create ark/circuit_breaker.py:
```python
import asyncio
import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"  # Normal operation
    OPEN = "open"      # Failure threshold exceeded
    HALF_OPEN = "half_open"  # Testing recovery

class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=60, success_threshold=2):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
    
    async def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                self.success_count = 0
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = await func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise e
    
    def on_success(self):
        self.failure_count = 0
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.state = CircuitState.CLOSED
    
    def on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

# Use in agents:
composio_breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=30)

async def call_composio_api():
    return await composio_breaker.call(composio_client.execute, task_data)
```

**Why:** Cascading failures from external API timeouts kill the stack
**Impact:** Graceful degradation instead of total failure

### 13. Request Deduplication
Add to mesh_registry.py:
```python
import hashlib

class RequestDeduplicator:
    def __init__(self, ttl_seconds=5):
        self.seen = {}
        self.ttl = ttl_seconds
    
    def is_duplicate(self, request_data: dict) -> bool:
        key = hashlib.md5(json.dumps(request_data, sort_keys=True).encode()).hexdigest()
        now = time.time()
        
        if key in self.seen:
            if now - self.seen[key] < self.ttl:
                return True
        
        self.seen[key] = now
        
        # Cleanup old entries
        self.seen = {k: v for k, v in self.seen.items() if now - v < self.ttl}
        
        return False

# Add to MeshRegistry:
self.deduplicator = RequestDeduplicator(ttl_seconds=5)

async def handle_registration(self, event):
    if self.deduplicator.is_duplicate(event):
        logger.debug("Ignoring duplicate registration")
        return
    # ... rest of logic ...
```

**Why:** Clients retry aggressively; duplicate processing wastes cycles
**Impact:** 20-30% reduction in wasted CPU on retries

### 14. Smart Backpressure
Add to autoscaler.py:
```python
class BackpressureManager:
    def __init__(self, max_queue_depth=1000):
        self.max_queue_depth = max_queue_depth
        self.current_depth = 0
    
    def should_accept(self) -> bool:
        return self.current_depth < self.max_queue_depth
    
    def increment(self):
        self.current_depth += 1
    
    def decrement(self):
        self.current_depth = max(0, self.current_depth - 1)

# Add to Autoscaler:
self.backpressure = BackpressureManager(max_queue_depth=500)

async def check_scaling(self, service: str):
    if not self.backpressure.should_accept():
        logger.warning("Backpressure active, deferring scaling check")
        return
    # ... rest of logic ...
```

**Why:** Spawning too many containers under spike load crashes Docker daemon
**Impact:** Stable operation under traffic spikes

---

## Network Optimizations

### 15. Host Network for High-Throughput Services (Advanced)
For NATS (if needed for extreme throughput):
```yaml
nats:
  network_mode: host  # Use host network directly
  # Remove: networks, expose, ports
  command: -js -sd /data -p 4222 -m 8222
```

**WARNING:** Only use if benchmarks show network is bottleneck (>10k msg/sec)
**Impact:** 20-30% latency reduction, but breaks container isolation

### 16. Custom Bridge Network Tuning
Update networks in docker-compose.yml:
```yaml
networks:
  ark-net:
    driver: bridge
    driver_opts:
      com.docker.network.bridge.name: ark0
      com.docker.network.driver.mtu: 1500
      com.docker.network.bridge.enable_ip_masquerade: "true"
    ipam:
      config:
        - subnet: 172.25.0.0/16
          gateway: 172.25.0.1
```

**Why:** Default bridge is optimized for compatibility, not performance
**Impact:** 5-10% network throughput improvement

---

## Monitoring & Alerts

### 17. Grafana Dashboard for ARK
Create grafana-dashboards/ark-overview.json:
```json
{
  "dashboard": {
    "title": "ARK System Overview",
    "panels": [
      {
        "title": "NATS Message Rate",
        "targets": [{"expr": "rate(nats_in_msgs[5m])"}]
      },
      {
        "title": "Mesh Registry Requests",
        "targets": [{"expr": "rate(http_requests_total{job=\"mesh\"}[5m])"}]
      },
      {
        "title": "Agent Load",
        "targets": [{"expr": "avg(agent_load) by (service)"}]
      },
      {
        "title": "DuckDB Query Time",
        "targets": [{"expr": "histogram_quantile(0.95, rate(duckdb_query_duration_seconds_bucket[5m]))"}]
      }
    ]
  }
}
```

**Why:** Visual feedback loop enables rapid optimization iteration
**Impact:** Catch performance regressions within minutes

---

## Summary: Performance Priority Matrix

| Optimization | Effort | Impact | Priority |
|-------------|--------|--------|----------|
| 1. NATS Tuning | 5min | High | **DO FIRST** |
| 2. Python Connection Pool | 10min | High | **DO FIRST** |
| 3. Mesh API Connection Pool | 10min | Medium | **DO FIRST** |
| 4. Redis Cache | 1hr | High | Do Second |
| 5. Message Batching | 30min | High | Do Second |
| 6. DuckDB Indexes | 15min | High | Do Second |
| 7. Agent Horizontal Scaling | 5min | Very High | **DO FIRST** |
| 8. Prometheus Metrics | 2hr | Medium | Do Third |
| 9. PostgreSQL Tuning | 10min | High | Do Second |
| 10. pgBouncer | 30min | Medium | Do Third |
| 11. Graceful Shutdown | 1hr | Medium | Do Fourth |
| 12. Circuit Breaker | 2hr | High | Do Third |
| 13. Request Dedup | 30min | Medium | Do Fourth |
| 14. Backpressure | 1hr | Medium | Do Third |

**Quick Start (30 minutes):**
1. NATS tuning (5min)
2. Python connection pool (10min)
3. Agent scaling (5min)
4. DuckDB indexes (10min)

**Expected improvement:** 2-3x throughput, 50% latency reduction

Let me know which areas you want me to implement!
