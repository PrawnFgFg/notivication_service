"""initial revision and db auth

Revision ID: 729d3a813342
Revises: 
Create Date: 2025-10-23 00:33:58.011301

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '729d3a813342'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=200), nullable=False),
        sa.Column('hashed_password', sa.String(length=200), nullable=False),
        sa.Column('nickname', sa.String(length=20), nullable=False),
        sa.Column('role', sa.Enum('user', 'admin', name='enumrole'), server_default='user', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )


def downgrade() -> None:
    op.drop_table('users')
