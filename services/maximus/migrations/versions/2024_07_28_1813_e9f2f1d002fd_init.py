"""init

Revision ID: e9f2f1d002fd
Revises: 
Create Date: 2024-07-28 18:13:33.902712

"""
import os
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'e9f2f1d002fd'
migrations = sorted(
    filter(
        lambda f: not f.startswith('_'), os.listdir(os.path.dirname(__file__))
    )
)
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'keys',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('keys')
    # ### end Alembic commands ###
