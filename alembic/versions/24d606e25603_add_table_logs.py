"""add table logs

Revision ID: 24d606e25603
Revises: c34923fc600b
Create Date: 2025-02-09 23:44:55.968356

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '24d606e25603'
down_revision: Union[str, None] = 'c34923fc600b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('logs',
    sa.Column('uid', sa.Uuid(), nullable=False),
    sa.Column('user_uid', sa.Uuid(), nullable=True),
    sa.Column('action', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('uid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('logs')
    # ### end Alembic commands ###