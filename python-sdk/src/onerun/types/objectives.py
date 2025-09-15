from datetime import datetime
from pydantic import BaseModel


class Objective(BaseModel):
    id: str
    """
    Unique identifier for the objective
    """
    created_at: datetime
    """
    When the objective was created
    """
    criteria: str
    """
    The specific criteria used to evaluate this objective
    """
    name: str
    """
    Human-readable name for the objective
    """
    project_id: str
    """
    ID of the project this objective belongs to
    """
    updated_at: datetime
    """
    When the objective was last modified
    """
