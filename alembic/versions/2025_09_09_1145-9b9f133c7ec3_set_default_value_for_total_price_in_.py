"""set default value for total_price in orders

Revision ID: 9b9f133c7ec3
Revises: 7953a6ec52bf
Create Date: 2025-09-09 11:45:59.285278

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = "9b9f133c7ec3"
down_revision: Union[str, Sequence[str], None] = "7953a6ec52bf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "orders",
        "total_price",
        server_default=text("0"),
        existing_type=sa.Integer(),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "orders",
        "total_price",
        server_default=None,
        existing_type=sa.Integer(),
        existing_nullable=False,
    )
