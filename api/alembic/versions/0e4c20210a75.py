"""Create persona tables

Revision ID: 0e4c20210a75
Revises: 1a17b9773bfd
Create Date: 2025-09-07 13:47:12.733905

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
revision: str = "0e4c20210a75"
down_revision: Union[str, Sequence[str], None] = "3ce3ee5b2f35"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create persona table
    op.create_table(
        "persona",
        Column("id", Text(), nullable=False),
        Column(
            "approval_status",
            Text(),
            nullable=False,
            server_default=text("'pending'"),
        ),
        Column(
            "attributes",
            JSONB(),
            nullable=False,
            server_default=text("'{}'"),
        ),
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
        Column(
            "metadata",
            JSONB(),
            nullable=False,
            server_default=text("'{}'"),
        ),
        Column("purpose", Text(), nullable=False),
        Column("seq_id", Integer(), nullable=False),
        Column("simulation_id", Text(), nullable=False),
        Column("story", Text(), nullable=False),
        Column("summary", Text(), nullable=False),
        Column(
            "updated_at",
            DateTime(),
            nullable=False,
            server_default=func.now(),
        ),
        PrimaryKeyConstraint("id"),
        ForeignKeyConstraint(
            ["simulation_id"],
            ["simulation.id"],
            ondelete="CASCADE",
        ),
    )

    # Create indexes for persona table
    op.create_index("idx_persona_created_at", "persona", ["created_at"])
    op.create_index("idx_persona_simulation_id", "persona", ["simulation_id"])

    # Create trigger function to auto-assign seq_id per simulation
    op.execute("""
        CREATE OR REPLACE FUNCTION set_persona_seq_id()
        RETURNS TRIGGER AS $$
        BEGIN
            -- Get the next seq_id for this specific simulation
            SELECT COALESCE(MAX(seq_id), 0) + 1
            INTO NEW.seq_id
            FROM persona
            WHERE simulation_id = NEW.simulation_id;

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    # Create trigger for persona
    op.execute("""
        CREATE TRIGGER persona_seq_id_trigger
        BEFORE INSERT ON persona
        FOR EACH ROW
        WHEN (NEW.seq_id IS NULL)
        EXECUTE FUNCTION set_persona_seq_id()
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TRIGGER IF EXISTS persona_seq_id_trigger ON persona")
    op.execute("DROP FUNCTION IF EXISTS set_persona_seq_id()")

    op.drop_table("persona")
