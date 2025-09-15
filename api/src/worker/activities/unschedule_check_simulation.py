from logging import getLogger
from typing import Callable

from temporalio import activity
from temporalio.client import Client
from temporalio.service import RPCError, RPCStatusCode

from src.worker.constants import UNSCHEDULE_CHECK_SIMULATION_ACTIVITY_ID
from src.worker.types import UnscheduleCheckSimulationActivityInput


def unschedule_check_simulation_activity(client: Client) -> Callable:
    logger = getLogger("unschedule_check_simulation")

    @activity.defn(name=UNSCHEDULE_CHECK_SIMULATION_ACTIVITY_ID)
    async def run(input: UnscheduleCheckSimulationActivityInput) -> None:
        """
        Unschedule the check simulation workflow for a simulation.
        """
        simulation_id = input.simulation_id

        logger.debug(
            f"Unscheduling check simulation workflow for {simulation_id}"
        )

        schedule_id = f"check_simulation:{simulation_id}"
        handle = client.get_schedule_handle(schedule_id)

        try:
            await handle.delete()

            logger.debug(
                f"Unscheduled check simulation workflow for {simulation_id}"
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
