from src.db.models import Project
from src.types import ProjectDTO


def project_model_to_dto(project: Project) -> ProjectDTO:
    return ProjectDTO(
        id=project.id,
        created_at=project.created_at,
        metadata=project.metadata_,
        name=project.name,
        updated_at=project.updated_at,
    )
