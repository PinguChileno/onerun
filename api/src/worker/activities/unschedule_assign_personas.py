from logging import getLogger
from typing import Callable

from temporalio import activity
from temporalio.client import Client
from temporalio.service import RPCError, RPCStatusCode

from src.worker.constants import UNSCHEDULE_ASSIGN_PERSONAS_ACTIVITY_ID
from src.worker.types import UnscheduleAssignPersonasActivityInput


def unschedule_assign_personas_activity(client: Client) -> Callable:
    logger = getLogger("unschedule_assign_personas")

    @activity.defn(name=UNSCHEDULE_ASSIGN_PERSONAS_ACTIVITY_ID)
    async def run(input: UnscheduleAssignPersonasActivityInput) -> None:
        """
        Unschedule the assign personas workflow for a simulation.
        """
        simulation_id = input.simulation_id

        logger.debug(
            f"Unscheduling assign personas workflow for {simulation_id}"
        )

        schedule_id = f"assign_personas:{simulation_id}"
        handle = client.get_schedule_handle(schedule_id)

        try:
            await handle.delete()

            logger.debug(
                f"Unscheduled assign personas workflow for {simulation_id}"
            )
        except RPCError as e:
            if e.status not in (
                RPCStatusCode.NOT_FOUND,
                RPCStatusCode.FAILED_PRECONDITION,
            ):
                raise

            if input.raise_on_missing:
                raise

            logger.exception("Schedule not found or already deleted")

    return run
