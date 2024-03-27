"""User DataProducer relationship

Revision ID: 9bb8e29b98fa
Revises: 68982ccf2c7c
Create Date: 2024-03-27 14:21:24.094899

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9bb8e29b98fa'
down_revision: Union[str, None] = '68982ccf2c7c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("activated", sa.Boolean, nullable=False, default=False),
    )

    op.add_column(
        "users",
        sa.Column("data_producer_id", sa.Integer, sa.ForeignKey("data_producers.id"), nullable=True),
    )

def downgrade() -> None:
    op.drop_column("users", "activated")
