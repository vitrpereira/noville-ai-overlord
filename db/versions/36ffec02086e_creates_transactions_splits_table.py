"""Creates transactions splits table

Revision ID: 36ffec02086e
Revises: 537989d27d2e
Create Date: 2025-01-18 16:01:47.628053

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '36ffec02086e'
down_revision = '537989d27d2e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('transactions_splits',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('transaction_id', sa.Integer(), sa.ForeignKey('transactions.id'), nullable=False),
        sa.Column('transaction_date', sa.Date(), nullable=False),
        sa.Column('installment_date', sa.Date(), nullable=False),
        sa.Column('installment_number', sa.Integer(), nullable=False),
        sa.Column('total_amount', sa.Float(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('transactions_splits')