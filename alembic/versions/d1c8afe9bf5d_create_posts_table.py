"""create posts table

Revision ID: d1c8afe9bf5d
Revises: 
Create Date: 2025-04-29 23:31:09.124120

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1c8afe9bf5d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column(
        'id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(32), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
