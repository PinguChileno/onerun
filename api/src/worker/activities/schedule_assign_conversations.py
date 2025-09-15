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
    ASSIGN_CONVERSATIONS_WORKFLOW_ID,
    SCHEDULE_ASSIGN_CONVERSATIONS_ACTIVITY_ID,
    MAIN_QUEUE_ID,
)
from src.worker.types import (
    AssignConversationsWorkflowInput,
    ScheduleAssignConversationsActivityInput,
)


def schedule_assign_conversations_activity(
    client: Client,
) -> Callable:
    logger = getLogger("schedule_assign_conversations")

    @activity.defn(name=SCHEDULE_ASSIGN_CONVERSATIONS_ACTIVITY_ID)
    async def run(input: ScheduleAssignConversationsActivityInput) -> None:
        """
        Schedule the assign conversations workflow for a simulation.
        """
        project_id = input.project_id
        simulation_id = input.simulation_id

        logger.debug(
            f"Scheduling assign conversations workflow for {simulation_id}"
        )

        handle = await client.create_schedule(
            f"assign_conversations:{simulation_id}",
            Schedule(
                action=ScheduleActionStartWorkflow(
                    ASSIGN_CONVERSATIONS_WORKFLOW_ID,
                    AssignConversationsWorkflowInput(
                        project_id=project_id,
                        simulation_id=simulation_id,
                    ),
                    id=f"assign_conversations:{simulation_id}",
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

        logger.debug(
            f"Scheduled assign conversations workflow for {simulation_id}"
        )

    return run
