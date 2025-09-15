from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import (
    agents as agents_router,
    objectives as objectives_router,
    projects as projects_router,
    simulations as simulations_router,
)
from src.temporal import init_temporal_client, close_temporal_client


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Manage the application lifespan."""
    # Startup
    await init_temporal_client()
    yield
    # Shutdown
    await close_temporal_client()


app = FastAPI(title="OneRun API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "message": "OneRun API is running"
    }


# Include routers
app.include_router(agents_router, prefix="/v1/agents")
app.include_router(objectives_router, prefix="/v1/objectives")
app.include_router(projects_router, prefix="/v1/projects")
app.include_router(simulations_router, prefix="/v1/simulations")
