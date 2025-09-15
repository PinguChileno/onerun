"""Create agent table

Revision ID: fb26c1436a87
Revises: 0d670fa3214f
Create Date: 2025-09-07 10:33:17.460071

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
    Text,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision: str = "fb26c1436a87"
down_revision: Union[str, Sequence[str], None] = "0d670fa3214f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create agent table
    op.create_table(
        "agent",
        Column("id", Text(), nullable=False),
        Column(
            "created_at",
            DateTime(),
            nullable=False,
            server_default=func.now(),
        ),
        Column("description", Text(), nullable=True),
        Column(
            "metadata",
            JSONB(),
            nullable=False,
            server_default=text("'{}'"),
        ),
        Column("name", Text(), nullable=False),
        Column("project_id", Text(), nullable=False),
        Column(
            "updated_at",
            DateTime(),
            nullable=False,
            server_default=func.now(),
        ),
        PrimaryKeyConstraint("id"),
        ForeignKeyConstraint(
            ["project_id"],
            ["project.id"],
            ondelete="CASCADE",
        ),
    )

    # Create indexes for agent table
    op.create_index("idx_agent_created_at", "agent", ["created_at"])
    op.create_index("idx_agent_name", "agent", ["name"])
    op.create_index("idx_agent_project_id", "agent", ["project_id"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("agent")
