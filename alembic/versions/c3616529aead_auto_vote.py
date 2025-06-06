"""auto-vote

Revision ID: c3616529aead
Revises: 1963ec061b42
Create Date: 2025-05-01 22:08:57.351547

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'c3616529aead'
down_revision: Union[str, None] = '1963ec061b42'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('post_id', 'user_id')
    )
    op.alter_column('posts', 'content',
               existing_type=mysql.VARCHAR(length=256),
               type_=sa.String(length=32),
               existing_nullable=False)
    op.alter_column('users', 'password',
               existing_type=mysql.VARCHAR(length=32),
               type_=sa.String(length=64),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'password',
               existing_type=sa.String(length=64),
               type_=mysql.VARCHAR(length=32),
               existing_nullable=False)
    op.alter_column('posts', 'content',
               existing_type=sa.String(length=32),
               type_=mysql.VARCHAR(length=256),
               existing_nullable=False)
    op.drop_table('votes')
    # ### end Alembic commands ###
