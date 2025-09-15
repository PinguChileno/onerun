from pydantic import BaseModel


class AgentUpdateParams(BaseModel):
    description: str | None = None
    """
    Description of the agent's purpose or capabilities (optional)
    """
    name: str | None = None
    """
    Human-readable name for the agent (optional)
    """

