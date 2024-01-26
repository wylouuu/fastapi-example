"""add some columns to posts table

Revision ID: f05c08ac0109
Revises: 52cd41745a64
Create Date: 2024-01-26 19:09:22.332269

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f05c08ac0109'
down_revision: Union[str, None] = '52cd41745a64'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE")
    )
    op.add_column(
        "posts",
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()"))
    )
    pass


def downgrade() -> None:
    op.drop_column(
        "posts",
        "published"
    )
    op.drop_column(
        "posts",
        "created_at"
    )
    pass
