"""create content column

Revision ID: a4b64f1adcb7
Revises: d0d59bb70210
Create Date: 2025-09-12 19:08:39.330120

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4b64f1adcb7'
down_revision: Union[str, Sequence[str], None] = 'd0d59bb70210'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
