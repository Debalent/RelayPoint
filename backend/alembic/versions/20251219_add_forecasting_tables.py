"""add forecasting tables

Revision ID: 20251219_add_forecasting_tables
Revises: 
Create Date: 2025-12-19 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20251219_add_forecasting_tables'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'forecast_models',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('property_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('model_type', sa.String(), nullable=False),
        sa.Column('version', sa.String(), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('path', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
    )

    op.create_table(
        'forecast_predictions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('property_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('date', sa.String(), nullable=False),
        sa.Column('predicted', sa.Float(), nullable=False),
        sa.Column('lower', sa.Float(), nullable=True),
        sa.Column('upper', sa.Float(), nullable=True),
        sa.Column('model_id', sa.Integer(), sa.ForeignKey('forecast_models.id'), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
    )

    op.create_table(
        'forecast_overrides',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('property_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('date', sa.String(), nullable=False),
        sa.Column('override_value', sa.Float(), nullable=False),
        sa.Column('reason', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
    )


def downgrade():
    op.drop_table('forecast_overrides')
    op.drop_table('forecast_predictions')
    op.drop_table('forecast_models')
