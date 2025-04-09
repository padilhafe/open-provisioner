"""create cpe table

Revision ID: 36c7d48b6359
Revises: 73383c554bd7
Create Date: 2025-04-09 12:47:35.861847

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '36c7d48b6359'
down_revision: Union[str, None] = '73383c554bd7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'cpes',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('customer_id', sa.Integer, sa.ForeignKey('customers.id'), nullable=False),
        sa.Column('device_id', sa.Integer, sa.ForeignKey('devices.id'), nullable=False)
    )

def downgrade() -> None:
    op.drop_table('cpes')
