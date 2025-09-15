from datetime import datetime
from typing import Any
from pydantic import BaseModel


class Agent(BaseModel):
    id: str
    """
    Unique identifier for the agent
    """
    created_at: datetime
    """
    When the agent was created
    """
    metadata: dict[str, Any]
    """
    Additional metadata
    """
    name: str
    """
    Human-readable name for the agent
    """
    project_id: str
    """
    ID of the project this agent belongs to
    """
    summary: str | None = None
    """
    Optional summary of the agent's purpose or capabilities
    """
    updated_at: datetime
    """
    When the agent was last modified
    """
