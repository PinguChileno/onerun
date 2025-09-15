from typing import Callable

from sqlalchemy import Engine, func
from sqlalchemy.orm import sessionmaker
from temporalio import activity

from src.db.models import Conversation
from src.worker.constants import (
    GET_CONVERSATIONS_COUNT_ACTIVITY_ID
)
from src.worker.types import (
    GetConversationsCountActivityInput,
    GetConversationsCountActivityOutput,
)


def get_conversations_count_activity(engine: Engine) -> Callable:
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    @activity.defn(name=GET_CONVERSATIONS_COUNT_ACTIVITY_ID)
    async def run(
        input: GetConversationsCountActivityInput
    ) -> GetConversationsCountActivityOutput:
        """
        Get conversation count for a simulation.
        """
        db = Session()

        try:
            simulation_id = input.simulation_id

            query = (
                db
                .query(func.count(Conversation.id))
                .filter(Conversation.simulation_id == simulation_id)
            )

            if input.evaluation_status:
                query = query.filter(
                    Conversation.evaluation_status == input.evaluation_status
                )

            if input.status:
                query = query.filter(Conversation.status == input.status)

            count = query.scalar() or 0

            return GetConversationsCountActivityOutput(count=count)

        finally:
            db.close()

    return run
