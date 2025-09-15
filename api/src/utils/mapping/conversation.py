from src.db.models import Conversation
from src.types import ConversationDTO

from .conversation_evaluation import conversation_evaluation_model_to_dto
from .persona import persona_model_to_dto


def conversation_model_to_dto(conversation: Conversation) -> ConversationDTO:
    if conversation.persona:
        persona = persona_model_to_dto(conversation.persona)
    else:
        persona = None

    return ConversationDTO(
        id=conversation.id,
        created_at=conversation.created_at,
        end_reason=conversation.end_reason,
        evaluation_status=conversation.evaluation_status,
        metadata=conversation.metadata_,
        persona_id=conversation.persona_id,
        persona=persona,
        evaluations=[
            conversation_evaluation_model_to_dto(evaluation)
            for evaluation in conversation.evaluations
        ],
        seq_id=conversation.seq_id,
        simulation_id=conversation.simulation_id,
        status=conversation.status,
        updated_at=conversation.updated_at,
    )
