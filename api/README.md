# OneRun API

This directory contains the backend API for OneRun, built with Python, FastAPI, and SQLAlchemy.

## Prerequisites

- **Python** 3.11+ and **uv** for dependency management
- **PostgreSQL** database (local installation or Docker)
- **Docker** and **Docker Compose** for services
- **Temporal server** for workflow orchestration

## Quick Setup

### 1. Install Dependencies

```bash
cd api
uv sync
```

### 2. Start Temporal Server

```bash
cd docker/temporal
docker compose up -d
```

### 3. Configure Environment

Create environment file:

```bash
cp .env.example .env
```

Update `.env` with your configuration:

```bash
# App
HOST=127.0.0.1
PORT=3001

# Logging
LOG_LEVEL=DEBUG

# Database
DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5432/postgres

# Auth
AUTH_API_KEY=a-secret-with-at-least-32-characters-long
AUTH_JWKS_URL=http://localhost:3000/api/auth/jwks
AUTH_JWT_ISSUER=http://localhost:3000
AUTH_JWT_AUDIENCE=http://localhost:3001
AUTH_JWT_ALGORITHM=EdDSA

# Temporal
TEMPORAL_ADDRESS=localhost:7233
TEMPORAL_NAMESPACE=default

# Anthropic 
ANTHROPIC_API_KEY=your-anthropic-api-key
```

**Key Variables:**
- `HOST/PORT`: Server binding configuration
- `DATABASE_URL`: PostgreSQL connection string
- `AUTH_API_KEY`: API authentication secret (must be 32+ characters)
- `AUTH_JWKS_URL`: JWT key endpoint from Next.js app
- `TEMPORAL_ADDRESS`: Temporal server connection
- `ANTHROPIC_API_KEY`: AI model API key

### 4. Run Database Migrations

```bash
uv run alembic upgrade head
```

### 5. Start Development Server

```bash
# Development server with auto-reload
uv run main.py --api --dev

# Production server
uv run main.py --api

# Start both API and worker
uv run main.py --api --worker
```

The API will be available at `http://localhost:3001`.

## Docker Setup (Alternative)

For containerized development:

1. Build the containers:
```bash
make docker-build
```

2. Create `.env` file:
```bash
make env
```

3. Start the services:
```bash
make docker-start
```

## Project Structure

```
api/
├── src/
│   ├── main.py           # FastAPI application entry point
│   ├── auth.py           # Authentication logic
│   ├── temporal.py       # Temporal client configuration
│   ├── routers/          # API endpoint definitions
│   ├── types/            # Pydantic request/response models
│   ├── services/         # Business logic layer
│   ├── db/               # Database models and connection
│   ├── worker/           # Temporal workflows and activities
│   └── utils/            # Helper functions and utilities
├── alembic/              # Database migration files
├── main.py               # Application entry point with CLI
├── Makefile              # Development commands
└── pyproject.toml        # Python dependencies and configuration
```

## Key Technologies

- **FastAPI** - Modern Python web framework with automatic OpenAPI docs
- **SQLAlchemy** - ORM for database operations and migrations
- **Pydantic** - Data validation and serialization
- **Better-Auth** - Authentication integration
- **Temporal** - Workflow orchestration client
- **Uvicorn** - ASGI server for development and production

## Development Commands

```bash
# Start development server
uv run main.py --api --dev

# Start production server  
uv run main.py --api

# Run database migrations
uv run alembic upgrade head

# Rollback database migrations
uv run alembic downgrade -1
```

## Development Guidelines

- Follow PEP 8 style guide
- Use type hints for all functions and variables
- Write tests for new features and endpoints
- Update documentation when making API changes
- Run migrations for database schema changes
- Ensure proper error handling and logging

## API Documentation

When the server is running, interactive API documentation is available at:
- Swagger UI: `http://localhost:3001/docs`
- ReDoc: `http://localhost:3001/redoc`