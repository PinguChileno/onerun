from datetime import datetime, timedelta, timezone
from logging import getLogger
import string
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
import nanoid
from sqlalchemy import desc, tuple_
from sqlalchemy.orm import Session, joinedload
from temporalio.client import Client
from temporalio.common import RetryPolicy, WorkflowIDReusePolicy

from src.db.session import get_db
from src.db.models import (
    Agent,
    Objective,
    ObjectiveVersion,
    Project,
    Simulation,
    SimulationObjective,
)
from src.temporal import get_temporal_client
from src.types import (
    Pagination,
    SimulationCreateParams,
    SimulationDTO,
    SimulationStatus,
)
from src.types.simulations.simulation_objective import SimulationObjectiveDTO
from src.utils.mapping.simulation import simulation_model_to_dto
from src.worker.constants import (
    MAIN_QUEUE_ID,
    RUN_SIMULATION_WORKFLOW_ID,
    CANCEL_SIMULATION_WORKFLOW_ID,
)
from src.worker.types import (
    RunSimulationWorkflowInput,
    CancelSimulationWorkflowInput,
)

from .conversations import router as conversations_router
from .personas import router as personas_router


logger = getLogger(__name__)

router = APIRouter(tags=["simulations"])

# Include sub-routers
router.include_router(
    conversations_router,
    prefix="/{simulation_id}/conversations"
)
router.include_router(
    personas_router,
    prefix="/{simulation_id}/personas"
)


@router.post("")
async def create_simulation(
    params: SimulationCreateParams,
    project_id: str = Query(...),
    db: Session = Depends(get_db),
    temporal_client: Client = Depends(get_temporal_client),
) -> SimulationDTO:
    project = (
        db
        .query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    agent = (
        db
        .query(Agent)
        .filter(
            Agent.id == params.agent_id,
            Agent.project_id == project_id
        )
        .first()
    )

    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    # Validate objectives exist and belong to the project
    if params.objective_ids:
        objectives = (
            db
            .query(Objective)
            .filter(
                Objective.id.in_(params.objective_ids),
                Objective.project_id == project_id
            )
            .all()
        )

        existing_objective_ids = {obj.id for obj in objectives}
        invalid_objective_ids = (
            set(params.objective_ids) - existing_objective_ids
        )

        if invalid_objective_ids:
            invalid_ids_str = ", ".join(invalid_objective_ids)
            raise HTTPException(
                status_code=404,
                detail=f"Objectives not found: {invalid_ids_str}",
            )

    simulation = Simulation(
        id=nanoid.generate(
            alphabet=string.ascii_letters + string.digits
        ),
        agent_id=params.agent_id,
        auto_approve=params.auto_approve,
        expires_at=datetime.now(timezone.utc) + timedelta(hours=24),
        max_turns=params.max_turns,
        name=params.name,
        project_id=project_id,
        scenario=params.scenario,
        status=SimulationStatus.PENDING,
        target_conversations=params.target_conversations,
        target_personas=params.target_personas,
    )

    db.add(simulation)
    db.commit()

    # Rfresh to get relationships
    simulation = (
        db
        .query(Simulation)
        .options(
            joinedload(Simulation.agent),
            joinedload(Simulation.objectives, SimulationObjective.objective)
        )
        .filter(Simulation.id == simulation.id)
        .first()
    )

    # Create simulation_objective records
    if params.objective_ids:
        simulation_objectives = [
            SimulationObjective(
                simulation_id=simulation.id,
                objective_id=objective.id,
                objective_version_id=objective.version_id
            )
            for objective in objectives
        ]

        db.add_all(simulation_objectives)
        db.commit()

    try:
        await temporal_client.start_workflow(
            RUN_SIMULATION_WORKFLOW_ID,
            RunSimulationWorkflowInput(
                project_id=project_id,
                simulation_id=simulation.id
            ),
            id=f"run_simulation:{simulation.id}",
            task_queue=MAIN_QUEUE_ID,
            id_reuse_policy=WorkflowIDReusePolicy.REJECT_DUPLICATE,
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=15),
                maximum_attempts=3,
            ),
        )

        simulation.status = SimulationStatus.QUEUED
        db.commit()
    except Exception as e:
        logger.error(f"Failed to start simulation: {e}")

    return simulation_model_to_dto(simulation)


