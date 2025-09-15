from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from src.db.session import Base


class ObjectiveVersion(Base):
    __tablename__ = "objective_version"

    id = Column(Integer, nullable=False, primary_key=True)
    objective_id = Column(
        Text,
        ForeignKey("objective.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    criteria = Column(Text, nullable=False)
    name = Column(Text, nullable=False)

    objective = relationship("Objective", back_populates="versions")
