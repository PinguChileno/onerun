from typing import Callable

from sqlalchemy import Engine, func
from sqlalchemy.orm import sessionmaker
from temporalio import activity

from src.db.models import Conversation, Persona
from src.types import ApprovalStatus
from src.worker.constants import GET_CONVERSATION_CANDIDATES_ACTIVITY_ID
from src.worker.types import (
    ConversationCandidate,
    GetConversationCandidatesActivityInput,
    GetConversationCandidatesActivityOutput,
)


def get_conversation_candidates_activity(engine: Engine) -> Callable:
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    @activity.defn(name=GET_CONVERSATION_CANDIDATES_ACTIVITY_ID)
    async def run(
        input: GetConversationCandidatesActivityInput
    ) -> GetConversationCandidatesActivityOutput:
        """
        Get approved personas that need conversations.
        """
        db = Session()

        try:
            simulation_id = input.simulation_id
            limit = input.limit or 10
            max_per_persona = input.max_per_persona
            prioritize = input.prioritize

            # Get approved personas with conversation counts
            query = (
                db
                .query(
                    Persona.id,
                    func.count(Conversation.id).label("conversation_count")
                )
                .outerjoin(
                    Conversation,
                    (Conversation.persona_id == Persona.id) &
                    (Conversation.simulation_id == simulation_id)
                )
                .filter(
                    Persona.simulation_id == simulation_id,
                    Persona.approval_status == ApprovalStatus.APPROVED
                )
                .group_by(Persona.id)
                .order_by(
                    func.count(Conversation.id),  # Fewer conversations first
                    func.random()  # Then random among ties
                )
            )

            # Apply filtering based on conversation limits
            # Note: prioritize takes precedence over max_per_persona
            if prioritize:
                query = query.having(func.count(Conversation.id) == 0)
            elif max_per_persona is not None and max_per_persona > 0:
                query = query.having(
                    func.count(Conversation.id) < max_per_persona
                )

            results = query.limit(limit).all()

            return GetConversationCandidatesActivityOutput(
                candidates=[
                    ConversationCandidate(
                        id=candidate.id,
                        conversation_count=candidate.conversation_count
                    )
                    for candidate in results
                ],
            )

        finally:
            db.close()

    return run
