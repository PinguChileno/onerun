from datetime import datetime
from typing import Any
from pydantic import BaseModel


class AgentDTO(BaseModel):
    id: str
    """
    Unique identifier for the agent
    """
    created_at: datetime
    """
    When the agent was created
    """
    description: str | None = None
    """
    Description of the agent's purpose or capabilities
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
    updated_at: datetime
    """
    When the agent was last modified
    """
