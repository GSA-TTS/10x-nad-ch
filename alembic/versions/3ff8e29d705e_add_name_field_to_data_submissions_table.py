"""Add name field to data_submissions table

Revision ID: 3ff8e29d705e
Revises: a511ca087149
Create Date: 2024-04-12 12:50:48.903157

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3ff8e29d705e"
down_revision: Union[str, None] = "a511ca087149"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "data_submissions",
        sa.Column("name", sa.String, nullable=False),
    )


def downgrade() -> None:
    op.drop_column("data_submissions", "name")
