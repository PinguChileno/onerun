import uuid

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Text,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from src.db.session import Base


class Agent(Base):
    __tablename__ = "agent"

    id = Column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        index=True,
    )
    description = Column(Text, nullable=True)
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
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    project = relationship("Project", back_populates="agents")
    simulations = relationship("Simulation", back_populates="agent")
