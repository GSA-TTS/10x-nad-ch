"""Rename data_submissions field

Revision ID: 558f8d429963
Revises: 3ff8e29d705e
Create Date: 2024-04-12 13:18:47.612471

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '558f8d429963'
down_revision: Union[str, None] = '3ff8e29d705e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('data_submissions', 'filename', new_column_name='file_path')


def downgrade() -> None:
    op.alter_column('data_submissions', 'file_path', new_column_name='filename')
