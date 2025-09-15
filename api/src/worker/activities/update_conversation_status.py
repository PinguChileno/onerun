from typing import Callable

from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker
from temporalio import activity

from src.db.models import Conversation
from src.worker.constants import UPDATE_CONVERSATION_STATUS_ACTIVITY_ID
from src.worker.types import UpdateConversationStatusActivityInput


def update_conversation_status_activity(engine: Engine) -> Callable:
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    @activity.defn(name=UPDATE_CONVERSATION_STATUS_ACTIVITY_ID)
    async def run(
        input: UpdateConversationStatusActivityInput,
    ) -> None:
        """
        Update the status of a conversation.
        """
        db = Session()

        try:
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

            if input.status:
                conversation.status = input.status

            if input.evaluation_status:
                conversation.evaluation_status = input.evaluation_status

            db.commit()
        finally:
            db.close()

    return run
