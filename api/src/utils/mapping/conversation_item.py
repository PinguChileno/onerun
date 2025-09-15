from src.db.models import ConversationItem
from src.types import ConversationItemDTO


def conversation_item_model_to_dto(
    item: ConversationItem,
) -> ConversationItemDTO:
    return ConversationItemDTO(
        id=item.id,
        content=item.content,
        conversation_id=item.conversation_id,
        created_at=item.created_at,
        role=item.role,
        type=item.type,
        updated_at=item.updated_at,
    )
