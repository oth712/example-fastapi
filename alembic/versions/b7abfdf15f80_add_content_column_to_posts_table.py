"""add content column to posts table

Revision ID: b7abfdf15f80
Revises: d1c8afe9bf5d
Create Date: 2025-04-30 22:40:12.300642

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7abfdf15f80'
down_revision: Union[str, None] = 'd1c8afe9bf5d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column(
        'content', sa.String(256), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
