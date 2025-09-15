from datetime import timedelta
from logging import getLogger

from temporalio import workflow
from temporalio.common import RetryPolicy

from src.types import SimulationDTO, SimulationStatus
from src.worker.constants import (
    CANCEL_SIMULATION_WORKFLOW_ID,
    GET_SIMULATION_ACTIVITY_ID,
    MAIN_QUEUE_ID,
    UNSCHEDULE_ASSIGN_CONVERSATIONS_ACTIVITY_ID,
    UNSCHEDULE_ASSIGN_PERSONAS_ACTIVITY_ID,
    UNSCHEDULE_CHECK_SIMULATION_ACTIVITY_ID,
    UPDATE_SIMULATION_STATUS_ACTIVITY_ID,
)
from src.worker.types import (
    CancelSimulationWorkflowInput,
    GetSimulationActivityInput,
    GetSimulationActivityOutput,
    UnscheduleAssignConversationsActivityInput,
    UnscheduleAssignPersonasActivityInput,
    UnscheduleCheckSimulationActivityInput,
    UpdateSimulationStatusActivityInput,
)


logger = getLogger("CancelSimulationWorkflow")
logger.setLevel("DEBUG")


@workflow.defn(name=CANCEL_SIMULATION_WORKFLOW_ID)
class CancelSimulationWorkflow:
    """
    Cancel a simulation process.
    """

    @workflow.run
    async def run(self, input: CancelSimulationWorkflowInput) -> str:
        project_id = input.project_id
        simulation_id = input.simulation_id

        # TODO Add support for force flag

        logger.debug(f"Started for simulation {simulation_id}")

        simulation = await self._get_simulation(
            project_id=project_id,
            simulation_id=simulation_id,
        )

        if not simulation:
            raise Exception(f"Simulation {simulation_id} does not exist")

        if simulation.status in [
            SimulationStatus.CANCELED,
            SimulationStatus.COMPLETED,
            SimulationStatus.EXPIRED,
            SimulationStatus.FAILED,
            SimulationStatus.PENDING,
        ]:
            # In these cases, just ensure cleanup and return
            await self._cleanup(project_id, simulation_id)
            return

        # Stop any active schedules
        await self._cleanup(project_id, simulation_id)

        await self._mark_as_canceled(project_id, simulation_id)

    async def _cleanup(self, project_id: str, simulation_id: str) -> None:
        await workflow.execute_activity(
            UNSCHEDULE_CHECK_SIMULATION_ACTIVITY_ID,
            UnscheduleCheckSimulationActivityInput(
                project_id=project_id,
                simulation_id=simulation_id,
                raise_on_missing=False,
            ),
            task_queue=MAIN_QUEUE_ID,
            start_to_close_timeout=timedelta(minutes=1),
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=15),
                maximum_attempts=3,
            ),
        )

        await workflow.execute_activity(
            UNSCHEDULE_ASSIGN_PERSONAS_ACTIVITY_ID,
            UnscheduleAssignPersonasActivityInput(
                project_id=project_id,
                simulation_id=simulation_id,
                raise_on_missing=False,
            ),
            task_queue=MAIN_QUEUE_ID,
            start_to_close_timeout=timedelta(minutes=1),
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=15),
                maximum_attempts=3,
            ),
        )

        await workflow.execute_activity(
            UNSCHEDULE_ASSIGN_CONVERSATIONS_ACTIVITY_ID,
            UnscheduleAssignConversationsActivityInput(
                project_id=project_id,
                simulation_id=simulation_id,
                raise_on_missing=False,
            ),
            task_queue=MAIN_QUEUE_ID,
            start_to_close_timeout=timedelta(minutes=1),
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=15),
                maximum_attempts=3,
            ),
        )

    async def _get_simulation(
        self,
        project_id: str,
        simulation_id: str,
    ) -> SimulationDTO | None:
        result: GetSimulationActivityOutput = (
            await workflow.execute_activity(
                GET_SIMULATION_ACTIVITY_ID,
                GetSimulationActivityInput(
                    project_id=project_id,
                    simulation_id=simulation_id,
                ),
                task_queue=MAIN_QUEUE_ID,
                result_type=GetSimulationActivityOutput,
                start_to_close_timeout=timedelta(minutes=1),
                retry_policy=RetryPolicy(
                    initial_interval=timedelta(seconds=15),
                    maximum_attempts=3,
                ),
            )
        )

        return result.simulation

    async def _mark_as_canceled(
        self,
        project_id: str,
        simulation_id: str,
    ) -> None:
        await workflow.execute_activity(
            UPDATE_SIMULATION_STATUS_ACTIVITY_ID,
            UpdateSimulationStatusActivityInput(
                project_id=project_id,
                simulation_id=simulation_id,
                status=SimulationStatus.CANCELED,
            ),
            task_queue=MAIN_QUEUE_ID,
            start_to_close_timeout=timedelta(minutes=1),
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=15),
                maximum_attempts=3,
            ),
        )
