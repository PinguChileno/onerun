# Temporal Server Setup

This directory contains Docker Compose configuration for running a Temporal server with PostgreSQL persistence.

## Overview

The setup is based on the official Temporal Docker Compose configuration from the [Temporal GitHub repository](https://github.com/temporalio/docker-compose). This provides a complete Temporal development environment with:

- **Temporal Server**: Auto-setup image with schema migration
- **PostgreSQL Database**: Persistent storage for Temporal workflows and activities
- **Temporal UI**: Web interface for monitoring workflows (accessible at http://localhost:8080)
- **Admin Tools**: CLI tools for managing Temporal clusters

## Quick Start

```bash
# Start Temporal services
docker compose up -d

# Verify services are running
docker compose ps

# Access Temporal UI
open http://localhost:8080
```

## Network Configuration

This setup creates a `temporal-network` that can be shared with other Docker Compose projects. Services in other compose files can connect to Temporal using:

```yaml
networks:
  temporal-network:
    external: true
```

## Connection Details

- **Temporal Address**: `temporal:7233` (from within Docker network)
- **Temporal Address**: `localhost:7233` (from host machine)
- **Web UI**: http://localhost:8080
- **Database**: PostgreSQL on port 5432 (internal only)

## Other Setups

For different deployment scenarios (Cassandra, Elasticsearch, etc.), refer to the [official Temporal Docker Compose repository](https://github.com/temporalio/docker-compose).
