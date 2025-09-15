from datetime import timedelta
from logging import getLogger

from temporalio import workflow
from temporalio.common import RetryPolicy

from src.types import SimulationDTO, SimulationStatus
from src.worker.constants import (
    ASSIGN_CONVERSATIONS_WORKFLOW_ID,
    CREATE_CONVERSATION_ACTIVITY_ID,
    GET_CONVERSATION_CANDIDATES_ACTIVITY_ID,
    GET_CONVERSATIONS_COUNT_ACTIVITY_ID,
    GET_SIMULATION_ACTIVITY_ID,
    MAIN_QUEUE_ID,
    UNSCHEDULE_ASSIGN_CONVERSATIONS_ACTIVITY_ID,
)
from src.worker.types import (
    AssignConversationsWorkflowInput,
    CreateConversationActivityInput,
    CreateConversationActivityOutput,
    GetConversationCandidatesActivityInput,
    GetConversationCandidatesActivityOutput,
    GetConversationsCountActivityInput,
    GetConversationsCountActivityOutput,
    GetSimulationActivityInput,
    GetSimulationActivityOutput,
    UnscheduleAssignConversationsActivityInput,
)


logger = getLogger("AssignConversationsWorkflow")
logger.setLevel("DEBUG")


@workflow.defn(name=ASSIGN_CONVERSATIONS_WORKFLOW_ID)
class AssignConversationsWorkflow:
    """
    Assign conversations to approved personas for a simulation.

    This workflow runs as a scheduled cron job.
    """

    @workflow.run
    async def run(self, input: AssignConversationsWorkflowInput) -> None:
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

        target_conversations = simulation.target_conversations
        target_personas = simulation.target_personas

        if target_conversations < 1 or target_personas < 1:
            logger.error(f"Invalid targets for simulation {simulation_id}")
            await self._cleanup(project_id, simulation_id)
            return

        remaining_conversations = await self._count_remaining(
            project_id=project_id,
            simulation_id=simulation_id,
            target=target_conversations,
        )

        if remaining_conversations == 0:
            logger.debug(
                f"All conversations assigned for simulation {simulation_id}"
            )
            await self._cleanup(project_id, simulation_id)
            return

        candidates = await self._get_candidates(
            project_id=project_id,
            simulation_id=simulation_id,
            target_personas=target_personas,
            target_conversations=target_conversations,
            remaining_conversations=remaining_conversations,
        )

        for candidate in candidates:
            try:
                await self._create_conversation(
                    project_id=project_id,
                    simulation_id=simulation_id,
                    persona_id=candidate.id,
                )
            except Exception as e:
                # Skip candidate and let next scheduled run
                # to select a new candidate
                logger.error(
                    f"Failed to create conversation for {simulation_id}: {e}"
                )

    async def _cleanup(self, project_id: str, simulation_id: str) -> None:
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

    async def _count_remaining(
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
                    simulation_id=simulation_id
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

        current = result.count
        return max(0, target - current)

    async def _get_candidates(
        self,
        project_id: str,
        simulation_id: str,
        target_personas: int,
        target_conversations: int,
        remaining_conversations: int
    ):
        # Determine filtering parameters
        if target_personas > target_conversations:
            # Only some personas will get conversations - prioritize with 0
            candidates_input = GetConversationCandidatesActivityInput(
                project_id=project_id,
                simulation_id=simulation_id,
                limit=min(10, remaining_conversations),
                prioritize=True,
            )
        else:
            # Distribute conversations as evenly as possible
            remainder = target_conversations % target_personas
            target_per_persona = target_conversations // target_personas
            # For candidate selection, allow up to base + 1 for the first
            # 'remainder' personas
            # This logic assumes candidate selection will handle the
            # extra assignment
            max_per_persona = target_per_persona + (1 if remainder > 0 else 0)
            candidates_input = GetConversationCandidatesActivityInput(
                project_id=project_id,
                simulation_id=simulation_id,
                limit=min(10, remaining_conversations),
                max_per_persona=max_per_persona,
            )

        result: GetConversationCandidatesActivityOutput = (
            await workflow.execute_activity(
                GET_CONVERSATION_CANDIDATES_ACTIVITY_ID,
                candidates_input,
                task_queue=MAIN_QUEUE_ID,
                result_type=GetConversationCandidatesActivityOutput,
                start_to_close_timeout=timedelta(minutes=1),
                retry_policy=RetryPolicy(
                    initial_interval=timedelta(seconds=15),
                    maximum_attempts=3,
                ),
            )
        )

        return result.candidates

    async def _create_conversation(
        self,
        project_id: str,
        simulation_id: str,
        persona_id: str,
    ):
        result: CreateConversationActivityOutput = (
            await workflow.execute_activity(
                CREATE_CONVERSATION_ACTIVITY_ID,
                CreateConversationActivityInput(
                    project_id=project_id,
                    simulation_id=simulation_id,
                    persona_id=persona_id,
                ),
                task_queue=MAIN_QUEUE_ID,
                result_type=CreateConversationActivityOutput,
                start_to_close_timeout=timedelta(minutes=1),
                retry_policy=RetryPolicy(
                    initial_interval=timedelta(seconds=15),
                    maximum_attempts=3,
                ),
            )
        )

        return result.conversation
