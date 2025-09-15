from typing import Callable

from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker
from temporalio import activity

from src.db.models import Conversation
from src.utils.mapping.conversation import conversation_model_to_dto
from src.worker.constants import GET_CONVERSATION_ACTIVITY_ID
from src.worker.types import (
    GetConversationActivityInput,
    GetConversationActivityOutput,
)


def get_conversation_activity(engine: Engine) -> Callable:
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    @activity.defn(name=GET_CONVERSATION_ACTIVITY_ID)
    async def run(
        input: GetConversationActivityInput
    ) -> GetConversationActivityOutput:
        """
        Get a specific conversation by ID.
        """
        db = Session()

        try:
            conversation = (
                db
                .query(Conversation)
                .filter(
                    Conversation.id == input.conversation_id,
                    Conversation.simulation_id == input.simulation_id,
                )
                .first()
            )

            if not conversation:
                return GetConversationActivityOutput(conversation=None)

            return GetConversationActivityOutput(
                conversation=conversation_model_to_dto(conversation),
            )
        finally:
            db.close()

    return run
