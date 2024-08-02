"""add gratter type

Revision ID: 5beaac2febd8
Revises: 0fe8c00d5374
Create Date: 2024-08-02 18:16:43.200160

"""
import os
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '5beaac2febd8'
migrations = sorted(
    filter(
        lambda f: not f.startswith('_'), os.listdir(os.path.dirname(__file__))
    )
)
down_revision: Union[str, None] = migrations[
    migrations.index(os.path.basename(__file__)) - 1
].split('_')[4]
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('gratter', sa.String(), nullable=True))
    op.execute('UPDATE events SET gratter = \'\'')
    op.alter_column('events', 'gratter', nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('events', 'gratter')
    # ### end Alembic commands ###
