from pydantic import BaseModel


class ObjectiveCreateParams(BaseModel):
    criteria: str
    """
    The specific criteria used to evaluate this objective
    """
    name: str
    """
    Human-readable name for the new objective
    """
