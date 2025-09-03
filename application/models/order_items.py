from sqlalchemy import Table, Column, ForeignKey, column
from application.db.base import Base

association_table = Table(
    # имя таблицы
    "order_items",
    Base.metadata,
    Column("product_id", ForeignKey("products.id")),
    # сначала имя колонки в таблице, потом внешний ключ, ссылка на имя основной таблицы и колонки в ней
    Column("order_id", ForeignKey("orders.id")),
)
