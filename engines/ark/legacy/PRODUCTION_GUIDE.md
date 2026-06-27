################################################################################
# ARK PRODUCTION SECURITY & OPERATIONS GUIDE
################################################################################

## Port Changes (from dev to prod)

### Removed Public Ports:
- NATS: 4222, 6222, 8222 (internal only via `expose`, not `ports`)
- Mesh Registry: 7000 (internal only)
- Autoscaler: 7001 (internal only)
- All agents: no ports (internal only)
- DuckDB: 8000 (internal only)

### Reverse Proxy Only (Traefik):
- n8n:           port 5678 → https://n8n.${DOMAIN}
- Grafana:       port 3000 → https://grafana.${DOMAIN}
- Meilisearch:   port 7700 → https://search.${DOMAIN}
- MinIO:         port 9000/9001 → https://s3.${DOMAIN} and https://minio.${DOMAIN}

### Public Ports (Traefik listens):
- 80 (HTTP → auto-redirects to 443)
- 443 (HTTPS with Let's Encrypt TLS)

## Environment Variable Changes

### Security:
- All default credentials removed (no more "admin" or "minioadmin")
- NATS: no longer exposed to WAN
- All services behind authentication layer (Traefik + Let's Encrypt)

### New Requirements:
```bash
# Generate strong passwords with:
openssl rand -base64 32

# Set these in .env.prod:
N8N_DB_PASSWORD=          # PostgreSQL password (32+ chars)
GRAFANA_PASSWORD=         # Grafana admin password (32+ chars)
MEILISEARCH_KEY=          # Search API key (32+ chars)
MINIO_USER=               # S3 root user (unique)
MINIO_PASSWORD=           # S3 root password (32+ chars)
POSTGRES_PASSWORD=        # PostgreSQL root password (32+ chars)
COMPOSIO_API_KEY=         # Optional: Composio integration
```

### Removed Dev Variables:
- NATS no longer needs authentication (it's internal-only now)
- REDIS_PASSWORD (not in use; was for Authelia)

## Resource Limits Added

All services now have CPU/memory limits:

```yaml
deploy:
  resources:
    limits:      # Hard cap; container stops if exceeded
      cpus: '2'
      memory: 1G
    reservations: # Requested; scheduler guarantees this
      cpus: '0.5'
      memory: 256M
```

This prevents runaway containers from crashing the host.

### Recommended Host Sizing:
- CPU: 8 cores minimum (4 recommended minimum)
- RAM: 16GB minimum (32GB recommended)
- Disk: 100GB+ with SSD for databases

## Production Database Setup

### PostgreSQL (newly required):
```bash
# Create n8n database and user
createdb n8n
createuser -P n8n  # Prompted for password

# Grant permissions
psql -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE n8n TO n8n"

# Or use docker-compose service (included in docker-compose.prod.yml)
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d postgres
```

### Backup PostgreSQL:
```bash
# Full backup
docker-compose exec postgres pg_dump -U postgres -d n8n | gzip > backup-n8n.sql.gz

# Restore from backup
gunzip < backup-n8n.sql.gz | docker-compose exec -T postgres psql -U postgres -d n8n
```

## Deployment Steps

### 1. Prepare production environment:
```bash
cp .env.example .env.prod
# Edit .env.prod with real values (see .env.prod for instructions)

# Verify it's production-safe
chmod 600 .env.prod  # Protect from world-readable
```

### 2. Run pre-deployment checks:
```bash
bash deploy-prod.sh  # Validates everything before starting
```

### 3. Start production stack:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --pull always
```

### 4. Verify services are healthy:
```bash
docker-compose ps
docker-compose logs -f --tail=20
```

### 5. Access services (all on HTTPS now):
```
https://n8n.${DOMAIN}       (Workflow automation)
https://grafana.${DOMAIN}   (Dashboards & monitoring)
https://search.${DOMAIN}    (Meilisearch)
https://minio.${DOMAIN}     (S3 object storage)
https://traefik.${DOMAIN}   (Reverse proxy dashboard)
```

## Security Best Practices

### 1. Network Isolation:
- All internal services on 172.25.0.0/16
- Only Traefik exposed to WAN (ports 80/443)
- Firewall rules: only 80/443 from world, everything else closed

### 2. Secrets Management:
- Never commit .env.prod to git (.gitignore includes .env*)
- Rotate passwords every 90 days
- Use environment variables, not config files
- Consider external secret manager (HashiCorp Vault, AWS Secrets Manager)

### 3. TLS/SSL:
- Let's Encrypt certificates auto-renewed (Traefik handles)
- All traffic encrypted in transit
- Certificate files in traefik-acme volume (back this up!)

### 4. Database Security:
- PostgreSQL only listens on internal network (172.25.0.0/16)
- Strong passwords enforced (32+ chars)
- SQL injection prevention: use prepared statements
- Regular backups encrypted

### 5. Container Security:
- All services run as non-root users (ark user in custom images)
- Read-only volumes where possible (./ark:/app/ark:ro)
- No privileged containers except Docker socket access (autoscaler)
- Resource limits prevent DoS

### 6. Monitoring & Logging:
- All containers use json-file driver (max 10MB, 3 files)
- Grafana tracks resource usage
- Set up AlertManager for critical events
- Log aggregation: ELK stack, Loki, or CloudWatch

### 7. Backup & Disaster Recovery:
```bash
# Daily backup script (cron)
#!/bin/bash
DATE=$(date -u +%Y-%m-%d)
mkdir -p /backups/$DATE

# Backup all volumes
for volume in $(docker volume ls -q | grep ark); do
    docker run --rm -v $volume:/data -v /backups/$DATE:/backup \
        alpine tar czf /backup/${volume}-${DATE}.tar.gz -C /data .
done

# Backup PostgreSQL
docker-compose exec -T postgres pg_dump -U postgres n8n | \
    gzip > /backups/$DATE/n8n-${DATE}.sql.gz

# Sync to S3 or remote storage
aws s3 sync /backups/$DATE s3://your-backup-bucket/$DATE/
```

### 8. Update & Patching:
```bash
# Check for updates
docker-compose pull --dry-run

# Update services (zero-downtime)
docker-compose pull
docker-compose up -d --no-deps

# Verify health
docker-compose ps
docker-compose logs -f
```

## Troubleshooting

### Services stuck in unhealthy state:
```bash
docker-compose logs <service>  # Check logs
docker-compose restart <service>
```

### Certificate renewal issues:
```bash
docker-compose logs traefik | grep acme
# Traefik auto-renews 30 days before expiry
```

### Out of disk space:
```bash
docker system df  # Check usage
docker system prune -a --volumes  # Clean unused images/volumes (CAREFUL!)
```

### PostgreSQL connection failures:
```bash
docker-compose exec postgres psql -U postgres -c "SELECT 1"
# Verify N8N_DB_* variables match in .env.prod
```

### MinIO bucket access:
```bash
docker-compose exec minio mc mb minio/ark-data
docker-compose exec minio mc policy set public minio/ark-data
```

## Compliance & Auditing

### Security Checklist:
- [ ] All passwords 32+ characters and unique
- [ ] .env.prod has 600 permissions
- [ ] TLS certificates valid (not self-signed)
- [ ] Firewall only allows 80/443 from WAN
- [ ] Regular backups tested and restored
- [ ] Monitoring/alerting configured
- [ ] Service accounts created for integrations (not root)
- [ ] Audit logging enabled (check container logs)
- [ ] GDPR/compliance data retention policies defined
- [ ] Disaster recovery plan documented and tested

### Logging & Auditing:
```bash
# View all container logs
docker-compose logs --since 1h

# Export logs for compliance
docker-compose logs > ark-logs-$(date -u +%Y-%m-%d).txt

# Preserve audit trails
docker inspect <container> | grep -A 10 LogPath
```

## Performance Tuning

### For high traffic (1000+ RPS):
1. Increase Meilisearch resources: 4 CPU, 2GB RAM
2. Add n8n replicas: `docker-compose up -d --scale n8n=3`
3. Enable PostgreSQL query cache
4. Add Redis cache layer for Grafana
5. Implement CDN for static assets via Traefik

### Monitoring bottlenecks:
```bash
docker stats  # Real-time resource usage
docker-compose top <service>  # Process-level details
```

## Contact & Support

For production issues:
1. Check logs first: `docker-compose logs -f`
2. Verify all env vars set: `docker-compose config | grep GRAFANA_PASSWORD`
3. Test connectivity: `docker-compose exec minio mc admin info`
4. Review health checks: `docker-compose ps`
