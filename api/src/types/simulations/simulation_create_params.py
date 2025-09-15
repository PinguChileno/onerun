from pydantic import BaseModel


class SimulationCreateParams(BaseModel):
    agent_id: str
    """
    ID of the agent to use in this simulation
    """
    auto_approve: bool = False
    """
    Whether to automatically approve generated personas (default: false)
    """
    max_turns: int = 5
    """
    Maximum number of turns allowed in each conversation (default: 5)
    """
    name: str
    """
    Human-readable name for the new simulation
    """
    objective_ids: list[str] = []
    """
    List of objective IDs to evaluate in this simulation
    """
    scenario: str
    """
    Description of the scenario that guides the simulation
    """
    target_conversations: int
    """
    Target number of conversations to generate
    """
    target_personas: int
    """
    Target number of personas to create
    """
