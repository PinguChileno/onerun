"""Create project tables

Revision ID: 0d670fa3214f
Revises: 6c4bd4ffbef1
Create Date: 2025-09-07 09:22:41.815580

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import (
    Column,
    DateTime,
    PrimaryKeyConstraint,
    Text,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision: str = "0d670fa3214f"
down_revision: Union[str, Sequence[str], None] = "6c4bd4ffbef1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create project table
    op.create_table(
        "project",
        Column("id", Text(), nullable=False),
        Column(
            "created_at",
            DateTime(),
            nullable=False,
            server_default=func.now(),
        ),
        Column(
            "metadata",
            JSONB(),
            nullable=False,
            server_default=text("'{}'"),
        ),
        Column("name", Text(), nullable=False),
        Column(
            "settings",
            JSONB(),
            nullable=False,
            server_default=text("'{}'"),
        ),
        Column(
            "updated_at",
            DateTime(),
            nullable=False,
            server_default=func.now(),
        ),
        PrimaryKeyConstraint("id"),
    )

    # Create indexes for project table
    op.create_index("idx_project_created_at", "project", ["created_at"])
    op.create_index("idx_project_name", "project", ["name"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("project")
