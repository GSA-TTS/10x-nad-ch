"""Remove username column from users table

Revision ID: dc3dd97eae46
Revises: 945ca77479d1
Create Date: 2024-03-05 13:21:29.812837

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "dc3dd97eae46"
down_revision: Union[str, None] = "945ca77479d1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_column("users", "username")


def downgrade():
    op.add_column(
        "users",
        sa.Column("username", sa.String, nullable=True),
    )
