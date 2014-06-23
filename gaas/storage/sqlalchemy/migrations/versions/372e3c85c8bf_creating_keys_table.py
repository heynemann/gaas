"""Creating Keys Table

Revision ID: 372e3c85c8bf
Revises: 177d816fd717
Create Date: 2014-06-22 18:56:19.388279

"""

# revision identifiers, used by Alembic.
revision = '372e3c85c8bf'
down_revision = '177d816fd717'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'keys',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('public_key', sa.String(512), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=True),
    )

    op.create_foreign_key(
        "fk_keys_user", "keys", "users",
        ["user_id"], ["id"]
    )

    op.create_unique_constraint("uq_keys_public_key", "keys", ["public_key"])


def downgrade():
    op.drop_constraint('uq_keys_public_key', 'keys', type_="unique")
    op.drop_constraint('fk_keys_user', 'keys', type_="foreignkey")
    op.drop_table('keys')
