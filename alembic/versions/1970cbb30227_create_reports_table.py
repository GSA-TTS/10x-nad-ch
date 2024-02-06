"""Create reports table

Revision ID: 1970cbb30227
Revises: c5596492c87b
Create Date: 2024-02-06 13:10:12.248041

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision: str = '1970cbb30227'
down_revision: Union[str, None] = 'c5596492c87b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "reports",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("created_at", sa.DateTime, server_default=func.now(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime,
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
        ),
        sa.Column("data", JSONB, nullable=False),
        sa.Column("data_submission_id", sa.Integer, sa.ForeignKey("data_submissions.id")),
    )

def downgrade() -> None:
    op.drop_table("reports")
