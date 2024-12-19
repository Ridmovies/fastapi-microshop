from fastapi import HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from api_v1.products import crud
from core.models.database import SessionDep
from core.models.product import Product


async def product_by_id(
    product_id: Annotated[int, Path],
    session: SessionDep,
) -> Product:
    product = await crud.get_product(session=session, product_id=product_id)
    if product:
        return product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product {product_id} not found",
    )
