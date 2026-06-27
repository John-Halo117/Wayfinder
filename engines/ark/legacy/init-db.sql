-- PostgreSQL initialization script for production
-- Creates databases for n8n and Grafana
-- Auto-run when postgres container starts

-- n8n database and user
CREATE DATABASE IF NOT EXISTS n8n;
CREATE USER IF NOT EXISTS n8n WITH ENCRYPTED PASSWORD :'n8n_password';
ALTER ROLE n8n SET client_encoding TO 'utf8';
ALTER ROLE n8n SET default_transaction_isolation TO 'read committed';
ALTER ROLE n8n SET default_transaction_deferrable TO on;
ALTER ROLE n8n SET default_transaction_level TO 'read committed';
GRANT ALL PRIVILEGES ON DATABASE n8n TO n8n;

-- Grafana database and user (optional; Grafana can use SQLite if empty)
CREATE DATABASE IF NOT EXISTS grafana;
CREATE USER IF NOT EXISTS grafana WITH ENCRYPTED PASSWORD :'grafana_password';
ALTER ROLE grafana SET client_encoding TO 'utf8';
ALTER ROLE grafana SET default_transaction_isolation TO 'read committed';
GRANT ALL PRIVILEGES ON DATABASE grafana TO grafana;

-- Connect as these users and set schema permissions
\connect n8n n8n
CREATE SCHEMA IF NOT EXISTS public;
GRANT ALL ON SCHEMA public TO n8n;
GRANT ALL ON ALL TABLES IN SCHEMA public TO n8n;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO n8n;

\connect grafana grafana
CREATE SCHEMA IF NOT EXISTS public;
GRANT ALL ON SCHEMA public TO grafana;
GRANT ALL ON ALL TABLES IN SCHEMA public TO grafana;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO grafana;

-- Root user password (change if needed)
\connect postgres
-- Already set via POSTGRES_PASSWORD env var
