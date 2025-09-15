"""Create objective table

Revision ID: 2ae95f47c715
Revises: 1a17b9773bfd
Create Date: 2025-09-07 11:45:29.596997

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKeyConstraint,
    Integer,
    PrimaryKeyConstraint,
    Text,
    func,
    text,
)


# revision identifiers, used by Alembic.
revision: str = "2ae95f47c715"
down_revision: Union[str, Sequence[str], None] = "fb26c1436a87"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create objective table
    op.create_table(
        "objective",
        Column("id", Text(), nullable=False),
        Column(
            "created_at",
            DateTime(),
            nullable=False,
            server_default=func.now(),
        ),
        Column(
            "version_id",
            Integer(),
            nullable=False,
            server_default=text("1"),
        ),
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

    # Create indexes for objective table
    op.create_index("idx_objective_created_at", "objective", ["created_at"])
    op.create_index("idx_objective_project_id", "objective", ["project_id"])

    # Create objective_version table
    op.create_table(
        "objective_version",
        Column("id", Integer(), nullable=False),
        Column("objective_id", Text(), nullable=False),
        Column(
            "created_at",
            DateTime(),
            nullable=False,
            server_default=func.now(),
        ),
        Column("criteria", Text(), nullable=False),
        Column("name", Text(), nullable=False),
        PrimaryKeyConstraint("objective_id", "id"),
        ForeignKeyConstraint(
            ["objective_id"],
            ["objective.id"],
            ondelete="CASCADE",
        ),
    )

    # Create indexes for objective_version table
    op.create_index(
        "idx_objective_version_id",
        "objective_version",
        ["id"],
    )
    op.create_index(
        "idx_objective_version_created_at",
        "objective_version",
        ["created_at"],
    )

    # Create trigger function to auto-assign version id per objective
    op.execute("""
        CREATE OR REPLACE FUNCTION set_objective_version()
        RETURNS TRIGGER AS $$
        BEGIN
            -- Get the next version id for this specific objective
            SELECT COALESCE(MAX(id), 0) + 1
            INTO NEW.id
            FROM objective_version
            WHERE objective_id = NEW.objective_id;

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    # Create trigger for objective_version
    op.execute("""
        CREATE TRIGGER objective_version_trigger
        BEFORE INSERT ON objective_version
        FOR EACH ROW
        WHEN (NEW.id IS NULL)
        EXECUTE FUNCTION set_objective_version()
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        "DROP TRIGGER IF EXISTS objective_version_trigger ON objective_version"
    )
    op.execute("DROP FUNCTION IF EXISTS set_objective_version()")

    op.drop_table("objective_version")
    op.drop_table("objective")
