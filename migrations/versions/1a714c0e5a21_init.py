"""Init

Revision ID: 1a714c0e5a21
Revises: bab9c42e8062
Create Date: 2024-05-09 20:38:06.821405

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a714c0e5a21'
down_revision: Union[str, None] = 'bab9c42e8062'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'confirmed')
    # ### end Alembic commands ###
