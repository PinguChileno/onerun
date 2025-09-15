import uuid

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Text,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from src.db.session import Base


class Conversation(Base):
    __tablename__ = "conversation"

    id = Column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(
        DateTime, nullable=False,
        server_default=func.now(),
        index=True,
    )
    end_reason = Column(Text, nullable=True)
    evaluation_status = Column(
        Text,
        nullable=False,
        server_default=text("'not_applicable'"),
    )
    metadata_ = Column(
        "metadata",
        JSONB,
        nullable=False,
        server_default=text("'{}'"),
    )
    persona_id = Column(
        Text,
        ForeignKey("persona.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    seq_id = Column(Integer, nullable=False)
    simulation_id = Column(
        Text,
        ForeignKey("simulation.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    status = Column(Text, nullable=False, server_default=text("'pending'"))
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    evaluations = relationship(
        "ConversationEvaluation",
        back_populates="conversation",
    )
    items = relationship("ConversationItem", back_populates="conversation")
    persona = relationship("Persona", back_populates="conversations")
    simulation = relationship("Simulation", back_populates="conversations")
