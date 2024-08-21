"""create conversations table

Revision ID: 0c106fe40043
Revises: b4e9c6e15921
Create Date: 2024-08-21 16:24:51.900723

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c106fe40043'
down_revision = 'b4e9c6e15921'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
    'conversations',
    sa.Column('id', sa.Integer(), primary_key=True),
    sa.Column('bot_name', sa.String(), nullable=True),
    sa.Column('user_message', sa.String(), nullable=True),
    sa.Column('agent_answer', sa.String(), nullable=True)
)


def downgrade():
    pass
