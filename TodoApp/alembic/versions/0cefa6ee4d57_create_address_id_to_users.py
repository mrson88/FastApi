"""create address_id to users

Revision ID: 0cefa6ee4d57
Revises: 1887dd7a54d3
Create Date: 2022-11-13 18:55:51.690844

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0cefa6ee4d57'
down_revision = '1887dd7a54d3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('address_id', sa.Integer(), nullable=True))
    op.create_foreign_key('address_users_fk', source_table='users', referent_table='address', local_cols=['address_id'],
                          remote_cols=['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('address_users_fk', table_name='users')
    op.drop_column('user', 'address_id')
