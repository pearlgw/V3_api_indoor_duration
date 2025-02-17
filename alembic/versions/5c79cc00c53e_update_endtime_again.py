"""update endtime again

Revision ID: 5c79cc00c53e
Revises: c0abaa0caf12
Create Date: 2025-02-08 09:07:59.643500

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '5c79cc00c53e'
down_revision: Union[str, None] = 'c0abaa0caf12'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('detail_person_durations', sa.Column('end_time', postgresql.TIMESTAMP(), nullable=True))
    op.drop_column('detail_person_durations', 'total_duration')
    op.alter_column('person_durations', 'total_duration',
               existing_type=postgresql.TIME(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('person_durations', 'total_duration',
               existing_type=postgresql.TIME(),
               nullable=False)
    op.add_column('detail_person_durations', sa.Column('total_duration', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.drop_column('detail_person_durations', 'end_time')
    # ### end Alembic commands ###