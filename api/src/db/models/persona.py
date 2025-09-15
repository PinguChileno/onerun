import uuid

from sqlalchemy import (
    Boolean,
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


class Persona(Base):
    __tablename__ = "persona"

    id = Column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    approval_status = Column(
        Text,
        nullable=False,
        server_default=text("'pending'"),
    )
    attributes = Column(JSONB, nullable=False, server_default=text("'{}'"))
    auto_approve = Column(
        Boolean,
        nullable=False,
        server_default=text("false"),
    )
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    metadata_ = Column(
        "metadata",
        JSONB,
        nullable=False,
        server_default=text("'{}'"),
    )
    purpose = Column(Text, nullable=False)
    seq_id = Column(Integer, nullable=False)
    simulation_id = Column(
        Text,
        ForeignKey("simulation.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    story = Column(Text, nullable=False)
    summary = Column(Text, nullable=False)
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    conversations = relationship("Conversation", back_populates="persona")
    simulation = relationship("Simulation", back_populates="personas")
