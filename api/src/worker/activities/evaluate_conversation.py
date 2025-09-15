from datetime import datetime, timezone
from typing import Any, Callable
from functools import lru_cache

from sqlalchemy import Engine, asc, tuple_
from sqlalchemy.orm import sessionmaker
from temporalio import activity

from src.db.models import (
    Conversation,
    ConversationItem,
    ConversationEvaluation,
    ObjectiveVersion,
    SimulationObjective,
)
from src.types import EvaluationStatus
from src.worker.constants import EVALUATE_CONVERSATION_ACTIVITY_ID
from src.worker.types import GetConversationActivityInput


@lru_cache(maxsize=1)
def get_eval_agent():
    """
    Cached factory for EvalAgent to avoid recreating it.

    NOTE: Workflows fail if agent is imported at top level.
    """
    from src.services.eval_agent import EvalAgent
    return EvalAgent()


def evaluate_conversation_activity(engine: Engine) -> Callable:
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    @activity.defn(name=EVALUATE_CONVERSATION_ACTIVITY_ID)
    async def run(input: GetConversationActivityInput) -> None:
        """
        Get a specific conversation by ID.
        """
        db = Session()

        try:
            agent = get_eval_agent()

            conversation = (
                db
                .query(Conversation)
                .filter(Conversation.id == input.conversation_id)
                .first()
            )

            if not conversation:
                raise Exception(
                    f"Conversation {input.conversation_id} not found"
                )

            # Find all objectives for the simulation
            simulation_objectives = (
                db
                .query(SimulationObjective)
                .filter(
                    SimulationObjective.simulation_id == input.simulation_id,
                )
                .all()
            )

            if len(simulation_objectives) == 0:
                # No objectives to evaluate against, mark as completed
                conversation.evaluation_status = EvaluationStatus.COMPLETED
                db.commit()
                return

            # Query all needed versions at once
            objective_versions = (
                db
                .query(ObjectiveVersion)
                .filter(
                    tuple_(ObjectiveVersion.objective_id, ObjectiveVersion.id)
                    .in_([
                        (obj.objective_id, obj.objective_version_id)
                        for obj in simulation_objectives
                    ])
                )
                .all()
            )

            objective_version_map = {
                (v.objective_id, v.id): v for v in objective_versions
            }

            objectives: list[dict[str, Any]] = []

            for obj in simulation_objectives:
                version_key = (obj.objective_id, obj.objective_version_id)
                version = objective_version_map.get(version_key)

                if version:
                    objective: dict[str, Any] = {
                        "id": obj.objective_id,
                        "name": version.name,
                        "criteria": version.criteria,
                    }
                    objectives.append(objective)

            items = (
                db
                .query(ConversationItem)
                .filter(
                    ConversationItem.conversation_id == input.conversation_id,
                )
                .order_by(asc(ConversationItem.created_at))
                .all()
            )

            history: list[dict[str, Any]] = []

            for item in items:
                # Only message items are considered
                if item.type != "message":
                    continue

                content: list[dict[str, Any]] = []

                for block in item.content:
                    # For now only text blocks are considered
                    if block["type"] != "text":
                        continue

                    content.append({
                        "type": block["type"],
                        "text": block["text"],
                    })

                history.append({
                    "role": item.role,
                    "content": content,
                })

            result = await agent.evaluate(objectives, history)

            evaluations: list[ConversationEvaluation] = []

            for evaluation in result.evaluations:
                objective = next((
                    obj for obj in simulation_objectives
                    if obj.objective_id == evaluation.objective_id
                ), None)

                if not objective:
                    continue

                now = datetime.now(tz=timezone.utc)

                evaluations.append(ConversationEvaluation(
                    id=evaluation.objective_id,
                    conversation_id=input.conversation_id,
                    created_at=now,
                    objective_id=objective.objective_id,
                    objective_version_id=objective.objective_version_id,
                    reason=evaluation.reason,
                    score=evaluation.score,
                    updated_at=now,
                ))

            # Remove any existing evaluations and add the new ones
            # TODO: Optimize this
            existing_evaluations = (
                db
                .query(ConversationEvaluation)
                .filter(
                    ConversationEvaluation.conversation_id == input.conversation_id,
                )
                .all()
            )

            for evaluation in existing_evaluations:
                db.delete(evaluation)

            db.flush()
            db.add_all(evaluations)
            db.refresh(conversation)

            conversation.evaluation_status = EvaluationStatus.COMPLETED

            db.commit()

        finally:
            db.close()

    return run
