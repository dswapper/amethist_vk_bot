"""Orders status and cost, RefMsg msg_text msg_attachments

Revision ID: 88ba6e8f517c
Revises: ab03ff38abe7
Create Date: 2023-03-08 01:47:31.566152

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88ba6e8f517c'
down_revision = 'ab03ff38abe7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("CREATE TYPE orderstatus AS ENUM('user_send_references', 'user_paid', 'artist_get_order', 'artist_done', 'archive')")
    op.add_column('orders', sa.Column('cost', sa.Integer(), nullable=True))
    op.add_column('orders', sa.Column('order_status', sa.Enum('user_send_references', 'user_paid', 'artist_get_order', 'artist_done', 'archive', name='orderstatus'), nullable=True))
    op.add_column('ref_msgs', sa.Column('message_text', sa.String(), nullable=True))
    op.add_column('ref_msgs', sa.Column('message_attachments', sa.String(), nullable=True))
    op.drop_column('ref_msgs', 'message_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("DROP TYPE orderstatus")
    op.add_column('ref_msgs', sa.Column('message_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('ref_msgs', 'message_attachments')
    op.drop_column('ref_msgs', 'message_text')
    op.drop_column('orders', 'order_status')
    op.drop_column('orders', 'cost')
    # ### end Alembic commands ###
