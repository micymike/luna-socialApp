"""Increase password_hash column size

Revision ID: f86077d5907f
Revises: 
Create Date: 2024-07-27 19:27:15.112746

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f86077d5907f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column('user', 'password_hash', type_=sa.String(length=256))


def downgrade():
    op.alter_column('user', 'password_hash', type_=sa.String(length=128))
