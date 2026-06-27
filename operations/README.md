# Operations

Operations contains runtime infrastructure.

Examples include deployment, provisioning, monitoring, observability,
maintenance, backups, disaster recovery, migrations, and workflows.
## Infrastructure Repository Boundary

The future `wayfinder-infra` repository implements deployment operations for Wayfinder. It may own Docker Compose, host directory layout, monitoring deployment, backups, recovery, and environment configuration. It must not own application logic, platform services, contracts, engines, or constitutional doctrine.

Planning evidence: `docs/wayfinder-infra-program.md`.

