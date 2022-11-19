"""create phone number for user col

Revision ID: 46d2abb06bf8
Revises: 
Create Date: 2022-11-13 18:32:35.132881

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '46d2abb06bf8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'phone_number')
