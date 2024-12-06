from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.products import crud
from api_v1.products.schemas import Product, ProductCreate
from core.models.database import get_session


router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=list[Product])
async def get_products(session: AsyncSession = Depends(get_session)):
    return await crud.get_products(session=session)


@router.post(
    "/",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    product_in: ProductCreate,
    session: AsyncSession = Depends(get_session),
):
    return await crud.create_product(session=session, product_in=product_in)


@router.get("/{product_id}/", response_model=Product)
async def get_product(
    product_id: int,
    session: AsyncSession = Depends(get_session),
):
    product = await crud.get_product(session=session, product_id=product_id)
    return product
