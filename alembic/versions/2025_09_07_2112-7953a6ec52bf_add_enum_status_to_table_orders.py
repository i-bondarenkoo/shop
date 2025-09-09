"""add enum status to table orders

Revision ID: 7953a6ec52bf
Revises: c47acf2fa495
Create Date: 2025-09-07 21:12:33.442833
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7953a6ec52bf"
down_revision: Union[str, Sequence[str], None] = "c47acf2fa495"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # создаём ENUM тип
    orderstatus = sa.Enum("created", "packed", "paid", "canceled", name="orderstatus")
    orderstatus.create(op.get_bind(), checkfirst=True)

    # изменяем колонку с использованием USING (для пустой таблицы это безопасно)
    op.execute(
        "ALTER TABLE orders ALTER COLUMN status TYPE orderstatus USING status::orderstatus"
    )


def downgrade() -> None:
    """Downgrade schema."""
    # меняем обратно на строку
    op.execute(
        "ALTER TABLE orders ALTER COLUMN status TYPE VARCHAR(30) USING status::VARCHAR"
    )

    # удаляем ENUM
    orderstatus = sa.Enum("created", "packed", "paid", "canceled", name="orderstatus")
    orderstatus.drop(op.get_bind(), checkfirst=True)
