from pydantic import BaseModel


class ObjectiveUpdateParams(BaseModel):
    criteria: str | None = None
    """
    The specific criteria used to evaluate this objective (optional)
    """
    name: str | None = None
    """
    Human-readable name for the objective (optional)
    """