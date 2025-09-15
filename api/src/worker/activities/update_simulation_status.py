from typing import Callable

from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker
from temporalio import activity

from src.db.models import Simulation
from src.worker.constants import UPDATE_SIMULATION_STATUS_ACTIVITY_ID
from src.worker.types import UpdateSimulationStatusActivityInput


def update_simulation_status_activity(engine: Engine) -> Callable:
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    @activity.defn(name=UPDATE_SIMULATION_STATUS_ACTIVITY_ID)
    async def run(
        input: UpdateSimulationStatusActivityInput,
    ) -> None:
        """
        Update the status of a simulation.
        """
        db = Session()

        try:
            simulation = (
                db
                .query(Simulation)
                .filter(Simulation.id == input.simulation_id)
                .first()
            )

            if not simulation:
                raise Exception(f"Simulation {input.simulation_id} not found")

            simulation.status = input.status

            db.commit()
        finally:
            db.close()

    return run
