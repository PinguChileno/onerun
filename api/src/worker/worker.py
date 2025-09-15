import os

from temporalio.client import Client
from temporalio.contrib.pydantic import pydantic_data_converter
from temporalio.worker import Worker

from src.db.session import engine
from src.worker.activities import (
    create_conversation_activity,
    create_persona_activity,
    evaluate_conversation_activity,
    get_conversation_activity,
    get_conversation_candidates_activity,
    get_conversations_count_activity,
    get_persona_count_activity,
    get_simulation_activity,
    list_conversations_activity,
    schedule_assign_conversations_activity,
    schedule_assign_personas_activity,
    schedule_check_simulation_activity,
    unschedule_assign_conversations_activity,
    unschedule_assign_personas_activity,
    unschedule_check_simulation_activity,
    update_conversation_status_activity,
    update_simulation_status_activity,
)
from src.worker.constants import MAIN_QUEUE_ID
from src.worker.workflows import (
    AssignConversationsWorkflow,
    AssignPersonasWorkflow,
    CancelSimulationWorkflow,
    CheckSimulationWorkflow,
    EvaluateConversationWorkflow,
    RunSimulationWorkflow,
)


TEMPORAL_ADDRESS = os.getenv("TEMPORAL_ADDRESS", "localhost:7233")
TEMPORAL_NAMESPACE = os.getenv("TEMPORAL_NAMESPACE", "default")


async def create_worker() -> Worker:
    client = await Client.connect(
        TEMPORAL_ADDRESS,
        namespace=TEMPORAL_NAMESPACE,
        data_converter=pydantic_data_converter
    )
    activities = [
        create_conversation_activity(engine),
        create_persona_activity(engine),
        evaluate_conversation_activity(engine),
        get_conversation_activity(engine),
        get_conversation_candidates_activity(engine),
        get_conversations_count_activity(engine),
        get_persona_count_activity(engine),
        get_simulation_activity(engine),
        list_conversations_activity(engine),
        schedule_assign_conversations_activity(client),
        schedule_assign_personas_activity(client),
        schedule_check_simulation_activity(client),
        unschedule_assign_conversations_activity(client),
        unschedule_assign_personas_activity(client),
        unschedule_check_simulation_activity(client),
        update_conversation_status_activity(engine),
        update_simulation_status_activity(engine),
    ]
    workflows = [
        AssignConversationsWorkflow,
        AssignPersonasWorkflow,
        CancelSimulationWorkflow,
        CheckSimulationWorkflow,
        EvaluateConversationWorkflow,
        RunSimulationWorkflow,
    ]

    return Worker(
        client,
        task_queue=MAIN_QUEUE_ID,
        activities=activities,
        workflows=workflows,
    )
