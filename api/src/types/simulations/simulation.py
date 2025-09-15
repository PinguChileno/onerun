from datetime import datetime
from enum import Enum
from typing import Any
from pydantic import BaseModel

from src.types.agents import AgentDTO

from .simulation_objective import SimulationObjectiveDTO


class SimulationStatus(str, Enum):
    CANCELED = "canceled"
    CANCELING = "canceling"
    COMPLETED = "completed"
    EXPIRED = "expired"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"
    PENDING = "pending"
    QUEUED = "queued"


class SimulationDTO(BaseModel):
    id: str
    """
    Unique identifier for the simulation
    """
    agent_id: str
    """
    ID of the agent being simulated
    """
    agent: AgentDTO | None = None
    """
    The populated agent data
    """
    auto_approve: bool
    """
    Whether to automatically approve generated personas
    """
    created_at: datetime
    """
    When the simulation was created
    """
    expires_at: datetime | None = None
    """
    Optional expiration time for the simulation
    """
    last_failure_reason: str | None = None
    """
    Reason for the last failure if the simulation failed
    """
    max_turns: int
    """
    Maximum number of turns allowed in each conversation
    """
    metadata: dict[str, Any]
    """
    Additional metadata
    """
    name: str
    """
    Human-readable name for the simulation
    """
    objectives: list[SimulationObjectiveDTO] = []
    """
    List of objectives being evaluated in this simulation
    """
    project_id: str
    """
    ID of the project this simulation belongs to
    """
    scenario: str
    """
    The scenario description that guides the simulation
    """
    status: SimulationStatus
    """
    Current status of the simulation
    """
    target_conversations: int
    """
    Target number of conversations to generate
    """
    target_personas: int
    """
    Target number of personas to create
    """
    updated_at: datetime
    """
    When the simulation was last modified
    """
