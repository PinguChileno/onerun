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


class SimulationObjective(Base):
    __tablename__ = "simulation_objective"

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    objective_id = Column(
        Text,
        ForeignKey("objective.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    objective_version_id = Column(Integer, nullable=False)
    simulation_id = Column(
        Text,
        ForeignKey("simulation.id", ondelete="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    simulation = relationship("Simulation", back_populates="objectives")
    objective = relationship("Objective")
