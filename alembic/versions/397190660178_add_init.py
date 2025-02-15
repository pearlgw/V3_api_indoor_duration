"""add_init

Revision ID: 397190660178
Revises: 
Create Date: 2025-02-06 22:48:15.901843

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '397190660178'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_tokens',
    sa.Column('uid', sa.Uuid(), nullable=False),
    sa.Column('user_uid', sa.Uuid(), nullable=True),
    sa.Column('token', sa.String(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('uid'),
    sa.UniqueConstraint('token')
    )
    op.create_table('users',
    sa.Column('uid', sa.Uuid(), nullable=False),
    sa.Column('nim', sa.String(), nullable=False),
    sa.Column('fullname', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('image', sa.String(), nullable=False),
    sa.Column('roles', sa.String(), nullable=True),
    sa.Column('is_verified', sa.String(), nullable=True),
    sa.Column('token', sa.String(), nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), nullable=True),
    sa.Column('status_embed', sa.Boolean(), server_default='false', nullable=False),
    sa.PrimaryKeyConstraint('uid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('user_tokens')
    # ### end Alembic commands ###