################################################################################
# ARK PRODUCTION QUICK REFERENCE
################################################################################

## Emergency Commands

### Check Status
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml ps
docker-compose logs -f --tail=100
docker stats
```

### Restart Everything
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml restart
```

### Restart One Service
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml restart n8n
```

### Full Redeploy (with latest images)
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml pull
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --no-deps <service>
```

### Check Certificate Status
```bash
docker-compose logs traefik | grep -i cert
# Or:
openssl s_client -connect n8n.${DOMAIN}:443 -showcerts 2>/dev/null | grep -A 2 "notBefore\|notAfter"
```

### Database Backup
```bash
docker-compose exec -T postgres pg_dump -U postgres n8n | gzip > backup-$(date -u +%s).sql.gz
```

### Database Restore
```bash
gunzip < backup-1234567890.sql.gz | docker-compose exec -T postgres psql -U postgres -d n8n
```

---

## Port Reference

| Service | Internal Port | External (Prod) | Purpose |
|---------|---------------|-----------------|---------|
| NATS | 4222 | ✗ (internal) | Event broker |
| Mesh Registry | 7000 | ✗ (internal) | Service mesh |
| Autoscaler | 7001 | ✗ (internal) | Container scaling |
| Agents (opencode/openwolf) | (none) | ✗ (internal) | Intelligence layer |
| DuckDB | 8000 | ✗ (internal) | Database |
| n8n | 5678 | https://n8n.${DOMAIN} | Workflows |
| Grafana | 3000 | https://grafana.${DOMAIN} | Dashboards |
| Meilisearch | 7700 | https://search.${DOMAIN} | Search |
| MinIO (S3) | 9000 | https://s3.${DOMAIN} | Object storage |
| MinIO (Console) | 9001 | https://minio.${DOMAIN} | S3 console |
| Traefik (API) | 8080 | https://traefik.${DOMAIN} | Reverse proxy |
| PostgreSQL | 5432 | ✗ (internal) | Database |

---

## Environment Variables (Prod Required)

```
DOMAIN=              # e.g., ark.example.com
GRAFANA_PASSWORD=    # 32+ chars from `openssl rand -base64 32`
MEILISEARCH_KEY=     # 32+ chars from `openssl rand -base64 32`
MINIO_USER=          # Custom username (NOT "minioadmin")
MINIO_PASSWORD=      # 32+ chars from `openssl rand -base64 32`
N8N_DB_PASSWORD=     # 32+ chars from `openssl rand -base64 32`
POSTGRES_PASSWORD=   # 32+ chars from `openssl rand -base64 32`
LETSENCRYPT_EMAIL=   # Your email for cert notifications
TZ=                  # e.g., UTC or America/New_York
LOG_LEVEL=           # debug, info, warn, error (default: info)
```

Generate strong passwords:
```bash
openssl rand -base64 32
```

---

## Common Errors & Fixes

### "Connection refused" on 4222
**Problem:** Trying to connect to NATS on public port (was exposed in dev, not in prod)
**Fix:** NATS is internal only. Use `nats://nats:4222` from other containers only.

### "Certificate not valid" on HTTPS
**Problem:** Let's Encrypt cert not issued yet
**Fix:** Check traefik logs: `docker-compose logs traefik | grep acme`
Wait 30s-5min for DNS propagation and challenge completion.

### n8n can't connect to database
**Problem:** `N8N_DB_PASSWORD` missing or incorrect
**Fix:** 
1. Verify .env.prod has password set
2. Check PostgreSQL is healthy: `docker-compose ps postgres`
3. Test connection: `docker-compose exec postgres psql -U postgres -c "SELECT 1"`

### MinIO bucket access denied
**Problem:** Wrong credentials or bucket doesn't exist
**Fix:**
1. Verify MINIO_USER/MINIO_PASSWORD in .env.prod
2. Create bucket: `docker-compose exec minio mc mb minio/ark-data`
3. Set permissions: `docker-compose exec minio mc policy set public minio/ark-data`

### Out of disk space
**Problem:** `/var/lib/docker/volumes` full
**Fix:**
1. Check usage: `docker system df`
2. Remove unused images: `docker image prune -a`
3. Remove unused volumes: `docker volume prune` (CAREFUL!)
4. Check log rotation: `du -sh /var/lib/docker/containers/*/`

### Services restarting repeatedly
**Problem:** Container exits, then restarts (infinite loop)
**Fix:**
1. Check logs: `docker-compose logs -f <service>`
2. Look for ERROR, FATAL, panic
3. Fix root cause (missing dependency, bad config, OOM)
4. Then restart: `docker-compose restart <service>`

### High memory usage
**Problem:** Container using more than limit
**Fix:**
1. Check which: `docker stats`
2. Review logs for memory leaks
3. Increase limit in docker-compose.yml if necessary
4. Restart container: `docker-compose restart <service>`

