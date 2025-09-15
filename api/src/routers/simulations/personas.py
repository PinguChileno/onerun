from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.db.models import Simulation, Persona, Project
from src.types import ApprovalStatus, Pagination, PersonaDTO
from src.utils.mapping.persona import persona_model_to_dto


router = APIRouter(tags=["personas"])


@router.get("")
async def list_personas(
    simulation_id: str,
    project_id: str = Query(...),
    db: Session = Depends(get_db)
) -> Pagination[PersonaDTO]:
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

    query = (
        db
        .query(Persona)
        .filter(Persona.simulation_id == simulation_id)
        .order_by(desc(Persona.created_at))
    )

    personas = query.all()

    # TODO Implement pagination

    return Pagination(
        data=[
            persona_model_to_dto(persona)
            for persona in personas
        ],
        has_more=False,  # Since we're fetching all personas
    )


@router.post("/{persona_id}/approve")
async def approve_persona(
    simulation_id: str,
    persona_id: str,
    project_id: str = Query(...),
    db: Session = Depends(get_db)
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

    persona = (
        db
        .query(Persona)
        .filter(
            Persona.id == persona_id,
            Persona.simulation_id == simulation_id
        )
        .first()
    )

    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found")

    persona.approval_status = ApprovalStatus.APPROVED
    db.commit()

    return {"message": "Persona approved successfully"}


@router.post("/{persona_id}/reject")
async def reject_persona(
    simulation_id: str,
    persona_id: str,
    project_id: str = Query(...),
    db: Session = Depends(get_db)
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

    persona = (
        db
        .query(Persona)
        .filter(
            Persona.id == persona_id,
            Persona.simulation_id == simulation_id
        )
        .first()
    )

    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found")

    persona.approval_status = ApprovalStatus.REJECTED
    db.commit()

    return {"message": "Persona rejected successfully"}
