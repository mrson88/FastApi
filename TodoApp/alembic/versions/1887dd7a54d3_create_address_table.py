"""create address table

Revision ID: 1887dd7a54d3
Revises: 46d2abb06bf8
Create Date: 2022-11-13 18:45:22.477327

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1887dd7a54d3'
down_revision = '46d2abb06bf8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('address',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('address1', sa.String(), nullable=False),
                    sa.Column('address2', sa.String(), nullable=False),
                    sa.Column('city', sa.String(), nullable=False),
                    sa.Column('state', sa.String(), nullable=False),
                    sa.Column('country', sa.String(), nullable=False),
                    sa.Column('postalcode', sa.String(), nullable=False),
                    )


def downgrade() -> None:
    op.drop_table('address')
