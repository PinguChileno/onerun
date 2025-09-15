from pydantic import BaseModel


class ProjectCreateParams(BaseModel):
    name: str
    """
    Human-readable name for the new project
    """
