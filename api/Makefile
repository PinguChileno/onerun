.PHONY: help env dev-api start-api start-worker start docker-build docker-start migrate-up migrate-down

help:
	@echo "Available commands:"
	@echo "  make env       - Copy .env.example to .env"
	@echo "  make dev       - Start the development server with auto-reload"
	@echo "  make start     - Start the production server"
	@echo "  make docker-build - Build the Docker image"
	@echo "  make docker-start - Start the API in a Docker container"
	@echo "  make migrate-up   - Run database migrations"
	@echo "  make migrate-down - Rollback database migrations"

env:
	.env.example .env

dev-api:
	uv run main.py --api --dev

start-api:
	uv run main.py --api

start-worker:
	uv run main.py --worker

start:
	uv run main.py --api --worker

docker-build:
	docker build -t onerun/onerun-api:latest .

docker-start:
	docker run --name onerun-api -p 3001:3001 onerun/onerun-api:latest --env-file .env

migrate-up:
	alembic upgrade head

migrate-down:
	alembic downgrade -1
