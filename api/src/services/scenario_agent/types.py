from pydantic import BaseModel, Field


class PersonaContext(BaseModel):
    """Individual story and purpose for a persona within a simulation scenario"""
    story: str = Field(
        description="Background story describing this persona's specific "
        "situation and context within the simulation scenario"
    )
    purpose: str = Field(
        description="Specific goal or reason this persona has for contacting "
        "the AI agent in this conversation"
    )
