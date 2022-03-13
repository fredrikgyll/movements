"""create poop table

Revision ID: 824917f9684f
Revises:
Create Date: 2022-03-13 22:15:41.616380

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '824917f9684f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'poops',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column(
            'created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True
        ),
        sa.Column(
            'updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True
        ),
        sa.Column('taken_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('poops')
