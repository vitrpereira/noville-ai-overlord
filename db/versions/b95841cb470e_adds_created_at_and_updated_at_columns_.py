"""adds created_at and updated_at columns to conversations

Revision ID: b95841cb470e
Revises: fd927b33c5a7
Create Date: 2024-08-23 19:18:37.392513

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b95841cb470e'
down_revision = 'fd927b33c5a7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('conversations', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('conversations', sa.Column('updated_at', sa.DateTime(), nullable=True))

def downgrade():
    op.drop_column('conversations', 'created_at')
    op.drop_column('conversations', 'updated_at')
