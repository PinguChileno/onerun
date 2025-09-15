from datetime import datetime
from typing import Any
from pydantic import BaseModel


class ProjectDTO(BaseModel):
    id: str
    """
    Unique identifier for the project
    """
    created_at: datetime
    """
    When the project was created
    """
    metadata: dict[str, Any]
    """
    Additional metadata
    """
    name: str
    """
    Human-readable name for the project
    """
    updated_at: datetime
    """
    When the project was last modified
    """
