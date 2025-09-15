import string

from fastapi import APIRouter, Depends, HTTPException, Query
import nanoid
from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from src.auth import auth_middleware
from src.db.session import get_db
from src.db.models import Agent, Project, Simulation
from src.types import (
    AgentDTO,
    AgentCreateParams,
    AgentUpdateParams,
    Pagination,
)
from src.utils.mapping.agent import agent_model_to_dto


class AgentWithStatsDTO(AgentDTO):
    total_simulations: int


router = APIRouter(
    tags=["agents"],
    dependencies=[Depends(auth_middleware)],
)


@router.post("")
async def create_agent(
    params: AgentCreateParams,
    project_id: str = Query(...),
    db: Session = Depends(get_db)
) -> AgentWithStatsDTO:
    project = (
        db
        .query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    agent = Agent(
        id=nanoid.generate(
            alphabet=string.ascii_letters + string.digits,
            size=12,
        ),
        description=params.description,
        metadata_=params.metadata,
        name=params.name,
        project_id=project_id,
    )

    db.add(agent)
    db.commit()
    db.refresh(agent)

    return AgentWithStatsDTO(
        **agent_model_to_dto(agent).model_dump(),
        total_simulations=0,
    )


@router.get("")
async def list_agents(
    project_id: str = Query(...),
    name: str | None = Query(None),
    sort_by: str = Query("created_at"),
    sort_dir: str = Query("desc"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
) -> Pagination[AgentWithStatsDTO]:
    project = (
        db
        .query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    query = db.query(Agent).filter(Agent.project_id == project_id)

    if name:
        query = query.filter(Agent.name.ilike(f"%{name}%"))

    if sort_by == "name":
        sort_field = Agent.name
    else:
        sort_field = Agent.created_at

    if sort_dir == "desc":
        query = query.order_by(desc(sort_field))
    else:
        query = query.order_by(sort_field)

    # Fetch one extra item to determine if there are more
    agents = query.offset(offset).limit(limit + 1).all()

    has_more = len(agents) > limit
    if has_more:
        agents = agents[:limit]  # Remove the extra item

    agent_ids = [agent.id for agent in agents]
    stats = (
        db
        .query(
            Agent.id,
            func.count(Simulation.id).label('total_simulations')
        )
        .outerjoin(Simulation)
        .filter(Agent.id.in_(agent_ids))
        .group_by(Agent.id)
        .all()
    )

    stats_map = {stat.id: stat.total_simulations for stat in stats}

    return Pagination(
        data=[
            AgentWithStatsDTO(
                **agent_model_to_dto(agent).model_dump(),
                total_simulations=stats_map.get(agent.id, 0)
            )
            for agent in agents
        ],
        has_more=has_more,
    )


@router.get("/{agent_id}")
async def get_agent(
    agent_id: str,
    project_id: str = Query(...),
    db: Session = Depends(get_db)
) -> AgentWithStatsDTO:
    project = (
        db
        .query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    agent = (
        db.query(Agent)
        .filter(
            Agent.id == agent_id,
            Agent.project_id == project_id,
        )
        .first()
    )

    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    simulation_count = (
        db
        .query(func.count(Simulation.id))
        .filter(Simulation.agent_id == agent_id)
        .scalar() or 0
    )

    return AgentWithStatsDTO(
        **agent_model_to_dto(agent).model_dump(),
        total_simulations=simulation_count
    )


@router.patch("/{agent_id}")
async def update_agent(
    agent_id: str,
    params: AgentUpdateParams,
    project_id: str = Query(...),
    db: Session = Depends(get_db)
) -> AgentWithStatsDTO:
    project = (
        db
        .query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    agent = (
        db.query(Agent)
        .filter(
            Agent.id == agent_id,
            Agent.project_id == project_id,
        )
        .first()
    )

    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    if params.name is not None:
        agent.name = params.name

    if params.description is not None:
        agent.description = params.description

    db.commit()
    db.refresh(agent)

    simulation_count = (
        db
        .query(func.count(Simulation.id))
        .filter(Simulation.agent_id == agent_id)
        .scalar() or 0
    )

    return AgentWithStatsDTO(
        **agent_model_to_dto(agent).model_dump(),
        total_simulations=simulation_count
    )
