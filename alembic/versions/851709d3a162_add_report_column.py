"""Add report column

Revision ID: 851709d3a162
Revises: c5596492c87b
Create Date: 2024-02-06 13:22:25.266733

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.types import JSON


# revision identifiers, used by Alembic.
revision: str = "851709d3a162"
down_revision: Union[str, None] = "c5596492c87b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "data_submissions",
        sa.Column("report", JSON, nullable=True),
    )


def downgrade():
    op.drop_column("data_submissions", "report")
