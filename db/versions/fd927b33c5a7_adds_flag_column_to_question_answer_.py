"""adds flag column to question answer model

Revision ID: fd927b33c5a7
Revises: b223879e3b10
Create Date: 2024-08-22 07:23:30.019247

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd927b33c5a7'
down_revision = 'b223879e3b10'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('question_answers', sa.Column('flag', sa.String(), nullable=False))


def downgrade():
    op.drop_columns('question_answers', 'flag')
