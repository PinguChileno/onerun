import uuid

from sqlalchemy import (
    Column,
    DateTime,
    Text,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from src.db.session import Base


class Project(Base):
    __tablename__ = "project"

    id = Column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        index=True,
    )
    metadata_ = Column(
        "metadata",
        JSONB,
        nullable=False,
        server_default=text("'{}'"),
    )
    name = Column(Text, nullable=False, index=True)
    settings = Column(
        "settings",
        JSONB,
        nullable=False,
        server_default=text("'{}'"),
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    agents = relationship("Agent", back_populates="project")
    objectives = relationship("Objective", back_populates="project")
    simulations = relationship("Simulation", back_populates="project")
