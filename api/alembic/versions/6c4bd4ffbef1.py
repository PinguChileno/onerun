"""Create auth tables

Revision ID: 6c4bd4ffbef1
Revises: e694c49f7612
Create Date: 2025-09-07 08:15:23.504394

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import (
    Boolean,
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
revision: str = "6c4bd4ffbef1"
down_revision: Union[str, Sequence[str], None] = "e694c49f7612"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create user table
    op.create_table(
        "user",
        Column("id", Text(), nullable=False),
        Column("ban_expires", DateTime(), nullable=True),
        Column("ban_reason", Text(), nullable=True),
        Column(
            "banned",
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
        Column("email", Text(), nullable=True),
        Column(
            "email_verified",
            Boolean(),
            nullable=False,
            server_default=text("false"),
        ),
        Column("image", Text(), nullable=True),
        Column(
            "metadata",
            JSONB(),
            nullable=False,
            server_default=text("'{}'"),
        ),
        Column("name", Text(), nullable=True),
        Column("role", Text(), nullable=True),
        Column(
            "updated_at",
            DateTime(),
            nullable=False,
            server_default=func.now(),
        ),
        PrimaryKeyConstraint("id"),
    )

    # Create indexes for user table
    op.create_index("idx_user_created_at", "user", ["created_at"])
    op.create_index("idx_user_email", "user", ["email"])
    op.create_index("idx_user_name", "user", ["name"])
    op.create_unique_constraint("uq_user_email", "user", ["email"])

    # Create session table
    op.create_table(
        "session",
        Column("id", Text(), nullable=False),
        Column(
            "created_at",
            DateTime(),
            nullable=False,
            server_default=func.now(),
        ),
        Column("expires_at", DateTime(), nullable=False),
        Column("impersonated_by", Text(), nullable=True),
        Column("ip_address", Text(), nullable=True),
        Column("token", Text(), nullable=False),
        Column(
            "updated_at",
            DateTime(),
            nullable=False,
            server_default=func.now(),
        ),
        Column("user_agent", Text(), nullable=True),
        Column("user_id", Text(), nullable=False),
        PrimaryKeyConstraint("id"),
        ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
    )

    # Create indexes for session table
    op.create_index("idx_session_user_id", "session", ["user_id"])
    op.create_unique_constraint("uq_session_token", "session", ["token"])

    # Create account table
    op.create_table(
        "account",
        Column("id", Text(), nullable=False),
        Column("access_token", Text(), nullable=True),
        Column("access_token_expires_at", DateTime(), nullable=True),
        Column("account_id", Text(), nullable=False),
        Column(
            "created_at",
            DateTime(),
            nullable=False,
            server_default=func.now(),
        ),
        Column("id_token", Text(), nullable=True),
        Column("password", Text(), nullable=True),
        Column("provider_id", Text(), nullable=False),
        Column("refresh_token", Text(), nullable=True),
        Column("refresh_token_expires_at", DateTime(), nullable=True),
        Column("scope", Text(), nullable=True),
        Column(
            "updated_at",
            DateTime(),
            nullable=False,
            server_default=func.now(),
        ),
        Column("user_id", Text(), nullable=False),
        PrimaryKeyConstraint("id"),
        ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
    )

    # Create indexes for account table
    op.create_index("idx_account_user_id", "account", ["user_id"])

    # Create verification table
    op.create_table(
        "verification",
        Column("id", Text(), nullable=False),
        Column(
            "created_at",
            DateTime(),
            nullable=False,
            server_default=func.now(),
        ),
        Column("expires_at", DateTime(), nullable=False),
        Column("identifier", Text(), nullable=False),
        Column(
            "updated_at",
            DateTime(),
            nullable=False,
            server_default=func.now(),
        ),
        Column("value", Text(), nullable=False),
        PrimaryKeyConstraint("id"),
    )

    # Create jwks table
    op.create_table(
        "jwks",
        Column("id", Text(), nullable=False),
        Column(
            "created_at",
            DateTime(),
            nullable=False,
            server_default=func.now(),
        ),
        Column("private_key", Text(), nullable=False),
        Column("public_key", Text(), nullable=False),
        PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("jwks")
    op.drop_table("verification")
    op.drop_table("account")
    op.drop_table("session")
    op.drop_table("user")
