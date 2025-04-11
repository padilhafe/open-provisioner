# app/db/migrations/36c7d48b6359_create_cpe_table.py

from alembic import op
import sqlalchemy as sa
from src.app.core.enums import GponOperState
from src.app.core.types import CPE_TYPE

revision = '36c7d48b6359'
down_revision = '73383c554bd7'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'cpes',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('cpe_type', sa.String(length=32), nullable=False, server_default=CPE_TYPE[0]),
        sa.Column('oper_state', sa.Integer, nullable=False, server_default=str(GponOperState.InitialState.value)),
        sa.Column('customer_id', sa.Integer, sa.ForeignKey('customers.id'), nullable=False),
        sa.Column('device_id', sa.Integer, sa.ForeignKey('devices.id'), nullable=False),
    )

def downgrade() -> None:
    op.drop_table('cpes')
    sa.Enum(name='cpetype').drop(op.get_bind(), checkfirst=True)