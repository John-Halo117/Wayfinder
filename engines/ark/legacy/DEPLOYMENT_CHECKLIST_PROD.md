################################################################################
# ARK PRODUCTION DEPLOYMENT CHECKLIST
################################################################################

## Pre-Deployment (72 hours before)

### Infrastructure & DNS
- [ ] Server provisioned (8+ cores, 16GB+ RAM, 100GB+ SSD)
- [ ] DNS A record created and propagating for DOMAIN
- [ ] Firewall configured: only 80/443 inbound, all others closed
- [ ] SSL/TLS certificate provider selected (Let's Encrypt recommended)
- [ ] Backup storage configured and tested (S3, NAS, cloud, etc.)
- [ ] Monitoring/alerting infrastructure ready
- [ ] Log aggregation setup (if required by compliance)

### Credentials & Secrets
- [ ] GRAFANA_PASSWORD generated: `openssl rand -base64 32`
- [ ] MEILISEARCH_KEY generated: `openssl rand -base64 32`
- [ ] MINIO_USER set (NOT "minioadmin")
- [ ] MINIO_PASSWORD generated: `openssl rand -base64 32`
- [ ] N8N_DB_PASSWORD generated: `openssl rand -base64 32`
- [ ] POSTGRES_PASSWORD generated: `openssl rand -base64 32`
- [ ] All secrets stored in .env.prod (mode 600)
- [ ] No CHANGE_ME values remaining in .env.prod

### Docker & Deployment
- [ ] Docker daemon updated to latest stable
- [ ] docker-compose updated to latest
- [ ] All source code committed and tagged (git tag v1.0.0)
- [ ] Docker images built and tested locally
- [ ] .dockerignore verified (no secrets included)
- [ ] Dockerfile.prod or similar created (if custom prod configs)

### Testing & Validation
- [ ] docker-compose config validates without errors
- [ ] All Dockerfiles build successfully
- [ ] Services start without errors: docker-compose up -d
- [ ] Health checks pass: docker-compose ps (all "healthy")
- [ ] Services can communicate (internal network)
- [ ] Logs reviewed for errors: docker-compose logs

## 24 Hours Before Deployment

### Final Checks
- [ ] Create .env.prod from .env.example template
- [ ] Review PRODUCTION_GUIDE.md line-by-line
- [ ] Run deploy-prod.sh in dry-run mode (if implemented)
- [ ] Verify all env vars load correctly
- [ ] Test database migrations (if any)
- [ ] Backup existing data if migrating from dev

### Communication
- [ ] Notify stakeholders of deployment window
- [ ] Schedule post-deployment verification meeting
- [ ] Create incident response contact list
- [ ] Prepare rollback plan (document)

## Deployment Day (Execution)

### Pre-Deployment (1 hour)
- [ ] ssh into production server
- [ ] Verify internet connectivity: `ping 8.8.8.8`
- [ ] Verify disk space: `df -h` (should be >50% free)
- [ ] Stop any existing services (if upgrading)
- [ ] Create timestamped backup directory: `backup-$(date -u +%Y-%m-%dT%H-%M-%SZ)`

### Deployment (run in order)
1. [ ] Pull latest code: `git pull origin main` (or checkout tag)
2. [ ] Copy .env.prod and verify permissions: `ls -la .env.prod`
3. [ ] Run pre-flight checks:
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml config > /dev/null
   echo "docker-compose config: $?"
   ```
4. [ ] Pull latest images:
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml pull
   ```
5. [ ] Start stack with explicit compose files:
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --pull always
   ```
6. [ ] Monitor startup (5-10 minutes):
   ```bash
   watch -n 2 'docker-compose ps'
   # Watch until all containers show "healthy" or "up"
   ```
7. [ ] Tail logs for errors:
   ```bash
   docker-compose logs -f --tail=50
   # Look for ERROR, FATAL, panic keywords
   ```

### Post-Deployment (30 minutes)

#### Health Checks
- [ ] All services healthy: `docker-compose ps` (all show "healthy")
- [ ] NATS reachable: `docker-compose exec nats nats server info`
- [ ] PostgreSQL responding: `docker-compose exec postgres psql -U postgres -c "SELECT 1"`
- [ ] n8n accessible: `curl -I https://n8n.${DOMAIN}` (200 OK)
- [ ] Grafana accessible: `curl -I https://grafana.${DOMAIN}` (200 OK)
- [ ] MinIO accessible: `curl -I https://minio.${DOMAIN}` (200 OK)

#### Functional Tests
- [ ] n8n can connect to PostgreSQL (check in UI)
- [ ] Grafana shows dashboards without errors
- [ ] MinIO console accessible and login works (username/password set)
- [ ] NATS has running subjects: `docker-compose exec nats nats sub -all`
- [ ] Mesh registry responding: `docker-compose exec mesh-registry python -c "import socket; socket.create_connection(('mesh-registry', 7000), timeout=2)"`

#### Monitoring Setup
- [ ] Grafana data sources configured
- [ ] Dashboard(s) created and displaying data
- [ ] Alert thresholds set:
  - CPU > 80%
  - Memory > 90%
  - Disk > 85%
  - Service down (health check failed)

#### Security Verification
- [ ] TLS certificate valid (check in browser or: openssl s_client -connect ${DOMAIN}:443)
- [ ] Firewall rules verified (only 80/443 public)
- [ ] Internal services NOT accessible on WAN (nats:4222, mesh:7000, etc.)
- [ ] .env.prod not world-readable: `ls -l .env.prod` shows 600
- [ ] No default credentials in use (admin/admin, minioadmin, etc.)

#### Backup & Disaster Recovery
- [ ] First backup taken successfully
- [ ] Backup files verified (not empty): `ls -lh backup-*/`
- [ ] Restore test performed (simulate recovery):
  ```bash
  # Create test database from backup
  docker-compose exec -T postgres psql -U postgres -c "DROP DATABASE IF EXISTS n8n_test"
  docker-compose exec -T postgres psql -U postgres -c "CREATE DATABASE n8n_test"
  gunzip < backup-n8n.sql.gz | docker-compose exec -T postgres psql -U postgres -d n8n_test
  # Verify data: docker-compose exec postgres psql -U postgres -d n8n_test -c "SELECT COUNT(*) FROM workflows"
  ```
- [ ] Backup storage accessible and synced

## Post-Deployment (Next 24 Hours)

### Monitoring & Stability
- [ ] Monitor for errors: `docker-compose logs --since 1h | grep -i error`
- [ ] Check resource usage doesn't spike: `docker stats --no-stream`
- [ ] Verify data persistence (create test records, restart container, verify data still there)
- [ ] Test failover (stop one service, verify system still works)
- [ ] Review all container restart counts: `docker-compose ps` (should be "0")

### User Acceptance Testing (UAT)
- [ ] n8n workflows execute successfully
- [ ] Grafana dashboards display expected data
- [ ] Search functionality works (Meilisearch)
- [ ] File storage works (MinIO)
- [ ] User access controls enforced (if using Traefik auth)

### Documentation
- [ ] Document actual deployment start/end times
- [ ] Record all credentials in secure password manager
- [ ] Note any deviations from plan
- [ ] Update runbooks with actual commands used
- [ ] Create incident response procedures

### Cleanup
- [ ] Remove old backup files if space needed
- [ ] Clean up temporary test data
- [ ] Archive deployment logs

## Rollback Plan (If Issues Found)

### Immediate (first 30 minutes)
1. [ ] Stop deployed stack: `docker-compose -f docker-compose.yml -f docker-compose.prod.yml down`
2. [ ] Restore from backup (if data corrupted)
3. [ ] Restart previous version (if available)

### Database Rollback (if data corrupted)
```bash
docker-compose exec -T postgres psql -U postgres -d n8n -c "DROP TABLE IF EXISTS workflows CASCADE"
gunzip < backup-n8n.sql.gz | docker-compose exec -T postgres psql -U postgres -d n8n
docker-compose restart n8n
```

### Full Rollback (if critical failure)
1. Stop ARK: `docker-compose down -v` (WARNING: removes data)
2. Restore all volumes from backup
3. Restore .env.prod from backup
4. Deploy previous version by checking out old git tag

### Communication
- [ ] Notify stakeholders immediately of issue
- [ ] Status updates every 15 minutes
- [ ] Incident timeline documented
- [ ] Remediation plan approved before resuming

## One Week Post-Deployment

### Stability Review
- [ ] System uptime ≥ 99.9% (< 6 seconds downtime)
- [ ] No OOMKilled containers (check docker-compose logs)
- [ ] No restart loops (docker-compose ps shows 0-1 restarts)
- [ ] Backup jobs completed successfully

### Performance Review
- [ ] Response times acceptable (< 200ms median)
- [ ] Resource usage within expected limits
- [ ] No memory leaks detected
- [ ] Database query performance acceptable

### Security Review
- [ ] All TLS certificates valid and auto-renewing
- [ ] Access logs reviewed for suspicious activity
- [ ] No failed login attempts from unknown IPs
- [ ] Backup encryption verified

### User Feedback
- [ ] Gather feedback from users/stakeholders
- [ ] Document issues and schedule fixes
- [ ] Performance/usability improvements identified

## One Month Post-Deployment

### Long-Term Monitoring
- [ ] Review Grafana metrics over full month
- [ ] Capacity planning: will resources suffice for 6/12 months?
- [ ] Cost optimization: any unnecessary services/resources?
- [ ] Security updates applied
- [ ] Database maintenance: VACUUM, ANALYZE run

### Disaster Recovery Drill
- [ ] Full backup restore test (in separate environment if possible)
- [ ] Failover scenarios tested
- [ ] RTO/RPO targets verified
- [ ] Incident response procedures reviewed

### Documentation Update
- [ ] Runbooks updated with lessons learned
- [ ] Troubleshooting guide expanded
- [ ] Architecture diagrams current
- [ ] Credentials rotated (if policy requires)

---

## Sign-Off

- Deployed By: ____________________   Date: ________
- Verified By: ____________________   Date: ________
- Approved By: ____________________   Date: ________

Notes/Issues:
________________________________________________________________________
________________________________________________________________________
________________________________________________________________________
