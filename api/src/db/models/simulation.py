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


class Simulation(Base):
    __tablename__ = "simulation"

    id = Column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id = Column(
        Text,
        ForeignKey("agent.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    auto_approve = Column(
        Boolean,
        nullable=False,
        server_default=text("false"),
    )
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        index=True,
    )
    expires_at = Column(DateTime, nullable=True)
    last_failure_reason = Column(Text, nullable=True)
    max_turns = Column(Integer, nullable=False, server_default=text("5"))
    metadata_ = Column(
        "metadata",
        JSONB,
        nullable=False,
        server_default=text("'{}'"),
    )
    name = Column(Text, nullable=False, index=True)
    project_id = Column(
        Text,
        ForeignKey("project.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    scenario = Column(Text, nullable=False)
    status = Column(Text, nullable=False, server_default=text("'pending'"))
    target_conversations = Column(Integer, nullable=False)
    target_personas = Column(Integer, nullable=False)
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    agent = relationship("Agent", back_populates="simulations")
    conversations = relationship("Conversation", back_populates="simulation")
    objectives = relationship(
        "SimulationObjective",
        back_populates="simulation",
    )
    project = relationship("Project", back_populates="simulations")
    personas = relationship("Persona", back_populates="simulation")
