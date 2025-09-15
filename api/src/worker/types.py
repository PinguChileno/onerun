from dataclasses import dataclass
from typing import List

from src.types import ConversationDTO, PersonaDTO, SimulationDTO


# =============================================================================
# ACTIVITY SCHEMAS
# =============================================================================


@dataclass
class CreateConversationActivityInput:
    project_id: str
    simulation_id: str
    persona_id: str


@dataclass
class CreateConversationActivityOutput:
    conversation: ConversationDTO


@dataclass
class CreatePersonaActivityInput:
    project_id: str
    simulation_id: str
    scenario: str
    agent_description: str
    auto_approve: bool = False


@dataclass
class CreatePersonaActivityOutput:
    persona: PersonaDTO


@dataclass
class EvaluateConversationActivityInput:
    project_id: str
    simulation_id: str
    conversation_id: str


@dataclass
class GetSimulationActivityInput:
    project_id: str
    simulation_id: str


@dataclass
class GetSimulationActivityOutput:
    simulation: SimulationDTO | None


@dataclass
class GetConversationsCountActivityInput:
    project_id: str
    simulation_id: str
    status: str | None = None
    evaluation_status: str | None = None


@dataclass
class GetConversationsCountActivityOutput:
    count: int


@dataclass
class GetPersonaCountActivityInput:
    project_id: str
    simulation_id: str
    approval_status: str | None = None


@dataclass
class GetPersonaCountActivityOutput:
    count: int


@dataclass
class GetConversationCandidatesActivityInput:
    project_id: str
    simulation_id: str
    limit: int | None = 10
    max_per_persona: int | None = None
    prioritize: bool = False


@dataclass
class ConversationCandidate:
    id: str
    conversation_count: int


@dataclass
class GetConversationCandidatesActivityOutput:
    candidates: List[ConversationCandidate]


@dataclass
class GetConversationActivityInput:
    project_id: str
    simulation_id: str
    conversation_id: str


@dataclass
class GetConversationActivityOutput:
    conversation: ConversationDTO | None


@dataclass
class ListConversationsActivityInput:
    project_id: str
    simulation_id: str
    evaluation_status: str | None = None
    status: str | None = None


@dataclass
class ListConversationsActivityOutput:
    conversations: list[ConversationDTO]


@dataclass
class ScheduleAssignConversationsActivityInput:
    project_id: str
    simulation_id: str


@dataclass
class ScheduleAssignPersonasActivityInput:
    project_id: str
    simulation_id: str


@dataclass
class ScheduleCheckSimulationActivityInput:
    project_id: str
    simulation_id: str


@dataclass
class UnscheduleAssignConversationsActivityInput:
    project_id: str
    simulation_id: str
    raise_on_missing: bool = True
    # Whether to raise an error if the schedule is missing


@dataclass
class UnscheduleAssignPersonasActivityInput:
    project_id: str
    simulation_id: str
    raise_on_missing: bool = True
    # Whether to raise an error if the schedule is missing


@dataclass
class UnscheduleCheckSimulationActivityInput:
    project_id: str
    simulation_id: str
    raise_on_missing: bool = True
    # Whether to raise an error if the schedule is missing


@dataclass
class UpdateConversationStatusActivityInput:
    project_id: str
    simulation_id: str
    conversation_id: str
    status: str | None = None
    evaluation_status: str | None = None


@dataclass
class UpdateSimulationStatusActivityInput:
    project_id: str
    simulation_id: str
    status: str


# =============================================================================
# WORKFLOW SCHEMAS
# =============================================================================

@dataclass
class AssignConversationsWorkflowInput:
    project_id: str
    simulation_id: str


@dataclass
class AssignPersonasWorkflowInput:
    project_id: str
    simulation_id: str


@dataclass
class CancelSimulationWorkflowInput:
    project_id: str
    simulation_id: str


@dataclass
class CheckSimulationWorkflowInput:
    project_id: str
    simulation_id: str


@dataclass
class EvaluateConversationWorkflowInput:
    project_id: str
    simulation_id: str
    conversation_id: str


@dataclass
class RunSimulationWorkflowInput:
    project_id: str
    simulation_id: str
