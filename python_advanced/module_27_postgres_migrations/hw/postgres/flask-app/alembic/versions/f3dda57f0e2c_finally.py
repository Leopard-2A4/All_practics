"""Finally

Revision ID: f3dda57f0e2c
Revises: 6a3f32b82c0d, a1c1da4258bc
Create Date: 2026-06-01 18:31:57.117285

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3dda57f0e2c'
down_revision: Union[str, Sequence[str], None] = ('6a3f32b82c0d', 'a1c1da4258bc')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
