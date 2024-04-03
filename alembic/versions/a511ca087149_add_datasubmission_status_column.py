"""Add DataSubmission status column

Revision ID: a511ca087149
Revises: 9bb8e29b98fa
Create Date: 2024-03-29 09:30:08.502456

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'a511ca087149'
down_revision: Union[str, None] = '9bb8e29b98fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    data_submission_status = postgresql.ENUM('PENDING_SUBMISSION', 'CANCELED', 'PENDING_VALIDATION', 'FAILED', 'VALIDATED', name='data_submission_status')
    data_submission_status.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "data_submissions",
        sa.Column("status", data_submission_status, nullable=False, server_default="PENDING_SUBMISSION"),
    )


def downgrade():
    op.drop_column("data_submissions", "status")
    data_submission_status = postgresql.ENUM('PENDING_SUBMISSION', 'CANCELED', 'PENDING_VALIDATION', 'FAILED', 'VALIDATED', name='data_submission_status')
    data_submission_status.drop(op.get_bind(), checkfirst=True)
