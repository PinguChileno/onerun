from src.db.models import Objective
from src.types import ObjectiveDTO


def objective_model_to_dto(objective: Objective) -> ObjectiveDTO:
    # Get name and criteria from current version
    current_version = objective.version
    
    return ObjectiveDTO(
        id=objective.id,
        created_at=objective.created_at,
        criteria=current_version.criteria if current_version else "",
        name=current_version.name if current_version else "",
        project_id=objective.project_id,
        updated_at=objective.updated_at,
        version=current_version.id if current_version else 0,
    )