@router.get("")
async def list_simulations(
    project_id: str = Query(...),
    name: str | None = Query(None),
    status: str | None = Query(None),
    agent_id: str | None = Query(None),
    sort_by: str = Query("created_at"),
    sort_dir: str = Query("desc"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
) -> Pagination[SimulationDTO]:
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
        .query(Simulation)
        .options(joinedload(Simulation.agent))
        .filter(Simulation.project_id == project_id)
    )

    if name:
        query = query.filter(Simulation.name.ilike(f"%{name}%"))
    if status:
        query = query.filter(Simulation.status == status)
    if agent_id:
        query = query.filter(Simulation.agent_id == agent_id)

    if sort_by == "name":
        sort_field = Simulation.name
    elif sort_by == "status":
        sort_field = Simulation.status
    else:
        sort_field = Simulation.created_at

    if sort_dir == "desc":
        query = query.order_by(desc(sort_field))
    else:
        query = query.order_by(sort_field)

    # Fetch one extra item to determine if there are more
    simulations = query.offset(offset).limit(limit + 1).all()

    has_more = len(simulations) > limit
    if has_more:
        simulations = simulations[:limit]  # Remove the extra item

    return Pagination(
        data=[
            simulation_model_to_dto(simulation)
            for simulation in simulations
        ],
        has_more=has_more,
    )


@router.get("/{simulation_id}")
async def get_simulation(
    simulation_id: str,
    project_id: str = Query(...),
    db: Session = Depends(get_db)
) -> None:
    project = (
        db
        .query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    simulation = (
        db
        .query(Simulation)
        .options(
            joinedload(Simulation.agent),
            joinedload(Simulation.objectives, SimulationObjective.objective)
        )
        .filter(Simulation.id == simulation_id)
        .first()
    )

    # Get objective versions and build DTOs
    objective_dtos: list[SimulationObjectiveDTO] = []

    if simulation.objectives:
        # Query all needed versions at once
        versions = (
            db
            .query(ObjectiveVersion)
            .filter(
                tuple_(ObjectiveVersion.objective_id, ObjectiveVersion.id)
                .in_([
                    (obj.objective_id, obj.objective_version_id)
                    for obj in simulation.objectives
                ])
            )
            .all()
        )

        # Create version lookup and build DTOs
        version_map = {(v.objective_id, v.id): v for v in versions}
        objective_dtos = [
            SimulationObjectiveDTO(
                id=obj.objective_id,
                name=version.name,
                criteria=version.criteria,
                version=obj.objective_version_id,
            )
            for obj in simulation.objectives
            if (version := version_map.get(
                (obj.objective_id, obj.objective_version_id)
            ))
        ]

    if not simulation:
        raise HTTPException(status_code=404, detail="Simulation not found")

    simulation_dto = simulation_model_to_dto(simulation)
    simulation_dto.objectives = objective_dtos
    return simulation_dto


@router.post("/{simulation_id}/run")
async def run_simulation(
    simulation_id: str,
    project_id: str = Query(...),
    db: Session = Depends(get_db),
    temporal_client: Client = Depends(get_temporal_client),
) -> dict[str, Any]:
    project = (
        db
        .query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    simulation = (
        db
        .query(Simulation)
        .filter(Simulation.id == simulation_id)
        .first()
    )

    if not simulation:
        raise HTTPException(status_code=404, detail="Simulation not found")

    await temporal_client.start_workflow(
        RUN_SIMULATION_WORKFLOW_ID,
        RunSimulationWorkflowInput(
            project_id=project_id,
            simulation_id=simulation.id
        ),
        id=f"run_simulation:{simulation.id}",
        task_queue=MAIN_QUEUE_ID,
        id_reuse_policy=WorkflowIDReusePolicy.ALLOW_DUPLICATE_FAILED_ONLY,
        retry_policy=RetryPolicy(
            initial_interval=timedelta(seconds=15),
            maximum_attempts=3,
        ),
    )

    simulation.status = SimulationStatus.QUEUED
    db.commit()

    return {"message": "Simulation run requested"}


@router.post("/{simulation_id}/cancel")
async def cancel_simulation(
    simulation_id: str,
    project_id: str = Query(...),
    db: Session = Depends(get_db),
    temporal_client: Client = Depends(get_temporal_client),
) -> dict[str, Any]:
    project = (
        db
        .query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    simulation = (
        db
        .query(Simulation)
        .filter(Simulation.id == simulation_id)
        .first()
    )

    if not simulation:
        raise HTTPException(status_code=404, detail="Simulation not found")

    await temporal_client.start_workflow(
        CANCEL_SIMULATION_WORKFLOW_ID,
        CancelSimulationWorkflowInput(
            project_id=project_id,
            simulation_id=simulation.id
        ),
        id=f"cancel_simulation:{simulation.id}",
        task_queue=MAIN_QUEUE_ID,
        id_reuse_policy=WorkflowIDReusePolicy.ALLOW_DUPLICATE_FAILED_ONLY,
        retry_policy=RetryPolicy(
            initial_interval=timedelta(seconds=15),
            maximum_attempts=3,
        ),
    )

    simulation.status = SimulationStatus.CANCELING
    db.commit()

    return {"message": "Simulation cancel requested"}
