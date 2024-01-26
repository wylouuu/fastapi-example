"""Create post table

Revision ID: 1414ed7f9b2e
Revises: 
Create Date: 2024-01-26 18:41:19.195195

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1414ed7f9b2e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "posts", 
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True), 
        sa.Column("title", sa.String(), nullable=False)
    )
    pass


def downgrade() -> None:
    op.drop_table(
        "posts"
    )
    pass
