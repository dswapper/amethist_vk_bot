"""Change peer_id to vk_id

Revision ID: ab03ff38abe7
Revises: 48bb366ca47c
Create Date: 2023-03-06 15:04:08.614294

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab03ff38abe7'
down_revision = '48bb366ca47c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'peer_id', new_column_name='vk_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'vk_id', new_column_name='peer_id')
    # ### end Alembic commands ###