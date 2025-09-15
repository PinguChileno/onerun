from src.db.models import Agent
from src.types import AgentDTO


def agent_model_to_dto(agent: Agent) -> AgentDTO:
    return AgentDTO(
        id=agent.id,
        created_at=agent.created_at,
        description=agent.description,
        metadata=agent.metadata_,
        name=agent.name,
        project_id=agent.project_id,
        updated_at=agent.updated_at
    )
