"""Creating Repository Table

Revision ID: 2e40b858f75a
Revises: None
Create Date: 2014-06-21 19:29:23.032276

"""

# revision identifiers, used by Alembic.
revision = '2e40b858f75a'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'repositories',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(120), nullable=False),
        sa.Column('uuid', sa.String(36), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=True),
    )


def downgrade():
    op.drop_table('repositories')
