"""create templates

Revision ID: 8339df6a6eb9
Revises: 729d3a813342
Create Date: 2025-10-31 18:17:10.638316

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8339df6a6eb9'
down_revision: Union[str, Sequence[str], None] = '729d3a813342'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('templates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('template_key', sa.String(), nullable=False),
    sa.Column('body', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('template_key')
    )


def downgrade() -> None:
    op.drop_table('templates')
