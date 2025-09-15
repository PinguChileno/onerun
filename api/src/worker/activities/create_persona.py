from functools import lru_cache
import string
from typing import Callable

import nanoid
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker
from temporalio import activity

from src.db.models import Persona
from src.utils.mapping.persona import persona_model_to_dto
from src.worker.constants import CREATE_PERSONA_ACTIVITY_ID
from src.worker.types import (
    CreatePersonaActivityInput,
    CreatePersonaActivityOutput,
)


@lru_cache(maxsize=1)
def get_persona_agent():
    """
    Cached factory for PersonaAgent to avoid recreating it.

    NOTE: Workflows fail if agent is imported at top level.
    """
    from src.services.persona_agent import PersonaAgent
    return PersonaAgent()


@lru_cache(maxsize=1)
def get_scenario_agent():
    """
    Cached factory for ScenarioAgent to avoid recreating it.

    NOTE: Workflows fail if agent is imported at top level.
    """
    from src.services.scenario_agent import ScenarioAgent
    return ScenarioAgent()


def create_persona_activity(engine: Engine) -> Callable:
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    @activity.defn(name=CREATE_PERSONA_ACTIVITY_ID)
    async def run(
        input: CreatePersonaActivityInput,
    ) -> CreatePersonaActivityOutput:
        """
        Create a new persona for a simulation.
        """
        db = Session()

        try:
            # Generate persona attributes and summary
            persona_agent = get_persona_agent()
            persona_generation = await persona_agent.generate_persona()

            # Generate scenario context for this persona
            scenario_agent = get_scenario_agent()
            scenario_context = await scenario_agent.generate_context(
                scenario=input.scenario,
                agent_description=input.agent_description,
                persona_attributes=persona_generation.attributes.model_dump(),
            )

            persona = Persona(
                id=nanoid.generate(
                    alphabet=string.ascii_letters + string.digits
                ),
                approval_status=(
                    "approved" if input.auto_approve else "pending"
                ),
                attributes=persona_generation.attributes.model_dump(),
                auto_approve=input.auto_approve,
                purpose=scenario_context.purpose,
                simulation_id=input.simulation_id,
                story=scenario_context.story,
                summary=persona_generation.summary,
            )

            db.add(persona)
            db.commit()

            db.refresh(persona)  # Refresh to get the latest data

            return CreatePersonaActivityOutput(
                persona=persona_model_to_dto(persona),
            )
        finally:
            db.close()

    return run
