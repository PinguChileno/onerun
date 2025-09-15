from datetime import timedelta
from logging import getLogger

from temporalio import workflow
from temporalio.common import RetryPolicy

from src.types import (
    ConversationDTO,
    EvaluationStatus,
    SimulationDTO,
    SimulationStatus,
)
from src.worker.constants import (
    EVALUATE_CONVERSATION_ACTIVITY_ID,
    EVALUATE_CONVERSATION_WORKFLOW_ID,
    GET_CONVERSATION_ACTIVITY_ID,
    GET_SIMULATION_ACTIVITY_ID,
    MAIN_QUEUE_ID,
    UPDATE_CONVERSATION_STATUS_ACTIVITY_ID,
)
from src.worker.types import (
    EvaluateConversationActivityInput,
    EvaluateConversationWorkflowInput,
    GetConversationActivityInput,
    GetConversationActivityOutput,
    GetSimulationActivityInput,
    GetSimulationActivityOutput,
    UpdateConversationStatusActivityInput,
)


logger = getLogger("EvaluateConversationWorkflow")
logger.setLevel("DEBUG")


@workflow.defn(name=EVALUATE_CONVERSATION_WORKFLOW_ID)
class EvaluateConversationWorkflow:
    """
    Workflow to evaluate a conversation.
    """

    @workflow.run
    async def run(self, input: EvaluateConversationWorkflowInput) -> str:
        project_id = input.project_id
        simulation_id = input.simulation_id
        conversation_id = input.conversation_id

        logger.debug(f"Started for conversation {conversation_id}")

        simulation = await self._get_simulation(
            project_id=project_id,
            simulation_id=simulation_id,
        )

        if not simulation:
            raise Exception(f"Simulation {simulation_id} does not exist")

        if simulation.status != SimulationStatus.IN_PROGRESS:
            raise Exception(f"Simulation {simulation_id} is not in progress")

        conversation = await self._get_conversation(
            project_id=project_id,
            simulation_id=simulation_id,
            conversation_id=conversation_id,
        )

        if not conversation:
            raise Exception(f"Conversation {conversation_id} does not exist")

        if conversation.evaluation_status != EvaluationStatus.QUEUED:
            raise Exception(f"Conversation {conversation_id} is not queued")

        await self._evaluate(
            project_id=project_id,
            simulation_id=simulation_id,
            conversation_id=conversation_id,
        )

        await self._mark_as_completed(
            project_id=project_id,
            simulation_id=simulation_id,
            conversation_id=conversation_id,
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

    async def _get_conversation(
        self,
        project_id: str,
        simulation_id: str,
        conversation_id: str,
    ) -> ConversationDTO | None:
        result: GetConversationActivityOutput = (
            await workflow.execute_activity(
                GET_CONVERSATION_ACTIVITY_ID,
                GetConversationActivityInput(
                    project_id=project_id,
                    simulation_id=simulation_id,
                    conversation_id=conversation_id
                ),
                task_queue=MAIN_QUEUE_ID,
                result_type=GetConversationActivityOutput,
                start_to_close_timeout=timedelta(minutes=1),
                retry_policy=RetryPolicy(
                    initial_interval=timedelta(seconds=15),
                    maximum_attempts=3,
                ),
            )
        )

        return result.conversation

    async def _evaluate(
        self,
        project_id: str,
        simulation_id: str,
        conversation_id: str,
    ) -> None:
        await workflow.execute_activity(
            EVALUATE_CONVERSATION_ACTIVITY_ID,
            EvaluateConversationActivityInput(
                project_id=project_id,
                simulation_id=simulation_id,
                conversation_id=conversation_id
            ),
            task_queue=MAIN_QUEUE_ID,
            start_to_close_timeout=timedelta(minutes=5),
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=30),
                maximum_attempts=5,
            ),
        )

    async def _mark_as_completed(
        self,
        project_id: str,
        simulation_id: str,
        conversation_id: str,
    ) -> None:
        await workflow.execute_activity(
            UPDATE_CONVERSATION_STATUS_ACTIVITY_ID,
            UpdateConversationStatusActivityInput(
                project_id=project_id,
                simulation_id=simulation_id,
                conversation_id=conversation_id,
                evaluation_status=EvaluationStatus.COMPLETED,
            ),
            task_queue=MAIN_QUEUE_ID,
            start_to_close_timeout=timedelta(minutes=1),
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=15),
                maximum_attempts=3,
            ),
        )
