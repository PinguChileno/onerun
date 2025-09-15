from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel


class ApprovalStatus(str, Enum):
    APPROVED = "approved"
    PENDING = "pending"
    REJECTED = "rejected"


class PersonaDTO(BaseModel):
    id: str
    """
    Unique identifier for the persona
    """
    approval_status: ApprovalStatus
    """
    Current approval status of the persona
    """
    attributes: dict[str, Any]
    """
    Attributes that define the persona
    """
    created_at: datetime
    """
    When the persona was created
    """
    metadata: dict[str, Any]
    """
    Additional metadata
    """
    purpose: str
    """
    Purpose within the simulation
    """
    seq_id: int
    """
    Sequence identifier within a simulation
    """
    simulation_id: str
    """
    ID of the simulation this persona belongs to
    """
    story: str
    """
    Story within the simulation
    """
    summary: str
    """
    Brief descriptive label for the persona (e.g., 'Detail-Oriented Analyst')
    """
    updated_at: datetime
    """
    When the persona was last modified
    """
