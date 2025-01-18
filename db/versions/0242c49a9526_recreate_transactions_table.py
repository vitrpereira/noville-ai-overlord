"""Recreate transactions table

Revision ID: 0242c49a9526
Revises: 939304b0f808
Create Date: 2025-01-18 13:45:18.267928

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0242c49a9526'
down_revision = '939304b0f808'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'transactions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('installments', sa.Integer(), nullable=False),
        sa.Column('payment_method', sa.String(), nullable=False),
        sa.Column('operation', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False)
    )



def downgrade():
    op.drop_table('transactions')
