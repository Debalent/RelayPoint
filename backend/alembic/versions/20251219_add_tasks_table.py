"""add tasks table

Revision ID: 20251219_add_tasks_table
Revises: 20251219_add_cloudbeds_tables
Create Date: 2025-12-19 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20251219_add_tasks_table'
down_revision = '20251219_add_cloudbeds_tables'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tasks',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('role', sa.String(), nullable=True),
        sa.Column('priority', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=True, server_default='pending'),
        sa.Column('department', sa.String(), nullable=True),
        sa.Column('guest_room', sa.String(), nullable=True),
        sa.Column('guest_name', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        sa.Column('due_at', sa.DateTime(), nullable=True),
        sa.Column('shift', sa.String(), nullable=True),
        sa.Column('guest_impact', sa.Boolean(), nullable=True),
        sa.Column('raw', sa.JSON(), nullable=True),
    )


def downgrade():
    op.drop_table('tasks')