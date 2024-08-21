"""Creates Q&A and Investment Profile tables

Revision ID: 90ce1fa4d184
Revises: 0c106fe40043
Create Date: 2024-08-21 18:58:30.612954

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90ce1fa4d184'
down_revision = '0c106fe40043'
branch_labels = None
depends_on = None


def upgrade():
    # Create investment_profiles table
    op.create_table(
        'investment_profiles',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('profile', sa.String(), nullable=False),
        sa.Column('minimum_score', sa.Integer(), nullable=False),
        sa.Column('maximum_score', sa.Integer(), nullable=False),
        sa.Column('metadata', sa.JSON(), nullable=True)
    )

    # Create question_answers table
    op.create_table(
        'question_answers',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('question', sa.String(), nullable=False),
        sa.Column('answer', sa.String(), nullable=False),
        sa.Column('score', sa.Integer(), nullable=False),
        sa.Column('profile_id', sa.Integer(), sa.ForeignKey('investment_profiles.id'), nullable=False)
    )


def downgrade():
    # Drop question_answers table
    op.drop_table('question_answers')

    # Drop investment_profiles table
    op.drop_table('investment_profiles')
