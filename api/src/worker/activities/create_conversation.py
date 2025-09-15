import string
from typing import Callable

import nanoid
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker
from temporalio import activity

from src.db.models import Conversation
from src.types import ConversationStatus, EvaluationStatus
from src.utils.mapping.conversation import conversation_model_to_dto
from src.worker.constants import CREATE_CONVERSATION_ACTIVITY_ID
from src.worker.types import (
    CreateConversationActivityInput,
    CreateConversationActivityOutput,
)


def create_conversation_activity(engine: Engine) -> Callable:
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    @activity.defn(name=CREATE_CONVERSATION_ACTIVITY_ID)
    async def run(
        input: CreateConversationActivityInput,
    ) -> CreateConversationActivityOutput:
        """
        Create a new conversation for a simulation.
        """
        db = Session()

        try:
            conversation = Conversation(
                id=nanoid.generate(
                    alphabet=string.ascii_letters + string.digits
                ),
                evaluation_status=EvaluationStatus.PENDING,
                persona_id=input.persona_id,
                simulation_id=input.simulation_id,
                status=ConversationStatus.QUEUED,
            )

            # TODO: We automatically set conversation status to QUEUED
            #  but we should have a better mechanism to determine this.
            #  For example, we should wait for the persona to be ready to
            #  handle a new conversation.

            db.add(conversation)
            db.commit()
            db.refresh(conversation)

            return CreateConversationActivityOutput(
                conversation=conversation_model_to_dto(conversation),
            )
        finally:
            db.close()

    return run
