from datetime import datetime
from enum import Enum
from typing import Any
from pydantic import BaseModel

from src.types.objectives import ObjectiveDTO
from src.types.simulations.personas import PersonaDTO


class ConversationStatus(str, Enum):
    ENDED = "ended"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"
    PENDING = "pending"
    QUEUED = "queued"


class EvaluationStatus(str, Enum):
    COMPLETED = "completed"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"
    NOT_APPLICABLE = "not_applicable"
    PENDING = "pending"
    QUEUED = "queued"


class ConversationItemDTO(BaseModel):
    id: str
    """
    Unique identifier for the conversation item
    """
    content: Any
    """
    The content of this conversation item (structure varies by type)
    """
    conversation_id: str
    """
    ID of the conversation this item belongs to
    """
    created_at: datetime
    """
    When this conversation item was created
    """
    role: str
    """
    Role of the speaker (e.g., 'system', 'assistant', 'user')
    """
    type: str
    """
    Type of conversation item (e.g., 'message')
    """
    updated_at: datetime
    """
    When this conversation item was last modified
    """


class ConversationEvaluationDTO(BaseModel):
    id: str
    """
    Unique identifier for the conversation score
    """
    conversation_id: str
    """
    ID of the conversation being scored
    """
    created_at: datetime
    """
    When the score was created
    """
    objective_id: str
    """
    ID of the objective this score evaluates
    """
    objective: ObjectiveDTO | None = None
    """
    The populated objective data
    """
    reason: str | None = None
    """
    Explanation or reasoning for why this score was given
    """
    score: float
    """
    Numeric score value (typically 0.0-1.0) indicating how well the
    conversation met the objective
    """
    updated_at: datetime
    """
    When the score was last modified
    """


class ConversationDTO(BaseModel):
    id: str
    """
    Unique identifier for the conversation
    """
    created_at: datetime
    """
    When the conversation was started
    """
    end_reason: str | None = None
    """
    Reason why the conversation ended (if applicable)
    """
    evaluation_status: EvaluationStatus
    """
    Current status of the conversation evaluation process
    """
    evaluations: list[ConversationEvaluationDTO]
    """
    List of evaluations assigned to this conversation
    """
    metadata: dict[str, Any]
    """
    Additional metadata
    """
    persona_id: str
    """
    ID of the persona participating in this conversation
    """
    persona: PersonaDTO | None = None
    """
    The populated persona data
    """
    seq_id: int
    """
    Sequence identifier within a simulation
    """
    simulation_id: str
    """
    ID of the simulation this conversation belongs to
    """
    status: ConversationStatus
    """
    Current status of the conversation
    """
    updated_at: datetime
    """
    When the conversation was last modified
    """
