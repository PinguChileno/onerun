import string

from fastapi import APIRouter, Depends, HTTPException, Query
import nanoid
from sqlalchemy import desc
from sqlalchemy.orm import Session

from src.auth import auth_middleware
from src.db.session import get_db
from src.db.models import Project
from src.types import (
    ProjectDTO,
    ProjectCreateParams,
    ProjectUpdateParams,
    Pagination,
)
from src.utils.mapping.project import project_model_to_dto


router = APIRouter(
    tags=["projects"],
    dependencies=[Depends(auth_middleware)],
)


@router.post("")
async def create_project(
    params: ProjectCreateParams,
    db: Session = Depends(get_db)
) -> ProjectDTO:
    project = Project(
        id=nanoid.generate(
            alphabet=string.ascii_letters + string.digits,
            size=12,
        ),
        name=params.name,
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project_model_to_dto(project)


@router.get("")
async def list_projects(
    sort_by: str = Query("created_at"),
    sort_dir: str = Query("desc"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
) -> Pagination[ProjectDTO]:
    query = db.query(Project)

    if sort_by == "name":
        sort_field = Project.name
    else:
        sort_field = Project.created_at

    if sort_dir == "desc":
        query = query.order_by(desc(sort_field))
    else:
        query = query.order_by(sort_field)

    # Fetch one extra item to determine if there are more
    projects = query.offset(offset).limit(limit + 1).all()

    has_more = len(projects) > limit
    if has_more:
        projects = projects[:limit]  # Remove the extra item

    return Pagination(
        data=[
            project_model_to_dto(project)
            for project in projects
        ],
        has_more=has_more,
    )


@router.get("/{project_id}")
async def get_project(
    project_id: str,
    db: Session = Depends(get_db)
) -> ProjectDTO:
    project = (
        db
        .query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project_model_to_dto(project)


@router.patch("/{project_id}")
async def update_project(
    project_id: str,
    params: ProjectUpdateParams,
    db: Session = Depends(get_db)
) -> ProjectDTO:
    project = (
        db
        .query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if params.name is not None:
        project.name = params.name

    db.commit()
    db.refresh(project)

    return project_model_to_dto(project)
