"""create data_submissions table

Revision ID: c5596492c87b
Revises: a6db87212637
Create Date: 2024-01-26 12:25:47.404511

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision: str = "c5596492c87b"
down_revision: Union[str, None] = "a6db87212637"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "data_submissions",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("created_at", sa.DateTime, server_default=func.now(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime,
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
        ),
        sa.Column("filename", sa.String, nullable=False),
        sa.Column("data_provider_id", sa.Integer, sa.ForeignKey("data_providers.id")),
    )


def downgrade():
    op.drop_table("data_submissions")
