from datetime import datetime, timedelta, timezone
import string
from typing import Any, cast

from fastapi import APIRouter, Depends, HTTPException, Query
import nanoid
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session, joinedload
from temporalio.client import Client
from temporalio.common import RetryPolicy, WorkflowIDReusePolicy

from src.db.models import (
    Agent,
    Conversation,
    ConversationItem,
    ConversationEvaluation,
    Persona,
    Project,
    Simulation,
)
from src.db.session import get_db
from src.services.conversation_agent import ConversationAgent
from src.temporal import get_temporal_client
from src.types import (
    ConversationDTO,
    ConversationItemDTO,
    ConversationStatus,
    EvaluationStatus,
    Pagination,
    ResponseDTO,
    ResponseCreateParams,
    ResponseOutputItemDTO,
    ResponseOutputContentDTO,
)
from src.utils.mapping.conversation import conversation_model_to_dto
from src.utils.mapping.conversation_item import conversation_item_model_to_dto
from src.worker.constants import (
    EVALUATE_CONVERSATION_WORKFLOW_ID,
    MAIN_QUEUE_ID,
)
from src.worker.types import EvaluateConversationWorkflowInput


router = APIRouter(tags=["conversations"])


@router.get("")
async def list_conversations(
    simulation_id: str,
    project_id: str = Query(...),
    status: str | None = Query(None),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
) -> Pagination[ConversationDTO]:
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
        .query(Conversation)
        .options(
            joinedload(Conversation.persona),
            joinedload(
                Conversation.evaluations,
                ConversationEvaluation.objective,
            ),
        )
        .filter(Conversation.simulation_id == simulation_id)
    )

    if status:
        query = query.filter(Conversation.status == status)

    query = query.order_by(desc(Conversation.created_at))

    # Fetch one extra item to determine if there are more
    conversations = query.offset(offset).limit(limit + 1).all()

    has_more = len(conversations) > limit

    if has_more:
        conversations = conversations[:limit]

    return Pagination(
        data=[
            conversation_model_to_dto(conversation)
            for conversation in conversations
        ],
        has_more=has_more,
    )


@router.get("/{conversation_id}")
async def get_conversation(
    simulation_id: str,
    conversation_id: str,
    project_id: str = Query(...),
    db: Session = Depends(get_db)
) -> ConversationDTO:
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

    conversation = (
        db
        .query(Conversation)
        .options(
            joinedload(Conversation.persona),
            joinedload(
                Conversation.evaluations,
                ConversationEvaluation.objective,
            ),
        )
        .filter(
            Conversation.id == conversation_id,
            Conversation.simulation_id == simulation_id
        )
        .first()
    )

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return conversation_model_to_dto(conversation)


