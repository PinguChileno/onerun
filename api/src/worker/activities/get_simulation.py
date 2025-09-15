from typing import Callable

from sqlalchemy import Engine
from sqlalchemy.orm import joinedload, sessionmaker
from temporalio import activity

from src.db.models import Simulation
from src.utils.mapping.simulation import simulation_model_to_dto
from src.worker.constants import GET_SIMULATION_ACTIVITY_ID
from src.worker.types import (
    GetSimulationActivityInput,
    GetSimulationActivityOutput,
)


def get_simulation_activity(engine: Engine) -> Callable:
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    @activity.defn(name=GET_SIMULATION_ACTIVITY_ID)
    async def run(
        input: GetSimulationActivityInput,
    ) -> GetSimulationActivityOutput:
        """
        Get simulation details by ID.
        """
        db = Session()

        try:
            # TODO: Maybe have `includes` field to specify related entities

            simulation = (
                db
                .query(Simulation)
                .options(joinedload(Simulation.agent))
                .filter(
                    Simulation.id == input.simulation_id,
                    Simulation.project_id == input.project_id,
                )
                .first()
            )

            if not simulation:
                return GetSimulationActivityOutput(simulation=None)

            return GetSimulationActivityOutput(
                simulation=simulation_model_to_dto(simulation),
            )
        finally:
            db.close()

    return run
