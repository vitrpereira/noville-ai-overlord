"""drops profile relation in question answer model

Revision ID: b223879e3b10
Revises: d62bf8d0189a
Create Date: 2024-08-21 20:11:26.372571

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b223879e3b10'
down_revision = 'd62bf8d0189a'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('question_answers', 'profile_id')


def downgrade():
    op.add_column('question_answers', 'profile_id')
