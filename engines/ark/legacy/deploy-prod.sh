#!/bin/bash
################################################################################
# ARK Production Deployment Script
# Pre-deployment validation and safety checks
# Usage: bash deploy-prod.sh
################################################################################

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

################################################################################
# 1. CHECK ENVIRONMENT
################################################################################

log_info "Checking production environment..."

if [ ! -f .env.prod ]; then
    log_error ".env.prod not found. Copy from .env.example and update values."
    exit 1
fi

# Source .env.prod but don't export it
set -a
source .env.prod 2>/dev/null || true
set +a

# Check required variables
required_vars=("DOMAIN" "GRAFANA_PASSWORD" "MEILISEARCH_KEY" "MINIO_USER" "MINIO_PASSWORD" "N8N_DB_PASSWORD")
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        log_error "Missing required variable: $var"
        exit 1
    fi
done

log_success "All required environment variables set"

################################################################################
# 2. VALIDATE FILES
################################################################################

log_info "Validating configuration files..."

# Check docker-compose files exist
for file in docker-compose.yml docker-compose.prod.yml init-db.sql; do
    if [ ! -f "$file" ]; then
        log_error "Missing file: $file"
        exit 1
    fi
done

log_success "All configuration files present"

################################################################################
# 3. VALIDATE DOCKER COMPOSE CONFIG
################################################################################

log_info "Validating docker-compose configuration..."

if ! docker-compose -f docker-compose.yml -f docker-compose.prod.yml config > /dev/null 2>&1; then
    log_error "docker-compose configuration invalid"
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml config
    exit 1
fi

log_success "docker-compose configuration valid"

################################################################################
# 4. CHECK DOCKER DAEMON
################################################################################

log_info "Checking Docker daemon..."

if ! docker ps > /dev/null 2>&1; then
    log_error "Docker daemon not running or not accessible"
    exit 1
fi

log_success "Docker daemon running"

################################################################################
# 5. CHECK DISK SPACE
################################################################################

log_info "Checking disk space..."

available=$(df -BG . | awk 'NR==2 {print $4}' | sed 's/G//')
if [ "$available" -lt 50 ]; then
    log_warn "Less than 50GB available. Recommended: 100GB+ for production"
fi

log_success "Disk space check passed (${available}GB available)"

################################################################################
# 6. VALIDATE PORTS
################################################################################

log_info "Checking ports..."

for port in 80 443; do
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        log_warn "Port $port already in use"
    fi
done

log_success "Port check passed"

################################################################################
# 7. SET .env.prod PERMISSIONS
################################################################################

log_info "Setting .env.prod permissions..."
chmod 600 .env.prod
log_success ".env.prod permissions set to 600"

################################################################################
# 8. BACKUP EXISTING DATA (optional)
################################################################################

log_info "Checking for existing volumes to back up..."

if docker volume ls | grep -q ark; then
    read -p "Existing ARK volumes found. Create backup? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        backup_dir="./backups/$(date -u +%Y-%m-%dT%H-%M-%SZ)"
        mkdir -p "$backup_dir"
        
        for volume in $(docker volume ls -q | grep ark); do
            log_info "Backing up volume: $volume"
            docker run --rm -v "$volume:/data" -v "$backup_dir:/backup" \
                alpine tar czf "/backup/${volume}.tar.gz" -C /data . 2>/dev/null || true
        done
        
        log_success "Backup created at $backup_dir"
    fi
fi

################################################################################
# 9. PULL LATEST IMAGES
################################################################################

log_info "Pulling latest Docker images..."

docker-compose -f docker-compose.yml -f docker-compose.prod.yml pull --quiet 2>&1 | grep -v "Pulling\|Downloaded\|Digest\|Status" || true

log_success "Docker images pulled"

################################################################################
# 10. FINAL CHECKLIST
################################################################################

log_info "Final production checklist:"
echo ""
echo "Deployment will start with the following configuration:"
echo "  Domain:           ${DOMAIN}"
echo "  Timezone:         ${TZ}"
echo "  Log Level:        ${LOG_LEVEL}"
echo "  n8n Database:     ${N8N_DB_HOST}:${N8N_DB_PORT}/${N8N_DB_NAME}"
echo "  Grafana Password: ****** (${#GRAFANA_PASSWORD} chars)"
echo "  Meilisearch Key:  ****** (${#MEILISEARCH_KEY} chars)"
echo "  MinIO User/Pass:  *****/****** (${#MINIO_USER}/${#MINIO_PASSWORD} chars)"
echo ""
echo "Verify above is correct before proceeding."
echo ""

read -p "Start production deployment? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    log_warn "Deployment cancelled"
    exit 0
fi

################################################################################
# 11. DEPLOY
################################################################################

log_info "Starting ARK production stack..."

docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --pull always

log_success "Docker Compose stack started"

################################################################################
# 12. WAIT FOR SERVICES
################################################################################

log_info "Waiting for services to become healthy..."

services=("ark-nats" "ark-postgres" "ark-traefik" "ark-n8n")
max_attempts=60
attempt=0

while [ $attempt -lt $max_attempts ]; do
    all_healthy=true
    
    for service in "${services[@]}"; do
        if ! docker ps --format "{{.Names}}" | grep -q "^${service}$"; then
            all_healthy=false
            break
        fi
        
        status=$(docker inspect -f '{{.State.Health.Status}}' "$service" 2>/dev/null || echo "none")
        if [ "$status" != "healthy" ] && [ "$status" != "none" ]; then
            all_healthy=false
            echo -n "."
        fi
    done
    
    if $all_healthy; then
        break
    fi
    
    sleep 2
    ((attempt++))
done

if [ $attempt -ge $max_attempts ]; then
    log_warn "Services took longer than expected to become healthy"
    log_info "Check with: docker-compose logs"
else
    log_success "All services healthy"
fi

################################################################################
# 13. DISPLAY STATUS
################################################################################

log_info "Deployment complete! Status:"
echo ""
docker-compose ps
echo ""

log_info "Access services at:"
echo "  Traefik Dashboard:  https://traefik.${DOMAIN}"
echo "  n8n:                https://n8n.${DOMAIN}"
echo "  Grafana:            https://grafana.${DOMAIN} (admin/${GRAFANA_PASSWORD:0:8}****)"
echo "  MinIO Console:      https://minio.${DOMAIN}"
echo "  Search (Meili):     https://search.${DOMAIN}"
echo ""

log_warn "IMPORTANT:"
echo "  1. First-time setup: Change all default passwords"
echo "  2. Test backups: docker-compose exec postgres pg_dump -U postgres n8n | gzip > backup.sql.gz"
echo "  3. Set up monitoring: Configure Grafana data sources"
echo "  4. Monitor logs: docker-compose logs -f"
echo ""

log_success "ARK production deployment ready"
