from src.db.models import ConversationEvaluation
from src.types import ConversationEvaluationDTO
from src.utils.mapping.objective import objective_model_to_dto


def conversation_evaluation_model_to_dto(
    evaluation: ConversationEvaluation,
) -> ConversationEvaluationDTO:
    if evaluation.objective:
        objective = objective_model_to_dto(evaluation.objective)
    else:
        objective = None

    return ConversationEvaluationDTO(
        id=evaluation.id,
        conversation_id=evaluation.conversation_id,
        created_at=evaluation.created_at,
        objective_id=evaluation.objective_id,
        objective=objective,
        reason=evaluation.reason,
        score=evaluation.score,
        updated_at=evaluation.updated_at,
    )
