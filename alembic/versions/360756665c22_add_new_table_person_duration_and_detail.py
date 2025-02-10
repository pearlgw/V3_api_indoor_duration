"""add new table person duration and detail

Revision ID: 360756665c22
Revises: 76dcc1bc7fab
Create Date: 2025-02-08 08:46:47.212170

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '360756665c22'
down_revision: Union[str, None] = '76dcc1bc7fab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('person_durations',
    sa.Column('uid', sa.Uuid(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('total_duration', sa.Time(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_table('detail_person_durations',
    sa.Column('uid', sa.Uuid(), nullable=False),
    sa.Column('person_duration_uid', sa.Uuid(), nullable=False),
    sa.Column('labeled_image', sa.String(), nullable=False),
    sa.Column('nim', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('name_track_id', sa.String(), nullable=False),
    sa.Column('start_time', postgresql.TIMESTAMP(), nullable=True),
    sa.Column('end_time', postgresql.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['person_duration_uid'], ['person_durations.uid'], ),
    sa.PrimaryKeyConstraint('uid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('detail_person_durations')
    op.drop_table('person_durations')
    # ### end Alembic commands ###