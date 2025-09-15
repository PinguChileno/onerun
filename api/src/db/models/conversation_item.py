import uuid

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from src.db.session import Base


class ConversationItem(Base):
    __tablename__ = "conversation_item"

    id = Column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    content = Column(JSONB, nullable=False)
    conversation_id = Column(
        Text,
        ForeignKey("conversation.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        index=True,
    )
    role = Column(Text, nullable=False)
    type = Column(Text, nullable=False)
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    conversation = relationship("Conversation", back_populates="items")