@router.post("/{conversation_id}/start")
async def start_conversation(
    simulation_id: str,
    conversation_id: str,
    project_id: str = Query(...),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Connect an agent to a conversation for processing."""
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

    conversation = (
        db
        .query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.simulation_id == simulation_id,
        )
        .first()
    )

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    if conversation.status != ConversationStatus.QUEUED:
        raise HTTPException(
            status_code=409,
            detail="Conversation is not available to be started",
        )

    conversation.status = ConversationStatus.IN_PROGRESS

    db.commit()

    return {"message": "Conversation started successfully"}


@router.post("/{conversation_id}/end")
async def end_conversation(
    project_id: str,
    simulation_id: str,
    conversation_id: str,
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

    conversation = (
        db
        .query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.simulation_id == simulation_id
        )
        .first()
    )

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    if conversation.status == ConversationStatus.ENDED:
        raise HTTPException(
            status_code=400,
            detail="Conversation has already been ended"
        )

    if conversation.status != ConversationStatus.IN_PROGRESS:
        raise HTTPException(
            status_code=400,
            detail="Conversation is not in a valid state to end"
        )

    conversation.status = ConversationStatus.ENDED
    conversation.end_reason = "agent_decided"

    conversation.evaluation_status = EvaluationStatus.QUEUED

    await temporal_client.start_workflow(
        EVALUATE_CONVERSATION_WORKFLOW_ID,
        EvaluateConversationWorkflowInput(
            project_id=project_id,
            simulation_id=simulation_id,
            conversation_id=conversation.id,
        ),
        id=f"evaluate_conversation:{simulation_id}:{conversation.id}",
        task_queue=MAIN_QUEUE_ID,
        id_reuse_policy=WorkflowIDReusePolicy.ALLOW_DUPLICATE_FAILED_ONLY,
        retry_policy=RetryPolicy(
            initial_interval=timedelta(seconds=15),
            maximum_attempts=5,
        ),
    )

    db.commit()

    return {"message": "Conversation ended successfully"}


@router.post("/{conversation_id}/items")
async def list_items(
    simulation_id: str,
    conversation_id: str,
    project_id: str = Query(...),
    db: Session = Depends(get_db),
) -> Pagination[ConversationItemDTO]:
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

    conversation = (
        db
        .query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.simulation_id == simulation_id
        )
        .first()
    )

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    items = (
        db
        .query(ConversationItem)
        .filter(ConversationItem.conversation_id == conversation.id)
        .order_by(asc(ConversationItem.created_at))
        .all()
    )

    # TODO Implement pagination

    return Pagination(
        data=[
            conversation_item_model_to_dto(item)
            for item in items
        ],
        has_more=False,  # Since we're fetching all conversation items
    )


@router.post("/{conversation_id}/responses")
async def create_response(
    simulation_id: str,
    conversation_id: str,
    params: ResponseCreateParams,
    project_id: str = Query(...),
    db: Session = Depends(get_db),
    temporal_client: Client = Depends(get_temporal_client),
) -> ResponseDTO:
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
        .options(joinedload(Simulation.agent))
        .filter(Simulation.id == simulation_id)
        .first()
    )

    if not simulation:
        raise HTTPException(status_code=404, detail="Simulation not found")

    conversation = (
        db
        .query(Conversation)
        .options(joinedload(Conversation.persona))
        .filter(
            Conversation.id == conversation_id,
            Conversation.simulation_id == simulation_id
        )
        .first()
    )

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    if conversation.status == ConversationStatus.ENDED:
        raise HTTPException(
            status_code=400,
            detail="Conversation has already been ended"
        )

    items = (
        db.query(ConversationItem)
        .filter(ConversationItem.conversation_id == conversation.id)
        .order_by(asc(ConversationItem.created_at))
        .all()
    )

    # Collect the conversation history for the prompt

    history: list[dict[str, Any]] = [
        {
            "role": item.role,
            "content": item.content,
        }
        for item in items
    ]

    if params.input:
        history.extend(
            {
                "role": "assistant",
                "content": [
                    {
                        "type": block.type,
                        "text": block.text,
                    }
                    for block in item.content
                ],
            }
            for item in params.input
        )

    agent = cast(Agent, simulation.agent)
    persona = cast(Persona, conversation.persona)

    conversation_agent = ConversationAgent()

    reply = await conversation_agent.generate_reply(
        agent_description=agent.description,
        persona_attributes=persona.attributes,
        persona_story=persona.story,
        persona_purpose=persona.purpose,
        max_turns=simulation.max_turns,
        history=history,
    )

    decided_to_end = False

    if reply and reply.endswith("[END]"):
        decided_to_end = True
        reply = reply[:-len("[END]")].strip()

    # Persist the new items
    # Manually set timestamps to preserve order, otherwise they will all be
    # set to the same time on insert
    new_items: list[ConversationItem] = []

    if params.input:
        for item in params.input:
            now = datetime.now(timezone.utc)

            new_items.append(ConversationItem(
                id=nanoid.generate(
                    alphabet=string.ascii_letters + string.digits
                ),
                content=[
                    {
                        "type": block.type,
                        "text": block.text,
                    }
                    for block in item.content
                ],
                conversation_id=conversation.id,
                created_at=now,
                role="assistant",
                type="message",
                updated_at=now,
            ))

    if reply:
        now = datetime.now(timezone.utc)

        new_items.append(
            ConversationItem(
                id=nanoid.generate(
                    alphabet=string.ascii_letters + string.digits
                ),
                content=[{
                    "type": "text",
                    "text": reply,
                }],
                conversation_id=conversation.id,
                created_at=now,
                role="user",
                type="message",
                updated_at=now,
            )
        )

    # Update conversation status to IN_PROGRESS if not already
    if conversation.status != ConversationStatus.IN_PROGRESS:
        conversation.status = ConversationStatus.IN_PROGRESS

    # Check if conversation has ended

    # Case 1: No reply from persona or responded with [END] and got stripped
    if not reply:
        conversation.status = ConversationStatus.ENDED
        conversation.end_reason = "persona_decided"

    # Case 2: Persona decided to end
    if conversation.status != ConversationStatus.ENDED and decided_to_end:
        conversation.status = ConversationStatus.ENDED
        conversation.end_reason = "persona_decided"

    # Case 3: Check if max turns has been reached
    if conversation.status != ConversationStatus.ENDED:
        current_turns = len(items) + len(new_items)
        if current_turns >= simulation.max_turns:
            conversation.status = ConversationStatus.ENDED
            conversation.end_reason = "max_turns_reached"

    if conversation.status == ConversationStatus.ENDED:
        conversation.evaluation_status = EvaluationStatus.QUEUED

        await temporal_client.start_workflow(
            EVALUATE_CONVERSATION_WORKFLOW_ID,
            EvaluateConversationWorkflowInput(
                project_id=project_id,
                simulation_id=simulation_id,
                conversation_id=conversation.id,
            ),
            id=f"evaluate_conversation:{simulation_id}:{conversation.id}",
            task_queue=MAIN_QUEUE_ID,
            id_reuse_policy=WorkflowIDReusePolicy.ALLOW_DUPLICATE_FAILED_ONLY,
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=15),
                maximum_attempts=5,
            ),
        )

    db.add_all(new_items)
    db.commit()

    response = ResponseDTO(
        ended=conversation.status == ConversationStatus.ENDED,
        output=[],
    )

    if reply:
        response.output = [ResponseOutputItemDTO(
            type="message",
            content=[ResponseOutputContentDTO(
                type="text",
                text=reply,
            )],
        )]

    return response
