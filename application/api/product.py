from application.crud.product import (
    create_product_crud,
    delete_product_crud,
    get_list_product_by_id_crud,
    get_product_by_id_crud,
    update_product_crud,
)
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, Body, Path, Query, status, APIRouter
from application.schemas.product import CreateProduct, ResponseProduct, UpdateProduct
from typing import Annotated
from application.db.database import db_helper

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post("/", response_model=ResponseProduct, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: Annotated[
        CreateProduct, Body(description="Данные о продукте для создания")
    ],
    session: AsyncSession = Depends(db_helper.get_session),
):
    return await create_product_crud(product_data=product_data, session=session)


@router.get("/{product_id}", response_model=ResponseProduct)
async def get_product_by_id(
    product_id: Annotated[
        int, Path(gt=0, description="ID продукта для получения информации")
    ],
    session: AsyncSession = Depends(db_helper.get_session),
):
    product = await get_product_by_id_crud(product_id=product_id, session=session)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Продукт не найден"
        )
    return product


@router.get("/", response_model=list[ResponseProduct])
async def get_list_product_by_id(
    start: int = Query(0, ge=0, description="Начальный диапазон списка продуктов"),
    stop: int = Query(3, gt=0, description="Конечный диапазон списка продуктов"),
    session: AsyncSession = Depends(db_helper.get_session),
):
    if start > stop:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Некорректный диапазон списка",
        )
    list_products = await get_list_product_by_id_crud(
        start=start, stop=stop, session=session
    )
    return list_products


@router.patch("/{product_id}", response_model=ResponseProduct)
async def update_product(
    product_data: Annotated[UpdateProduct, Body(description="Поля для обновления")],
    product_id: Annotated[
        int, Path(gt=0, description="ID продукта для обновления данных")
    ],
    session: AsyncSession = Depends(db_helper.get_session),
):
    data: dict = product_data.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Данные для обновления не переданы",
        )
    product = await update_product_crud(
        product_data=product_data, product_id=product_id, session=session
    )
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Продукт не найден"
        )
    return product


@router.delete("/{product_id}")
async def delete_product(
    product_id: Annotated[int, Path(gt=0, description="ID продукта для удаления")],
    session: AsyncSession = Depends(db_helper.get_session),
):
    product = await delete_product_crud(product_id=product_id, session=session)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Продукт не найден"
        )
    return product
