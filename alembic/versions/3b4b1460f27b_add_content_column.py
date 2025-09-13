"""Add content column

Revision ID: 3b4b1460f27b
Revises: ec0f277efcb2
Create Date: 2025-09-13 08:46:57.686688

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b4b1460f27b'
down_revision: Union[str, Sequence[str], None] = 'ec0f277efcb2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