### Grafana dashboards empty
**Problem:** No data sources configured
**Fix:**
1. Log into Grafana (https://grafana.${DOMAIN})
2. Go to Configuration → Data Sources
3. Add NATS or other metrics source
4. Create new dashboard

---

## Health Check Status

Command:
```bash
docker-compose ps
```

Expected output (all healthy or up):
```
NAME                  STATUS              PORTS
ark-nats              healthy (10s)       
ark-postgres          healthy (5s)        
ark-traefik           healthy (5s)        
ark-mesh              Up (healthy)        
ark-autoscaler        Up (healthy)        
ark-opencode          Up (healthy)        
ark-n8n               healthy (10s)       
ark-grafana           healthy (10s)       
ark-meilisearch       healthy (5s)        
ark-minio             healthy (5s)        
```

If "unhealthy" or "exited":
```bash
docker-compose logs <service>  # See error details
docker-compose restart <service>  # Restart it
```

---

## Performance Baselines

**Normal Resource Usage (full stack idle):**
- NATS: 5-10MB RAM, <1% CPU
- PostgreSQL: 20-30MB RAM, <1% CPU
- Traefik: 15-25MB RAM, <1% CPU
- n8n: 100-200MB RAM, <5% CPU
- Grafana: 50-100MB RAM, <1% CPU
- MinIO: 100-150MB RAM, <1% CPU

**Total Idle:** ~300-500MB RAM, <10% CPU

**Under Load (1000 requests/sec):**
- n8n: 300-500MB RAM, 50-80% CPU
- PostgreSQL: 100-200MB RAM, 40-60% CPU
- Traefik: 50-100MB RAM, 10-20% CPU

---

## Monitoring Queries (in Prometheus/Grafana)

### CPU Usage
```
100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

### Memory Usage
```
node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes * 100
```

### Disk Free
```
node_filesystem_avail_bytes{fstype!~"tmpfs|fuse.lxcfs"} / 1024^3
```

### Container Restarts
```
increase(container_last_seen{name!=""}[1h]) > 0
```

---

## Scaling Up (for high traffic)

### Add more agents (opencode/openwolf):
```bash
# Remove container_name from opencode in docker-compose.yml
# Then:
docker-compose up -d --scale opencode=3 opencode
```

### Increase resource limits:
Edit docker-compose.yml:
```yaml
deploy:
  resources:
    limits:
      cpus: '4'      # From 2
      memory: 2G     # From 1G
```

Then restart:
```bash
docker-compose up -d --no-deps <service>
```

### Add caching layer:
Add Redis to docker-compose.prod.yml for Grafana caching

---

## Maintenance Window Procedure

### 1. Notify users (5min before)
```bash
# Display message in Grafana, n8n, etc.
# Schedule maintenance window
```

### 2. Stop ingestion gracefully
```bash
docker-compose pause opencode openwolf composio
# Allows existing workflows to complete
sleep 30
```

### 3. Stop services
```bash
docker-compose stop n8n grafana
```

### 4. Perform maintenance
```bash
# Database migration, config change, etc.
docker-compose exec postgres psql -U postgres n8n < migration.sql
```

### 5. Restart services
```bash
docker-compose up -d
```

### 6. Resume agents
```bash
docker-compose unpause opencode openwolf composio
```

### 7. Verify health
```bash
docker-compose ps  # All healthy?
docker-compose logs --tail=20  # Any errors?
```

---

## Backup Retention Policy

**Recommended:**
- Hourly: Keep last 24 hours
- Daily: Keep last 30 days
- Weekly: Keep last 12 weeks
- Monthly: Keep last 12 months

**Example cron job:**
```bash
0 */1 * * * /usr/local/bin/ark-backup-hourly.sh
0 2 * * * /usr/local/bin/ark-backup-daily.sh
0 3 * * 0 /usr/local/bin/ark-backup-weekly.sh
0 4 1 * * /usr/local/bin/ark-backup-monthly.sh
```

---

## Upgrade Procedure

### 1. Test in staging environment first
### 2. Backup production database
```bash
docker-compose exec -T postgres pg_dump -U postgres n8n | gzip > backup-pre-upgrade.sql.gz
```

### 3. Pull latest images
```bash
docker-compose pull
```

### 4. Update one service at a time
```bash
docker-compose up -d --no-deps n8n
docker-compose logs -f n8n  # Watch for errors
```

### 5. Verify health
```bash
docker-compose ps  # All healthy?
```

### 6. Test functionality
```bash
curl -I https://n8n.${DOMAIN}  # Should be 200 OK
```

---

## Support Resources

- Production Guide: `PRODUCTION_GUIDE.md`
- Deployment Checklist: `DEPLOYMENT_CHECKLIST_PROD.md`
- Fixes Summary: `PRODUCTION_FIXES_SUMMARY.md`
- Logs: `docker-compose logs -f <service>`
- Health: `docker-compose ps`
- Docker Docs: https://docs.docker.com/compose/
