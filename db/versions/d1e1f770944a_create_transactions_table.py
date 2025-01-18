"""Create transactions table

Revision ID: d1e1f770944a
Revises: c356c68b560c
Create Date: 2025-01-18 13:17:58.587947

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision = 'd1e1f770944a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create the transactions table
    op.create_table('transactions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('installments', sa.Integer(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('payment_method', sa.String(), nullable=False),
        sa.Column('operation', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=func.now(), onupdate=func.now()),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    # Drop the transactions table
    op.drop_table('transactions')
