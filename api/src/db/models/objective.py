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
from sqlalchemy.orm import relationship

from src.db.session import Base


class Objective(Base):
    __tablename__ = "objective"

    id = Column(Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        index=True,
    )
    version_id = Column(
        Integer,
        nullable=False,
        server_default=text("1"),
    )
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

    project = relationship("Project", back_populates="objectives")
    versions = relationship(
        "ObjectiveVersion",
        back_populates="objective",
        cascade="all, delete-orphan",
    )
    version = relationship(
        "ObjectiveVersion",
        primaryjoin="and_(Objective.id == ObjectiveVersion.objective_id, Objective.version_id == ObjectiveVersion.id)",
        viewonly=True,
        uselist=False,
    )
