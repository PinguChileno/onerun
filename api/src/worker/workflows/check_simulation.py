from datetime import timedelta, timezone
from logging import getLogger

from temporalio import workflow
from temporalio.common import RetryPolicy

from src.types import EvaluationStatus, SimulationDTO, SimulationStatus
from src.worker.constants import (
    CHECK_SIMULATION_WORKFLOW_ID,
    GET_CONVERSATIONS_COUNT_ACTIVITY_ID,
    GET_SIMULATION_ACTIVITY_ID,
    MAIN_QUEUE_ID,
    UNSCHEDULE_CHECK_SIMULATION_ACTIVITY_ID,
    UPDATE_SIMULATION_STATUS_ACTIVITY_ID,
)
from src.worker.types import (
    CheckSimulationWorkflowInput,
    GetConversationsCountActivityInput,
    GetConversationsCountActivityOutput,
    GetSimulationActivityInput,
    GetSimulationActivityOutput,
    UnscheduleCheckSimulationActivityInput,
    UpdateSimulationStatusActivityInput,
)


logger = getLogger("CheckSimulationWorkflow")
logger.setLevel("DEBUG")


@workflow.defn(name=CHECK_SIMULATION_WORKFLOW_ID)
class CheckSimulationWorkflow:
    """
    Check if the simulation should be marked as completed, failed or expired.

    This workflow runs as a scheduled cron job.
    """

    @workflow.run
    async def run(self, input: CheckSimulationWorkflowInput) -> None:
        project_id = input.project_id
        simulation_id = input.simulation_id

        logger.debug(f"Started for simulation {simulation_id}")

        simulation = await self._get_simulation(
            project_id=project_id,
            simulation_id=simulation_id,
        )

        if not simulation:
            await self._cleanup(project_id, simulation_id)
            raise Exception(f"Simulation {simulation_id} does not exist")

        if simulation.status == SimulationStatus.PENDING:
            # Return and wait for next scheduled run
            return

        if simulation.status in [
            SimulationStatus.CANCELED,
            SimulationStatus.COMPLETED,
            SimulationStatus.EXPIRED,
            SimulationStatus.FAILED,
            SimulationStatus.PENDING,
        ]:
            # Cleanup and stop
            await self._cleanup(project_id, simulation_id)
            return

        if simulation.status != SimulationStatus.IN_PROGRESS:
            # This should not happen, unless an unknown status is encountered
            await self._cleanup(project_id, simulation_id)
            raise Exception(f"Simulation {simulation_id} is not in progress")

        is_expired = await self._check_expiration(simulation)

        if is_expired:
            await self._cleanup(project_id, simulation.id)
            raise Exception(f"Simulation {simulation.id} expired")

        is_completed = await self._check_conversations(
            project_id=project_id,
            simulation_id=simulation.id,
            target=simulation.target_conversations,
        )

        if not is_completed:
            # Return and wait for next scheduled run
            return

        await self._mark_as_completed(project_id, simulation.id)
        logger.debug(f"Simulation {simulation.id} completed!")

    async def _cleanup(self, project_id: str, simulation_id: str) -> None:
        await workflow.execute_activity(
            UNSCHEDULE_CHECK_SIMULATION_ACTIVITY_ID,
            UnscheduleCheckSimulationActivityInput(
                project_id=project_id,
                simulation_id=simulation_id
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

    async def _check_expiration(self, simulation: SimulationDTO) -> bool:
        now = workflow.datetime.now(timezone.utc)
        is_expired = False

        expires_at = simulation.expires_at
        if expires_at:
            # Ensure expires_at is timezone-aware
            if expires_at.tzinfo is None:
                expires_at = expires_at.replace(tzinfo=timezone.utc)
            is_expired = now > expires_at
        else:
            # Fallback: use 24h from creation if expires_at not set
            if simulation.created_at:
                is_expired = now - simulation.created_at > timedelta(hours=24)

        if is_expired:
            await workflow.execute_activity(
                UPDATE_SIMULATION_STATUS_ACTIVITY_ID,
                UpdateSimulationStatusActivityInput(
                    project_id=simulation.project_id,
                    simulation_id=simulation.id,
                    status=SimulationStatus.EXPIRED,
                ),
                task_queue=MAIN_QUEUE_ID,
                start_to_close_timeout=timedelta(minutes=1),
                retry_policy=RetryPolicy(
                    initial_interval=timedelta(seconds=15),
                    maximum_attempts=3,
                ),
            )

        return is_expired

    async def _check_conversations(
        self,
        project_id: str,
        simulation_id: str,
        target: int,
    ) -> int:
        result: GetConversationsCountActivityOutput = (
            await workflow.execute_activity(
                GET_CONVERSATIONS_COUNT_ACTIVITY_ID,
                GetConversationsCountActivityInput(
                    project_id=project_id,
                    simulation_id=simulation_id,
                    evaluation_status=EvaluationStatus.COMPLETED,
                ),
                task_queue=MAIN_QUEUE_ID,
                result_type=GetConversationsCountActivityOutput,
                start_to_close_timeout=timedelta(minutes=1),
                retry_policy=RetryPolicy(
                    initial_interval=timedelta(seconds=15),
                    maximum_attempts=3,
                ),
            )
        )

        evaluated = result.count

        return evaluated >= target

    async def _mark_as_completed(
        self,
        project_id: str,
        simulation_id: str,
    ) -> None:
        await workflow.execute_activity(
            UPDATE_SIMULATION_STATUS_ACTIVITY_ID,
            UpdateSimulationStatusActivityInput(
                project_id=project_id,
                simulation_id=simulation_id,
                status=SimulationStatus.COMPLETED
            ),
            task_queue=MAIN_QUEUE_ID,
            start_to_close_timeout=timedelta(minutes=1),
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=15),
                maximum_attempts=3,
            ),
        )
