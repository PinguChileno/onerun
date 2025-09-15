from datetime import timedelta
from logging import getLogger
from typing import Callable

from temporalio import activity
from temporalio.client import (
    Client,
    Schedule,
    ScheduleActionStartWorkflow,
    ScheduleIntervalSpec,
    ScheduleOverlapPolicy,
    ScheduleSpec,
    ScheduleState,
)

from src.worker.constants import (
    SCHEDULE_CHECK_SIMULATION_ACTIVITY_ID,
    CHECK_SIMULATION_WORKFLOW_ID,
    MAIN_QUEUE_ID,
)
from src.worker.types import (
    ScheduleCheckSimulationActivityInput,
    CheckSimulationWorkflowInput,
)


def schedule_check_simulation_activity(
    client: Client,
) -> Callable:
    logger = getLogger("schedule_check_simulation")

    @activity.defn(name=SCHEDULE_CHECK_SIMULATION_ACTIVITY_ID)
    async def run(input: ScheduleCheckSimulationActivityInput) -> None:
        """
        Schedule the check simulation workflow for a simulation.
        """
        project_id = input.project_id
        simulation_id = input.simulation_id

        logger.debug(
            f"Scheduling check simulation workflow for {simulation_id}"
        )

        handle = await client.create_schedule(
            f"check_simulation:{simulation_id}",
            Schedule(
                action=ScheduleActionStartWorkflow(
                    CHECK_SIMULATION_WORKFLOW_ID,
                    CheckSimulationWorkflowInput(
                        project_id=project_id,
                        simulation_id=simulation_id,
                    ),
                    id=f"check_simulation:{simulation_id}",
                    task_queue=MAIN_QUEUE_ID,
                ),
                spec=ScheduleSpec(
                    intervals=[
                        ScheduleIntervalSpec(every=timedelta(minutes=1))
                    ]
                ),
                state=ScheduleState(paused=False),
            ),
            trigger_immediately=False,
        )

        await handle.trigger(overlap=ScheduleOverlapPolicy.SKIP)

        logger.debug(
            f"Scheduled check simulation workflow for {simulation_id}")

    return run
