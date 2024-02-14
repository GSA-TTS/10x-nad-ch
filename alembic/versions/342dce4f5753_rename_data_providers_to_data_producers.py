"""Rename data_providers to data_producers and rename column in data_submissions

Revision ID: 342dce4f5753
Revises: 851709d3a162
Create Date: 2024-02-14 08:40:16.897824

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "342dce4f5753"
down_revision: Union[str, None] = "851709d3a162"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table("data_providers", "data_producers")
    op.alter_column(
        "data_submissions", "data_provider_id", new_column_name="data_producer_id"
    )


def downgrade() -> None:
    op.alter_column(
        "data_submissions", "data_producer_id", new_column_name="data_provider_id"
    )
    op.rename_table("data_producers", "data_providers")
