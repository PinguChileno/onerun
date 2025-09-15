import uuid

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Text,
    func,
    text,
)
from sqlalchemy.orm import relationship

from src.db.session import Base


class ConversationEvaluation(Base):
    __tablename__ = "conversation_evaluation"

    id = Column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(
        Text,
        ForeignKey("conversation.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    objective_id = Column(
        Text,
        ForeignKey("objective.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    objective_version_id = Column(Integer, nullable=False)
    reason = Column(Text, nullable=True)
    score = Column(Float, nullable=False, server_default=text("0.0"))
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    conversation = relationship("Conversation", back_populates="evaluations")
    objective = relationship("Objective")
