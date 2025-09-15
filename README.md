# OneRun AI

**Open source AI agent testing and conversation simulation platform**

OneRun helps you test, evaluate, and improve your AI agents through realistic conversation simulation at scale.

## 🚀 What OneRun Does

- **Simulate realistic user conversations** with your AI agents across diverse personas and scenarios
- **Generate evaluation datasets** with judge-labeled conversations for testing and benchmarking
- **Create training data** for fine-tuning with preference pairs, critique-and-revise triples, and clean JSONL exports
- **Automate QA testing** by running hundreds of conversations per build to catch issues before production
- **Surface edge cases** that manual testing misses through adversarial and varied interaction patterns

## Prerequisites

- Docker and Docker Compose
- Node.js 22+ (for local development)
- Python 3.12+ (for local development)

## Quick Start

### 1. Environment Setup

Copy the environment variables:

```bash
# In the docker directory
cd docker
cp .env.example .env
```

Edit `.env` with your configuration values.

### 2. Start Temporal Services

First, start the Temporal server (required for workflow processing):

```bash
cd docker/temporal
docker compose up -d
```

Verify Temporal is running:
- Temporal UI: http://localhost:8080
- Temporal should show as "healthy" in `docker compose ps`

### 3. Start OneRun Services

From the main docker directory:

```bash
cd docker
docker compose up
```

This will start:
- **Database** (PostgreSQL on port 5432)
- **API** (FastAPI on port 3001) 
- **App** (Next.js on port 3000)

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **API**: http://localhost:3001
- **API Docs**: http://localhost:3001/docs
- **Temporal UI**: http://localhost:8080

## Development

### API Development

```bash
cd api
# Install dependencies
uv sync
# Run with auto-reload
make dev
```

### Frontend Development

```bash
cd app
# Install dependencies
pnpm install
# Run development server
pnpm dev
```

### Database Migrations

```bash
cd api
# Run migrations
make migrate-up
# Rollback migrations
make migrate-down
```

## Project Structure

```
├── api/                 # FastAPI backend
├── app/                 # Next.js frontend
├── docker/              # Docker Compose configurations
│   ├── temporal/        # Temporal server setup
│   └── docker-compose.yml
├── python-sdk/          # Python SDK for workflows
└── README.md
```

## Stopping Services

```bash
# Stop OneRun services
cd docker
docker compose down

# Stop Temporal services
cd docker/temporal  
docker compose down
```