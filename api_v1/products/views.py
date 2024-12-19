from fastapi import APIRouter, status, HTTPException, Depends

from api_v1.products import crud
from api_v1.products.schemas import (
    Product,
    ProductCreate,
    ProductUpdate,
    ProductUpdatePartial,
)
from core.models.database import SessionDep
from api_v1.products.dependencies import product_by_id

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=list[Product])
async def get_products(session: SessionDep):
    return await crud.get_products(session=session)


@router.post(
    "/",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    product_in: ProductCreate,
    session: SessionDep,
):
    return await crud.create_product(session=session, product_in=product_in)


@router.get("/{product_id}/", response_model=Product)
async def get_product(
    product: Product = Depends(product_by_id),
):
    return product


@router.put("/{product_id}/", response_model=Product)
async def get_update_product(
    session: SessionDep,
    product_update: ProductUpdate,
    product: Product = Depends(product_by_id),
):
    updated_product = await crud.update_product(
        session=session, product=product, product_update=product_update, partial=False
    )
    return updated_product


@router.patch("/{product_id}/", response_model=Product)
async def get_update_product(
    session: SessionDep,
    product_update: ProductUpdatePartial,
    product: Product = Depends(product_by_id),
):
    updated_product = await crud.update_product(
        session=session, product=product, product_update=product_update, partial=True
    )
    return updated_product


@router.delete("/{product_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    session: SessionDep, product: Product = Depends(product_by_id)
) -> None:
    await crud.delete_product(session=session, product=product)

