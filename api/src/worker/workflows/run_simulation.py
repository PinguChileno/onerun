from datetime import timedelta
from logging import getLogger

from temporalio import workflow
from temporalio.common import RetryPolicy

from src.types import SimulationDTO, SimulationStatus
from src.worker.constants import (
    GET_SIMULATION_ACTIVITY_ID,
    MAIN_QUEUE_ID,
    SCHEDULE_ASSIGN_CONVERSATIONS_ACTIVITY_ID,
    SCHEDULE_ASSIGN_PERSONAS_ACTIVITY_ID,
    SCHEDULE_CHECK_SIMULATION_ACTIVITY_ID,
    RUN_SIMULATION_WORKFLOW_ID,
    UPDATE_SIMULATION_STATUS_ACTIVITY_ID,
)
from src.worker.types import (
    GetSimulationActivityInput,
    GetSimulationActivityOutput,
    ScheduleAssignConversationsActivityInput,
    ScheduleAssignPersonasActivityInput,
    ScheduleCheckSimulationActivityInput,
    RunSimulationWorkflowInput,
    UpdateSimulationStatusActivityInput,
)


logger = getLogger("RunSimulationWorkflow")
logger.setLevel("DEBUG")


@workflow.defn(name=RUN_SIMULATION_WORKFLOW_ID)
class RunSimulationWorkflow:
    """Workflow to start a simulation process."""

    @workflow.run
    async def run(self, input: RunSimulationWorkflowInput) -> str:
        project_id = input.project_id
        simulation_id = input.simulation_id

        logger.debug(f"Started for simulation {simulation_id}")

        simulation = await self._get_simulation(
            project_id=project_id,
            simulation_id=simulation_id,
        )

        if not simulation:
            raise Exception(f"Simulation {simulation_id} does not exist")

        allowed_states: list[SimulationStatus] = [
            SimulationStatus.QUEUED,
            SimulationStatus.PENDING,
            SimulationStatus.CANCELED,
        ]

        if simulation.status not in allowed_states:
            raise Exception(
                f"Simulation {simulation_id} is in an invalid state"
                f" ({simulation.status})"
            )

        await self._mark_as_in_progress(project_id, simulation_id)
        await self._start_schedules(project_id, simulation_id)

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

    async def _mark_as_in_progress(
        self,
        project_id: str,
        simulation_id: str,
    ) -> None:
        await workflow.execute_activity(
            UPDATE_SIMULATION_STATUS_ACTIVITY_ID,
            UpdateSimulationStatusActivityInput(
                project_id=project_id,
                simulation_id=simulation_id,
                status=SimulationStatus.IN_PROGRESS,
            ),
            task_queue=MAIN_QUEUE_ID,
            start_to_close_timeout=timedelta(minutes=1),
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=15),
                maximum_attempts=3,
            ),
        )

    async def _start_schedules(
        self,
        project_id: str,
        simulation_id: str,
    ) -> None:
        await workflow.execute_activity(
            SCHEDULE_ASSIGN_PERSONAS_ACTIVITY_ID,
            ScheduleAssignPersonasActivityInput(
                project_id=project_id,
                simulation_id=simulation_id
            ),
            task_queue=MAIN_QUEUE_ID,
            start_to_close_timeout=timedelta(minutes=1),
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=15),
                maximum_attempts=5,
            ),
        )

        await workflow.execute_activity(
            SCHEDULE_ASSIGN_CONVERSATIONS_ACTIVITY_ID,
            ScheduleAssignConversationsActivityInput(
                project_id=project_id,
                simulation_id=simulation_id
            ),
            task_queue=MAIN_QUEUE_ID,
            start_to_close_timeout=timedelta(minutes=1),
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=15),
                maximum_attempts=5,
            ),
        )

        await workflow.execute_activity(
            SCHEDULE_CHECK_SIMULATION_ACTIVITY_ID,
            ScheduleCheckSimulationActivityInput(
                project_id=project_id,
                simulation_id=simulation_id
            ),
            task_queue=MAIN_QUEUE_ID,
            start_to_close_timeout=timedelta(minutes=1),
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=15),
                maximum_attempts=5,
            ),
        )
