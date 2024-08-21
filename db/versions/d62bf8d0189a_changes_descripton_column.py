"""changes descripton column

Revision ID: d62bf8d0189a
Revises: 90ce1fa4d184
Create Date: 2024-08-21 19:18:20.526258

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd62bf8d0189a'
down_revision = '90ce1fa4d184'
branch_labels = None
depends_on = None

def upgrade():
    # Drop the old column
    op.drop_column('investment_profiles', 'metadata')

    # Add the new column
    op.add_column('investment_profiles', sa.Column('description', sa.String(), nullable=True))

def downgrade():
    # Re-add the old column
    op.add_column('investment_profiles', sa.Column('metadata', sa.JSON(), nullable=True))

    # Drop the new column
    op.drop_column('investment_profiles', 'description')
