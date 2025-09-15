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
    ASSIGN_PERSONAS_WORKFLOW_ID,
    SCHEDULE_ASSIGN_PERSONAS_ACTIVITY_ID,
    MAIN_QUEUE_ID,
)
from src.worker.types import (
    AssignPersonasWorkflowInput,
    ScheduleAssignPersonasActivityInput,
)


def schedule_assign_personas_activity(
    client: Client,
) -> Callable:
    logger = getLogger("schedule_assign_personas")

    @activity.defn(name=SCHEDULE_ASSIGN_PERSONAS_ACTIVITY_ID)
    async def run(input: ScheduleAssignPersonasActivityInput) -> None:
        """
        Schedule the assign personas workflow for a simulation.
        """
        project_id = input.project_id
        simulation_id = input.simulation_id

        logger.debug(
            f"Scheduling assign personas workflow for {simulation_id}"
        )

        handle = await client.create_schedule(
            f"assign_personas:{simulation_id}",
            Schedule(
                action=ScheduleActionStartWorkflow(
                    ASSIGN_PERSONAS_WORKFLOW_ID,
                    AssignPersonasWorkflowInput(
                        project_id=project_id,
                        simulation_id=simulation_id,
                    ),
                    id=f"assign_personas:{simulation_id}",
                    task_queue=MAIN_QUEUE_ID,
                ),
                spec=ScheduleSpec(
                    intervals=[
                        ScheduleIntervalSpec(every=timedelta(minutes=1))
                    ],
                ),
                state=ScheduleState(paused=False),
            ),
        )

        await handle.trigger(overlap=ScheduleOverlapPolicy.SKIP)

        logger.debug(f"Scheduled assign personas workflow for {simulation_id}")

    return run
