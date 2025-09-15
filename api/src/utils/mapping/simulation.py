from src.db.models import Simulation
from src.types import SimulationDTO
from src.utils.mapping.agent import agent_model_to_dto


def simulation_model_to_dto(simulation: Simulation) -> SimulationDTO:
    if simulation.agent:
        agent = agent_model_to_dto(simulation.agent)
    else:
        agent = None

    return SimulationDTO(
        id=simulation.id,
        agent=agent,
        agent_id=simulation.agent_id,
        auto_approve=simulation.auto_approve,
        created_at=simulation.created_at,
        expires_at=simulation.expires_at,
        last_failure_reason=simulation.last_failure_reason,
        max_turns=simulation.max_turns,
        metadata=simulation.metadata_,
        name=simulation.name,
        objectives=[],
        project_id=simulation.project_id,
        scenario=simulation.scenario,
        status=simulation.status,
        target_conversations=simulation.target_conversations,
        target_personas=simulation.target_personas,
        updated_at=simulation.updated_at,
    )
