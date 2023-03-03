"""User role to enum

Revision ID: 57e75e99b736
Revises: 83f6d471e39b
Create Date: 2023-03-04 01:20:54.053743

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57e75e99b736'
down_revision = '83f6d471e39b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.get_context().autocommit_block():
        op.execute("ALTER TYPE roles ADD VALUE 'role_user' ")


def downgrade() -> None:
    op.execute("ALTER TYPE roles RENAME TO roles_old")
    op.execute("CREATE TYPE roles AS ENUM('role_admin', 'role_artist')")
    op.execute((
        "ALTER TABLE users ALTER COLUMN role TYPE roles USING "
        "role::text::roles"
    ))
    op.execute("DROP TYPE roles_old")
