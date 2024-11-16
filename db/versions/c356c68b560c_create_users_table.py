"""create_users_table

Revision ID: c356c68b560c
Revises: b1e641576176
Create Date: 2024-11-16 11:30:06.823268

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime
from app.models.db import db


# revision identifiers, used by Alembic.
revision = 'c356c68b560c'
down_revision = 'b1e641576176'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('phone_number', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow),
        sa.Column('product_id', sa.Integer(), db.ForeignKey('products.id'), nullable=False)
    )


def downgrade():
    op.drop_table('users')