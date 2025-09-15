import string

from fastapi import APIRouter, Depends, HTTPException, Query
import nanoid
from sqlalchemy import desc
from sqlalchemy.orm import Session, joinedload

from src.auth import auth_middleware
from src.db.session import get_db
from src.db.models import Objective, ObjectiveVersion, Project
from src.types import (
    ObjectiveDTO,
    ObjectiveCreateParams,
    ObjectiveUpdateParams,
    Pagination,
)
from src.utils.mapping.objective import objective_model_to_dto


router = APIRouter(
    tags=["objectives"],
    dependencies=[Depends(auth_middleware)],
)


@router.post("")
async def create_objective(
    params: ObjectiveCreateParams,
    project_id: str = Query(...),
    db: Session = Depends(get_db)
) -> ObjectiveDTO:
    project = (
        db
        .query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    objective_id = nanoid.generate(
        alphabet=string.ascii_letters + string.digits,
        size=12,
    )

    # Create objective metadata
    objective = Objective(
        id=objective_id,
        project_id=project_id,
        version_id=1,  # First version
    )

    # Create first version with actual data
    objective_version = ObjectiveVersion(
        objective_id=objective_id,
        name=params.name,
        criteria=params.criteria,
        # id will be auto-assigned as 1 by trigger
    )

    db.add(objective)
    db.add(objective_version)
    db.commit()
    db.refresh(objective)

    return objective_model_to_dto(objective)


@router.get("")
async def list_objectives(
    project_id: str = Query(...),
    sort_by: str = Query("created_at"),
    sort_dir: str = Query("desc"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
) -> Pagination[ObjectiveDTO]:
    project = (
        db
        .query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    query = (
        db
        .query(Objective)
        .options(joinedload(Objective.version))
        .filter(Objective.project_id == project_id)
    )

    if sort_by == "name":
        # Join with ObjectiveVersion to sort by name
        query = query.join(
            ObjectiveVersion,
            (Objective.id == ObjectiveVersion.objective_id) &
            (Objective.version_id == ObjectiveVersion.id)
        )
        sort_field = ObjectiveVersion.name
    else:
        sort_field = Objective.created_at

    if sort_dir == "desc":
        query = query.order_by(desc(sort_field))
    else:
        query = query.order_by(sort_field)

    # Fetch one extra item to determine if there are more
    objectives = query.offset(offset).limit(limit + 1).all()

    has_more = len(objectives) > limit
    if has_more:
        objectives = objectives[:limit]  # Remove the extra item

    return Pagination(
        data=[
            objective_model_to_dto(objective)
            for objective in objectives
        ],
        has_more=has_more,
    )


@router.get("/{objective_id}")
async def get_objective(
    objective_id: str,
    project_id: str = Query(...),
    db: Session = Depends(get_db)
) -> ObjectiveDTO:
    project = (
        db
        .query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    objective = (
        db
        .query(Objective)
        .options(joinedload(Objective.version))
        .filter(Objective.id == objective_id)
        .first()
    )

    if not objective:
        raise HTTPException(status_code=404, detail="Objective not found")

    return objective_model_to_dto(objective)


@router.patch("/{objective_id}")
async def update_objective(
    objective_id: str,
    params: ObjectiveUpdateParams,
    project_id: str = Query(...),
    db: Session = Depends(get_db)
) -> ObjectiveDTO:
    project = (
        db
        .query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    objective = (
        db
        .query(Objective)
        .filter(
            Objective.id == objective_id,
            Objective.project_id == project_id,
        )
        .first()
    )

    if not objective:
        raise HTTPException(status_code=404, detail="Objective not found")

    # Only create new version if something actually changed
    if params.name is not None or params.criteria is not None:
        # Get current version data
        current_version = (
            db.query(ObjectiveVersion)
            .filter(
                ObjectiveVersion.objective_id == objective_id,
                ObjectiveVersion.id == objective.version_id
            )
            .first()
        )

        if not current_version:
            raise HTTPException(
                status_code=404, detail="Current version not found")

        # Create new version with updated data
        new_version = ObjectiveVersion(
            objective_id=objective_id,
            name=(
                params.name
                if params.name is not None
                else current_version.name
            ),
            criteria=(
                params.criteria
                if params.criteria is not None
                else current_version.criteria
            ),
            # id will be auto-assigned by trigger
        )

        db.add(new_version)
        db.commit()  # Commit to trigger the version assignment

        # Query to get the latest version ID for this objective
        latest_version = (
            db.query(ObjectiveVersion)
            .filter(ObjectiveVersion.objective_id == objective_id)
            .order_by(ObjectiveVersion.id.desc())
            .first()
        )

        # Update objective to point to new version
        objective.version_id = latest_version.id

    db.commit()
    db.refresh(objective)

    return objective_model_to_dto(objective)
