"""Initial revision

Revision ID: e694c49f7612
Revises:
Create Date: 2025-09-07 07:34:12.673155

"""
from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "e694c49f7612"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
