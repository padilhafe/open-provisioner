"""create customer table

Revision ID: 73383c554bd7
Revises: 6de152f39832
Create Date: 2025-04-09 12:44:50.583474

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from api.core.types import CUSTOMER_STATUS

# revision identifiers, used by Alembic.
revision: str = '73383c554bd7'
down_revision: Union[str, None] = '6de152f39832'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('customers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('status', sa.String(length=32), nullable=False, server_default=CUSTOMER_STATUS[0]),
    sa.Column('integration_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('customers')
