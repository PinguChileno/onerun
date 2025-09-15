from typing import Callable

from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker
from temporalio import activity

from src.db.models import Conversation
from src.utils.mapping.conversation import conversation_model_to_dto
from src.worker.constants import LIST_CONVERSATIONS_ACTIVITY_ID
from src.worker.types import (
    ListConversationsActivityInput,
    ListConversationsActivityOutput,
)


def list_conversations_activity(engine: Engine) -> Callable:
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    @activity.defn(name=LIST_CONVERSATIONS_ACTIVITY_ID)
    async def run(
        input: ListConversationsActivityInput
    ) -> ListConversationsActivityOutput:
        """
        List conversations for a simulation.
        """
        db = Session()

        try:
            query = (
                db
                .query(Conversation)
                .filter(Conversation.simulation_id == input.simulation_id)
            )

            if input.evaluation_status:
                query = query.filter(
                    Conversation.evaluation_status == input.evaluation_status
                )

            if input.status:
                query = query.filter(Conversation.status == input.status)

            conversations = query.all()

            return ListConversationsActivityOutput(
                conversations=[
                    conversation_model_to_dto(conversation)
                    for conversation in conversations
                ],
            )
        finally:
            db.close()

    return run
