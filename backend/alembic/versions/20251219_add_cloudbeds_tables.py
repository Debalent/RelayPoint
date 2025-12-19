"""add cloudbeds tables

Revision ID: 20251219_add_cloudbeds_tables
Revises: 20251219_add_forecasting_tables
Create Date: 2025-12-19 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20251219_add_cloudbeds_tables'
down_revision = '20251219_add_forecasting_tables'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'cloudbeds_rooms',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('property_id', sa.Integer(), nullable=False),
        sa.Column('room_id', sa.String(), nullable=False, unique=False),
        sa.Column('room_number', sa.String(), nullable=True),
        sa.Column('room_type', sa.String(), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
    )

    op.create_table(
        'cloudbeds_reservations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('property_id', sa.Integer(), nullable=False),
        sa.Column('reservation_id', sa.String(), nullable=False),
        sa.Column('guest_name', sa.String(), nullable=True),
        sa.Column('check_in', sa.Date(), nullable=True),
        sa.Column('check_out', sa.Date(), nullable=True),
        sa.Column('room_id', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('raw', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
    )


def downgrade():
    op.drop_table('cloudbeds_reservations')
    op.drop_table('cloudbeds_rooms')