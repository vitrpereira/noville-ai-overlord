"""Adds installment_number column do transactions

Revision ID: 537989d27d2e
Revises: 0242c49a9526
Create Date: 2025-01-18 14:06:33.892415

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '537989d27d2e'
down_revision = '0242c49a9526'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('transactions', sa.Column('installment_number', sa.Integer(), nullable=True))

def downgrade():
    op.drop_column('transactions', 'installment_number')