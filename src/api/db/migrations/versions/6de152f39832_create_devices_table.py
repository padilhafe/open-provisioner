"""create devices table

Revision ID: 6de152f39832
Revises: 4999aa4847a4
Create Date: 2025-04-09 11:12:36.042052

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '6de152f39832'
down_revision: Union[str, None] = '4999aa4847a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('devices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hostname', sa.String(length=100), nullable=False),
    sa.Column('device_type', sa.String(length=32), nullable=False),
    sa.Column('device_hostname', sa.String(length=32), nullable=True),

    sa.Column('device_mgmt_ipv4', sa.String(length=16), nullable=True),
    sa.Column('device_username', sa.String(length=16), nullable=True),
    sa.Column('device_password', sa.String(length=16), nullable=True),
    sa.Column('device_mgmt_port', sa.Integer, nullable=False, server_default=sa.text('22')),
    
    sa.Column('snmp_version', sa.Integer(), nullable=True),
    sa.Column('snmp_port', sa.Integer, nullable=False, server_default=sa.text('161')),
    sa.Column('snmp_community', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('devices')
