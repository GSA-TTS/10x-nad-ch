"""create users table

Revision ID: 945ca77479d1
Revises: 342dce4f5753
Create Date: 2024-02-16 16:16:13.902219

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision: str = "945ca77479d1"
down_revision: Union[str, None] = "342dce4f5753"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
        ),
        sa.Column("username", sa.String, nullable=False),
        sa.Column("email", sa.String, nullable=False),
        sa.Column("login_provider", sa.String, nullable=True),
        sa.Column("logout_url", sa.String, nullable=True),
    )


def downgrade() -> None:
    op.drop_table("users")
