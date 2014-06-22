"""Creating User Table

Revision ID: 177d816fd717
Revises: 2e40b858f75a
Create Date: 2014-06-22 11:29:13.865581

"""

# revision identifiers, used by Alembic.
revision = '177d816fd717'
down_revision = '2e40b858f75a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(2000), nullable=False),
        sa.Column('slug', sa.String(2000), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=True),
    )


def downgrade():
    op.drop_table('users')
