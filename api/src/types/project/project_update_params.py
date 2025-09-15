from pydantic import BaseModel


class ProjectUpdateParams(BaseModel):
    name: str | None = None
    """
    Human-readable name for the project
    """
