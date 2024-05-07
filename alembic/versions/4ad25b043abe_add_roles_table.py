"""Add roles table

Revision ID: 4ad25b043abe
Revises: 558f8d429963
Create Date: 2024-05-07 15:54:43.589517

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON

# revision identifiers, used by Alembic.
revision: str = "4ad25b043abe"
down_revision: Union[str, None] = "558f8d429963"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("permissions", JSON, default=list),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "user_role",
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column("role_id", sa.Integer, sa.ForeignKey("roles.id", ondelete="CASCADE")),
    )


def downgrade() -> None:
    op.drop_table("roles")
    op.drop_table("user_role")
