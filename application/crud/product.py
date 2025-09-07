from sqlalchemy.ext.asyncio import AsyncSession
from application.models.product import ProductOrm
from application.db.database import db_helper
from application.schemas.product import CreateProduct, UpdateProduct
from sqlalchemy import select


async def create_product_crud(product_data: CreateProduct, session: AsyncSession):
    new_product = ProductOrm(**product_data.model_dump())
    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)
    return new_product


async def get_product_by_id_crud(product_id: int, session: AsyncSession):
    product = await session.get(ProductOrm, product_id)
    if product is None:
        return None
    return product


async def get_list_product_by_id_crud(
    session: AsyncSession, start: int = 0, stop: int = 3
):
    stmt = select(ProductOrm).order_by(ProductOrm.id).offset(start).limit(stop - start)
    result = await session.execute(stmt)
    list_products: list = result.scalars().all()
    return list_products


async def update_product_crud(
    product_data: UpdateProduct, product_id: int, session: AsyncSession
):
    product = await session.get(ProductOrm, product_id)
    if product is None:
        return None
    data: dict = product_data.model_dump(exclude_unset=True)

    for key, value in data.items():
        if value is not None:
            setattr(product, key, value)

    await session.commit()
    await session.refresh(product)
    return product


async def delete_product_crud(product_id: int, session: AsyncSession):
    product = await session.get(ProductOrm, product_id)
    if product is None:
        return None
    await session.delete(product)
    await session.commit()
    return {"message": "Продукт удален"}
