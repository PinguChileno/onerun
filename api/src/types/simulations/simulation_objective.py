from pydantic import BaseModel


class SimulationObjectiveDTO(BaseModel):
    id: str
    """
    ID of the objective being evaluated
    """
    criteria: str
    """
    The evaluation criteria for this objective
    """
    name: str
    """
    Name of the objective
    """
    version: int
    """
    Current version number of the objective
    """
