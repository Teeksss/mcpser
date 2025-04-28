"""create users and tenants tables

Revision ID: 0001
Revises:
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'tenants',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, unique=True, index=True),
        sa.Column('description', sa.String, nullable=True)
    )
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String, unique=True, index=True),
        sa.Column('hashed_password', sa.String),
        sa.Column('role', sa.String, default="user"),
        sa.Column('email', sa.String, unique=True, index=True, nullable=True),
        sa.Column('is_active', sa.Integer, default=1),
        sa.Column('tenant_id', sa.Integer, sa.ForeignKey('tenants.id'), nullable=True)
    )

def downgrade():
    op.drop_table('users')
    op.drop_table('tenants')