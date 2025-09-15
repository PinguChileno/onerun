"""Create simulation tables

Revision ID: 3ce3ee5b2f35
Revises: fb26c1436a87
Create Date: 2025-09-07 12:58:05.987233

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKeyConstraint,
    Integer,
    PrimaryKeyConstraint,
    Text,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision: str = "3ce3ee5b2f35"
down_revision: Union[str, Sequence[str], None] = "2ae95f47c715"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create simulation table
    op.create_table(
        "simulation",
        Column("id", Text(), nullable=False),
        Column("agent_id", Text(), nullable=False),
        Column(
            "auto_approve",
            Boolean(),
            nullable=False,
            server_default=text("false"),
        ),
        Column(
            "created_at",
            DateTime(),
            nullable=False,
            server_default=func.now(),
        ),
        Column("expires_at", DateTime(), nullable=True),
        Column("last_failure_reason", Text(), nullable=True),
        Column(
            "max_turns",
            Integer(),
            nullable=False,
            server_default=text("5"),
        ),
        Column(
            "metadata",
            JSONB(),
            nullable=False,
            server_default=text("'{}'"),
        ),
        Column("name", Text(), nullable=False),
        Column("project_id", Text(), nullable=False),
        Column("scenario", Text(), nullable=False),
        Column(
            "status",
            Text(),
            nullable=False,
            server_default=text("'pending'"),
        ),
        Column("target_conversations", Integer(), nullable=False),
        Column("target_personas", Integer(), nullable=False),
        Column(
            "updated_at",
            DateTime(),
            nullable=False,
            server_default=func.now(),
        ),
        PrimaryKeyConstraint("id"),
        ForeignKeyConstraint(["agent_id"], ["agent.id"], ondelete="CASCADE"),
        ForeignKeyConstraint(
            ["project_id"],
            ["project.id"],
            ondelete="CASCADE",
        ),
    )

    # Create indexes for simulation table
    op.create_index("idx_simulation_agent_id", "simulation", ["agent_id"])
    op.create_index("idx_simulation_created_at", "simulation", ["created_at"])
    op.create_index("idx_simulation_name", "simulation", ["name"])
    op.create_index("idx_simulation_project_id", "simulation", ["project_id"])

    # Create simulation_objective table
    op.create_table(
        "simulation_objective",
        Column(
            "created_at",
            DateTime(),
            nullable=False,
            server_default=func.now(),
        ),
        Column("objective_id", Text(), nullable=False),
        Column("objective_version_id", Integer(), nullable=False),
        Column("simulation_id", Text(), nullable=False),
        Column(
            "updated_at",
            DateTime(),
            nullable=False,
            server_default=func.now(),
        ),
        PrimaryKeyConstraint("simulation_id", "objective_id"),
        ForeignKeyConstraint(
            ["objective_id"],
            ["objective.id"],
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["simulation_id"],
            ["simulation.id"],
            ondelete="CASCADE",
        ),
    )

    # Create indexes for simulation_objective table
    op.create_index(
        "idx_simulation_objective_objective_id",
        "simulation_objective",
        ["objective_id"],
    )
    op.create_index(
        "idx_simulation_objective_simulation_id",
        "simulation_objective",
        ["simulation_id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("simulation_objective")
    op.drop_table("simulation")
