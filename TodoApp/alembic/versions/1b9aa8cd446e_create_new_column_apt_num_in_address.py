"""create new column apt_num in address

Revision ID: 1b9aa8cd446e
Revises: 0cefa6ee4d57
Create Date: 2022-11-13 22:13:59.262663

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1b9aa8cd446e'
down_revision = '0cefa6ee4d57'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('address', sa.Column('apt_num', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('address', 'apt_num')
