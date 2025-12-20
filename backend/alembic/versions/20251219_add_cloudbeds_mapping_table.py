"""add cloudbeds mapping table

Revision ID: 20251219_add_cloudbeds_mapping_table
Revises: 20251219_add_cloudbeds_tables
Create Date: 2025-12-19 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20251219_add_cloudbeds_mapping_table'
down_revision = '20251219_add_cloudbeds_tables'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'cloudbeds_room_mappings',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('property_id', sa.Integer(), nullable=False),
        sa.Column('cloud_room_id', sa.String(), nullable=False),
        sa.Column('property_room_id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
    )


def downgrade():
    op.drop_table('cloudbeds_room_mappings')