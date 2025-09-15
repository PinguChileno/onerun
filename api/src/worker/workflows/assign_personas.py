from datetime import timedelta
from logging import getLogger

from temporalio import workflow
from temporalio.common import RetryPolicy

from src.types import ApprovalStatus, SimulationDTO, SimulationStatus
from src.worker.constants import (
    ASSIGN_PERSONAS_WORKFLOW_ID,
    CREATE_PERSONA_ACTIVITY_ID,
    GET_PERSONA_COUNT_ACTIVITY_ID,
    GET_SIMULATION_ACTIVITY_ID,
    MAIN_QUEUE_ID,
    UNSCHEDULE_ASSIGN_PERSONAS_ACTIVITY_ID,
)
from src.worker.types import (
    AssignPersonasWorkflowInput,
    CreatePersonaActivityInput,
    CreatePersonaActivityOutput,
    GetPersonaCountActivityInput,
    GetPersonaCountActivityOutput,
    GetSimulationActivityInput,
    GetSimulationActivityOutput,
    UnscheduleAssignPersonasActivityInput,
)


logger = getLogger("AssignPersonasWorkflow")
logger.setLevel("DEBUG")


@workflow.defn(name=ASSIGN_PERSONAS_WORKFLOW_ID)
class AssignPersonasWorkflow:
    """
    Assign personas to a simulation.

    This workflow runs as a scheduled cron job.
    """

    @workflow.run
    async def run(self, input: AssignPersonasWorkflowInput) -> None:
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

        target_personas = simulation.target_personas

        if target_personas < 1:
            logger.error(f"Invalid targets for simulation {simulation_id}")
            await self._cleanup(project_id, simulation_id)
            return

        remaining_personas = await self._count_remaining(
            project_id=project_id,
            simulation_id=simulation_id,
            target=target_personas,
        )

        if remaining_personas == 0:
            logger.debug(
                f"All personas assigned for simulation {simulation_id}"
            )
            await self._cleanup(project_id, simulation_id)
            return

        for _ in range(remaining_personas):
            await self._create_persona(
                project_id=simulation.project_id,
                simulation_id=simulation_id,
                scenario=simulation.scenario,
                agent_description=simulation.agent.description,
                auto_approve=simulation.auto_approve,
            )

    async def _cleanup(self, project_id: str, simulation_id: str) -> None:
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

    async def _count_remaining(
        self,
        project_id: str,
        simulation_id: str,
        target: int,
    ) -> int:
        result: GetPersonaCountActivityOutput = (
            await workflow.execute_activity(
                GET_PERSONA_COUNT_ACTIVITY_ID,
                GetPersonaCountActivityInput(
                    project_id=project_id,
                    simulation_id=simulation_id,
                ),
                task_queue=MAIN_QUEUE_ID,
                result_type=GetPersonaCountActivityOutput,
                start_to_close_timeout=timedelta(minutes=1),
                retry_policy=RetryPolicy(
                    initial_interval=timedelta(seconds=15),
                    maximum_attempts=3,
                ),
            )
        )

        total = result.count

        result: GetPersonaCountActivityOutput = (
            await workflow.execute_activity(
                GET_PERSONA_COUNT_ACTIVITY_ID,
                GetPersonaCountActivityInput(
                    project_id=project_id,
                    simulation_id=simulation_id,
                    approval_status=ApprovalStatus.REJECTED,
                ),
                task_queue=MAIN_QUEUE_ID,
                result_type=GetPersonaCountActivityOutput,
                start_to_close_timeout=timedelta(minutes=1),
                retry_policy=RetryPolicy(
                    initial_interval=timedelta(seconds=15),
                    maximum_attempts=3,
                ),
            )
        )

        rejected = result.count

        return max(0, target - (total - rejected))

    async def _create_persona(
        self,
        project_id: str,
        simulation_id: str,
        scenario: str,
        agent_description: str,
        auto_approve: bool,
    ) -> None:
        await workflow.execute_activity(
            CREATE_PERSONA_ACTIVITY_ID,
            CreatePersonaActivityInput(
                project_id=project_id,
                simulation_id=simulation_id,
                scenario=scenario,
                agent_description=agent_description,
                auto_approve=auto_approve,
            ),
            task_queue=MAIN_QUEUE_ID,
            result_type=CreatePersonaActivityOutput,
            start_to_close_timeout=timedelta(minutes=5),
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=30),
                maximum_attempts=5,
            ),
        )

        logger.debug(f"Creating persona for simulation {simulation_id}")
