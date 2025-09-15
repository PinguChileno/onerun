.PHONY: help env docker-build docker-start

help:
	@echo "Available commands:"
	@echo "  make docker-build - Build the Docker image"
	@echo "  make docker-start - Start the app in a Docker container"

env:
	.env.example .env.local

docker-build:
	docker build -t onerun/onerun-app:latest .

docker-start:
	docker run --name onerun-app -p 3001:3001 onerun/onerun-app:latest --env-file .env.local
