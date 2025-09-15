"""Create conversation tables

Revision ID: 1a17b9773bfd
Revises: 3ce3ee5b2f35
Create Date: 2025-09-07 15:14:38.473674

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKeyConstraint,
    Integer,
    PrimaryKeyConstraint,
    Text,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision: str = "1a17b9773bfd"
down_revision: Union[str, Sequence[str], None] = "0e4c20210a75"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create conversation table
    op.create_table(
        "conversation",
        Column("id", Text(), nullable=False),
        Column(
            "created_at",
            DateTime(),
            nullable=False,
            server_default=func.now(),
        ),
        Column("end_reason", Text(), nullable=True),
        Column(
            "evaluation_status",
            Text(),
            nullable=False,
            server_default=text("'not_applicable'"),
        ),
        Column(
            "metadata",
            JSONB(),
            nullable=False,
            server_default=text("'{}'"),
        ),
        Column("persona_id", Text(), nullable=False),
        Column("seq_id", Integer(), nullable=False),
        Column("simulation_id", Text(), nullable=False),
        Column(
            "status",
            Text(),
            nullable=False,
            server_default=text("'pending'"),
        ),
        Column(
            "updated_at",
            DateTime(),
            nullable=False,
            server_default=func.now(),
        ),
        PrimaryKeyConstraint("id"),
        ForeignKeyConstraint(
            ["persona_id"],
            ["persona.id"],
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["simulation_id"],
            ["simulation.id"],
            ondelete="CASCADE",
        ),
    )

    # Create indexes for conversation table
    op.create_index(
        "idx_conversation_created_at",
        "conversation",
        ["created_at"],
    )
    op.create_index(
        "idx_conversation_persona_id",
        "conversation",
        ["persona_id"],
    )
    op.create_index(
        "idx_conversation_simulation_id",
        "conversation",
        ["simulation_id"],
    )

    # Add unique constraint for seq_id per simulation
    op.create_index(
        "idx_conversation_simulation_seq_unique",
        "conversation",
        ["simulation_id", "seq_id"],
        unique=True,
    )

    # Create conversation_item table
    op.create_table(
        "conversation_item",
        Column("id", Text(), nullable=False),
        Column("content", JSONB(), nullable=False),
        Column("conversation_id", Text(), nullable=False),
        Column(
            "created_at",
            DateTime(),
            nullable=False,
            server_default=func.now(),
        ),
        Column("role", Text(), nullable=False),
        Column("type", Text(), nullable=False),
        Column(
            "updated_at",
            DateTime(),
            nullable=False,
            server_default=func.now(),
        ),
        PrimaryKeyConstraint("id"),
        ForeignKeyConstraint(
            ["conversation_id"],
            ["conversation.id"],
            ondelete="CASCADE",
        ),
    )

    # Create indexes for conversation_item table
    op.create_index(
        "idx_conversation_item_conversation_id",
        "conversation_item",
        ["conversation_id"],
    )
    op.create_index(
        "idx_conversation_item_created_at",
        "conversation_item",
        ["created_at"],
    )

    # Create conversation_evaluation table
    op.create_table(
        "conversation_evaluation",
        Column("id", Text(), nullable=False),
        Column("conversation_id", Text(), nullable=False),
        Column(
            "created_at",
            DateTime(),
            nullable=False,
            server_default=func.now(),
        ),
        Column("objective_id", Text(), nullable=False),
        Column("objective_version_id", Integer(), nullable=False),
        Column("reason", Text(), nullable=True),
        Column(
            "score",
            Float(),
            nullable=False,
            server_default=text("0.0"),
        ),
        Column(
            "updated_at",
            DateTime(),
            nullable=False,
            server_default=func.now(),
        ),
        PrimaryKeyConstraint("id"),
        ForeignKeyConstraint(
            ["conversation_id"],
            ["conversation.id"],
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["objective_id"],
            ["objective.id"],
            ondelete="CASCADE",
        ),
    )

    # Create indexes for conversation_evaluation table
    op.create_index(
        "idx_conversation_evaluation_conversation_id",
        "conversation_evaluation",
        ["conversation_id"],
    )
    op.create_index(
        "idx_conversation_evaluation_objective_id",
        "conversation_evaluation",
        ["objective_id"],
    )

    # Create trigger function to auto-assign seq_id per simulation
    op.execute("""
        CREATE OR REPLACE FUNCTION set_conversation_seq_id()
        RETURNS TRIGGER AS $$
        BEGIN
            -- Get the next seq_id for this specific simulation
            SELECT COALESCE(MAX(seq_id), 0) + 1
            INTO NEW.seq_id
            FROM conversation
            WHERE simulation_id = NEW.simulation_id;

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    # Create trigger for conversation
    op.execute("""
        CREATE TRIGGER conversation_seq_id_trigger
        BEFORE INSERT ON conversation
        FOR EACH ROW
        WHEN (NEW.seq_id IS NULL)
        EXECUTE FUNCTION set_conversation_seq_id()
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        "DROP TRIGGER IF EXISTS conversation_seq_id_trigger ON conversation"
    )
    op.execute("DROP FUNCTION IF EXISTS set_conversation_seq_id()")

    op.drop_table("conversation_evaluation")
    op.drop_table("conversation_item")
    op.drop_table("conversation")
