"""add foreign key to post table

Revision ID: ec0f277efcb2
Revises: 8a23717b2584
Create Date: 2025-09-13 08:32:45.505506

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec0f277efcb2'
down_revision: Union[str, Sequence[str], None] = '8a23717b2584'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fkey', source_table="posts", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('post_users_fkey', table_name="posts")
    op.drop_column('posts', 'owner_id')
