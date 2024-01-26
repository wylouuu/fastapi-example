"""add content colum to posts table

Revision ID: 9aaaea3f5142
Revises: 1414ed7f9b2e
Create Date: 2024-01-26 18:49:08.937392

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9aaaea3f5142'
down_revision: Union[str, None] = '1414ed7f9b2e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("content", sa.String(), nullable=False)
    )
    pass


def downgrade() -> None:
    op.drop_column(
        "posts",
        "content"
    )
    pass
