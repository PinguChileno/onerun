from typing import Callable

from sqlalchemy import Engine, func
from sqlalchemy.orm import sessionmaker
from temporalio import activity

from src.db.models import Persona
from src.worker.constants import GET_PERSONA_COUNT_ACTIVITY_ID
from src.worker.types import (
    GetPersonaCountActivityInput,
    GetPersonaCountActivityOutput,
)


def get_persona_count_activity(engine: Engine) -> Callable:
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    @activity.defn(name=GET_PERSONA_COUNT_ACTIVITY_ID)
    async def run(
        input: GetPersonaCountActivityInput
    ) -> GetPersonaCountActivityOutput:
        """
        Get personas count for a simulation.
        """
        db = Session()

        try:
            simulation_id = input.simulation_id

            query = (
                db
                .query(func.count(Persona.id))
                .filter(Persona.simulation_id == simulation_id)
            )

            if input.approval_status:
                query = query.filter(
                    Persona.approval_status == input.approval_status
                )

            count = query.scalar() or 0

            return GetPersonaCountActivityOutput(count=count)

        finally:
            db.close()

    return run
