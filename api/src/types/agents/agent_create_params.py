from typing import Any
from pydantic import BaseModel


class AgentCreateParams(BaseModel):
    description: str | None = None
    """
    Description of the agent's purpose or capabilities
    """
    metadata: dict[str, Any] = {}
    """
    Additional metadata for the agent
    """
    name: str
    """
    Human-readable name for the new agent
    """
